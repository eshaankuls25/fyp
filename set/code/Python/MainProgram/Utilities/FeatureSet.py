from collections import OrderedDict
import numpy as np

class FeatureSet:
    def __init__(self, documentName, documentCategory, documentClass):
        self.documentName = documentName
        self.documentCategory = documentCategory
        self.documentClass = documentClass
        self._vector = OrderedDict()

    def addFeature(self, featureName, value):
        if featureName in self._vector:
            raise AssertionError('Feature value already set.')
        else:
            self._vector[featureName] = value

    def replaceFeatureValue(self, featureName, value):
        assert featureName in self._vector
        self._vector[featureName] = value

    def setValidCategory(category, categoryDictionary):
        if category in categoryDictionary:
            self.documentCategory = category
            return True
        else:
            return False

    def removeFeature(self, featureName):
        del self._vector[featureName]

    def getLabels(self):
        return self._vector.keys()

    def getClass(self):
        return self.documentClass
            
    def getVector(self):
        #return np.array(self._vector.values())
        return {k:v for k, v in enumerate(self._vector.values())}
