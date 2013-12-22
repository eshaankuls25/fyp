class FeatureSet:
	documentName = None
	documentCategory = None
	vector = {}
	
	def __init__(self, documentName, documentCategory):
		self.documentName = documentName
		self.documentCategory = documentCategory

	def addFeature(self, featureName, value, scalingFunction):
		self.vector[featureName] = [value, scalingFunction(value)]

	def setValidCategory(category, categoryDictionary):
		if category in categoryDictionary:
			self.documentCategory = category
			return True
		else:
			return False

	def removeFeature(self, featureName):
		del self.vector[featureName]