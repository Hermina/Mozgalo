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
import sys
k = ['L','T','S','F']
category=load.load_pickle_file_sparse("simple_category.txt",False)

#def split_sentence(comment):
#    l = comment.comment.replace('!','.').replace('?','.').split('.')
#    sent = [load.simplify(nltk.WordPunctTokenizer().tokenize(s)) for s in l]
#    return sent

#def f(x):
#    return sum([s[key].projection<x] for key in k if sum([s[key].projection(sent) < x])

#def merge_comment(comment):
#    return (" ").join(comment.comment)
        
#def parameters(category, s):
   
 #   for key in k:
 #       for comment in category[key][:1]:
 #       	print merge_comment(comment)


s = dict()
path = sys.path[0]+'/../pycode/'
for key in k:
    s[key] = svd.Svd([key+'svdM.txt', key+'svdF.txt'],True)
parameters(category, s)