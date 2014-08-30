import nltk
import comment
import load
import pickle
import get_category_sentences as gcs
import random

#returns list of words sorted in decreasing order by tf-idf value
def tf_idf(sparse_comments, comments, count):
    words = set()
    category = sum([com.comment for com in sparse_comments], [])
    words.update(category)
    document = sum([com.comment for com in comments], [])
    tf = nltk.text.TextCollection(document)
    tf_idfs = []
    for word in words:
        tf_idfs.append((word,tf.tf_idf(word,category)))
    pairs = sorted(tf_idfs,key=lambda x: x[1], reverse=True)   
    return [p[0] for p in pairs[:count]]

#returns most frequent words
def most_frequent(comments, count):
    all_words = sum([com.comment for com in comments], [])
    all_words = nltk.FreqDist(all_words)
    return all_words.keys()[:count]
    
#returns most frequent bigrams
def most_frequent_bigrams(comments, count):
    all_bigrams = sum([nltk.bigrams(com.comment) for com in comments], [])
    all_bigrams = nltk.FreqDist(all_bigrams)
    return all_bigrams.keys()[:count]

#get tf-idf values per category using count comments per category
def get_tfidf_values(open_file, save_file, count):
    dic = load.load_pickle_file_sparse(open_file,False,True)
    tfidf = gcs.prepare_dictionary(['L','T','S','F','O'])
    for i in dic.keys():
        print i
        random.shuffle(dic[i])
        comments = []
        for j in dic.keys():
            random.shuffle(dic[j])
            comments += dic[j][:count]
        tfidf[i] = tf_idf(dic[i][:count], comments, 2000)     
    f = open('files/'+save_file,'wb')
    pickle.dump(tfidf,f)
    f.close()
  
#get tf-idf values per category for positive and negative and average comments in one list
#saves dictionary of features per category in save_file 
def get_tfidf_posneg_category(open_file,save_file, number, count):
   dic = load.load_pickle_file_sparse(open_file,False)
   tfidf = gcs.prepare_dictionary(['L','T','S','F','O'])
   for i in dic.keys():
       dic[i] = determine_class(dic[i])
       random.shuffle(dic[i])
       pos = [d for d in dic[i] if d.grade == 'pos'][:number]
       avg = [d for d in dic[i] if d.grade == 'avg'][:number]
       neg = [d for d in dic[i] if d.grade == 'neg'][:number]
       _all = pos + avg+ neg
       pos_f = set(tf_idf(pos,_all,count))
       avg_f = set(tf_idf(avg,_all,count))
       neg_f = set(tf_idf(neg,_all,count))
       tfidf[i] = list(pos_f | avg_f | neg_f)     
   f = open(save_file,'wb')
   pickle.dump(tfidf,f)
   f.close()

#get tf-idf values for positive and negative and average comments in one list
#saves list of features in save_file
def get_tfidf_posneg(open_file,save_file, number, count):
    tfidf = {'pos':[],'neg':[],'avg':[]}
    pos = load.load_pickle_file(open_file[0],False,True)
    neg = load.load_pickle_file(open_file[1],False,True)
    doc = determine_class(pos) + determine_class(neg)
    pos = [d for d in doc if d.grade == 'pos']
    avg = [d for d in doc if d.grade == 'avg']
    neg = [d for d in doc if d.grade == 'neg']
    random.shuffle(pos)
    random.shuffle(avg)
    random.shuffle(neg)
    pos = pos[:number]
    neg = neg[:number]
    avg = avg[:number]
    _all = pos + neg + avg
    tfidf['pos'] = tf_idf(pos, pos + neg + avg, count)
    tfidf['neg'] = tf_idf(neg, pos + neg + avg, count)
    tfidf['avg'] = tf_idf(avg, pos + neg + avg, count)
    features = list(set(tfidf['pos']) | set(tfidf['avg']) | set(tfidf['neg']))
    print len(features)
    f = open(save_file,'wb')
    pickle.dump(tfidf,f)
    f.close()
    
    
#determines if the comment is very positive or very negative in order to learn on such sentences, all other sentences are considered neutral
def determine_class(comments):
    for com in comments:
        if (com.grade<=2.5):
            com.grade = 'neg'
        elif(com.grade>4.75):
            com.grade = 'pos'
        else:
            com.grade = 'avg'   
    return comments

#call examples
#get_tfidf_posneg(['files//simplebeersP.txt','simplebeersN.txt'],'posneg_features.txt', 2000 ,2000)
#get_tfidf_posneg_category('simplecategory.txt','posneg_category_features.txt', 5000, 2000)
