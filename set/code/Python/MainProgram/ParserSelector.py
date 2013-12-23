from TextParser import TextParser

class ParserSelector:

	categoryDictionary = {}
	parserDictionary = {}

	def __init__(self, categoryList, parserList):
		for group in zip(categoryList, parserList):
			self.categoryDictionary[group[0]] = set()
			self.parserDictionary[group[0]] = group[1]		

	def addParser(self, category, parser):
		assert category not in self.categoryDictionary
		assert category not in self.parserDictionary

		self.categoryDictionary[category] = set()
		self.parserDictionary[category] = parser	

	def removeParser(self, category):
		assert category in self.categoryDictionary
		assert category in self.parserDictionary

		del self.categoryDictionary[category]
		del self.parserDictionary[category]	
	
	def addParserIdentifierSet(self, category, identifierList):
		assert category in self.categoryDictionary

		currentIdentifierSet = self.categoryDictionary[category]
		self.categoryDictionary[category] = currentIdentifierSet | set(identifierList)

	def isIdentifierInCategory(self, category, identifier):
		assert category in self.categoryDictionary

		if identifier in self.categoryDictionary[category]:
			return True
		else:
			return False


	def clearParserIdentifierSet(self, category):
		assert category in self.categoryDictionary
		self.categoryDictionary[category] = set()

	def determineBestParser(self, identifierList):
		categoryCountDict = {key:0 for key in self.categoryDictionary}
		for category in categoryCountDict:
			currentIdentifierSet = self.categoryDictionary[category]

			for identifier in set(identifierList):
				if identifier in currentIdentifierSet:
					categoryCountDict[category] +=1

		parserName = None
		bestParser = None
		count = 0
		
		for category in categoryCountDict:
			identifierCount = categoryCountDict[category]
			if identifierCount > count:
				parserName = category
				bestParser = self.parserDictionary[category]
				count = identifierCount

		if parserName is not None:
			return (parserName, bestParser)	
		else:
			return (None, TextParser())


