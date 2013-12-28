from scrapy.spider import BaseSpider

class SETSpider(BaseSpider):
    name = "set"
    allowed_domains = ["localhost"]

    start_urls = [
        "http://127.0.0.1/"
        ]

    def parse(self, response):
    	sel = Selector(response)
    	sites = sel.xpath('//ul/li')
       	items = []
       	for site in sites:
        	item = SetwebscanItem()
           	item['title'] = site.xpath('a/text()').extract()
           	item['link'] = site.xpath('a/@href').extract()
           	item['desc'] = site.xpath('text()').extract()
           	item['body'] = None
           	items.append(item)

        item = SetwebscanItem()
        item['title'] = "response_body"
        item['link'] = response.url
        item['desc'] = "Webpage response"
       	item['body'] = response.body

       	filename = response.url.split("/")[-2]
       	filepath = expanduser("~") + "/tmp/scrapy/" + filename

       	pickleObject(filepath, items, "wb")
       	return items