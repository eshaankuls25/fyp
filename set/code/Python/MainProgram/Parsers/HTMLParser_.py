import os, sys, re
sys.path.append("..")

from Extractors.HTMLScraper.items import HTMLScraperItem
from Utilities.Utils import unpickleObject

class HTMLParser:
        parsedText = {}
        
        def __init__(self):
        	pass

        #Source: StackOverflow - http://stackoverflow.com/questions/4436008/how-to-get-html-tags
        def getTagsFromString(self, textString):
        	return re.findall('<.*?>', textString)

        def getTagsFromPickledObject(self, filePath):
        	dataObject = unpickleObject(filePath)
        	tagList = []

        	if not isinstance(dataObject, (list, tuple)):
        		TypeError("\nUnpickled data must be an instance of list or tuple.\n")

        	for item in dataObject:
        		if isinstance(item, dict):
        			tagList.append(getTagsFromString(item['body']))        			       				item[k]) for k in item))
        	return tagList
                
