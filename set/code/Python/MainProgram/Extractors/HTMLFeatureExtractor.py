import re, sys
from twisted.internet import reactor

from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings

sys.path.append("..")

from Utilities.Utils import downloadNLTKData
from BaseExtractor import BaseExtractor
from Extractors.HTMLScraper.spiders.SETSpider import SETSpider

#Use scrapy code here - items, spiders etc.
#Source - Stack Overflow: http://stackoverflow.com/questions/14777910/scrapy-crawl-from-script-always-blocks-script-execution-after-scraping/19060485
class HTMLFeatureExtractor(BaseExtractor):

        def __init__(self):
        	BaseExtractor.__init__(self)
        	self.createCrawler(stopReactor, signals.spider_closed)

        def stopReactor(self, reactor):
            reactor.stop()

        def createCrawler(stopReactorFunction, signalFunction):
                spider = SETSpider()
                crawler = Crawler(get_project_settings())
                crawler.signals.connect(stopReactorFunction, signal=signalFunction)
                crawler.configure()
                crawler.crawl(spider)
                crawler.start()
                log.start()
                reactor.run() # the script will block here until the spider_closed signal was sent
                

        
