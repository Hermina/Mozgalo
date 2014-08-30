import svd_class as svd
import bayes as nb
import load
import nltk
import pickle
import sys

class Beer_rater:

    #constructor for a Beer_rater
    def __init__(self):
        self.k = ['L','T','S','F']
        self.cl = dict()
        self.svd = dict()
        path = sys.path[0]+'/../pycode/'
        f = open(path+'/files/parameters.txt','rb')
        self.parameters = pickle.load(f)
        f.close()
        #print self.parameters
        for key in self.k:
            self.cl[key] = nb.Bayes([key+'cl.txt'],True)
            self.svd[key] = svd.Svd([key+'svdM.txt', key+'svdF.txt'],True)
        self.cl_all = nb.Bayes(['all_cl.txt'],True)

    #returns grades for a sentence in shape [grade, look, smell, taste, feel, overall]
    def classify(self, comment):
        sentences = self.__split_sentence(comment)
        comment = sum(sentences,[])
        test_set=dict()
        gr=dict()
        occured=dict()
        for key in self.k:
            test_set[key] = []
            gr[key] = 0
            occured[key]=0
            for sent in sentences:
                if(self.svd[key].projection(sent) < self.parameters[key]):
                    test_set[key]+=sent
                    occured[key]=1
            if occured[key] == 1:
                gr[key]=self.cl[key].grade_sentence(test_set[key])
        overall=self.cl_all.grade_sentence(comment)
        grade=0.05*gr['L']+0.2*gr['T']+0.15*gr['S']+0.1*gr['F']+0.5*overall
        control=0.05*occured['L'] +0.2*occured['T']+0.15*occured['S']+0.1*occured['F']+0.5*1
        grade=grade/control
        grades = [grade, gr['L'], gr['S'], gr['T'], gr['F'], overall]
        return ["{0:.2f}".format(g) for g in grades]

    #returns grades for a sentence in shape [grade, look, smell, taste, feel, overall] using synonims
    def classify_sin(self, comment):
        sentences = self.__split_sentence(comment)
        comment = sum(sentences,[])
        test_set=dict()
        gr=dict()
        occured=dict()
        for key in self.k:
            test_set[key] = []
            gr[key] = 0
            occured[key]=0
            for sent in sentences:
                if(self.svd[key].projection(sent) < self.parameters[key]):
                    test_set[key]+=sent
                    occured[key]=1
            if occured[key] == 1:
                gr[key]=self.cl[key].grade_sentence_sin(test_set[key])
        overall=self.cl_all.grade_sentence_sin(comment)
        grade=0.05*gr['L']+0.2*gr['T']+0.15*gr['S']+0.1*gr['F']+0.5*overall
        control=0.05*occured['L'] +0.2*occured['T']+0.15*occured['S']+0.1*occured['F']+0.5*1
        grade=grade/control
        grades = [grade, gr['L'], gr['S'], gr['T'], gr['F'], overall]
        return ["{0:.2f}".format(g) for g in grades]

    #splits a comment into sentences for category analysis
    def __split_sentence(self, comment):
        l = comment.replace('!','.').replace('?','.').split('.')
        sent = [load.simplify(nltk.WordPunctTokenizer().tokenize(s)) for s in l]
        return sent

#b=Beer_rater()
#print b.classify(" Only my second Belgian Ale and a fun experience. A pale clear straw color in the glass with a thin, quickly dissipating head. Drinkable and refreshing with complex spice and herb notes, notably mild clove, and a hint of grain. One of the best jobs of masking a high alcohol content I have experienced. Our table of four agreed that the beer seemed very light and drinkable.")
#print b.classify("clear straw")
