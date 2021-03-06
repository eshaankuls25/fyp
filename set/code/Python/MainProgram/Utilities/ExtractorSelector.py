import sys
import cPickle as pickle
sys.path.append("..")

from Extractors.BaseExtractor                   import BaseExtractor                    as be
from Extractors.InitialFeatureExtractor         import InitialFeatureExtractor          as ife
from Extractors.DeceptionFeatureExtractor       import DeceptionFeatureExtractor        as dfe
from Extractors.TextFeatureExtractor            import TextFeatureExtractor             as tfe

from Extractors.GeneralFeatureExtractor         import GeneralFeatureExtractor          as gfe
from Extractors.FinalFeatureExtractor           import FinalFeatureExtractor            as ffe

class ExtractorSelector:
        categoryDictionary = {}
        extractorDictionary = {}

        def __init__(self, extractorDict):
                for category in extractorDict:
                        extractor = extractorDict[category]
                        if isinstance(extractor, be):
                                self.categoryDictionary[category] = set(extractor.indicators)
                        else:
                                self.categoryDictionary[category] = set()
                self.extractorDictionary = extractorDict
                self.defaultExtractor = gfe()
                #self.defaultExtractor = ffe()

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
                        return (None,  (self.defaultExtractor,))
                
                """
                if extractorName is not None:
                        if isinstance(bestExtractor, (list, tuple)):
                                return (extractorName, pickle.dumps(bestExtractor))
                        else:
                                return (extractorName, (pickle.dumps(bestExtractor), ))        
                else:
                        return (None,  (pickle.dumps(self.defaultExtractor), ))
                """

                


