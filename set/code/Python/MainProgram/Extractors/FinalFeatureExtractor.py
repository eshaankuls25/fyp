import sys, os, re, nltk.data
from nltk.corpus import cmudict
from nltk.corpus import brown
from collections import *
sys.path.append("..")

from BaseExtractor import BaseExtractor as be

class FinalFeatureExtractor(be):
        def __init__(self, documentName="currentWebsite", indicators=[]):
                be.__init__(self, documentName, indicators)

        def averageNumberOfSyllablesPerWord(self, textString):
                words = Counter(re.findall(r"[\w]+", textString.lower())).keys()
                wordCount = len(words)
                return float(sum([self._numberOfSyllablesInWord(word) for word in words]))/wordCount

        def averageWordLength(self, textString):
                words = Counter(re.findall(r"[\w]+", textString.lower())).keys()
                wordCount = len(words)
                return float(sum([len(word) for word in words]))/wordCount

        def lackOfFullStops(self, textString):
                return self._lackOfCharInString(textString, '.')

        
        #Source: NLTK - http://www.nltk.org/book/ch01.html#sec-automatic-natural-language-understanding
        def lexicalDiversity(self, textString):
                ldiv = len(textString) /len(set(textString))
                return 1 if ldiv >= 1.3 else 0 #return 1, if 30% repetition of words
                
                
        def numOfIPAddressLinks(self, textString):
                maxIPCount = 3 #Unsure of how many IP addresses exist in the document, so not perfect
                return float(len(self.htmlParser.findIPAddressesInEmail(textString)))/maxIPCount
        

        def numberOfSentences(self, textString):
                sentenceNumberLimiter = 300; #Unsure of average line count of email, must check
                try:
                        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
                        return float(len(tokenizer.tokenize(textString)))/sentenceNumberLimiter
                except NameError:
                        sys.stderr.write("\n\n'punkt' not available.\n")
                        return 0
