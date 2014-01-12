from collections import Counter
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
		#print self.numOfIPAddressLinks("vdvrf23.2.2.5rwwr1r127.0.0.1")
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
	
        #source: StackOverflow - http://stackoverflow.com/questions/106179/regular-expression-to-match-hostname-or-ip-address?lq=1 
        def numOfIPAddressLinks(self, textString):
		countExp = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
		return len(re.findall(countExp, textString))



