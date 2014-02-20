import sys, os
sys.path.append("..")

from Extractors.HTMLScraper.WebsiteScraper import WebsiteScraper
from Parsers.HTMLParser_ import HTMLParser
from TextFeatureExtractor import TextFeatureExtractor

class HTMLFeatureExtractor(TextFeatureExtractor):
        def __init__(self, documentName="currentWebsite", urlString=None):
                TextFeatureExtractor.__init__(self, documentName)

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
                                
        #source: StackOverflow - http://stackoverflow.com/questions/106179/regular-expression-to-match-hostname-or-ip-address?lq=1 
        #Need to edit regex for use with Python. In the meantime, look below...
        def _numOfIPAddressLinks(self, textString):
                countExp = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
                return len(re.findall(countExp, textString))

        def numOfIPAddressLinks(self, textString):
                return len(self.htmlParser.findIPAddressesInEmail(textString))

        def numOfTagsInString(self, textString):
                return len(self.htmlParser.findTagsInString(textString))

        def numOfURLsinString(self, textString):
                return len(self.htmlParser.getEmailURLs(textString))

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
