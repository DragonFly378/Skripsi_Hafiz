import numpy as np 
from GMM import GaussianMixtureModels


COLOR = {
    'red' : [0, 0, 255],
    'white' : [255, 255, 255],
    'black' : [0, 0, 0],
    'yellow' : [0, 255, 255]
}

F_BG = 0
F_FG = 1
F_PR_BG = 2
F_PR_FG = 3

class GrabCut:
    def __init__(self, gambar, mask, rect=None, komponen_gmm = 5):

        self.gambar = gambar
        self.mask = mask
        self.rect = rect
        self.komponen_gmm = komponen_gmm

        self.baris, self.kolom, _ = gambar.shape

        self.graf = None
        self.kapasitas_graph = None
        self.source_gc = 0
        self.sink_gc = (self.baris * self.kolom)

        self.gmm_fg = None
        self.gmm_bg = None

        self.gamma_val = 50
        self.beta_val = 0

        self.komponen_piksel = np.zeros((self.baris, self.kolom), dtype=np.uint32)
        print('class grabcut berjalan')
        # print(self.baris)

        self.count_smoothness()
        self.idx_bg, self.idx_fg = self.inisiasi_piksel()
        self.init_assign_gmm()
        self.mempelajari_gmm()
        self.build_graph()
        print("program kelar")

    
    def inisiasi_piksel(self):
        print("\nInisasi piksel", self.rect)
        # ix, iy, x, y = 134, 41, 263, 136
        # ix, iy, x, y = 176, 47, 351, 189
        ix, iy, x, y = self.rect[0], self.rect[1], self.rect[2], self.rect[3]

        self.mask[iy:y, ix:x] = F_PR_FG

        idx_bg = np.where(np.logical_or(
            self.mask == F_BG, self.mask == F_PR_BG
        ))

        idx_fg = np.where(np.logical_or(
            self.mask == F_FG, self.mask == F_PR_FG
        ))
        
        print('(pr_)bgd count: ', idx_bg, '(pr_)fgd count: ', idx_fg)
        print('(pr_)bgd count: ', idx_bg[1].size, '(pr_)fgd count:', idx_fg[1].size)

        print('Inisiasi piksel selesai')
        return(idx_bg, idx_fg)

    def init_assign_gmm(self):
        # print(self.idx_fg[1].size)
        """Init GMM bg dan fg dengan target gambar"""
        print('\nMulai init GMM')
        self.gmm_fg = GaussianMixtureModels(self.gambar[self.idx_fg])
        self.gmm_bg = GaussianMixtureModels(self.gambar[self.idx_bg])

        """Lanjut step 1 (assign GMM) pada gambar 2.11"""
        print('\nMulai assign GMM')
        self.komponen_piksel[self.idx_fg] = self.gmm_fg.assign_component(
            self.gambar[self.idx_fg]
        )
        self.komponen_piksel[self.idx_bg] = self.gmm_bg.assign_component(
            self.gambar[self.idx_bg]
        )

        print('hasil komponen piksel fg: ',self.komponen_piksel[self.idx_fg])
        print('hasil komponen piksel bg: ',self.komponen_piksel[self.idx_bg])
        
        print('Komponen piksel FG: %d, Komponen piksel BG: %d, Total komponen: %d' % (
        len(self.komponen_piksel[self.idx_fg]), len(self.komponen_piksel[self.idx_bg]), len(self.komponen_piksel)))


    def mempelajari_gmm(self):
        """
        Lanjut step 2 (learn GMM) pada gambar 2.11
        """
        print("\nMulai learn gmm")
        self.gmm_fg.count_params(self.gambar[self.idx_fg], 
                                 self.komponen_piksel[self.idx_fg])
        self.gmm_bg.count_params(self.gambar[self.idx_bg], 
                                 self.komponen_piksel[self.idx_bg])

    def count_smoothness(self):
        left_diff_V = self.gambar[:, 1:] - self.gambar[:, :-1]
        upleft_diff_V = self.gambar[1:, 1:] - self.gambar[:-1, :-1]
        up_diff_V = self.gambar[1:, :] - self.gambar[:-1, :]
        upright_diff_V = self.gambar[1:, :-1] - self.gambar[:-1, 1:]

        self.beta_val = np.sum(np.square(left_diff_V)) + \
                        np.sum(np.square(upleft_diff_V)) + \
                        np.sum(np.square(up_diff_V)) + \
                        np.sum(np.square(upright_diff_V))

        print('Beta pertama: ', self.beta_val)
        '''
        # Rumus nilai beta pada bagian 2.19
        # - Setiap piksel punya 4 tetangga (left, upleft, up, upright)
        # - Kolom pertama tidak punya tetangga left dan upleft. Kolom terakhir tidak punya tetangga upright
        # - Baris pertama tidak punya tetangga up, upleft, upright
        # - Piksel pertama dan terakhir pada baris pertama dipindahkan dua kali
        '''
        self.beta_val = 1 / (2 * self.beta_val / (
        4 * self.kolom * self.baris 
        - 3 * self.kolom  
        - 3 * self.baris  
        + 2)) 
        print('Beta kedua: ', self.beta_val)

        # Rumus mencari smoothness pada bagian 2.25
        self.left_V = self.gamma_val * np.exp(-self.beta_val * np.sum(np.square(left_diff_V), axis=2))
        self.upleft_V = self.gamma_val * np.exp(-self.beta_val * np.sum(np.square(upleft_diff_V), axis=2))
        self.upright_V = self.gamma_val * np.exp(-self.beta_val * np.sum(np.square(upright_diff_V), axis=2))
        self.up_V = self.gamma_val * np.exp(-self.beta_val * np.sum(np.square(up_diff_V), axis=2))
        print("beta smoothness selesai")

    def build_graph(self):
        idx_fg = np.where(self.mask.reshape(-1) == F_FG)
        idx_bg = np.where(self.mask.reshape(-1) == F_BG)
        idx_pr = np.where(np.logical_or(
            self.mask.reshape(-1) == F_PR_FG, self.mask.reshape(-1) == F_PR_BG
            ))

        print("jumlah tu: ", idx_pr)
        print("jumlah tu: ", len(idx_pr[0]))
        print('jumlah TB: %d, jumlah TF: %d, jumlah TU: %d' % (
            len(idx_bg[0]), len(idx_fg[0]), len(idx_pr[0])))

        edges = []
        self.kapasitas_graph = []
        print('edges awal : %d, kapasitas awal: %d' % (len(edges), len(self.kapasitas_graph)))


        # T-Links
        edges.extend(list(zip([self.source_gc] * idx_pr[0].size, idx_pr[0])))
        edges.extend(list(zip([self.source_gc] * idx_bg[0].size, idx_bg[0])))
        edges.extend(list(zip([self.source_gc] * idx_fg[0].size, idx_fg[0])))
        edges.extend(list(zip([self.sink_gc] * idx_pr[0].size, idx_pr[0])))
        edges.extend(list(zip([self.sink_gc] * idx_bg[0].size, idx_bg[0])))
        edges.extend(list(zip([self.sink_gc] * idx_fg[0].size, idx_fg[0])))

        D_count = -np.log(self.gmm_fg.count_prob(self.gambar.reshape(-1, 3)[idx_pr]))
        self.kapasitas_graph.extend(D_count.tolist())
        
        D_count = -np.log(self.gmm_bg.count_prob(self.gambar.reshape(-1, 3)[idx_pr]))
        self.kapasitas_graph.extend(D_count.tolist())

        self.kapasitas_graph.extend([9 * self.gamma_val] * idx_fg[0].size)
        self.kapasitas_graph.extend([9 * self.gamma_val] * idx_bg[0].size)

        self.kapasitas_graph.extend([0] * idx_fg[0].size)
        self.kapasitas_graph.extend([0] * idx_bg[0].size)

        print('edges dan kapasitas: ', len(edges), len(self.kapasitas_graph))



        