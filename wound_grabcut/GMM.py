import numpy as np
import random

class GaussianMixtureModels:
    def __init__(self, target, komponen_gmm = 5):
        self.komponen_gmm = komponen_gmm
        # print('target object: ', target.shape)
        self.n_channels = target.shape[1]
        # print(self.n_channels)
        self.n_samples = np.zeros(self.komponen_gmm)

        self.koefisien = np.zeros(self.komponen_gmm)
        self.means = np.zeros((self.komponen_gmm, self.n_channels))
        self.kovarians = np.zeros((self.komponen_gmm, self.n_channels, self.n_channels))

        # print("ini x shape: ", target.shape)
        # print('means = ', self.means)
        # print('ini covariance awal :', self.kovarians)
        self.init_gmm_rand(target)


    def init_gmm_rand(self, target):
        labels_k = np.array([random.randint(0,4) for i in range(target.shape[0])])
        print('random labels selesai yaitu :')
        print(labels_k)
        print("banyaknya labels: ",labels_k.size)
        self.count_params(target, labels_k)


    def count_params(self, target, labels_k):
        """
        Fungsi ini untuk menghitung nilai dari parameter dari GMM
        Parameter fungsi :
            1. target : array, shape(n_samples, n_features rgb)
            2. labels_k : nilai k untuk tiap piksel

        hasil :
            - nilai koefisien
            - nilai mean
            - nilai kovarians
        """
        self.n_samples[:] = 0
        self.koefisien[:] = 0   

        # print(len(target))

        variables_k, count = np.unique(labels_k, return_counts=True)
        self.n_samples[variables_k] = count
        print(self.n_samples)
        print('nilai K: ', variables_k)
        print('jumlah piksel untuk k = 0,1,2,3,4: ', count)

        for k in variables_k:
            print(k)
            n_k = self.n_samples[k]

            self.koefisien[k] = n_k / np.sum(self.n_samples)
            self.means[k] = np.mean(target[k == labels_k], axis = 0)
            if(self.n_samples[k] <= 1):
                self.kovarians[k] = 0
            else:
                self.kovarians[k] = np.cov(target[k == labels_k].T)

            # self.kovarians[k] = 0 if self.n_samples[k] <= 1 else np.cov(target[k == labels_k].T)
            # print(tmp)

        print('koefisien: ', self.koefisien)
        print('means: ', self.means)
        print('kovarians: ', self.kovarians)
        print('\n')
        # print(np.sum(self.n_samples))
    
    def dis_mult(self, target, k):
        """
        Fungsi untuk menghitung distribusi gaussian multivariate pada rumus 2.4
        Parameter fungsi:
            1. Target : array, shape (n_samples, n_features)
            2. k : int

        return
        score : array, shape(n_samples)
        ----------------
        """
    
        # print('menghitung distribusi multivariate ', k)
        result = np.zeros(target.shape[0])
        # print(result.shape)
        if self.koefisien[k] > 0 :
            diff = target - self.means[k]
            mult  = np.einsum('ij,ij->i', diff, 
                   np.dot(np.linalg.inv(self.kovarians[k]), diff.T).T)
            result = np.exp(-.5 * mult) / (np.sqrt(2 * np.pi) * np.sqrt(np.linalg.det(self.kovarians[k])))

        return result

    def assign_component(self, target):

        res = []
        for k in range(self.komponen_gmm):
            tmp_score = self.dis_mult(target, k)
            res.append(tmp_score)
        res = np.array(res)
        print("karakter matriks res: ",res.shape)
        res = res.T
        print("karakter matriks res: ",res.shape)

        return np.argmax(res, axis=1)

    def count_prob(self, target):
        res_prob = []
        for k in range(self.komponen_gmm):
            tmp_prob = self.dis_mult(target, k)
            res_prob.append(tmp_prob)
        res_prob = np.array(res_prob)
        print("cal prob: ", res_prob.shape)

        return np.dot(self.koefisien, res_prob)