import numpy as np
import random

class MixtureModel:
    def __init__(self, alpha, z, komponen_gmm, theta):
        self.komponen_gmm = komponen_gmm
        # print('z object: ', z.shape)
        self.n_channels = z.shape[1]
        # print(self.n_channels)
        self.n_samples = np.zeros(self.komponen_gmm)

        self.theta = theta
        self.F_TB = 0
        self.F_TF = 1


        # self.koefisien = np.zeros(self.komponen_gmm)
        # self.means = np.zeros((self.komponen_gmm, self.n_channels))
        # self.kovarians = np.zeros((self.komponen_gmm, self.n_channels, self.n_channels))

        # print("ini x shape: ", z.shape)
        # print('means = ', self.means)
        # print('ini covariance awal :', self.kovarians)
        # self.init_gmm_rand(z)

    def init_gmm_rand(self, z, theta):
        labels_k = []
        for i in range(z.shape[0]):
            labels_k.append(random.randint(0, self.komponen_gmm-1))
        labels_k = np.array(labels_k)
        # labels_k = np.array([random.randint(0, self.komponen_gmm-1) for i in range(z.shape[0])])
        print('random labels selesai yaitu :')
        print(labels_k)
        print("banyaknya labels: ",labels_k.size)
        self.count_params(z, labels_k, theta)

    def count_params(self, z, labels_k, theta):
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
        theta['koefisien'][:] = 0   

        # print(len(target))

        variables_k, count = np.unique(labels_k, return_counts=True)
        self.n_samples[variables_k] = count

        print(self.n_samples)
        print('nilai K: ', variables_k)
        print('jumlah piksel untuk k = 0,1,2,3,4: ', count)

        for k in variables_k:
            # print(k)
            n_k = self.n_samples[k]

            theta['koefisien'][k] = n_k / np.sum(self.n_samples)
            theta['means'][k] = np.mean(z[k == labels_k], axis = 0)
            theta['kovarians'][k] = np.cov(z[k == labels_k].T) 

            # self.kovarians[k] = 0 if self.n_samples[k] <= 1 else np.cov(target[k == labels_k].T)
            # print(tmp)

        # print('koefisien: ', theta['koefisien'])
        # print('means: ', theta['means'])
        # print('kovarians: ', theta['kovarians'])
        # print('\n')
        # print('theta: ', theta)
        # print(np.sum(self.n_k_samples))

    def assign_component(self, z, theta, komponen_gmm):
        """
        Tahap assign gmm dengan menggunakan rumus 2.7
        """
        print('target assign: \n', z.shape)
        gauss_distribution = []

        for k in range(komponen_gmm):
            gauss_score = self.dis_mult(z, k, theta)
            gauss_distribution.append(gauss_score)

        gauss_distribution = np.array(gauss_distribution)
        # print("karakter matriks res: ",gauss_distribution.shape)

        gauss_distribution = gauss_distribution.T
        print("karakter matriks res: ",gauss_distribution.shape)

        return np.argmin(gauss_distribution, axis=1)

    def dis_mult(self, z, k, theta):
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
        # print('komponen z: ', z)
        # print(result.shape)
        # theta['kovarians']
        if theta['koefisien'][k] > 0 :

            diff = z - theta['means'][k]
            # print('selisih:\n, ', diff[:10])
            # print(theta['kovarians'][k])

            inv_covariance = np.linalg.inv(theta['kovarians'][k])
            mult  = np.einsum('ij,ij->i', diff, np.dot(inv_covariance, diff.T).T)
            print('mult: ',mult)
            result = np.exp(-.5 * mult) / (np.sqrt(2 * np.pi) * np.sqrt(np.linalg.det(theta['kovarians'][k])))
        return result


    def gauss_dist(self, zn, kn, theta):
        diff = zn - theta['means'][kn]
        # print('bahan kn, zn: ', kn, " ", zn)
        # print('means: ', theta['means'][kn])
        # print('selisih: , ', diff, '\n')

        inv_covariance = np.linalg.inv(theta['kovarians'][kn])
        mult  = np.einsum('ij,ij->i', diff, np.dot(inv_covariance, diff.T).T)
        result = np.exp(-.5 * mult) / (np.sqrt(2 * np.pi) * np.sqrt(np.linalg.det(theta['kovarians'][kn])))

        # print(inv_covariance)
        # print('mult: ',mult)
        # print('result gauss ', result)
        return result

    def gauss_dist_second(self, zn, kn, theta):
        # print('bahan kn, zn: ', kn, " ", zn)
        # print('means: ', theta['means'][kn])

        diff = zn - theta['means'][kn]
        inv_covariance = np.linalg.inv(theta['kovarians'][kn])
        # mult  = np.dot( diff, np.dot(inv_covariance, diff.T).T) # <-- kode asal
        # mult  = np.dot(np.dot(diff, inv_covariance), diff.T)
        mult = np.sum(diff * np.dot(diff, inv_covariance.T), axis=1)
        # mult = np.einsum('ij,ji->i', diff, np.dot(inv_covariance, diff.T))
        result = 0.5 * (np.log(np.linalg.det(theta['kovarians'][kn]))) + 0.5 * mult
        # result = np.exp(-.5 * mult) / (np.sqrt(2 * np.pi) * np.sqrt(np.linalg.det(theta['kovarians'][kn])))
      
        # print("diff shape: ", diff.shape)
        # print("anu shape: ", np.dot(inv_covariance, diff.T).T.shape)

        # print(inv_covariance)
        # print('mult: ',mult)
        # print('result gauss ', result)
        return result


    def count_D_formula(self, z, komponen_gmm, theta):
        gauss_distribution = []
        # print(theta)
        for k in range(komponen_gmm):
            tmp_gauss_distribution = self.dis_mult(z, k, theta)
            gauss_distribution.append(tmp_gauss_distribution)
        gauss_distribution = np.array(gauss_distribution)
        print("gauss shape: ", gauss_distribution.shape)
        # print("koef shape: ", self.theta['koefisien'].shape)

        return -np.log(np.dot(self.theta['koefisien'], gauss_distribution))

 
    def d_calc(self, zn, kn, theta):
        # gauss_res1 = self.gauss_dist_second(zn, kn, theta)
        gauss_res1 = self.gauss_dist(zn, kn, theta)

        # print(gauss_res)
        d_res1 = -np.log(theta['koefisien'][kn]) + gauss_res1
        # d_res = -np.log(np.dot(theta['koefisien'][kn], gauss_res))

        # print("dres1: ", d_res1)
        # exit()
        return d_res1
