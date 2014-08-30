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
from scipy.optimize import minimize_scalar

#split comment in list of sentences
def split_sentence(comment):
    l = comment.replace('!','.').replace('?','.').split('.')
    sent = [load.simplify(nltk.WordPunctTokenizer().tokenize(s)) for s in l]
    return [s for s in sent if len(s) > 0]

#merge comment in sentence
def merge_comment(comment):
    string = ''
    for c in comment.comment:
        string += c + ' '
    return string[:-1]

#find parameters for svd classifier
def find_parameters(category,s):
    k = ['L','T','S','F']
    values = {}
    for key in k:
        for k2 in k:
            random.shuffle(category[k2])
            values[(key,k2)] = np.array([s[key].projection(merge_comment(i[0])) for i in category[k2][:2000]])
        fun = lambda x: sum([len(np.where(values[(key,k2)] > x)[0]) for k2 in k if k2 != key])  - len(np.where(values[(key,k2)] > x)[0])
        minimize_scalar(fun, bounds=(0.1,10))
    f = open('files/parameters.txt','wb')
    pickle.dump(result,f)
    f.close()
    print "finished"
        

#train classifiers
def train_classifiers(train, category, set_svd_parameters):
    k = ['L','T','S','F']
    svd_features = load.load_features("tfidf5000.txt")
    bayes_category_features = load.load_features("posneg_category_features.txt")
    bayes_features = load.load_features("posneg_features.txt")
    features=dict()
    s=dict()
    cl=dict()

    #SVD
    for key in k:
        random.shuffle(category[key])
        features[key]=list(set([f[0] for f in svd_features[key][:1500]]) | set(feat.most_frequent(category[key],1500)))
        print "training " +key+ " svd..."
        sentences = sum([split_sentence(merge_comment(c)) for c in category[key][:4000]],[])
        random.shuffle(category[key])
        try:
            s[key]=svd.Svd([features[key], sentences[:4000]], False)
        except:
            s[key]=svd.Svd([features[key], sentences[:3000]],False)
            print "dimension reduced..."
        print "saving..."
        s[key].save_me(str(key+"svdM.txt"), str(key+"svdF.txt"))
    if set_svd_parameters:
        parameters(category, s)

    category=load.load_pickle_file_sparse("simple_category.txt",False)
    
    cl_all = nb.Bayes([list(set(bayes_features[:3000]) | set(feat.most_frequent(train[20000:40000],1500))) + feat.most_frequent_bigrams(train[:20000],100), train],False)
    cl_all.save_me("all_cl.txt")
    print "Overall classificator trained"

    for key in k:
        cl[key]=nb.Bayes([list(set(bayes_category_features[key]) | set(feat.most_frequent(category[key],1500))) + feat.most_frequent_bigrams(category[key],100), category[key]],False)
        cl[key].save_me(key+"cl.txt")
        print key + " classificator trained"


#function for loading data for training
def init():
    print "loading..."
    positive=load.load_pickle_file("simplebeersP.txt")
    negative=load.load_pickle_file("simplebeersN.txt")
    category=load.load_pickle_file_sparse("category.txt",False)
    print "loaded..."
    train=positive + negative
    random.shuffle(train)
    train_classifiers(train, category, False)

#call example
#init()