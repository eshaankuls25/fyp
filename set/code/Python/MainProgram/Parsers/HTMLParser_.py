import os, sys, re
from urlparse import urlparse

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

	def getTagsFromString(self, item):
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
	
	def getTagCounter(self, item):
		return(Counter(self.getTagsFromString(item)))

	#source: StackOverflow - http://stackoverflow.com/questions/9000960/python-regular-expressions-re-search-vs-re-findall
        def _findIPAddressesInEmail(self, textString):
                countExp = re.compile("((?:\d{1,3}\.){3}\d{1,3})")
                return re.findall(countExp, textString)


        #source: StackOverflow - http://stackoverflow.com/questions/8436818/regular-expression-to-extract-urls-with-difficult-formatting?rq=1
        def _findUrlsInEmail(self, textString):
                return re.findall("((http:|https:)//[^ \<]+)", textString)

        def _parseURLString(self, textString):
                return urlparse(textString)
                #Must use 'tldextract' library - Source: https://github.com/john-kurkowski/tldextract
                #To get correct domains from a URL

                #Then send list of URLs, and associated domain list (in order), to Scrapy, for parsing.

