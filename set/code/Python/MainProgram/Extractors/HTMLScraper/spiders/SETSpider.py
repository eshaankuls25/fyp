import re, sys

from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

sys.path.append("..")
from Extractors.HTMLScraper.items import HTMLScraperItem

class SETSpider(Spider):
    name = "setSpider"
    allowed_domains = ["localhost"]

    start_urls = [
        "http://127.0.0.1/"
        ]
    
    """ 
    #Use 'from scrapy.contrib.spiders import CrawlSpider, Rule'
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(SgmlLinkExtractor(allow=('*\.html', ), deny=('*\.html', ))), #Too broad at the moment...

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        #Rule(SgmlLinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )
    """

    def __init__(self, domainList=None, urlList=None, documentName="currentWebsite"):
        
        if domainList is None or urlList is None:
            raise RuntimeError("\nYou must provide a domain list and url list to parse responses from.\n")
        else:
            self.allowed_domains = domainList
            self.start_urls = urlList
            self.documentName = documentName
            
        print "SETSpider -- Domain list:", self.allowed_domains, " URL list:", self.start_urls
        
    def parse(self, response):
        self.log('This is an item page, from: %s' % response.url)
    	
        item = HTMLScraperItem()
        sel = Selector(response)
        
        #Find menu links
    	sites = sel.xpath('//ul/li')
        
        item['links'] = {}
        i=0

        for site in sites:
            siteDict = {
                'title':site.xpath('a/text()').extract(),
                'link':site.xpath('a/@href').extract(),
                'desc':site.xpath('text()').extract(),
            }

            item['links']['site_'+str(i)] = siteDict
            i+=1
            
        #Table data
        tableData = sel.xpath('//td/text()')

        item['tableData'] = {
            'tableData': tableData.xpath('td/text()').extract()
        }

        #Whole document body
        paragraphText = sel.xpath('//body//p//text()').extract()
        tags = sel.xpath('//html/*').re('<.*?>')
        item['response'] = {
        'all' : sel.xpath('//html/*').extract(),
        'tags' : tags,
        'link' : response.url,
        'headers' : response.headers,
        'body' : response.body,
        'para' : paragraphText
        }

        item['documentName'] = self.documentName

        return item
