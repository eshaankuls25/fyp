import sys, os
sys.path.append("..")

from Extractors.HTMLScraper.WebsiteScraper import WebsiteScraper
from Parsers.HTMLParser_ import HTMLParser
from TextFeatureExtractor import TextFeatureExtractor as tfe

class HTMLFeatureExtractor(tfe):
        def __init__(self, documentName="currentWebsite", urlString=None,\
                     indicators=('http://', 'www', '.com', '.co.uk')):
                tfe.__init__(self, documentName, indicators)
                
                self.website = None
                self.htmlParser = HTMLParser()
                self.scraper = WebsiteScraper(documentName=self.documentName, startScrapyScan=False)
                self.foundWebsite = False
                
                if urlString is not None:
                        self.scrapeWebsiteFromURL(urlString)

        def scrapeWebsiteFromURL(self, urlString, documentName=None):
                domainList, urlList = self.htmlParser.getURLsWithDomains(urlString)

                if documentName is not None:
                        self.documentName = documentName           
                self.website = self.scraper.startCrawler(domainList,\
                        urlList, self.documentName)                
                self.foundWebsite = True

        def lengthOfWebsiteBodyText(self, textString):
                if self.foundWebsite:
                        return len(self.htmlParser.getResponseAttribute(self.website, 'body'))
                else:
                        return 1

        def numOfURLsInWebsite(self, textString):
                if self.foundWebsite:
                        return len(self.htmlParser.getWebsiteURLs(self.website))
                else:
                        return 1

        def numOfUniqueTagsInWebsite(self, textString):
                if self.foundWebsite:
                        return len(self.htmlParser.getTagCounter(self.website).keys())        
                else:
                        return 1
