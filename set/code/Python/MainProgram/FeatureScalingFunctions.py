from collections import *
from Utils import downloadNLTKData
from nltk.corpus import cmudict
from TextParser import TextParser

import re, sys
import nltk.data


"""Scaling functions"""

###Utility Functions###

#-1 means an error has occurred - e.g. wrong parameter type passed into function

def charCountInString(textString, char):
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

def lackOfCharInString(textString, char):
        count = charCountInString(textString, char)
        if count != -1:
                try:
                        return 1/float(1+(0.1*count))
                except Exception, e:
                        raise e
        else:
                return count

###Actual Feature Scaling Functions###

##Obfuscation and Imitation functions
        
#Normalized - between 0 and 1
def lackOfApostrophes(textString):
        return lackOfCharInString(textString, '\'')

#Not normalized (yet)
def wordCountInString(textString, word):
        #Using regular expression: [\w]+
        #\w - word character class
        #r - represents that the following string is in rawstring notation
        return Counter(re.findall(r"[\w]+", textString.lower()))[word]

def averageWordLength(textString):
        words = Counter(re.findall(r"[\w]+", textString.lower())).keys()
        wordCount = len(words)
        return float(sum([len(word) for word in words]))/wordCount

def averageNumberOfSyllablesPerWord(textString):
        words = Counter(re.findall(r"[\w]+", textString.lower())).keys()
        wordCount = len(words)
        return float(sum([numberOfSyllablesInWord(word) for word in words]))/wordCount

#Source: Stack Overflow - http://stackoverflow.com/questions/405161/detecting-syllables-in-a-word
def numberOfSyllablesInWord(word):
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

##Obfuscation-Specific functions
        
#Normalized - between 0 and 1
def lackOfCommas(textString):
        return lackOfCharInString(textString, ',')

#Not normalized (yet)
def numberOfSentences(textString):
        downloaded = downloadNLTKData('punkt')

        if downloaded:
                tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
                return len(tokenizer.tokenize(textString))
        else:
                return -1

def uniqueWordCount(textString):
        return len(set(Counter(re.findall(r"[\w]+", textString.lower())).keys()))


###Imitation-Specific functions###

#Normalized - between 0 and 1
def lackOfFullStops(textString):
        return lackOfCharInString(textString, '.')

#Not normalized (yet)
def numberOfChars(textString):
        return len(textString)

def numberOfPersonalPronouns(textString):
        tp = TextParser()
        tp.tagText("temp", textString)

        count = 0
        print tp.taggedText
        for x, y in tp.taggedText["temp"]:
                if y == 'PRP':
                        count+=1
        return count
