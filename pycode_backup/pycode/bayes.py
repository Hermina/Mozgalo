import nltk
import comment
import math
import pickle
import sys

class Bayes:

    #trains a naive bayes classifier on a given train set with a given feature set, or loads a classifier from a file
    def __init__(self, parameters, load):
        if load:
            path = sys.path[0]+'/../pycode/'
    	    load_file = parameters[0]
    	    f = open(path+'/files/'+load_file, 'rb')
    	    temp = pickle.load(f)
    	    self.classifier = temp[0]
    	    self.features = set(temp[1])
    	    f.close()
    	else:
    	    features = parameters[0]
    	    train = parameters[1]
    	    t = self.determine_class(train)
    	    self.features = set(features)
    	    self.train_set = [(self.document_features(d),c) for (d,c) in t]
    	    self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)


    #determines if the comment is very positive or very negative in order to learn on such sentences, all other sentences are considered neutral
    def determine_class(self,train):
        documents = []
        poz=0
        neg=0
        avg=0
        for com in train:
            if (com.grade<=2.5):
                documents.append([com.comment,'neg'])
                neg+=1
            elif(com.grade>4.75):
                documents.append([com.comment,'pos'])
                poz+=1
            else:
                documents.append([com.comment,'avg'])
                avg+=1
        return documents

    #converts a sentence to a list of features
    def document_features(self,sent):
	sent.extend(nltk.bigrams(sent))
	features = {}
	common = list(self.features & set(sent))
	for feat in common:
	    features[feat] = True
        return features

    #returns synonims
    def returnSynonims(self,word):
        x = []
        for y in wn.synsets(word):
            x.append(y.lemma_names)
        return x

    #returns our grade computed for a comment
    def grade(self,com):
        test = self.document_features(com.comment)
        dist=self.classifier.prob_classify(test)
        return dist.prob("pos")*5+dist.prob("avg")*3+dist.prob("neg")*1

    #returns our grade computed for a sentence
    def grade_sentence(self,sent):
        test = self.document_features(sent)
        dist=self.classifier.prob_classify(test)
        return dist.prob("pos")*5+dist.prob("avg")*3+dist.prob("neg")*1

    #returns our grades computed for beers in the test set
    def grade_set(self,test):
        beers=dict()
        for d in test:
            if (d.beer not in beers.keys()):
                beers[d.beer]=[]
            beers[d.beer].append(self.document_features(d.comment))
        i = 0
        grades=dict()
        for k in beers.keys():
            g=0
            for t in beers[k]:
                dist=self.classifier.prob_classify(t)
                g=g+ dist.prob("pos")*5+dist.prob("avg")*3+dist.prob("neg")*1
                i += 1
            grades[k]=(1.0*g)/len(beers[k])
        return grades

    #prints the absolute and the square difference between our grade and their grade for the first num comments in test
    def test(self,test,num):
        test_set = [(self.document_features(d.comment),d.grade) for d in test]
        s=0
        s2=0
        for t in test_set[:num]:
            dist=self.classifier.prob_classify(t[0])
            s = s + abs(dist.prob("pos")*5+dist.prob("avg")*3+dist.prob("neg") - t[1])
            s2 = s + (dist.prob("pos")*5+dist.prob("avg")*3+dist.prob("neg") - t[1])**2
        s2 = s2/num
        s = s/num
        print "apsolutna greska: ", s
        print "kvadratna greska: ", s2

    #saves a trained classifier to a file
    def save_me(self, save_file):
	f = open("files/" + save_file, 'wb')
	pickle.dump([self.classifier, self.features],f)
	f.close()
