import sys, os, re, nltk.data
from collections import *
sys.path.append("..")
from BaseExtractor import BaseExtractor as be

class DeceptionFeatureExtractor(be):
        def __init__(self, documentName="currentWebsite", indicators=[]):
                be.__init__(self, documentName, indicators)    
        
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
                self.textParser.tagText("temp", textString)

                count = 0
                for x, y in self.textParser.taggedText["temp"]:
                        if y == 'PRP':
                                count+=1
                taggedText = self.textParser.taggedText["temp"]
                if len(taggedText) == 0:
                        return 0
                return float(count)/len(taggedText)

        #source: StackOverflow - http://stackoverflow.com/questions/106179/regular-expression-to-match-hostname-or-ip-address?lq=1 
        #Need to edit regex for use with Python. In the meantime, look below...
        def _numOfIPAddressLinks(self, textString):
                maxIPCount = 3 #Unsure of how many IP addresses exist in the document, so not perfect
                countExp = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
                return float(len(re.findall(countExp, textString)))/maxIPCount

        def numOfIPAddressLinks(self, textString):
                maxIPCount = 3 #Unsure of how many IP addresses exist in the document, so not perfect
                return float(len(self.htmlParser.findIPAddressesInEmail(textString)))/maxIPCount

        def numOfURLsinString(self, textString):
                maxURLCount = 30 #Unsure of how many URLs exist in the document, so not perfect
                return float(len(self.htmlParser.getEmailURLs(textString)))/maxURLCount

