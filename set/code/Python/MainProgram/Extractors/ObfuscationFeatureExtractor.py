from collections import *
from TextFeatureExtractor import TextFeatureExtractor
from HTMLFeatureExtractor import HTMLFeatureExtractor

import nltk.data, sys, re
sys.path.append("..")

from Utilities.Utils import downloadNLTKData

class ObfuscationFeatureExtractor(TextFeatureExtractor, HTMLFeatureExtractor):

        def __init__(self):
                TextFeatureExtractor.__init__(self)
                HTMLFeatureExtractor.__init__(self)
                
                downloaded = downloadNLTKData('punkt')

                if not downloaded:
                        raise RuntimeError("\n\nCould not download 'punkt' dictionary.\n")

        #Normalized - between 0 and 1
        def lackOfCommas(self, textString):
                return self._lackOfCharInString(textString, ',')

        #Not normalized (yet)
        def numberOfSentences(self, textString):
                try:
                        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
                        return len(tokenizer.tokenize(textString))
                except NameError:
                        sys.stderr.write("\n\n'punkt' not available.\n")
                        return 0
                
        def uniqueWordCount(self, textString):
                return len(set(Counter(re.findall(r"[\w]+", textString.lower())).keys()))

