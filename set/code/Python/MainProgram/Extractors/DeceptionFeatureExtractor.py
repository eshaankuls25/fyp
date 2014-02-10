import sys, os
sys.path.append("..")
from Parsers.TextParser import TextParser
import nltk.data, sys, re, os
from collections import *
from TextFeatureExtractor import TextFeatureExtractor

sys.path.append("..")
from Parsers.TextParser import TextParser

class DeceptionFeatureExtractor(TextFeatureExtractor):

        def __init__(self, urlString=None, documentName="currentWebsite"):
                TextFeatureExtractor.__init__(self, urlString, documentName)
        
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
                pathToParser = os.getcwd()+"/Parsers"
                
                tp = TextParser(os.path.normpath(pathToParser))
                tp.tagText("temp", textString)

                count = 0
                for x, y in tp.taggedText["temp"]:
                        if y == 'PRP':
                                count+=1
                return count

