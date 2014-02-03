import sys, re

from twisted.internet import reactor
from twisted.internet.error import ConnectionRefusedError

from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.settings import CrawlerSettings
from CrawlerWorker import CrawlerWorker

sys.path.append("..")

from Utilities.Utils import downloadNLTKData
from spiders.SETSpider import SETSpider
from Extractors.HTMLScraper.items import HTMLScraperItem
from Parsers.HTMLParser_ import HTMLParser
from multiprocessing import Queue

#Use scrapy code here - items, spiders etc.
#Source - Stack Overflow: http://stackoverflow.com/questions/14777910/scrapy-crawl-from-script-always-blocks-script-execution-after-scraping/19060485
class WebsiteScraper():

        def __init__(self, documentName="currentWebsite", startScrapyScan=False, domainList=["localhost"],\
                     urlList=["http://127.0.0.1/"]):
                self.domainList = domainList
                self.urlList = urlList
                self.documentName = documentName
                self.scrapeResults = Queue()
                if startScrapyScan is True:
                        item = self._createCrawler()
                        return list(item)[0]
        

        def _createCrawler(self):
                spider = SETSpider(self.domainList, self.urlList, self.documentName)
                crawler = CrawlerWorker(spider, self.scrapeResults)
                crawler.run()

                for item in self.scrapeResults.get():
                        yield item
                
   
        def startCrawler(self, domainList=None,\
                     urlList=None, documentName=None):
                if domainList is not None and urlList is not None:
                        self.domainList = domainList
                        self.urlList = urlList
                if documentName is not None:
                        self.documentName = documentName
                item = self._createCrawler()
                return list(item)[0]
