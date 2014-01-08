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
			unicodeBody = item['response']['body']
			responseBody = ''.join([x.encode('utf8') for x in unicodeBody])
			responseAll = item['response']['tags']
			return [x.encode('utf8') for x in responseAll]
	
		if isinstance(item, basestring):
			return self._findTagsInString(item)
	
	def _getResponseAllText(self, item):
		if isinstance(item, dict):
			unicodeBody = item['response']['all']
			return ''.join([x.encode('utf8') for x in unicodeBody])
	
	def _getResponseBodyText(self, item):
		if isinstance(item, dict):
			unicodeBody = item['response']['body']
			return ''.join([x.encode('utf8') for x in unicodeBody])

	def getTagCountDictionary(self, item):
		return(Counter(self.getTagsFromString(item)))

	
