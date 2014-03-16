import sys, re, importlib

from twisted.internet           import reactor
from twisted.internet.error     import ConnectionRefusedError

from scrapy                     import log, signals
from scrapy.crawler             import Crawler
from scrapy.settings            import CrawlerSettings
from CrawlerWorker              import CrawlerWorker
from scrapy.crawler             import CrawlerProcess
from scrapy.xlib.pydispatch     import dispatcher
from multiprocessing            import Process

sys.path.append("..")

from Utilities.Utils            import downloadNLTKData
from spiders.SETSpider          import SETSpider
from multiprocessing            import Queue, Manager

queue = Queue()

#Use scrapy code here - items, spiders etc.
#Source - Stack Overflow: http://stackoverflow.com/questions/14777910/scrapy-crawl-from-script-always-blocks-script-execution-after-scraping/19060485
class WebsiteScraper():

        def __init__(self, documentName="currentWebsite", startScrapyScan=False, domainList=["localhost"],\
                     urlList=["http://127.0.0.1/"]):
                self.domainList = domainList
                self.urlList = urlList
                self.documentName = documentName
                if startScrapyScan is True:
                        itemGenerator = self._createCrawler()
                        retrievedItem = tuple(itemGenerator) #Because item is a generator, needs to be 'unpacked'

                        if len(retrievedItem) != 0:
                                return retrievedItem[0]
                        else:
                                return None
        

        def _createCrawler(self):
                spider = SETSpider(self.domainList, self.urlList, self.documentName)

                #Check Multiprocessing rules fow windows here:
                #Source: http://docs.python.org/2/library/multiprocessing.html#windows
                if sys.platform == 'win32':
                        crawlerWorker = Process(target=_runCrawler, args=(spider, queue))
                elif sys.platform.startswith('linux') or sys.platform == 'darwin':
                        crawlerWorker = CrawlerWorker(spider, queue)
                else:
                    raise RuntimeError('ERROR: Operating System Not Supported')  

                crawlerWorker.start()
                for item in queue.get():
                        yield item
                
   
        def startCrawler(self, domainList=None,\
                     urlList=None, documentName=None):
                if domainList is not None and urlList is not None:
                        self.domainList = domainList
                        self.urlList = urlList
                if documentName is not None:
                        self.documentName = documentName
                itemGenerator = self._createCrawler()
                retrievedItem = tuple(itemGenerator) #Because item is a generator, needs to be 'unpacked'

                if len(retrievedItem) != 0:
                        return retrievedItem[0]
                else:
                        return None

def _runCrawler(spider, results):
        settings_module = importlib.import_module('Extractors.HTMLScraper.settings')
        settings = CrawlerSettings(settings_module)
        crawlerProcess = CrawlerProcess(settings)
        items = []

        def _item_passed(item, response, spider):
                items.append(item)

        dispatcher.connect(_item_passed, signals.item_scraped)

        crawler = crawlerProcess.create_crawler("currentCrawler")
        crawler.crawl(spider)
        crawlerProcess.start()
        crawlerProcess.stop()
        results.put(items)

                        
