import os, sys, re, tldextract
from urlparse import urlparse

from collections import Counter
sys.path.append("..")

from Extractors.HTMLScraper.items import HTMLScraperItem

class HTMLParser:
        parsedText = {}
        
        def __init__(self):
                pass

        #Source: StackOverflow - http://stackoverflow.com/questions/4436008/how-to-get-html-tags
        def findTagsInString(self, textString):
                return re.findall('<.*?>', textString)

        def getTagsFromItem(self, item):
                if isinstance(item, HTMLScraperItem):
                        responseAll = item['response']['tags']
                        return [x.encode('utf8') for x in responseAll]
                else:
                        return TypeError("The 'item' must be of type 'HTMLScraperItem'.")
    
        def getTagsFromString(self, textString):
                if isinstance(textString, basestring):
                        return self.findTagsInString(textString)
                elif not isinstance(textString, basestring):
                        raise TypeError("The parameter must be a string.")

        #Choices: 'all', 'headers', 'body', 'para', 'url'
        def getResponseAttribute(self, item, attributeString):
                if isinstance(attributeString, basestring)\
                        and isinstance(item, HTMLScraperItem):

                        try:
                                unicodeText = item['response'][attributeString]
                                return ''.join([x.encode('utf8') for x in unicodeText])
                        except UnicodeDecodeError:
                                return '1'

                elif not isinstance(attributeString, basestring):
                        raise TypeError("The attribute must be a string.")
                elif not isinstance(item, HTMLScraperItem):
                        return TypeError("The 'item' must be of type 'HTMLScraperItem'.")
    
        def getTagCounter(self, item):
                return(Counter(self.getTagsFromItem(item)))

        #source: StackOverflow - http://stackoverflow.com/questions/9000960/python-regular-expressions-re-search-vs-re-findall
        def findIPAddressesInEmail(self, textString):
                countExp = re.compile("((?:\d{1,3}\.){3}\d{1,3})")
                return re.findall(countExp, textString)

        def getWebsiteURLs(self, item):
                if isinstance(item, HTMLScraperItem):
                        return [item['links']['site_'+str(i)]['link']\
                                for i in range(len(item['links']))]
                else:
                        return TypeError("The 'item' must be of type 'HTMLScraperItem'.")

        #source: StackOverflow - http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
        def getEmailURLs(self, textString):
                return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', textString)

        #'tldextract' library - Source: https://github.com/john-kurkowski/tldextract
        #To get correct domains from a URL
        def getURLDomain(self, urlString):
                return tldextract.extract(urlString).domain
                #return '.'.join(tldextract.extract(textString)[:2]) - Domain and Subdomain joined together

        def getURLsWithDomains(self, textString):
                urlList = self.getEmailURLs(textString)
                domainList = [self.getURLDomain(url) for url in urlList]
                return (domainList, urlList)


