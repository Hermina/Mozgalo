import nltk
import load
import svd_class as svd
import bayes as nb
import comment as com
import feature_selection as feat
import random
import get_category_sentences as gcs
import numpy as np
import pickle
import string
import scipy as sp
from scipy import optimize
from scipy.optimize import minimize

#makes a confusy matrix for the SVD
k=['L','T','S','F']
category=load.load_pickle_file_sparse("simple_category.txt",False)
s={}
for key in k:
	s[key]=svd.Svd([key+'svdM.txt', key+'svdF.txt'],True)
suma=np.zeros((4,4))
for i in range(2001,3001):
    for key in range(4):
        z = np.array([s['L'].projection(category[k[key]][i].comment),s['T'].projection(category[k[key]][i].comment),s['S'].projection(category[k[key]][i].comment),s['F'].projection(category[k[key]][i].comment)])
        rez = z.argmin()
        suma[key][rez]+=1
print suma
