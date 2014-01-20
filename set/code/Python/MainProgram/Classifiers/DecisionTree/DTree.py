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
            i = 0

            for label, vector in zip(classList, featureMatrix):
                index = '"%s",' % str(i)
                delimitedFeatures = index.join(["%s," % str(feature) for feature in vector.keys()])
                featureString = "%s,%s\n" %(delimitedFeatures, str(label))

                writeToFile(self._decisionTreePath, featureString, "a")
                i+=1


