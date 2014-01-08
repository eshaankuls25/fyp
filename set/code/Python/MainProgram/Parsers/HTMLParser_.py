import os, sys, re
from collections import Counter
sys.path.append("..")

from Extractors.HTMLScraper.items import HTMLScraperItem

class HTMLParser:
        parsedText = {}
        
	def __init__(self):
		pass

        #Source: StackOverflow - http://stackoverflow.com/questions/4436008/how-to-get-html-tags
	def _findTagsInString(self, textString):
		return re.findall('<.*?>', textString)

	def _getTagsFromString(self, item):
		if isinstance(item, dict):
			responseAll = item['response']['tags']
			return [x.encode('utf8') for x in responseAll]
	
		if isinstance(item, basestring):
			return self._findTagsInString(item)

	#Choices: 'all', 'headers', 'body', 'para', 'url'
	def _getResponseAttribute(self, item, attributeString):
		if isinstance(attributeString, basestring)\
			    and isinstance(item, dict):
			unicodeBody = item['response'][attributeString]
			return ''.join([x.encode('utf8') for x in unicodeBody])
		elif isinstance(item, dict):
                        raise TypeError("The attribute must be a string.")
	
	def getTagCountDictionary(self, item):
		return(Counter(self._getTagsFromString(item)))

                
