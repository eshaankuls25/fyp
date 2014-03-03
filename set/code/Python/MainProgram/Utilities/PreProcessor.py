# -*- coding: utf-8 -*-
import sys, chardet, unicodedata

sys.path.append("..")
from Parsers.Stemming.lovins    import stem              as lovins_stem
from nltk.stem.porter           import PorterStemmer     as porter
from nltk.stem.lancaster        import LancasterStemmer  as lancs
from nltk.stem.snowball         import EnglishStemmer    as snowball
from nltk.stem                  import WordNetLemmatizer as wnl

#Source : http://stackoverflow.com/questions/446052/python-best-way-to-check-for-python-version-in-a-program-that-uses-new-language
reqVersion = (3,0)
curVersion = sys.version_info

_lancs = lancs()
_porter = porter()
_snowball = snowball()
_wnl = wnl()
        
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

def stem(textString, stemmerType="porter"): #Defaults to Porter stemmer
        if not (isinstance(stemmerType, basestring)\
                and isinstance(textString, basestring)):
                raise TypeError("Both 'textString' and 'stemmerType' must be strings.")
        
        if stemmerType == "lovins":
                return lovins_stem(textString)
        elif stemmerType == "lancaster":
                return _lancs.stem(textString)
        elif stemmerType == "porter":
                return _porter.stem(textString)
        elif stemmerType == "snowball":
                return _snowball.stem(textString)

def lemmatise(textString):
        return _wnl.lemmatize(textString)

def lemmatiseText(textString):
        return ''.join(["%s "%lemmatise(word) for word in textString.split()])
        
