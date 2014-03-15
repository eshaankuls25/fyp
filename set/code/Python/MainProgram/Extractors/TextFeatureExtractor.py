import nltk.data, re, sys
from nltk.probability import FreqDist

from collections import *
from nltk.corpus import cmudict
sys.path.append("..")

from Utilities.Utils import downloadNLTKData
from InitialFeatureExtractor import InitialFeatureExtractor as ife

class TextFeatureExtractor(ife):

        def __init__(self, documentName="currentWebsite",\
                     indicators=('From:', 'Date:', 'Message-ID', 'In-Reply-To:')):
                ife.__init__(self, documentName, indicators)
                        
        #Normalized - between 0 and 1
        def lackOfApostrophes(self, textString):
                return self._lackOfCharInString(textString, '\'')

        def averageWordLength(self, textString):
                words = Counter(re.findall(r"[\w]+", textString.lower())).keys()
                wordCount = len(words)
                return float(sum([len(word) for word in words]))/wordCount

        def averageNumberOfSyllablesPerWord(self, textString):
                words = Counter(re.findall(r"[\w]+", textString.lower())).keys()
                wordCount = len(words)
                return float(sum([self._numberOfSyllablesInWord(word) for word in words]))/wordCount

        #Source: NLTK - http://www.nltk.org/book/ch01.html#sec-automatic-natural-language-understanding
        def lexicalDiversity(self, textString):
                ldiv = len(textString) /len(set(textString))
                return 1 if ldiv >= 1.3 else 0 #return 1, if 30% repetition of words

        #Source: NLTK - http://www.nltk.org/book/ch01.html#sec-automatic-natural-language-understanding
        def proportionOfLongWords(self, textString):
                threshold = 7
                freqDist = FreqDist(textString)
                wordSet = Counter(re.findall(r"[\w]+", textString.lower())).keys()
                
                return float(len([word for word in wordSet \
                                  if len(word) > threshold and freqDist[word] > threshold]))/len(wordSet)                    

        def numberOfTrigrams(self, textString):
                #Unsure of average trigram length. Need to check
                return float(len(self.textParser.ngram(textString, n=3)))/1000

        def numberOfBigrams(self, textString):
                #Unsure of average bigram length. Need to check
                return float(len(self.textParser.ngram(textString, n=2)))/2000

        def getNumberOfSubDomains(self, textString):
                return self.htmlParser.getNumberOfSubDomains(textString)

        def getNumberOfDomains(self, textString):
                return self.htmlParser.getNumberOfDomains(textString)

        def htmlInDocument(self, textString):
                #Use lxml.html.fromstring(textString)
