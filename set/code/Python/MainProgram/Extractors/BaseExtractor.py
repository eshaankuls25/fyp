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
                        self.scrapeWebsiteFromURL(urlString)
        
        def getFeatureSet(self, documentName, documentCategory, params=None, documentClass=-1):
                memberList = inspect.getmembers(self, predicate=inspect.ismethod)
                self.featureSet = FeatureSet(documentName, documentCategory, documentClass)

                if isinstance(params, (list, tuple)):
                        parameters = params
                elif params is not None:
                        parameters = [params]

                if params is not None:
                        for x, y in memberList:
                                if x[0] != '_' and x != 'getFeatureSet' and x != 'scrapeWebsiteFromURL':
                                        self.featureSet.addFeature(x, getattr(self, x)(*parameters))
                if params is None:
                        for x, y in memberList:
                                if x[0] != '_' and x != 'getFeatureSet' and x != 'scrapeWebsiteFromURL':
                                        self.featureSet.addFeature(x, getattr(self, x)())        

                return self.featureSet

        def scrapeWebsiteFromURL(self, urlString, documentName=None):
                domainList, urlList = self.htmlParser.getURLsWithDomains(urlString)

                if documentName is not None:
                        self.documentName = documentName           
                self.website = self.scraper.startCrawler(domainList,\
                        urlList, self.documentName)                
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

        def lengthOfWebsiteBodyText(self, textString):
                if self.foundWebsite:
			return len(self.htmlParser.getResponseAttribute(self.website, 'body'))
		else:
			return 0.1

        def numberOfURLsInWebsite(self, textString):
                if self.foundWebsite:
			return len(self.htmlParser.getWebsiteURLs(self.website))
		else:
			return 0.1

        def numOfUniqueTagsInWebsite(self, textString):
                if self.foundWebsite:
			return len(self.htmlParser.getTagCounter(self.website).keys())        
		else:
			return 0.1


