from collections import *
import re

"""Scaling functions"""

###Utility Functions###

#-1 means an error has occurred - e.g. wrong parameter type passed into function

def charCountInString(textString, char):
	if isinstance(textString, basestring) and \
	isinstance(char, basestring) and len(char) == 1:
		return len(textString.split(char))-1
	else:
		return -1

def wordCountInString(textString, word):
	#Using regular expression: [\w]+
	#\w - word character class
	#r - represents that the following string is in rawstrin notation
	return Counter(re.findall(r"[\w]+", textString.lower()))[word]

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

def lackOfApostrophes(textString):
	return lackOfCharInString(textString, '\'')

def lackOfCommas(textString):
	return lackOfCharInString(textString, ',')




