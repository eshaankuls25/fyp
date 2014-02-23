# -*- coding: utf-8 -*-
import sys, chardet, unicodedata

#Source : http://stackoverflow.com/questions/446052/python-best-way-to-check-for-python-version-in-a-program-that-uses-new-language
reqVersion = (3,0)
curVersion = sys.version_info
        
def removeEscapeChars(textString):
        if curVersion < reqVersion:
                return textString.encode('string_escape').decode('string_escape')  #Python 2
        else:
                return textString.encode('encode_escape').decode("unicode_escape") #Python 3

def getASCIIChars(textString):
        return unicode(string, 'ascii', 'ignore')

#Source: http://www.packtpub.com/article/parsing-specific-data-python-text-processing
def detectEncoding(textString):
        try:
                return chardet.detect(textString)
        except UnicodeDecodeError:
                return chardet.detect(textString.encode('utf-8'))

def convertString(textString):
        encoding = detectEncoding(textString)['encoding']
        if encoding == 'utf-8':
                return unicode(textString)
        else:
                return unicode(textString, encoding)

def convertToAscii(textString):
        #'NFKD' means that non-ASCII chars will be replaced with the ASCII equivalents
        return unicodedata.normalize('NFKD', textString).encode('ascii', 'ignore')
                
