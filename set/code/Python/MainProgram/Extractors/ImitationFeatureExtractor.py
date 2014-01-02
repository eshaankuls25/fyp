import sys
sys.path.append("..")
import Parsers.TextParser

from collections import *
from TextFeatureExtractor import TextFeatureExtractor
from HTMLFeatureExtractor import HTMLFeatureExtractor

class ImitationFeatureExtractor(TextFeatureExtractor, HTMLFeatureExtractor):

        def __init__(self, string):
                TextFeatureExtractor.__init__(self)
                HTMLFeatureExtractor.__init__(self)

                self.string = string                

        #Normalized - between 0 and 1
        def lackOfFullStops(self, textString):
                return self.lackOfCharInString(textString, '.')

        #Not normalized (yet)
        def numberOfChars(self, textString):
                return len(textString)

        def numberOfPersonalPronouns(self, textString):
                tp = TextParser()
                tp.tagText("temp", textString)

                count = 0
                for x, y in tp.taggedText["temp"]:
                        if y == 'PRP':
                                count+=1
                return count
