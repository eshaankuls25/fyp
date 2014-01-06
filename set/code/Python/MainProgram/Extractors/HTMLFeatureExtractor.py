import re, sys
from twisted.internet import reactor

from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings

sys.path.append("..")

from Utilities.Utils import downloadNLTKData
from BaseExtractor import BaseExtractor
from HTMLScraper.spiders.SETSpider import SETSpider

#Use scrapy code here - items, spiders etc.
#Source - Stack Overflow: http://stackoverflow.com/questions/14777910/scrapy-crawl-from-script-always-blocks-script-execution-after-scraping/19060485
class HTMLFeatureExtractor(BaseExtractor):

        def __init__(self, startScrapyScan=False, domainList=["localhost"],\
        urlList=["http://127.0.0.1/"]):
        	BaseExtractor.__init__(self) 

		self.domainList = domainList
		self.urlList = urlList

		if startScrapyScan is True:
			self._createCrawler(self._stopReactor, signals.spider_closed)

        def _stopReactor(self):
            reactor.stop()

        def _createCrawler(self, stopReactorFunction, signalFunction):
                spider = SETSpider(self.domainList, self.urlList)
                crawler = Crawler(get_project_settings())
                crawler.signals.connect(stopReactorFunction, signal=signalFunction)
                crawler.configure()
                crawler.crawl(spider)
                crawler.start()
                log.start()
                reactor.run() # the script will block here until the spider_closed signal was sent

	#Define private methods as utilities for actual text parsing, instance methods, which will produce features, via inherited 'getFeatureSet' function

	


