import sys, os
sys.path.append("..")
from Parsers.TextParser import TextParser

from collections import *
from TextFeatureExtractor import TextFeatureExtractor
from HTMLFeatureExtractor import HTMLFeatureExtractor

class ImitationFeatureExtractor(TextFeatureExtractor, HTMLFeatureExtractor):

        def __init__(self):
                TextFeatureExtractor.__init__(self)
                HTMLFeatureExtractor.__init__(self)      

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

        
