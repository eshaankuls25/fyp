import sys, importlib, re

from twisted.internet import reactor
from twisted.internet.error import ConnectionRefusedError

from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.settings import CrawlerSettings

sys.path.append("..")

from Utilities.Utils import downloadNLTKData
from spiders.SETSpider import SETSpider
from Extractors.HTMLScraper.items import HTMLScraperItem
from Parsers.HTMLParser_ import HTMLParser

#Use scrapy code here - items, spiders etc.
#Source - Stack Overflow: http://stackoverflow.com/questions/14777910/scrapy-crawl-from-script-always-blocks-script-execution-after-scraping/19060485
class WebsiteScraper():

        def __init__(self, documentName="currentWebsite", startScrapyScan=False, domainList=["localhost"],\
                     urlList=["http://127.0.0.1/"]):
                self.domainList = domainList
                self.urlList = urlList
                self.documentName = documentName

                if startScrapyScan is True:
                        self._createCrawler(self._stopReactor, signals.spider_closed)

                        
        def _stopReactor(self):
                reactor.stop()
        

        def _createCrawler(self, stopReactorFunction, signalFunction):
                spider = SETSpider(self.domainList, self.urlList, self.documentName)
                settings_module = importlib.import_module('Extractors.HTMLScraper.settings')
                settings = CrawlerSettings(settings_module)
                crawler = Crawler(settings)
                crawler.configure()
                crawler.signals.connect(stopReactorFunction, signal=signalFunction)
                crawler.crawl(spider)
                crawler.start()
                log.start()
                reactor.run() # the script will block here until the spider_closed signal was sent

   
        def startCrawler(self, domainList=None,\
                     urlList=None, documentName=None):
                if domainList is not None and urlList is not None:
                        self.domainList = domainList
                        self.urlList = urlList
                if documentName is not None:
                        self.documentName = documentName
                self._createCrawler(self._stopReactor, signals.spider_closed)
