from collections import *
from TextParser import TextParser
from TextFeatureScaler import TextFeatureScaler

class ImitationFeatureScaler(TextFeatureScaler):

        def __init__(self):
                TextFeatureScaler.__init__(self)

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
                print tp.taggedText
                for x, y in tp.taggedText["temp"]:
                        if y == 'PRP':
                                count+=1
                return count
