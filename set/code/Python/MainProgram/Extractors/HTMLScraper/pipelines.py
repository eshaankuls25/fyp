import os
from scrapy.contrib.exporter import PickleItemExporter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class HTMLScraperPipeline(object):
    
    def __init__(self):
        self.files = {}
       	self.dirPath = os.path.dirname(os.getcwd()) + "/Sites/"

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(dirPath+spider.name+'_website.obj', 'wb')
        self.files[spider] = file
        self.exporter = PickleItemExporter(file, protocol=2)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
