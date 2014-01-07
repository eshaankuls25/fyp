# Scrapy settings for HTMLScraper  project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'HTMLScraper'

SPIDER_MODULES = ['Extractors.HTMLScraper.spiders']
NEWSPIDER_MODULE = 'Extractors.HTMLScraper.spiders'

EXTENSIONS = {
    'Extractors.HTMLScraper.ScrapyLogger.ScrapyLogger': 501,
}

SCRAPYLOGGER_ENABLED = True
SCRAPYLOGGER_MAXITEMCOUNT = 1200

ITEM_PIPELINES = {
    'Extractors.HTMLScraper.pipelines.HTMLScraperPipeline': 300, 
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'HTMLScraper (+http://www.yourdomain.com)'
