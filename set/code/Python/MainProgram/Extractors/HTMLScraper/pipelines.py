import os, datetime
from scrapy.contrib.exporter import PickleItemExporter
from scrapy import signals

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class HTMLScraperPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        return item

    """
    def __init__(self):
        self.files = {}
       	self.dirPath = os.getcwd() + "/Sites/"
        self.exporter = None
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spiderOpened, signals.spider_opened)
        crawler.signals.connect(pipeline.spiderClosed, signals.spider_closed)
        return pipeline

    def spiderOpened(self, spider):
        file = open(self.dirPath+spider.documentName+'.obj', 'wb')
        self.files[spider] = file
        self.exporter = PickleItemExporter(file, protocol=2)
        self.exporter.start_exporting()

    def spiderClosed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    """
