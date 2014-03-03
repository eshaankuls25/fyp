import os, sys
sys.path.append("..")
from nltk.classify.naivebayes import NaiveBayesClassifier as NB

class NaiveBayes(object):
    """docstring for NaiveBayes"""

    nb = None
    classes = None
    featureMatrix = None

    def __init__(self, classList, featureMatrix):
        super(NaiveBayes, self).__init__()
        print "\n-------------------------\nNaive Bayes:\n-------------------------\n"
        
        self.classes = classList
        self.featureMatrix = featureMatrix
        self.nb = NB.train(zip(featureMatrix, classList))
        self.showMostInformativeFeatures()

    def classifyDocument(self, classes, vectors):
        if isinstance(vectors, dict) and isinstance(classes, int):
            return self.nb.classify((vectors, classes))
        elif isinstance(vectors, list) and isinstance(classes, list):
            return self.nb.classify(zip(vectors, classes))

    def showMostInformativeFeatures(self, n=10):
        self.nb.show_most_informative_features(n)

    def getMostInformativeFeatures(self, n=100):
        return self.nb.most_informative_features(n)

    
	
	
