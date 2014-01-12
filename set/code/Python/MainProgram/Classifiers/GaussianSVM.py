import os, sys
sys.path.append("..")

from Utilities.FeatureSet import FeatureSet
from svmutil import *

class GaussianSVM(object):
    """docstring for GaussianSVM"""
    svmModel = None
    labels = None
    featureMatrix = None

    #featureMatrix is an iterable (list, tuple etc.) of numpy arrays/vectors:
    ##e.g. [featureSet1.getVector(), featureSet2.getVector(), fe5.getVector() ...]

    #Use like this:
    #gSVM = GaussianSVM(costParam=your_chosen_number)
    def __init__(self, labelList=None, featureMatrix=None,\
                     pathToModel='./Classifiers/gaussianSVM_model.bak', costParam=5):
        super(GaussianSVM, self).__init__()

        if labelList is None or featureMatrix is None:     
                self.svmModel = self.loadModel(pathToModel)
        else:
                self.labels = labelList
                self.featureMatrix = featureMatrix
                svmProb = svm_problem(self.labels, self.featureMatrix)

                #t = 2 model type Gaussian/RBF
                #s = 0 C-SVC multi-class classifier
                #c = cost parameter of C-SVC
                params = svm_parameter('-s 0 -t 2 -c %s -b 1'%str(costParam))
                self.svmModel = svm_train(svmProb, params)
                self.saveModel(pathToModel, self.svmModel)

    def saveModel(self, filename, model):
        try:
            svm_save_model(filename, model)
        except IOError:
            sys.stderr.write("\nCould not save model.\n")

    def loadModel(self, filename):
        try:
            return svm_load_model(filename)
        except IOError:
            sys.stderr.write("\nCould not load model.\n")

    def classifyDocument(self, label, featureSet):
        vector = featureSet.getVector()
        if isinstance(featureSet, FeatureSet):
            p_labels, p_acc, p_vals = svm_predict([0]*len(vector), [vector], self.svmModel)
            #Do stuff with variables
        else:
            raise TypeError("Feature set is not of the correct type.\nMust be of type 'FeatureSet'.\n")

        
