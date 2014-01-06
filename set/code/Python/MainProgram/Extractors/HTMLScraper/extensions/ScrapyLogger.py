class ScrapyLogger(object):
	"""docstring for ScrapyLogger"""
	def __init__(self, maxItemCounter):
		self.maxItemCount = maxItemCounter
		self.itemsScraped = 0

	@classmethod
	def from_crawler(cls, crawler):
		if not crawler.settings.getbool('SCRAPYLOGGER_ENABLED'):
            raise NotConfigured

        # get the number of items from settings
        maxItemCount = crawler.settings.getint('SCRAPYLOGGER_MAXITEMCOUNT', 1000)

        # instantiate the extension object
        extension = cls(item_count)

        # connect the extension object to signals
        crawler.signals.connect(extension.spiderOpened, signal=signals.spider_opened)
        crawler.signals.connect(extension.spiderClosed, signal=signals.spider_closed)
        crawler.signals.connect(extension.itemScraped, signal=signals.item_scraped)
        crawler.signals.connect(extension.spiderError, signal=signals.spider_error)

        return extension

	def spiderError(self, failure, response, spider):
    		print "Error on {0}, traceback: {1}".format(response.url, failure.getTraceback())

    def spiderOpened(self, spider):
        spider.log("opened spider %s" % spider.name)

    def spiderClosed(self, spider):
        spider.log("closed spider %s" % spider.name)

    def itemScraped(self, item, spider):
        self.itemsScraped += 1
        if self.itemsScraped == self.maxItemCount:
            spider.log("Scraped %d items, resetting counter" % self.itemsScraped)
            self.maxItemCount = 0
