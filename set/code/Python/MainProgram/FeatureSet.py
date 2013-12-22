class FeatureSet:
	documentName = None
	vector = {}
	
	documentTypes = None
	documentType = None

	def createCategoryDictionary(*sequential, **named):	#From StackOverflow - http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    	return dict(zip(sequential, range(len(sequential))), **named)

	
	def __init__(self, documentName, categoryList):
		self.documentName = documentName
		self.documentTypes = self.createCategoryDictionary(*categoryList)


	def setDocumentType(self, category):
		if category in self.documentTypes:
			self.documentType = category
			return False
		else:
			return True

	def addFeature(self, featureName, value, scalingFunction):
		self.vector[featureName] = [value, scalingFunction(value)]
