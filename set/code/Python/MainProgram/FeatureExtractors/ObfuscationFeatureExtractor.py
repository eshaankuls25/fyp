from collections import *
from Utils import downloadNLTKData
from TextFeatureExtractor import TextFeatureExtractor
from HTMLFeatureExtractor import HTMLFeatureExtractor

import nltk.data

class ObfuscationFeatureExtractor(TextFeatureExtractor, HTMLFeatureExtractor):

        def __init__(self, string):
                TextFeatureExtractor.__init__(self)
                HTMLFeatureExtractor.__init__(self)
                
                self.string = string

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

