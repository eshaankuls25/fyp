import sys, os, re, nltk.data
from collections import *
sys.path.append("..")

from Parsers.TextParser import TextParser
from BaseExtractor import BaseExtractor

class DeceptionFeatureExtractor(BaseExtractor):
        def __init__(self, documentName="currentWebsite"):
                BaseExtractor.__init__(self, documentName)
                
                pathToParser = os.getcwd()+"/Parsers"
                self.textParser = TextParser(pathToParser)
        
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

