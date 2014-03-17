import os, sys
from os.path import normpath, isfile
sys.path.append("..")

#from Utilities.FeatureSet import FeatureSet
from svmutil import *

class SVM(object):
    """docstring for SVM"""
    model = None
    classes = None
    featureMatrix = None

    #featureMatrix is an iterable (list, tuple etc.) of dictionaries/vectors:
    ##e.g. [featureSet1.getVector(), featureSet2.getVector(), fe5.getVector() ...]

    #Use like this:
    #gSVM = SVM(costParam=your_chosen_number, modelType=2) #GaussianSVM
    def __init__(self, classList=None, featureMatrix=None,\
                     pathToModel='./Classifiers/SupportVectorMachine/svm_model.bak',
                     modelType=2, costParam=1):
        super(SVM, self).__init__()
        print "\n-------------------------\nSVM:\n-------------------------\n"
        
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

                #t = 2 Model type: Gaussian/RBF
                #s = 0 C-SVC multi-class classifier
                #c = Cost parameter of C-SVC
                #v = 5 k-fold cross-validation 'block' size
                #b = 0 Create probability estimates for SVC type SVM
                #g = 1/len(featureSet) - Implicitly set at the moment
                params = svm_parameter('-s 0 -t %s -c %s -b 0' %(str(modelType), str(costParam)) )
                self.model = svm_train(svmProb, params)
                self.saveModel(pathToModel, self.model)

        """

        print "\n--------------\nSupport Vectors:\n",\
              "--------------\nCoefficients: ", self.model.get_sv_coef(),\
              "\nVectors: ", self.model.get_SV()

        """

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
        #print "\nExpected Class(es): ", classes, " Vector(s): ", vectors, "\n"    
        if isinstance(vectors, dict) and isinstance(classes, int):
            p_classes, p_acc, p_vals = svm_predict([classes], [vectors], self.model) #options="-b 1"

            if p_classes == 1.0:
                return "\nClassified as non-deceptive."
            else:
                return "\nClassified as deceptive."
        elif isinstance(vectors, list) and isinstance(classes, list):
            p_classes, p_acc, p_vals = svm_predict(classes, vectors, self.model)
            docCount = 1
            for label in p_classes:
                if label == 1.0:
                    return "\nDocument %d: Classified as non-deceptive."%docCount
                else:
                    return "\nDocument %d: Classified as deceptive."%docCount
                docCount+=1
            
        else:
            sys.stderr.write("Vector is not of the correct type.\nIt must be of type 'dict'.\n"\
                             +"Otherwise, a list of features, and a list of their labels, must be provided.\n")
            return

        
