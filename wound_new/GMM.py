import numpy as np
import random

class GaussianMixtureModels:
    def __init__(self, z, komponen_gmm = 5):
        self.komponen_gmm = komponen_gmm
        # print('z object: ', z.shape)
        self.n_channels = z.shape[1]
        # print(self.n_channels)
        self.n_samples = np.zeros(self.komponen_gmm)

        self.theta ={
            'koefisien' : np.zeros(self.komponen_gmm),
            'kovarians' : np.zeros((self.komponen_gmm, self.n_channels, self.n_channels)),
            'means' : np.zeros((self.komponen_gmm, self.n_channels))
        }
        # self.koefisien = np.zeros(self.komponen_gmm)
        # self.means = np.zeros((self.komponen_gmm, self.n_channels))
        # self.kovarians = np.zeros((self.komponen_gmm, self.n_channels, self.n_channels))

        # print("ini x shape: ", z.shape)
        # print('means = ', self.means)
        # print('ini covariance awal :', self.kovarians)
        # self.init_gmm_rand(z)


    def init_gmm_rand(self, z):
        labels_k = []
        for i in range(z.shape[0]):
            labels_k.append(random.randint(0, self.komponen_gmm-1))
        labels_k = np.array(labels_k)
        # labels_k = np.array([random.randint(0, self.komponen_gmm-1) for i in range(z.shape[0])])
        print('random labels selesai yaitu :')
        print(labels_k)
        print("banyaknya labels: ",labels_k.size)
        self.count_params(z, labels_k)

    def count_params(self, z, labels_k):
        """
        Fungsi ini untuk menghitung nilai dari parameter dari GMM
        Parameter fungsi :
            1. z (target) : array, shape(n_samples, n_features rgb)
            2. labels_k : nilai k untuk tiap piksel

        hasil :
            - nilai koefisien
            - nilai mean
            - nilai kovarians
        """
        self.n_samples[:] = 0
        self.theta['koefisien'][:] = 0   

        # print(len(target))

        variables_k, count = np.unique(labels_k, return_counts=True)
        self.n_samples[variables_k] = count
        print(self.n_samples)
        print('nilai K: ', variables_k)
        print('jumlah piksel untuk k = 0,1,2,3,4: ', count)

        for k in variables_k:
            print(k)
            n_k = self.n_samples[k]

            self.theta['koefisien'][k] = n_k / np.sum(self.n_samples)
            self.theta['means'][k] = np.mean(z[k == labels_k], axis = 0)
            self.theta['kovarians'][k] = np.cov(z[k == labels_k].T) 

            # self.kovarians[k] = 0 if self.n_samples[k] <= 1 else np.cov(target[k == labels_k].T)
            # print(tmp)

        # print('koefisien: ', self.koefisien)
        # print('means: ', self.means)
        # print('kovarians: ', self.kovarians)
        print('\n')
        # print(np.sum(self.n_samples))

        
    def assign_component(self, z):
        """
        Tahap assign gmm dengan menggunakan rumus 2.7
        """
        print('target assign: \n', z.shape)
        gauss_distribution = []

        for k in range(self.komponen_gmm):
            gauss_score = self.dis_mult(z, k)
            gauss_distribution.append(gauss_score)

        gauss_distribution = np.array(gauss_distribution)
        # print("karakter matriks res: ",gauss_distribution.shape)

        gauss_distribution = gauss_distribution.T
        print("karakter matriks res: ",gauss_distribution.shape)

        return np.argmin(gauss_distribution, axis=1)

    def dis_mult(self, z, k):
        """
        Fungsi untuk menghitung 
        distribusi gaussian multivariate 
        pada rumus 2.4

        **Parameter fungsi:
            1. Z (image target) : array, shape (n_samples, n_features)
            2. k : int

        return
        score : array, shape(n_samples)
        ----------------
        """
    
        # print('menghitung distribusi multivariate ', k)
        result = np.zeros(z.shape[0])
        # print(result.shape)
        if self.theta['koefisien'][k] > 0 :
            diff = z - self.theta['means'][k]
            # print('selisih:\n, ', diff[:10])
            inv_covariance = np.linalg.inv(self.theta['kovarians'][k])
            mult  = np.einsum('ij,ij->i', diff, np.dot(inv_covariance, diff.T).T)
            result = np.exp(-.5 * mult) / (np.sqrt(2 * np.pi) * np.sqrt(np.linalg.det(self.theta['kovarians'][k])))
        return result

    
    def count_D_formula(self, z):
        gauss_distribution = []
        print("koefisien: ",self.theta['koefisien'])
        print("kovarians: ",self.theta['kovarians'])
        print("means: ",self.theta['means'])
        for k in range(self.komponen_gmm):
            tmp_gauss_distribution = self.dis_mult(z, k)
            gauss_distribution.append(tmp_gauss_distribution)
        gauss_distribution = np.array(gauss_distribution)
        print("gauss shape: ", gauss_distribution.shape)
        print("koef shape: ", self.theta['koefisien'].shape)

        return -np.log(np.dot(self.theta['koefisien'], gauss_distribution))

