import os, sys
from os.path import normpath, isfile
sys.path.append("..")

#from Utilities.FeatureSet import FeatureSet
from svmutil import *

class GaussianSVM(object):
    """docstring for GaussianSVM"""
    model = None
    classes = None
    featureMatrix = None

    #featureMatrix is an iterable (list, tuple etc.) of dictionaries/vectors:
    ##e.g. [featureSet1.getVector(), featureSet2.getVector(), fe5.getVector() ...]

    #Use like this:
    #gSVM = GaussianSVM(costParam=your_chosen_number)
    def __init__(self, classList=None, featureMatrix=None,\
                     pathToModel='./Classifiers/gaussianSVM_model.bak', costParam=5):
        super(GaussianSVM, self).__init__()

        if classList is None or featureMatrix is None:
                if isinstance(pathToModel, basestring) and isfile(pathToModel):
                    self.model = self.loadModel(pathToModel)
                else:
                    sys.stderr.write("\nPath to model is incorrect.\n")
                    sys.exit(1)
        else:
                self.classes = classList
                self.featureMatrix = featureMatrix
                svmProb = svm_problem(self.classes, self.featureMatrix)

                #t = 2 model type Gaussian/RBF
                #s = 0 C-SVC multi-class classifier
                #c = cost parameter of C-SVC
                params = svm_parameter('-s 0 -t 2 -c %s -b 1'%str(costParam))
                self.model = svm_train(svmProb, params)
                self.saveModel(pathToModel, self.model)

                print "--------------Support Vectors:\n",\
                      "--------------\nCoefficients: ", self.model.get_sv_coef(),\
                      "\nVectors: ", self.model.get_SV() 

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

    def classifyDocument(self, classes, vectors):
        print "Expected Class(es): ", classes, " Vector(s): ", vectors, "\n"    
        if isinstance(vectors, dict) and isinstance(classes, int):
            p_classes, p_acc, p_vals = svm_predict([classes], [vectors], self.model, options="-b 1")
        elif isinstance(vectors, list) and isinstance(classes, list):
            p_classes, p_acc, p_vals = svm_predict(classes, vectors, self.model, options="-b 1")        
        else:
            sys.stderr.write("Vector is not of the correct type.\nIt must be of type 'dict'.\n"\
                             +"Otherwise, a list of features, and a list of their labels, must be provided.\n")
            return
        return {'classes':p_classes, 'accuracy':p_acc, 'values':p_vals}

        
