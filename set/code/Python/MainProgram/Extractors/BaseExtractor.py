import inspect

import sys, os
sys.path.append("..")

from Utilities.FeatureSet import FeatureSet
from Utilities.PreProcessor import PreProcessor
from Extractors.HTMLScraper.WebsiteScraper import WebsiteScraper
from Parsers.HTMLParser_ import HTMLParser
from Utilities.Utils import listFilesInDirWithExtension, unpickleHTMLScraperItem

class BaseExtractor():
        def __init__(self, urlString, documentName):
                self.featureSet = None
                self.website = None
                self.documentName = documentName
                self.htmlParser = HTMLParser()
                self.scraper = WebsiteScraper(documentName=self.documentName, startScrapyScan=False)
                self.foundWebsite = False
                
                if urlString is not None:
                        self._scrapeWebsiteFromURL(urlString)
        
        def getFeatureSet(self, documentName, documentCategory, params=None, documentClass=-1):
                if isinstance(params, (list, tuple)):
                        parameters = params
                else:
                        parameters = [params]

                memberList = inspect.getmembers(self, predicate=inspect.ismethod)
                self.featureSet = FeatureSet(documentName, documentCategory, documentClass)
                for x, y in memberList:
                        if x[0] != '_' and x != 'getFeatureSet' and x != 'scrapeWebsiteFromURL':
                                self.featureSet.addFeature(x, getattr(self, x)(*parameters))
                return self.featureSet

        def scrapeWebsiteFromURL(self, urlString, documentName=None):
                domainList, urlList = getURLsWithDomains(urlString)

                if documentName is not None:
                        self.documentName = documentName
                
                self.scraper.startCrawler(domainList, urlList, self.documentName)
                filepathPrefix = "./Sites/"
                filepath = filepathPrefix+"%s.obj" %self.documentName
                notAvailable = True

                #Must implement a timeout feature here - other could have infinite hang
                while notAvailable:
                        if os.path.isfile(filepath):
                                self.website = unpickleHTMLScraperItem(filepath)
                                notAvailable = False
                self.foundWebsite = True
                                
        #source: StackOverflow - http://stackoverflow.com/questions/106179/regular-expression-to-match-hostname-or-ip-address?lq=1 
        #Need to edit regex for use with Python. In the meantime, look below...
        def _numOfIPAddressLinks(self, textString):
                countExp = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
                return len(re.findall(countExp, textString))

        def numOfIPAddressLinks(self, textString):
                return len(self.htmlParser.findIPAddressesInEmail(textString))

        def numOfTagsInString(self, textString):
                return len(self.htmlParser.findTagsInString(textString))

        def numberOfURLsinWebsite(self, textString):
                return len(self.htmlParser.getEmailURLs(textString))

        #Below will be in use, once website parsing works 100%, remove '_' - to make methods public

        def _lengthOfWebsiteBodyText(self):
                assert self.foundWebsite
                return len(self.htmlParser.getResponseAttribute(self.website, 'body'))

        def _numberOfURLsinWebsite(self):
                assert self.foundWebsite
                return len(self.htmlParser.getWebsiteURLs(self.website))

        def _numOfUniqueTagsInWebsite(self):
                assert self.foundWebsite
                return len(self.htmlParser.getTagCounter(self.website).keys())
                

        """
        def _extractFromWebsites(self, textString):
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
        """
