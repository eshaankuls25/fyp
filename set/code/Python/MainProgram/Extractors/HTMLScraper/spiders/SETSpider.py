from scrapy.contrib.spiders import CrawlSpider, Rule
from os.path import expanduser
from Utilities.Utils import pickleObject
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class SETSpider(CrawlSpider):
    name = "setSpider"
    allowed_domains = ["localhost"]

    start_urls = [
        "http://127.0.0.1/"
        ]

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(SgmlLinkExtractor(allow=('*\.html', ), deny=('*\.html', ))), #Too broad at the moment...

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def __init__(domainList=["localhost"],\
        urlList = ["http://127.0.0.1/"]):
        allowed_domains = domainList
        start_urls = urlList
        
    def parse_item(self, response):
        self.log('This is an item page, from: %s' % response.url)
    	
        items = []
        sel = Selector(response)
        
        #Find menu links
    	menuData = sel.xpath('//ul/li')
        item = HTMLScraperItem()

        item['title'] = menuData.xpath('a/text()').extract()
        item['link'] = menuData.xpath('a/@href').extract()
        item['desc'] = menuData.xpath('text()').extract()
        item['body'] = None
        items.append(item)
        
        #Table data
        tableData = sel.xpath('//td/text()')
        item = HTMLScraperItem()

        item['title'] = 'tableData'
        item['link'] = None
        item['desc'] = None
        item['body'] = tableData.xpath('td/text()').extract()
        items.append(item)

        #Whole document
        item = HTMLScraperItem()
        
        item['title'] = "response_body"
        item['link'] = response.url
        item['desc'] = "Webpage response"
       	item['body'] = response.body
        items.append(item)

        """
       	filename = response.url.split("/")[-2]
       	filepath = expanduser("~") + "/tmp/scrapy/" + filename

       	print "Result: %b\n" %(pickleObject(filepath, items, "wb"))
        """

        return items
