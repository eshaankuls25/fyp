import inspect

import sys
sys.path.append("..")

from Utilities.FeatureSet import FeatureSet
from Extractors.HTMLScraper.WebsiteScraper import WebsiteScraper
from Parsers.HTMLParser_ import HTMLParser
from Utilities.Utils import readFromFile, listFilesInDirWithExtension, unpickleObject, unpickleHTMLScraperItem, listFilesInDir

class BaseExtractor():
	def __init__(self, documentName="currentWebsite.dat"):
		self.featureSet = None
                self.scraper = WebsiteScraper(documentName, startScrapyScan=False)
                self.htmlParser = HTMLParser()

	def getFeatureSet(self, documentName, documentCategory, textString, documentClass=-1):
                memberList = inspect.getmembers(self, predicate=inspect.ismethod)
                self.featureSet = FeatureSet(documentName, documentCategory, documentClass)
                for x, y in memberList:
                        if x[0] != '_' and x != 'getFeatureSet':
                                self.featureSet.addFeature(x, getattr(self, x)(textString))
                return self.featureSet

        
        def _extractFromWebsites(self):
                featureSetList = []
                filepathPrefix = "./Sites/"
                websiteList = listFilesInDirWithExtension(filepathPrefix, '.obj')

                tagCounter = {}
                headersDict = {}

                for websitePath in websiteList:

                        item = unpickleHTMLScraperItem(filepathPrefix+websitePath)

                        #response = hparser._getResponseAttribute(item, 'all')
                        #preProcessor = PreProcessor()
                        #processedResponse = preProcessor.removeEscapeChars(response)

                        #tempFeatureSetList = selectExtractorAndProcess(extractorSelector, processedResponse)
                        #featureSetList.extend(tempFeatureSetList)
                
                        tagCounter[websitePath] = self.htmlParser.getTagCounter(item)
                        headersDict[websitePath] = self.htmlParser.getResponseAttribute(item, 'headers')

                        print "---"
                        print tagCounter[websitePath]
                        print "---"
                        print headersDict[websitePath]
                        print "---"
        
                return None
                #Must return a list of feature set objects, later on
