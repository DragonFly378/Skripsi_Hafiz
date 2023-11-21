import numpy as np 
from GMM import GaussianMixtureModels
import igraph as ig

COLOR = {
    'red' : [0, 0, 255],
    'white' : [255, 255, 255],
    'black' : [0, 0, 0],
    'yellow' : [0, 255, 255]
}


F_TB = 0
F_TF = 1

# F_PR_BG = 2
# F_PR_FG = 3

class GrabCut:
    def __init__(self, gambar, mask, rect=None, komponen_gmm = 5):

        self.gambar = gambar
        self.mask = mask
        self.alpha = mask
        self.rect = rect
        self.komponen_gmm = komponen_gmm

        self.trimap = {
            'TU' : [],
            'TB' : [],
            'TF' : []
        }

        self.baris, self.kolom, _ = gambar.shape

        self.graf = None
        self.kapasitas_graph = []
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
        self.inisiasi_piksel()
        self.assign_gmm()
        self.mempelajari_gmm()
        self.build_graph()
        # self.mincut_segmentation()

        print("program kelar")

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
        - 3 * self.baris  +
        + 2)) 
        print('Beta kedua: ', self.beta_val)

        # Rumus mencari smoothness pada bagian 2.25
        self.left_V = self.gamma_val * np.exp(-self.beta_val * np.sum(np.square(left_diff_V), axis=2))
        self.upleft_V = self.gamma_val * np.exp(-self.beta_val * np.sum(np.square(upleft_diff_V), axis=2))
        self.upright_V = self.gamma_val * np.exp(-self.beta_val * np.sum(np.square(upright_diff_V), axis=2))
        self.up_V = self.gamma_val * np.exp(-self.beta_val * np.sum(np.square(up_diff_V), axis=2))
        print("beta smoothness selesai")


    def inisiasi_piksel(self):
        print("\nInisasi piksel", self.rect)
        # ix, iy, x, y = 134, 41, 263, 136
        # ix, iy, x, y = 176, 47, 351, 189
        ix, iy, x, y = self.rect[0], self.rect[1], self.rect[2], self.rect[3]

        # self.mask[iy:y, ix:x] = F_TF
        self.alpha[iy:y, ix:x] = F_TF


        self.trimap['TB'] = np.where(self.alpha == F_TB)
        self.trimap['TU'] = np.where(self.alpha == F_TF)
        
        # print('(pr_)bgd count: \n', self.trimap['TU'][0], '\n (pr_)fgd count: \n', self.trimap['TU'])
        # print('(pr_)bgd count: ', self.trimap['TB'][1].size, '(pr_)fgd count:', self.trimap['TU'][1].size)
        print('anu: \n', self.alpha[self.trimap['TU']])

        """Inisiasi GMM untuk bg dan fg dengan parameter gambar"""
        print('\nMulai init GMM')
        self.gmm_fg = GaussianMixtureModels(self.gambar[self.trimap['TU']])
        self.gmm_bg = GaussianMixtureModels(self.gambar[self.trimap['TB']])
        
        print('Inisiasi piksel selesai')
        # return(trimap_TB, trimap_TU)

    def assign_gmm(self):
        """Step 1 (assign GMM) pada gambar 2.11"""
        print('\nMulai assign GMM')
        self.komponen_piksel[self.trimap['TU']] = self.gmm_fg.assign_component(
            self.gambar[self.trimap['TU']]
        )

        self.komponen_piksel[self.trimap['TB']] = self.gmm_bg.assign_component(
            self.gambar[self.trimap['TB']]
        )

        print('hasil komponen piksel fg: ',self.komponen_piksel[self.trimap['TU']])
        print('hasil komponen piksel bg: ',self.komponen_piksel[self.trimap['TB']])
        
        print('Komponen piksel TU: %d, Komponen piksel TB: %d, Total komponen: %d' % (
        len(self.komponen_piksel[self.trimap['TU']]), len(self.komponen_piksel[self.trimap['TB']]), len(self.komponen_piksel)))


    def mempelajari_gmm(self):
        """
        Lanjut step 2 (learn GMM) pada gambar 2.11
        """
        print("\nMulai learn gmm")
        self.gmm_fg.count_params(self.gambar[self.trimap['TU']], 
                                 self.komponen_piksel[self.trimap['TU']])
        self.gmm_bg.count_params(self.gambar[self.trimap['TB']], 
                                 self.komponen_piksel[self.trimap['TB']])

        idx_TF = np.where(self.alpha.reshape(-1) == 3)
        idx_TB = np.where(self.alpha.reshape(-1) == F_TB)
        idx_TU = np.where(self.alpha.reshape(-1) == F_TF)

               
        self.D_count_bg = self.gmm_bg.count_D_formula(self.gambar.reshape(-1, 3)[idx_TU])
        self.D_count_fg = self.gmm_fg.count_D_formula(self.gambar.reshape(-1, 3)[idx_TU])
        
    
    def build_graph(self):
        idx_TF = np.where(self.alpha.reshape(-1) == 3)
        idx_TB = np.where(self.alpha.reshape(-1) == F_TB)
        idx_TU = np.where(self.alpha.reshape(-1) == F_TF)

        print('jumlah TB: %d, jumlah TU: %d' % (
            len(idx_TB[0]), len(idx_TU[0])))

        edges = []
        print('edges awal : %d, kapasitas awal: %d' % (len(edges), len(self.kapasitas_graph)))


        print("edges: ", ([self.source_gc] * idx_TU[0].size)[:10])
        print("edges: ", ([self.source_gc] * idx_TB[0].size)[:10])
        print("edges: ", ([self.source_gc] * idx_TF[0].size)[:10])
        print("edges: ", ([self.sink_gc] * idx_TU[0].size)[:10])
        print("edges: ", ([self.sink_gc] * idx_TB[0].size)[:10])
        print("edges: ", ([self.sink_gc] * idx_TF[0].size)[:10])

        # Construct T-links
        edges.extend(list(zip([self.source_gc] * idx_TU[0].size, idx_TU[0])))
        self.kapasitas_graph.extend(self.D_count_bg.tolist())

        edges.extend(list(zip([self.source_gc] * idx_TB[0].size, idx_TB[0])))
        self.kapasitas_graph.extend([0] * idx_TB[0].size)

        edges.extend(list(zip([self.source_gc] * idx_TF[0].size, idx_TF[0])))
        self.kapasitas_graph.extend([9 * self.gamma_val] * idx_TF[0].size)

        edges.extend(list(zip([self.sink_gc] * idx_TU[0].size, idx_TU[0])))
        self.kapasitas_graph.extend(self.D_count_fg.tolist())

        edges.extend(list(zip([self.sink_gc] * idx_TB[0].size, idx_TB[0])))
        self.kapasitas_graph.extend([9 * self.gamma_val] * idx_TB[0].size)

        edges.extend(list(zip([self.sink_gc] * idx_TF[0].size, idx_TF[0])))
        self.kapasitas_graph.extend([0] * idx_TF[0].size)
        
        # left_diff_V = self.gambar[:, 1:] - self.gambar[:, :-1]
        # upleft_diff_V = self.gambar[1:, 1:] - self.gambar[:-1, :-1]
        # up_diff_V = self.gambar[1:, :] - self.gambar[:-1, :]
        # upright_diff_V = self.gambar[1:, :-1] - self.gambar[:-1, 1:]
        
        # n-links
        img_indexes = np.arange(self.baris * self.kolom, dtype=np.uint32).reshape(self.baris, self.kolom)

        mask1 = img_indexes[:, 1:].reshape(-1)
        mask2 = img_indexes[:, :-1].reshape(-1)
        edges.extend(list(zip(mask1, mask2)))
        self.kapasitas_graph.extend(self.left_V.reshape(-1).tolist())
        # assert len(edges) == len(self.kapasitas_graph)

        mask1 = img_indexes[1:, 1:].reshape(-1)
        mask2 = img_indexes[:-1, :-1].reshape(-1)
        edges.extend(list(zip(mask1, mask2)))
        self.kapasitas_graph.extend(
            self.upleft_V.reshape(-1).tolist())
        # assert len(edges) == len(self.kapasitas_graph)

        mask1 = img_indexes[1:, :].reshape(-1)
        mask2 = img_indexes[:-1, :].reshape(-1)
        edges.extend(list(zip(mask1, mask2)))
        self.kapasitas_graph.extend(self.up_V.reshape(-1).tolist())
        # assert len(edges) == len(self.kapasitas_graph)

        mask1 = img_indexes[1:, :-1].reshape(-1)
        mask2 = img_indexes[:-1, 1:].reshape(-1)
        edges.extend(list(zip(mask1, mask2)))
        self.kapasitas_graph.extend(
            self.upright_V.reshape(-1).tolist())
        # assert len(edges) == len(self.kapasitas_graph)

        # assert len(edges) == 4 * self.cols * self.rows - 3 * (self.cols + self.rows) + 2 + \
        #     2 * self.cols * self.rows

        print('graph capacity: ', len(self.kapasitas_graph))
        print('edges: ', len(edges))
        self.gc_graph = ig.Graph(self.kolom * self.baris + 2)
        print('gc_graph: ', self.gc_graph)
        self.gc_graph.add_edges(edges)


        print('graph capacity: ', len(self.kapasitas_graph))
        print('edges: ', len(edges))
        self.graf = ig.Graph(self.kolom * self.baris + 2)
        print('graf: ', self.graf)
        self.graf.add_edges(edges)

    def mincut_segmentation(self):
        """
        Lanjut step 3 (estimate segmentation) pada gambar 2.11
        """
        mincut = self.graf.st_mincut(
        self.source_gc, self.sink_gc, self.kapasitas_graph)
        print('foreground pixels: %d, background pixels: %d' % (
            len(mincut.partition[0]), len(mincut.partition[1])))
        # print('jumlah partisi: ', mincut.partition)


        idx_pr = np.where(self.alpha == F_TF)
        img_indexes = np.arange(self.baris * self.kolom,
                                dtype=np.uint32).reshape(self.baris, self.kolom)
        print('img_indexes: ', img_indexes)
        self.alpha[idx_pr] = np.where(np.isin(img_indexes[idx_pr], mincut.partition[0]),
                                         F_TF, F_TB)
        # self.classify_pixels()
