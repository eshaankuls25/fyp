class FeatureSet:
	def __init__(self, documentName, documentCategory):
		self.documentName = documentName
		self.documentCategory = documentCategory
		self.vector = {}

	def addFeature(self, featureName, value):
		if featureName in self.vector:
			raise AssertionError('Feature value already set.')
		else:
			self.vector[featureName] = value

	def replaceFeatureValue(self, featureName, value):
		assert featureName in self.vector
		self.vector[featureName] = value

	def setValidCategory(category, categoryDictionary):
		if category in categoryDictionary:
			self.documentCategory = category
			return True
		else:
			return False

	def removeFeature(self, featureName):
		del self.vector[featureName]