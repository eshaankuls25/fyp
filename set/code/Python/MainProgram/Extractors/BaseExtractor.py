import inspect
import sys, os
from nltk.corpus import cmudict
sys.path.append("..")

from Utilities.FeatureSet import FeatureSet
from Parsers.TextParser import TextParser
from Parsers.HTMLParser_ import HTMLParser

class BaseExtractor():
        def __init__(self, documentName, indicators=None, functionToCall=None, paramList=None):
                self.featureSet = None
                self.documentName = documentName
                self.tagged = False

                pathToParser = os.getcwd()+"/Parsers"
                self.textParser = TextParser(pathToParser)
                self.htmlParser = HTMLParser()
                self.functionToCall = functionToCall
                self.paramList = paramList
                
                if isinstance(indicators, (list, tuple)): #If 'indicators' is a list or tuple
                        self.indicators = indicators
                else:
                        self.indicators = []
                
        def getFeatureSet(self, documentName, documentCategory, params=None, documentClass=-1):
                memberList = inspect.getmembers(self, predicate=inspect.ismethod)
                self.featureSet = FeatureSet(documentName, documentCategory, documentClass)

                if self.functionToCall is not None\
                   and self.paramList is not None:
                        self.featureSet.setVector(self.functionToCall(*self.paramList))
                        return self.featureSet

                if isinstance(params, (list, tuple)):
                        parameters = params
                elif (not self.tagged) and isinstance(params, basestring):
                        self.textParser.tagText("temp", params)
                        self.tagged = True
                elif params is not None:
                        parameters = [params]

                if params is not None: #More efficient (less if checks), but some duplicated code
                        for x, y in memberList:
                                if x[0] != '_' and x not in ('getFeatureSet', 'setFunctionArgTuple', 'scrapeWebsiteFromURL'):
                                        self.featureSet.addFeature(x, getattr(self, x)(*parameters))
                if params is None:
                        for x, y in memberList:
                                if x[0] != '_' and x not in ('getFeatureSet', 'setFunctionArgTuple', 'scrapeWebsiteFromURL'):
                                        self.featureSet.addFeature(x, getattr(self, x)())        

                return self.featureSet

        def _setFunctionToCall(self, functionObject):
                self.functionToCall = functionObject

        def _setFunctionParams(self, params):
                if isinstance(params, (list, tuple)):
                        self.paramList = params
                elif params is not None:
                        self.paramList = [params]
                        
        def setFunctionArgTuple(self, functionArgTuple):
              if functionArgTuple is not None:
                        self._setFunctionToCall(functionArgTuple[0])
                        self._setFunctionParams(functionArgTuple[1])

        ###Utility Functions###

        #-1 means an error has occurred - e.g. wrong parameter type passed into function

        def _charCountInString(self, textString, char):
                if isinstance(textString, basestring) and \
                isinstance(char, basestring) and len(char) == 1:
                        return len(textString.split(char))-1
                else:
                        return -1

        #If charCount == 0 return value = 1
        #If charCount is far greater than 0, return value approaches 0
        #0.1 constant chosen, to reduce the effect of a chosen character being introduced

        #(in future constant should be based on 1/(Average Amount Of A Character In All Documents)

        #Done since there could be many of these special characters, over the span of a single document,
        #but not too many (max = approx. 25, for emails/websites [MUST RESEARCH TO DETERMINE IF VALID]), 
        #making resulting values in range over the internal [0, 1] be spread out more evenly

        def _lackOfCharInString(self, textString, char):
                count = self._charCountInString(textString, char)
                if count != -1:
                        try:
                                return 1/float(1+(0.1*count))
                        except Exception, e:
                                raise e
                else:
                        return count

        #Source: Stack Overflow - http://stackoverflow.com/questions/405161/detecting-syllables-in-a-word
        def _numberOfSyllablesInWord(self, word):
                try:
                        d = cmudict.dict()
                        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
                except (KeyError, NameError):
                        return 0

        #Not normalized (yet)
        def _wordCountInString(self, textString, word):
                #Using regular expression: [\w]+
                #\w - word character class
                #r - represents that the following string is in rawstring notation
                return Counter(re.findall(r"[\w]+", textString.lower()))[word]

        def _numberOfTag(self, tagTuple):
                if isinstance(tagTuple, basestring):
                        tagTuple = (tagTuple,)

                count = 0
                for x, y in self.textParser.taggedText["temp"]:
                        if y in tagTuple:
                                count+=1
                taggedText = self.textParser.taggedText["temp"]
                if len(taggedText) == 0:
                        return 0
                return float(count)/len(taggedText) 

        



