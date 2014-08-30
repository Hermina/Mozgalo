import nltk
import pickle
import random
import string
import comment
import get_category_sentences as gcs

#word stemmer
def stem(sentence):
    stemmer = nltk.PorterStemmer()
    return [stemmer.stem(word) for word in sentence]

#remove stopwords
def remove_stopwords(sentence):
    stopwords = nltk.corpus.stopwords.words('english')
    return [w for w in sentence if w not in stopwords and w != 'no']

#remove puntuation
def remove_punctuation(sentence):
    return [w for w in sentence if w not in string.punctuation]

#remove stopwords, punctuation and stem in one loop
def simplify(sentence):
    stopwords = nltk.corpus.stopwords.words('english')
    stemmer = nltk.PorterStemmer()
    return [stemmer.stem(w.lower()) for w in sentence if w == 'no' or (w not in stopwords and w not in string.punctuation)]

#word tagger
def tagger(sentence):
    return nltk.pos_tag(sentence)

#files like beersP.txt, as_list defines sentence as list of words
#simple is for calling simplify on every word in sentence
def load_pickle_file(fileName, simple = False, as_list = True):
    documents = []
    f = open('files/'+fileName, 'rb')
    load = pickle.load(f)
    f.close()
    for beer in load.keys():
        for com in load[beer][6]:
            if as_list:
                sent = com[8]
            else:
                sent = nltk.WordPunctTokenizer().tokenize(com[8])
            if simple:
                sent = simplify(sent)
            com = comment.Comment(beer, com[:8], sent, com[9])
            documents.append(com)
    return documents

#get beer names form file
def load_names(fileName):
    f = open('files/'+fileName, 'rb')
    load = pickle.load(f)
    return set(load.keys())

def load_features(fileName):
    f = open("files/"+fileName,'rb')
    load = pickle.load(f)
    f.close()
    return load
    
#files like category.txt, returns dictionary with keys ['L','T','S','F','O']
def load_pickle_file_sparse(fileName, simple = True):
    category_dictionary = gcs.prepare_dictionary(['L','T','S','F','O'])
    f = open('files/'+fileName, 'rb')
    load = pickle.load(f)
    f.close()
    for key in load.keys():
        for com in load[key]:
            sent = com[0]
            if simple:
                sent = simplify(sent)
            sc = comment.SparseComment(com[1], sent)
            category_dictionary[key].append(sc)
    return category_dictionary
