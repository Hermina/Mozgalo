import numpy as np
from scipy import linalg,spatial
import pickle
import sys

class Svd:

    #constructor for the class Svd, computes matrices U and S which contain a base for the suspace and the length of the ellipse axis
    def __init__(self, parameters, load):
        if load:
            matrix_file = parameters[0]
            features_file = parameters[1]
            path = sys.path[0]+'/../pycode/'
            f = open(path+'/files/'+matrix_file,'r')
            temp = np.load(f)
            self.U = temp['arr_0']
            self.S = temp['arr_1']
            self.Xnorm = temp['arr_2']
            f.close()
            f = open(path+'/files/'+features_file,'rb')
            temp = pickle.load(f)
            self.features = temp[0]
            self.featureIndex = temp[1]
            f.close()
        else:
            features = parameters[0]
            sentences = parameters[1]
            self.featureIndex = {}
            for i in range(len(features)):
                self.featureIndex[features[i]] = i
            self.features = set(features)
            self.sentences = sentences
            self.X, self.dimensions = self.__returnMatrix()
            self.Xnorm = self.X.mean(axis=1)
            self.A = self.X - self.Xnorm[:,np.newaxis]
            self.U, self.S, V = linalg.svd(self.A, full_matrices=False)
            try:
                index = np.where(self.S < 10**(-2))[0][0]
            except:
                index = len(self.S)
            self.index = index
            self.reduceUandS(self.index)

    #computes matrix X from the training set
    def __returnMatrix(self):
        (Xdim, Ydim) = (len(self.features),len(self.sentences))
        X = np.zeros((Xdim,Ydim))
        for i in range(len(self.sentences)):
            sentSet = set(self.sentences[i])
            words = self.features & sentSet
            for word in words:
                X[self.featureIndex[word],i] = 1
        return X, (Xdim, Ydim)

    #saves a trained classifier (matrices U and S) to a file
    def save_me(self, matrix_file, features_file):
        f = open("files/"+ matrix_file,'w')
        np.savez(f, self.U, self.S, self.Xnorm)
        f.close()
        f = open("files/" +features_file, 'wb')
        pickle.dump([self.features, self.featureIndex],f)

    #projects a sentence to the subspace
    def projection(self, sentence):
        sent = np.zeros(len(self.features))
        sentSet = set(sentence)
        words = self.features & sentSet
        for word in words:
            sent[self.featureIndex[word]] = 1
        y = np.dot(self.U.T, sent - self.Xnorm)
        return sum((np.absolute(y)/self.S)**2)

    #reduces sizes of U and S to the given dimension (creates a subspace)
    def reduceUandS(self,dimension):
        self.U = self.U[:,:dimension]
        self.S = self.S[:dimension]


