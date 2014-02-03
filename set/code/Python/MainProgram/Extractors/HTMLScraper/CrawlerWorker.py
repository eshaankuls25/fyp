import importlib
from scrapy import signals
from scrapy.settings import CrawlerSettings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing import Process

#Source - Stack Overflow: http://stackoverflow.com/questions/7993680/running-scrapy-tasks-in-python
class CrawlerWorker(Process):
    def __init__(self, spider, results):
        Process.__init__(self)
        self.results = results
        
        settings_module = importlib.import_module('Extractors.HTMLScraper.settings')
        settings = CrawlerSettings(settings_module)
        self.crawlerProcess = CrawlerProcess(settings)

        self.items = []
        self.spider = spider
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item):
        self.items.append(item)

    def run(self, name="currentCrawler"):
        crawler = self.crawlerProcess.create_crawler(name)
        crawler.crawl(self.spider)
        self.crawlerProcess.start()
        self.crawlerProcess.stop()
        self.results.put(self.items)
