import re, sys

from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

sys.path.append("..")
from Extractors.HTMLScraper.items import HTMLScraperItem

class SETSpider(BaseSpider):
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

            item['links']['site_'+str(i)] = siteDict
            i+=1
            
        #Table data
        tableData = sel.select('//td/text()')

        item['tableData'] = {
            'tableData': tableData.select('td/text()').extract()
        }

        #Whole document body
        paragraphText = sel.select('//body//p//text()').extract()
        tags = sel.select('//html/*').re('<.*?>')
        item['response'] = {
        'all' : sel.select('//html/*').extract(),
        'tags' : tags,
        'link' : response.url,
        'headers' : response.headers,
        'body' : response.body,
        'para' : paragraphText
        }

        return item
