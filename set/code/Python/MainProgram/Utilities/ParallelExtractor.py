import sys
import cPickle as pickle

sys.path.append("..")
import Utilities.PreProcessor as PreProcessor
from Parsers.TextParser import TextParser
from Parsers.HTMLParser_ import HTMLParser

from Extractors.HTMLFeatureExtractor import HTMLFeatureExtractor
from Extractors.TextFeatureExtractor import TextFeatureExtractor as tfe
from Extractors.HTMLDeceptionFeatureExtractor import HTMLDeceptionFeatureExtractor as hfe
from Extractors.BaseExtractor import BaseExtractor as be

from Utilities.ExtractorSelector import ExtractorSelector
from Utilities.Utils import readFromFile
from Utilities.FeatureSet import FeatureSet

def _selectExtractorAndProcess(extractorSelector, processedText,\
                           documentClass, email_ID=None, emailPayload=None):
    featureSetList = []
    selectedExtractorTuple = extractorSelector.\
                             determineBestExtractor(processedText.split())
    extractorCategory = selectedExtractorTuple[0]

    if extractorCategory is None:
            documentName = "DEFAULT"
            documentCategory = 'Text'
    else:
            documentName = "%s - %s" % (extractorCategory.upper(), str(uuid4()))
            documentCategory = extractorCategory

    if email_ID is None or emailPayload is None:
            textString = processedText
    else:
            documentName = email_ID
            textString = emailPayload

    #Start parsing using the chosen extractor(s)
    #extractorTuple = pickle.loads(selectedExtractorTuple[1])
    extractorTuple = selectedExtractorTuple[1]
    
    for extractor in extractorTuple:
            if isinstance(extractor, HTMLFeatureExtractor):
                    urlList = HTMLParser().getEmailURLs(textString) #Get all urls in email
                    if urlList != list():                           #If the list is not empty...
                            extractor.scrapeWebsiteFromURL(urlList[0], documentName=None) #Extract data from first url
            
            featureSet = extractor.getFeatureSet(\
                    documentName+": "+documentCategory,\
                    extractor.__class__.__name__, textString, documentClass)
            featureSetList.append(featureSet)
    return pickle.dumps(featureSetList)

def _extractFromDocument(extractorSelector, filepath, documentClass, index=None):   
    documentString = readFromFile(filepath)
    print "---\n", documentString, "\n---"
    processedDocument = PreProcessor.removeEscapeChars(documentString)

    if index is not None:
            parser = TextParser(os.getcwd()+"/Parsers")
            email, isMultipart = parser.getEmailFromString(documentString)
            payload = email.get_payload()
            
            print "Email no. "+str(index)+": "

            print "---"
            for header in email.keys():
                    print "\n"+header+": "+email.get(header)
            print "\nPayload: "+payload
            print "---"

            processedPayload = PreProcessor.removeEscapeChars(payload)
            return _selectExtractorAndProcess(extractorSelector,\
                                              processedDocument,\
                                              documentClass,\
                                              email.get("Message-Id"),\
                                              processedPayload)
    else:
            return _selectExtractorAndProcess(extractorSelector,\
                                              processedDocument,\
                                              documentClass)                      
                    
def extractFromEmails(extractorSelector, documentClass):
    featureSetList = []
    filepathPrefix = "./Emails/"

    i=0
    for filepath in listFilesInDirWithExtension(filepathPrefix, ".eml"):
        featureSetList.extend(_extractFromDocument(extractorSelector,\
                                                   filepathPrefix+filepath,\
                                                   documentClass))
    i+=1
        
    return featureSetList

if __name__ == '__channelexec__':
    for (i, arg) in channel:
        channel.send( (i, _extractFromDocument(pickle.loads(arg[0]), *arg[1:])) )


