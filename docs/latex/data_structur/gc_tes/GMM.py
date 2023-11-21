#!/usr/bin/env python
import numpy as np
from sklearn.cluster import KMeans
import random


class GaussianMixture:
    def __init__(self, X, n_components=5):
        self.n_components = n_components
        self.n_features = X.shape[1]

        self.n_samples = np.zeros(self.n_components)

        self.coefs = np.zeros(self.n_components)
        self.means = np.zeros((self.n_components, self.n_features))
    
        # Full covariance
        self.covariances = np.zeros(
            (self.n_components, self.n_features, self.n_features))

        # print("ini x shape: ", X.shape)
        # print('means = ', self.means)
        print('ini covariance awal :', self.covariances)

        self.init_with_rand(X)

    def init_with_rand(self, X):
        label = KMeans(n_clusters=self.n_components, n_init=1).fit(X).labels_
        label2 = np.array([random.randint(0, 4) for i in range(X.shape[0])])

        # print("inisiasi Kmeans Selesai", len(label))
        # print('random label', len(label2))
        self.fit(X, label)

    def calc_score(self, X, ci):
        """Predict probabilities of samples belong to component ci

        Parameters
        ----------
        X : array, shape (n_samples, n_features)

        ci : int

        Returns
        -------
        score : array, shape (n_samples,)
        """
        # print("nilai ci = ", ci)
        # print("nilai coefs[ci] = ", self.coefs[ci])
        score = np.zeros(X.shape[0])
        if self.coefs[ci] > 0:
            diff = X - self.means[ci]
            mult = np.einsum('ij,ij->i', diff, np.dot(np.linalg.inv(self.covariances[ci]), diff.T).T)
            score = np.exp(-.5 * mult) / (np.sqrt(2 * np.pi) * np.sqrt(np.linalg.det(self.covariances[ci])))
            print('score = ', score)
            print('score len = ', len(score))
        # print("kalkulasi score untuk ci = ", ci, " selesai \n")
        return score


    def which_component(self, X):
        """Predict samples belong to which GMM component

        Parameters
        ----------
        X : array, shape (n_samples, n_features)

        Returns
        -------
        comp : array, shape (n_samples,)
        """
        # print("nilai coefs = ", self.coefs)

        print("target : ", X)
        print("hasil res")
        res = np.array([self.calc_score(X, ci) for ci in range(self.n_components)])
        print("hasil res", res.shape)
        prob = res.T
        print("hasil prob",  np.argmax(prob, axis=1))
        return np.argmax(prob, axis=1)
        # return X

    def calc_prob(self, X):
        """Predict probability (weighted score) of samples belong to the GMM

        Parameters
        ----------
        X : array, shape (n_samples, n_features)

        Returns
        -------
        prob : array, shape (n_samples,)
        """
        prob = [self.calc_score(X, ci) for ci in range(self.n_components)]
        print("kalkulasi prob selesai")
        return np.dot(self.coefs, prob)

    def fit(self, X, labels):
        assert self.n_features == X.shape[1]
        # print("fungsi fit berjalan")
      
        print('label dari fit yaitu ', labels)
        self.n_samples[:] = 0
        self.coefs[:] = 0
        # print("ini coefs ",  self.coefs)

        
        uni_labels, count = np.unique(labels, return_counts=True)
        
        print("bilangan unik = ", np.unique(labels, return_counts=True))
        self.n_samples[uni_labels] = count
        print('n samples', self.n_samples)

        # variance = 0.01
        for ci in uni_labels:
            n = self.n_samples[ci]
            # print('mean ci: ', ci == labels)

            self.coefs[ci] = n / np.sum(self.n_samples)
            self.means[ci] = np.mean(X[ci == labels], axis=0)
            self.covariances[ci] = 0 if self.n_samples[ci] <= 1 else np.cov(X[ci == labels].T)
            # self.covariances[ci] = np.cov(X[ci == labels].T)

            # det = np.linalg.det(self.covariances[ci])
            # if det <= 0:
            #     # Adds the white noise to avoid singular covariance matrix.
            #     self.covariances[ci] += np.eye(self.n_features) * variance
            #     det = np.linalg.det(self.covariances[ci])
        print("ini coefs ",  self.coefs)
        print("ini fit dari mean",  self.means)
        print("ini fit dari cov",  self.covariances[4])
        # print("ini n_samples di fit",  self.n_samples)