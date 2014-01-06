# Scrapy settings for setWebScan project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'HTMLScraper'

SPIDER_MODULES = ['HTMLScraper.spiders']
NEWSPIDER_MODULE = 'HTMLScraper.spiders'

EXTENSIONS = {
	'extensions.ScrapyLogger.ScrapyLogger': 501,
}

#SCRAPYLOGGER_ENABLED = True
SCRAPYLOGGER_MAXITEMCOUNT = 1200

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'setWebScan (+http://www.yourdomain.com)'
