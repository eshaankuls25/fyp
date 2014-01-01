from collections import *
from Utils import downloadNLTKData
from nltk.corpus import cmudict

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
#Squared because number of special characters/punctuation per document
#(which is what this function will most be used for) is likely to be small,
#making points in range over the internal [0, 1] be spread out more evenly

def lackOfCharInString(textString, char):
	count = charCountInString(textString, char)
	if count != -1:
		try:
			return 1/float(1+(count**2))
		except Exception, e:
			raise e
	else:
		return count

###Actual Feature Scaling Functions###

#Normalized - between 0 and 1
def lackOfApostrophes(textString):
	return lackOfCharInString(textString, '\'')

def lackOfCommas(textString):
	return lackOfCharInString(textString, ',')

#Not normalized (yet)
def wordCountInString(textString, word):
	#Using regular expression: [\w]+
	#\w - word character class
	#r - represents that the following string is in rawstrin notation
	return Counter(re.findall(r"[\w]+", textString.lower()))[word]

def averageWordLength(textString):
	words = Counter(re.findall(r"[\w]+", textString.lower())).keys()
	wordCount = len(words)
	return float(sum([len(word) for word in words]))/wordCount

def numberOfSentences(textString):
	downloaded = downloadNLTKData('punkt')

	if downloaded:
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		return len(tokenizer.tokenize(textString))
	else:
		return -1

def uniqueWordCount(textString):
	return len(set(Counter(re.findall(r"[\w]+", textString.lower())).keys()))

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
