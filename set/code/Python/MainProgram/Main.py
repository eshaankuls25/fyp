import sys, shlex, os, getopt

from Extractors.ObfuscationFeatureExtractor import ObfuscationFeatureExtractor
from Extractors.ImitationFeatureExtractor import ImitationFeatureExtractor
from Extractors.HTMLFeatureExtractor import HTMLFeatureExtractor
from Extractors.HTMLScraper.items import HTMLScraperItem

from Utilities.PreProcessor import PreProcessor
from Utilities.ExtractorSelector import ExtractorSelector
from Utilities.Utils import readFromFile
from Utilities.Utils import listFilesInDirWithExtension
from Utilities.Utils import unpickleObject
from Utilities.Utils import unpickleHTMLScraperItem
from Utilities.listen import startFakeSMTPServer

from Parsers.HTMLParser_ import HTMLParser
from Parsers.TextParser import TextParser

from Classifiers.GaussianSVM import GaussianSVM

def selectExtractorAndProcess(extractorSelector, processedText,\
                              email_ID=None, emailPayload=None):
        currentFeatureSetList = []
        selectedExtractorTuple = extractorSelector.\
                                         determineBestExtractor(processedText.split())

        if selectedExtractorTuple[0] is None:
                documentName = "DEFAULT - TEXT"
                documentCategory = 'text'
                documentClass = 0
        elif selectedExtractorTuple[0] is 'text':
                documentName = "DEFAULT - TEXT"
                documentCategory = 'text'
                documentClass = 1
        elif selectedExtractorTuple[0] is 'html':
                documentName = "DEFAULT - HTML"
                documentCategory = "html"
                documentClass = 2

        if email_ID is None or emailPayload is None:
                textString = processedText
        else:
                documentName = email_ID
                textString = emailPayload

        #Start parsing using the chosen extractor(s)
        extractorTuple = selectedExtractorTuple[1]
                
        for extractor in extractorTuple:
                featureSet = extractor.getFeatureSet(\
                        documentName+": "+extractor.__class__.__name__,\
                        documentCategory, textString, documentClass)
                currentFeatureSetList.append(featureSet)
        return currentFeatureSetList

def extractFromEmails(extractorSelector):
        emailList = []
        featureSetList = []
        filepathPrefix = "./Emails/"
        parser = TextParser(os.getcwd()+"/Parsers")
        
        for filepath in listFilesInDirWithExtension(filepathPrefix, ".eml"):
                emailString = readFromFile(filepathPrefix+filepath)
                emailList.append(parser.getEmailFromString(emailString))

        i=0        
        for email, isMultipart in emailList:
                payload = email.get_payload()
                
                print "Email no. "+str(i)+": "

                print "---"
                for header in email.keys():
                        print "\n"+header+": "+email.get(header)
                print "\nPayload: "+payload
                print "---"

                preProcessor = PreProcessor()
                processedEmail = preProcessor.removeEscapeChars(emailString)
                processedPayload = preProcessor.removeEscapeChars(payload)
                
                tempFeatureSetList = selectExtractorAndProcess(extractorSelector, processedEmail, email.get("Message-Id"), processedPayload)
                featureSetList.extend(tempFeatureSetList)
                
                i+=1
                
        return featureSetList

def extractFromWebsites(extractorSelector):
        featureSetList = []
        filepathPrefix = "./Sites/"
        websiteList = listFilesInDirWithExtension(filepathPrefix, '.obj')

        hparser = HTMLParser()
        tagCounter = {}
        headersDict = {}

        for websitePath in websiteList:

                item = unpickleHTMLScraperItem(filepathPrefix+websitePath)

                #response = hparser._getResponseAttribute(item, 'all')
                #preProcessor = PreProcessor()
                #processedResponse = preProcessor.removeEscapeChars(response)

                #tempFeatureSetList = selectExtractorAndProcess(extractorSelector, processedResponse)
                #featureSetList.extend(tempFeatureSetList)
                
                tagCounter[websitePath] = hparser.getTagCounter(item)
                headersDict[websitePath] = hparser._getResponseAttribute(item, 'headers')

                print "---"
                print tagCounter[websitePath]
                print "---"
                print headersDict[websitePath]
                print "---"
        
        return None
        #Must return a list of feature set objects, later on


def main():

        ###Defaults###
        extractorSelector = None
        documentFilePath = 'test_email'
        documentCategory = 'text'
        categoryList = ['text', 'html']

        extractorList = [(ImitationFeatureExtractor(), ObfuscationFeatureExtractor()),\
                         HTMLFeatureExtractor(startScrapyScan=False)]
    
        indicatorDictionary = {'text':['From:', 'Date:', 'Message-ID', 'In-Reply-To:'],\
                              'html':['http://', 'www', '.com', '.co.uk']}

        featureMatrix = []
        
        ###User arguments###

        options, extras = getopt.getopt(sys.argv[1:], 'd:c:e:i:', ['docpath=', 'category=' 'categoriesfilepath=', 'indicatorsfilepath='])
                
        for opt, arg in options:
                if opt in ('-d', '--docpath'):
                        documentFilePath = arg.replace("\\", "/")
                elif opt in ('-c', '--category'):
                        documentCategory = arg
                elif opt in ('-x', '--categoriesfilepath'):
                        categoryList = shlex.split(readFromFile(arg))
                        categoryFileExists = True
                elif opt in ('-y', '--indicatorsfilepath'):
                        #Must change to allow file to contain
                        #multiple document names, which map to multiple indicators
                        #use 'indicatorDictionary' - maps docname to text features
                        indicatorList = shlex.split(readFromFile(arg))
                        indicatorFileExists = True

        extractorSelector = ExtractorSelector(categoryList, extractorList)

        for category in categoryList:
                extractorSelector.addExtractorIdentifierSet(category, indicatorDictionary[category])                   

        ###Extracting###

        featureMatrix.extend(extractFromEmails(extractorSelector))
        featureMatrix.extend(extractFromWebsites())

        labelMat = []
        valueMat = []
                        
        print "---"
        for featureSet in featureMatrix:
                print featureSet.documentName, "---", featureSet.documentCategory
                print featureSet.getClass()
                print featureSet.getVector()
                labelMat.append(featureSet.getClass())
                valueMat.append(featureSet.getVector())
                print "---"
                
        ###Testing Gaussian SVM###
        gSVM = GaussianSVM()

        startFakeSMTPServer()

        """
        if sys.platform == 'win32':
                #startProcess("python ./Utilities/listen.py")
        else:
                #startProcess("sudo chmod +x ./Utilities/listen.py")
                #startProcess("./Utilities/listen.py")
        """
        
if __name__ == "__main__":
        main()
