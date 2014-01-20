import os, sys
sys.path.append("..")

from Utilities.FeatureSet import FeatureSet
from Utilities.Utils import writeToFile
import DecisionTree

class DTree(object):
    """docstring for DTree"""
    decisionTree = None
    _decisionTreePath = None
    classes = None
    featureMatrix = None

    def __init__(self, classList, featureMatrix, filePath=None):
        if filePath is not None:
            self._decisionTreePath = filePath
        else:
            self._decisionTreePath = os.getcwd() + "/Classifiers/DecisionTree/training_data.csv" 

            i =0
            for label, vector in zip(classList, featureMatrix):

                if i == 0:
                    index = '"",'
                    classLabel = "%s%s,"  %(index, '"class_name"')
                    delimitedFeatures = classLabel + ''.join(['"%s",' %label for label in vector.keys()])
                else:
                    index = '"%d",' %i
                    classLabel = "%s%s,"  %(index, str(label))
                    delimitedFeatures = classLabel + ''.join(["%f," %feature for feature in vector.values()])

                writeToFile(self._decisionTreePath, delimitedFeatures[:-1], "a")
                i+=1


