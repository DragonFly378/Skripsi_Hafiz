import numpy as np 
from GMM import MixtureModel
import igraph as ig
from mincut import mincut_segmentation

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

        self.baris, self.kolom, self.n_channels = gambar.shape

        self.graf = None
        self.kapasitas_graph = []
        self.source_gc = 0
        self.sink_gc = (self.baris * self.kolom)

        self.gmm_fg = None
        self.gmm_bg = None

        self.gamma_val = 50
        self.beta_val = 0

        
        self.theta = {
            'TU' : {
                'koefisien' : np.zeros(self.komponen_gmm),
                'means' : np.zeros((self.komponen_gmm, self.n_channels)),
                'kovarians' : np.zeros((self.komponen_gmm, self.n_channels, self.n_channels))
            },
            'TB' : {
                'koefisien' : np.zeros(self.komponen_gmm),
                'means' : np.zeros((self.komponen_gmm, self.n_channels)),
                'kovarians' : np.zeros((self.komponen_gmm, self.n_channels, self.n_channels))
            }
        }

        
        self.komponen_piksel = np.zeros((self.baris, self.kolom), dtype=np.uint32)
        print('class grabcut berjalan')
        # print(self.baris)

        self.count_smoothness()
        self.inisiasi_piksel()
        self.assign_gmm()
        self.mempelajari_gmm()
        self.build_graph()
        self.mincut_segmentation()
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
        print("beta smoothness selesai")


    def inisiasi_piksel(self):
        print("\nInisasi piksel", self.rect)
        # ix, iy, x, y = 134, 41, 263, 136
        # ix, iy, x, y = 176, 47, 351, 189
        # ix, iy, x, y = self.rect[0], self.rect[1], self.rect[2], self.rect[3]

        self.alpha[self.rect[1]:self.rect[1] + self.rect[3],self.rect[0]:self.rect[0] + self.rect[2]] = F_TF
        self.trimap['TB'] = np.where(self.alpha == F_TB)
        self.trimap['TU'] = np.where(self.alpha == F_TF)
        # print("trimap TU: ", self.trimap['TU'])

        """Inisiasi GMM"""
        self.gmm_fg =  MixtureModel(self.trimap['TU'], 
                        self.gambar[self.trimap['TU']], 
                        self.komponen_gmm, self.theta['TU'])

        self.gmm_bg =  MixtureModel(self.trimap['TB'], 
                        self.gambar[self.trimap['TB']], 
                        self.komponen_gmm, self.theta['TB'])
        
        """Inisiasi GMM untuk bg dan fg dengan parameter gambar"""
        print('\nMulai init random GMM')
        
        self.gmm_fg.init_gmm_rand(self.gambar[self.trimap['TU']], self.theta['TU'])
        self.gmm_bg.init_gmm_rand(self.gambar[self.trimap['TB']], self.theta['TB'])

        # print('theta: ', self.theta)
        print('Inisiasi piksel selesai')


    def assign_gmm(self):
        """Step 1 (assign GMM) pada gambar 2.11"""
        print('\nMulai assign GMM')
        self.komponen_piksel[self.trimap['TU']] = self.gmm_fg.assign_component(
            self.gambar[self.trimap['TU']], self.theta['TU'], self.komponen_gmm
        )

        self.komponen_piksel[self.trimap['TB']] = self.gmm_bg.assign_component(
            self.gambar[self.trimap['TB']], self.theta['TB'], self.komponen_gmm
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
                                 self.komponen_piksel[self.trimap['TU']], 
                                 self.theta['TU'])

        self.gmm_bg.count_params(self.gambar[self.trimap['TB']], 
                                 self.komponen_piksel[self.trimap['TB']], 
                                 self.theta['TB'])

        # print('theta: ', self.theta)

        idx_TF = np.where(self.alpha.reshape(-1) == 3)
        idx_TB = np.where(self.alpha.reshape(-1) == F_TB)
        idx_TU = np.where(self.alpha.reshape(-1) == F_TF)
        print("Idx TU: ", self.alpha.reshape(-1)[idx_TU])


        print('\nmenghitung D')       
        print('theta shape: ', self.theta['TU']['koefisien'].shape)
        
        # Cara default
        # self.U_count_fg = self.gmm_fg.count_D_formula(self.gambar.reshape(-1, 3)[idx_TU], 
        #                     self.komponen_gmm, self.theta['TU'])
        # self.U_count_bg = self.gmm_bg.count_D_formula(self.gambar.reshape(-1, 3)[idx_TU], 
        #                     self.komponen_gmm, self.theta['TB'])

        
        # Cara kedua
        self.D_count_fg = []
        self.D_count_bg = []

        for kn in range(self.komponen_gmm):
            zn = self.gambar.reshape(-1, 3)[idx_TU]

            tmp_d_fg = self.gmm_fg.d_calc(zn, kn, self.theta['TU'])
            tmp_d_bg = self.gmm_bg.d_calc(zn, kn, self.theta['TB'])

            self.D_count_fg.append(tmp_d_fg)
            self.D_count_bg.append(tmp_d_bg)

        self.D_count_fg = np.array(self.D_count_fg)
        self.D_count_bg = np.array(self.D_count_bg)
        self.U_count_fg = np.sum(self.D_count_fg, axis=0)
        self.U_count_bg = np.sum(self.D_count_bg, axis=0)

        print("D fg count: ", self.U_count_fg.shape)
        print("D bg count: ", self.U_count_bg.shape)


    def build_graph(self):
        idx_TF = np.where(self.alpha.reshape(-1) == 3)
        idx_TB = np.where(self.alpha.reshape(-1) == F_TB)
        idx_TU = np.where(self.alpha.reshape(-1) == F_TF)

        print('\n jumlah TB: %d, jumlah TU: %d' % (
            idx_TB[0].size, idx_TU[0].size))
        
        print('sink gc: ', self.sink_gc)

        self.edges = []
        print('edges awal : %d, kapasitas awal: %d' % (len(self.edges), len(self.kapasitas_graph)))

        print("edges: ", ([self.source_gc] * idx_TU[0].size)[:10])
        print("edges: ", ([self.source_gc] * idx_TB[0].size)[:10])
        print("edges: ", ([self.source_gc] * idx_TF[0].size)[:10])
        print("edges: ", ([self.sink_gc] * idx_TU[0].size)[:10])
        print("edges: ", ([self.sink_gc] * idx_TB[0].size)[:10])
        print("edges: ", ([self.sink_gc] * idx_TF[0].size)[:10])

        # Construct T-links
        self.edges.extend(list(zip([self.source_gc] * idx_TB[0].size, idx_TB[0])))
        self.kapasitas_graph.extend([0] * idx_TB[0].size)

        self.edges.extend(list(zip([self.source_gc] * idx_TU[0].size, idx_TU[0])))
        self.kapasitas_graph.extend(self.U_count_bg.tolist())
    
        self.edges.extend(list(zip([self.source_gc] * idx_TF[0].size, idx_TF[0])))
        self.kapasitas_graph.extend([9 * self.gamma_val] * idx_TF[0].size)

        self.edges.extend(list(zip([self.sink_gc] * idx_TB[0].size, idx_TB[0])))
        self.kapasitas_graph.extend([9 * self.gamma_val] * idx_TB[0].size)
        
        self.edges.extend(list(zip([self.sink_gc] * idx_TU[0].size, idx_TU[0])))
        self.kapasitas_graph.extend(self.U_count_fg.tolist())

        self.edges.extend(list(zip([self.sink_gc] * idx_TF[0].size, idx_TF[0])))
        self.kapasitas_graph.extend([0] * idx_TF[0].size)
        
        # left_diff_V = self.gambar[:, 1:] - self.gambar[:, :-1]
        # upleft_diff_V = self.gambar[1:, 1:] - self.gambar[:-1, :-1]
        # up_diff_V = self.gambar[1:, :] - self.gambar[:-1, :]
        # upright_diff_V = self.gambar[1:, :-1] - self.gambar[:-1, 1:]

        print('edges first 5: ', self.edges[:5])
        print('edges last 5: ', self.edges[-5:])

        # n-links
        img_indexes = np.arange(self.baris * self.kolom, dtype=np.uint32).reshape(self.baris, self.kolom)

        mask1 = img_indexes[:, 1:].reshape(-1)
        mask2 = img_indexes[:, :-1].reshape(-1)
        self.edges.extend(list(zip(mask1, mask2)))
        self.kapasitas_graph.extend(self.left_V.reshape(-1).tolist())
        # assert len(edges) == len(self.kapasitas_graph)

        mask1 = img_indexes[1:, 1:].reshape(-1)
        mask2 = img_indexes[:-1, :-1].reshape(-1)
        self.edges.extend(list(zip(mask1, mask2)))
        self.kapasitas_graph.extend(
            self.upleft_V.reshape(-1).tolist())
        # assert len(edges) == len(self.kapasitas_graph)

        mask1 = img_indexes[1:, :].reshape(-1)
        mask2 = img_indexes[:-1, :].reshape(-1)
        self.edges.extend(list(zip(mask1, mask2)))
        self.kapasitas_graph.extend(self.up_V.reshape(-1).tolist())
        # assert len(edges) == len(self.kapasitas_graph)

        mask1 = img_indexes[1:, :-1].reshape(-1)
        mask2 = img_indexes[:-1, 1:].reshape(-1)
        self.edges.extend(list(zip(mask1, mask2)))
        self.kapasitas_graph.extend(self.upright_V.reshape(-1).tolist())
        # assert len(edges) == len(self.kapasitas_graph)

        # assert len(edges) == 4 * self.cols * self.rows - 3 * (self.cols + self.rows) + 2 + \
        #     2 * self.cols * self.rows

        print('graph capacity: ', len(self.kapasitas_graph))
        print('edges: ', len(self.edges))

        # Build the graph using Igraph
        self.gc_graph = ig.Graph(self.kolom * self.baris + 1)
        print('gc_graph: ', self.gc_graph)
        self.gc_graph.add_edges(self.edges)


        # self.gc_graph = mincut_segmentation(self.edges, self.kapasitas_graph)
        # self.gc_graph.build_graf(self.kolom, self.baris)

        # print('graf: ', self.graf)
        # print(self.graf)

    def mincut_segmentation(self):
        """
        Lanjut step 3 (estimate segmentation) pada gambar 2.11
        """
        # self.gc_graph.calc_mincut()
                
        mincut = self.gc_graph.st_mincut(
        self.source_gc, self.sink_gc, self.kapasitas_graph)
        print('foreground pixels: %d, background pixels: %d' % (
            len(mincut.partition[0]), len(mincut.partition[1])))
        # print('jumlah partisi: ', mincut.partition)


        idx_pr = np.where(self.alpha == F_TF)
        img_indexes = np.arange(self.baris * self.kolom,
                                dtype=np.uint32).reshape(self.baris, self.kolom)
        print('idx_pr: ', len(idx_pr[0]))
        print('img_indexes: ', img_indexes)

        self.alpha[idx_pr] = np.where(np.isin(img_indexes[idx_pr], mincut.partition[0]),F_TF, F_TB)
        # self.classify_pixels()
