from collections import *
from Utils import downloadNLTKData
from nltk.corpus import cmudict

import re, sys
import nltk.data

class TextFeatureScaler:

        def __init__(self):
                pass
                
        ##Obfuscation and Imitation methods
                        
        #Normalized - between 0 and 1
        def lackOfApostrophes(self, textString):
                return self.lackOfCharInString(textString, '\'')

        #Not normalized (yet)
        def wordCountInString(self, textString, word):
                #Using regular expression: [\w]+
                #\w - word character class
                #r - represents that the following string is in rawstring notation
                return Counter(re.findall(r"[\w]+", textString.lower()))[word]

        def averageWordLength(self, textString):
                words = Counter(re.findall(r"[\w]+", textString.lower())).keys()
                wordCount = len(words)
                return float(sum([len(word) for word in words]))/wordCount

        def averageNumberOfSyllablesPerWord(self, textString):
                words = Counter(re.findall(r"[\w]+", textString.lower())).keys()
                wordCount = len(words)
                return float(sum([self.numberOfSyllablesInWord(word) for word in words]))/wordCount

        ###Utility Functions###

        #-1 means an error has occurred - e.g. wrong parameter type passed into function

        def charCountInString(self, textString, char):
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

        def lackOfCharInString(self, textString, char):
                count = self.charCountInString(textString, char)
                if count != -1:
                        try:
                                return 1/float(1+(0.1*count))
                        except Exception, e:
                                raise e
                else:
                        return count

        #Source: Stack Overflow - http://stackoverflow.com/questions/405161/detecting-syllables-in-a-word
        def numberOfSyllablesInWord(self, word):
                downloaded = downloadNLTKData('cmudict')

                if downloaded:
                        d = cmudict.dict()

                        try:
                                return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
                        except KeyError:
                                sys.stderr.write('\n\nWord not in dictionary.\n')
                                return 0
                else:
                        raise RuntimeError("\n\nCould not download 'cmudict' dictionary.\n")
