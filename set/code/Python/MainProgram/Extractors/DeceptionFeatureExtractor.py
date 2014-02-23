import sys, os, re, nltk.data
from collections import *
sys.path.append("..")

from Parsers.TextParser import TextParser
from Parsers.HTMLParser_ import HTMLParser
from BaseExtractor import BaseExtractor as be

class DeceptionFeatureExtractor(be):
        def __init__(self, documentName="currentWebsite"):
                be.__init__(self, documentName)
                
                pathToParser = os.getcwd()+"/Parsers"
                self.textParser = TextParser(pathToParser)
                self.htmlParser = HTMLParser()
        
        #Obfuscation

        #Normalized - between 0 and 1
        def lackOfCommas(self, textString):
                return self._lackOfCharInString(textString, ',')

        #not normalized (yet)
        def numberOfSentences(self, textString):
                try:
                        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
                        return len(tokenizer.tokenize(textString))
                except NameError:
                        sys.stderr.write("\n\n'punkt' not available.\n")
                        return 0
                
        def uniqueWordCount(self, textString):
                return len(set(Counter(re.findall(r"[\w]+", textString.lower())).keys()))


        #Imitation

        #Normalized - between 0 and 1
        def lackOfFullStops(self, textString):
                return self._lackOfCharInString(textString, '.')

        #Not normalized (yet)
        def numberOfChars(self, textString):
                return len(textString)

        def numberOfPersonalPronouns(self, textString):
                self.textParser.tagText("temp", textString)

                count = 0
                for x, y in self.textParser.taggedText["temp"]:
                        if y == 'PRP':
                                count+=1
                return count

        #source: StackOverflow - http://stackoverflow.com/questions/106179/regular-expression-to-match-hostname-or-ip-address?lq=1 
        #Need to edit regex for use with Python. In the meantime, look below...
        def _numOfIPAddressLinks(self, textString):
                countExp = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
                return len(re.findall(countExp, textString))

        def numOfIPAddressLinks(self, textString):
                return len(self.htmlParser.findIPAddressesInEmail(textString))

        def numOfURLsinString(self, textString):
                return len(self.htmlParser.getEmailURLs(textString))

