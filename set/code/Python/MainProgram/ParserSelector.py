class ParserSelector:

	categoryDictionary = {}

	def __init__(self, categoryList):
		for category in categoryList:
			categoryDictionary[category] = set()

	def addIdentifierSetToCategory(self, category, identifierSet):
		currentIdentifierSet = self.categoryDictionary[category]
		self.categoryDictionary[category] = currentIdentifierSet | identifierSet

	def isIdentifierInCategory(self, category, identifier):
		if identifier in self.categoryDictionary[category]:
			return True
		else:
			return False

	def determineBestParser(self, identifierSet):
		categoryCountDict = {key:0 for key in self.categoryDictionary}

		for category in categoryCountDict:
			currentIdentifierSet = self.categoryDictionary[category]

			for identifier in identifierSet:
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

