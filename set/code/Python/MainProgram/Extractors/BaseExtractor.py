import inspect
from Utilities.FeatureSet import FeatureSet

class BaseExtractor():
	def __init__(self):
		pass

	def getFeatureSet(self, documentName, documentCategory, textString):
                memberList = inspect.getmembers(self, predicate=inspect.ismethod)
                self.featureSet = FeatureSet(documentName, documentCategory)

                for x, y in memberList:
                        if x[0] != '_' and x != 'getFeatureSet':
                                self.featureSet.addFeature(x, getattr(self, x)(textString))
                return self.featureSet
