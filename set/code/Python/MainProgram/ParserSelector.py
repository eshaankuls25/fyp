class ParserSelector:

	categoryDictionary = {}

	def __init__(self, *categoryList):
		for category in categoryList:
			self.categoryDictionary[category] = set()
	
	def addCategory(self, category):
		assert category not in self.categoryDictionary
		
		self.categoryDictionary[category] = set()
	
	def addIdentifierSetToCategory(self, category, identifierList):
		assert category in self.categoryDictionary

		currentIdentifierSet = self.categoryDictionary[category]
		self.categoryDictionary[category] = currentIdentifierSet | set(identifierList)

	def isIdentifierInCategory(self, category, identifier):
		assert category in self.categoryDictionary

		if identifier in self.categoryDictionary[category]:
			return True
		else:
			return False


	def clearCategoryIdentifierSet(self, category):
		assert category in self.categoryDictionary
		self.categoryDictionary[category] = set()

	def removeCategory(self, category):
		assert category in self.categoryDictionary
		del self.categoryDictionary[category]

	def determineBestParser(self, *identifierList):

		categoryCountDict = {key:0 for key in self.categoryDictionary}

		for category in categoryCountDict:
			currentIdentifierSet = self.categoryDictionary[category]

			for identifier in set(identifierList):
				if identifier in currentIdentifierSet:
					categoryCountDict[category] +=1

		bestParser = None
		count = 0
		for category in categoryCountDict:
			identifierCount = categoryCountDict[category]
			if identifierCount > count:
				bestParser = category
				count = identifierCount
		return bestParser		

