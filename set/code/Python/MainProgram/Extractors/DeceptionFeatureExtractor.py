import sys, os, re, nltk.data
from nltk.corpus import cmudict
from collections import *
sys.path.append("..")
from BaseExtractor import BaseExtractor as be
from nltk.corpus import brown

class DeceptionFeatureExtractor(be):
        def __init__(self, documentName="currentWebsite", indicators=[]):
                be.__init__(self, documentName, indicators)
                self.ipAddrRegex = re.compile(r"\((\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?))\b\)")
        
        #Obfuscation

        def lackOfCommas(self, textString):
                return self._lackOfCharInString(textString, ',')

        def numberOfSentences(self, textString):
                sentenceNumberLimiter = 300; #Unsure of average line count of email, must check
                try:
                        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
                        return float(len(tokenizer.tokenize(textString)))/sentenceNumberLimiter
                except NameError:
                        sys.stderr.write("\n\n'punkt' not available.\n")
                        return 0
                
        def uniqueWordCount(self, textString):
                allWords = re.findall(r"[\w]+", textString.lower()) 
                return float(len(set(Counter(allWords).keys())))/len(allWords)

        #Imitation

        def lackOfFullStops(self, textString):
                return self._lackOfCharInString(textString, '.')

        def numberOfChars(self, textString):
                charCountLimiter = 10000; #Unsure of average char count of email, must check
                return float(len(textString))/charCountLimiter

        def numberOfPersonalPronouns(self, textString):
                return self._numberOfTag('PRP')

        #source: StackOverflow - http://stackoverflow.com/questions/7907303/finding-ip-addresses-using-regular-expression-in-python
        def _numOfIPAddressLinks(self, textString):
                maxIPCount = 3 #Unsure of how many IP addresses exist in the document, so not perfect
                results = re.findall(self.ipAddrRegex, textString)
                return float( len(results) )/maxIPCount

        def numOfIPAddressLinks(self, textString):
                maxIPCount = 3 #Unsure of how many IP addresses exist in the document, so not perfect
                return float(len(self.htmlParser.findIPAddressesInEmail(textString)))/maxIPCount

        def numOfURLsinString(self, textString):
                maxURLCount = 30 #Unsure of how many URLs exist in the document, so not perfect
                return float(len(self.htmlParser.getEmailURLs(textString)))/maxURLCount

        def numberOfSecurityTerms(self, textString):
                urgencyTerms = {'reward', 'refund', 'limited',\
                                   'time', 'have', 'must', 'definitely',\
                                   'immediate', 'need'}
                commandTerms = {'confirm', 'validate', 'click', 'provide', 'select', 'write'}
                threatTerms = {'risk', 'loss', 'protection', 'lock', 'frozen', 'expire', 'closed'}
                otherTerms = {'attached', 'details'}

                allWords = re.findall(r"[\w]+", textString.lower())
                allTerms = urgencyTerms | commandTerms | threatTerms | otherTerms #union

                return float(sum([1 if word in allTerms else 0 for word in allWords]))/len(allWords)

        def numberOfAdjectives(self, textString):
                return self._numberOfTag(('JJ', 'JJR', 'JJS'))

        def numberOfAdverbs(self, textString):
                return self._numberOfTag('RB')

        def numberOfVerbs(self, textString):
                return self._numberOfTag(('VB', 'VBD', 'VBG',\
                                               'VBN', 'VBP', 'VBZ'))

        """
        def incorrectWords(self, textString):
                count = 0
                correctWords = brown.words() #Brown corpus
                allWords = re.findall(r"[\w]+", textString.lower())
                
                for word in allWords:
                        if word not in correctWords:
                                count+=1

                return float(count)/len(allWords)
        """

        
