# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class HTMLScraperItem(Item):
    # define the fields for your item here like:
    # name = Field()
    
    documentName = Field()
    links = Field()
    tableData = Field()
    response = Field()
    
    
