import re, sys, os
from os.path import expanduser

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

sys.path.append("..")
from Utilities.Utils import pickleObject, writeToFile
from Extractors.HTMLScraper.items import HTMLScraperItem

class SETSpider(CrawlSpider):
    name = "setSpider"
    allowed_domains = ["localhost"]

    start_urls = [
        "http://127.0.0.1/"
        ]
    
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(SgmlLinkExtractor(allow=('*\.html', ), deny=('*\.html', ))), #Too broad at the moment...

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        #Rule(SgmlLinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )
    
    def __init__(domainList=None, urlList=None):
        allowed_domains = domainList
        start_urls = urlList
        
    def parse(self, response):
        self.log('This is an item page, from: %s' % response.url)
    	
        items = []
        sel = HtmlXPathSelector(response)
        
        #Find menu links
    	sites = sel.select('//ul/li')
        item = HTMLScraperItem()
        
        for site in sites:
            item['title'] = site.select('a/text()').extract()
            item['link'] = site.select('a/@href').extract()
            item['desc'] = site.select('text()').extract()
            item['body'] = None
            items.append(item)
        
        #Table data
        tableData = sel.select('//td/text()')
        item = HTMLScraperItem()

        item['title'] = 'tableData'
        item['link'] = None
        item['desc'] = None
        item['body'] = tableData.select('td/text()').extract()
        items.append(item)

        #Whole document
        item = HTMLScraperItem()
        
        item['title'] = "response_body"
        item['link'] = response.url
        item['desc'] = "Webpage response"
       	item['body'] = response.body
        items.append(item)

        
       	filename = response.url.split("/")[-2]
       	filePath = os.path.dirname(os.getcwd()) + "/Sites/" + filename
        
       	pickleObject(filePath, items)

        return items
