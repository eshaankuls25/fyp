import sys
sys.path.append("..")

from Extractors.ObfuscationFeatureExtractor import ObfuscationFeatureExtractor
from Extractors.ImitationFeatureExtractor import ImitationFeatureExtractor

class ExtractorSelector:

	categoryDictionary = {}
	extractorDictionary = {}

	def __init__(self, categoryList, extractorList):
		for pair in zip(categoryList, extractorList):
			self.categoryDictionary[pair[0]] = set()
			self.extractorDictionary[pair[0]] = pair[1]		

	def addExtractor(self, category, extractor):
		assert category not in self.categoryDictionary
		assert category not in self.extractorDictionary

		self.categoryDictionary[category] = set()
		self.extractorDictionary[category] = extractor	

	def removeExtractor(self, category):
		assert category in self.categoryDictionary
		assert category in self.extractorDictionary

		del self.categoryDictionary[category]
		del self.extractorDictionary[category]	
	
	def addExtractorIdentifierSet(self, category, identifierList):
		assert category in self.categoryDictionary

		currentIdentifierSet = self.categoryDictionary[category]
		self.categoryDictionary[category] = currentIdentifierSet | set(identifierList)

	def isIdentifierInCategory(self, category, identifier):
		assert category in self.categoryDictionary

		if identifier in self.categoryDictionary[category]:
			return True
		else:
			return False


	def clearExtractorIdentifierSet(self, category):
		assert category in self.categoryDictionary
		self.categoryDictionary[category] = set()

	def determineBestExtractor(self, identifierList):
		categoryCountDict = {key:0 for key in self.categoryDictionary}
		for category in categoryCountDict:
			currentIdentifierSet = self.categoryDictionary[category]

			for identifier in set(identifierList):
				if identifier in currentIdentifierSet:
					categoryCountDict[category] +=1

		extractorName = None
		bestExtractor = None
		count = 0
		
		for category in categoryCountDict:
			identifierCount = categoryCountDict[category]
			if identifierCount > count:
				extractorName = category
				bestExtractor = self.extractorDictionary[category]
				count = identifierCount

		if extractorName is not None:
			if isinstance(bestExtractor, (list, tuple)):
				return (extractorName, bestExtractor)
			else:
				return (extractorName, (bestExtractor,))	
		else:
			return (None,  (ImitationFeatureExtractor(), ObfuscationFeatureExtractor()))

		


