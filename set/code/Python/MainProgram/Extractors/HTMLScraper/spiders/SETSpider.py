import re, sys

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

sys.path.append("..")
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
    
    def __init__(self, domainList=None, urlList=None):
        allowed_domains = domainList
        start_urls = urlList
        
    def parse(self, response):
        self.log('This is an item page, from: %s' % response.url)
    	
        item = HTMLScraperItem()
        sel = HtmlXPathSelector(response)
        
        #Find menu links
    	sites = sel.select('//ul/li')
        
        item['links'] = {}
        i=0

        for site in sites:
            siteDict = {
                'title':site.select('a/text()').extract(),
                'link':site.select('a/@href').extract(),
                'desc':site.select('text()').extract(),
            }

            item['links'].put('site_'+str(i), siteDict)
            i+=1
            
        #Table data
        tableData = sel.select('//td/text()')

        item['tableData'] = {
            'tableData': tableData.select('td/text()').extract()
        }

        #Whole document body
        bodyText = sel.select('//body//p//text()').extract()

        item['response'] = {
        'link' : response.url,
        'body' : bodyText
        }

        return item
