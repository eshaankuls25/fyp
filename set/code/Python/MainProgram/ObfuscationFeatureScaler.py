from collections import *
from Utils import downloadNLTKData
from TextFeatureScaler import TextFeatureScaler

import re, nltk.data

class ObfuscationFeatureScaler(TextFeatureScaler):

        def __init__(self):
                TextFeatureScaler.__init__(self)

        ##Obfuscation-Specific functions
                
        #Normalized - between 0 and 1
        def lackOfCommas(self, textString):
                return self.lackOfCharInString(textString, ',')

        #Not normalized (yet)
        def numberOfSentences(self, textString):
                downloaded = downloadNLTKData('punkt')

                if downloaded:
                        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
                        return len(tokenizer.tokenize(textString))
                else:
                        return -1

        def uniqueWordCount(self, textString):
                return len(set(Counter(re.findall(r"[\w]+", textString.lower())).keys()))

