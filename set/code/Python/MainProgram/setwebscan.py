from scrapy.spider import BaseSpider

class SETSpider(BaseSpider):
    name = "set"
    allowed_domains = ["localhost"]

    start_urls = [
        "http://127.0.0.1"
        ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
