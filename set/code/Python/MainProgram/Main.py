import sys, shlex, os, getopt, uuid
from collections import OrderedDict

from os.path import normpath, isfile, isdir
from uuid import uuid4

from Extractors.ObfuscationFeatureExtractor import ObfuscationFeatureExtractor
from Extractors.ImitationFeatureExtractor import ImitationFeatureExtractor
from Extractors.HTMLScraper.items import HTMLScraperItem

from Utilities.PreProcessor import PreProcessor
from Utilities.ExtractorSelector import ExtractorSelector
from Utilities.Utils import readFromFile, listFilesInDirWithExtension, unpickleObject, unpickleHTMLScraperItem, listFilesInDir
from Utilities.listen import startFakeSMTPServer

from Parsers.HTMLParser_ import HTMLParser
from Parsers.TextParser import TextParser

from Classifiers.GaussianSVM import GaussianSVM
from Classifiers.DecisionTree.DTree import DTree

def createExtractor(categoryList, indicatorDictionary, extractorList):
    extractorSelector = ExtractorSelector(categoryList, extractorList)
    for category in categoryList:
        extractorSelector.addExtractorIdentifierSet(category, indicatorDictionary[category])

    return extractorSelector

def selectExtractorAndProcess(extractorSelector, processedText,\
                              email_ID=None, emailPayload=None):
        featureSetList = []
        selectedExtractorTuple = extractorSelector.\
                                         determineBestExtractor(processedText.split())
        extractorCategory = selectedExtractorTuple[0]

        if extractorCategory is None:
                documentName = "DEFAULT - TEXT"
                documentCategory = 'text'
                documentClass = 0
        else:
                documentName = "%s - %s" % (extractorCategory.upper(), str(uuid4()))
                documentCategory = extractorCategory
            
                if extractorCategory is 'text':
                        documentClass = 1
                elif extractorCategory is 'html':
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
                        documentName+": "+documentCategory,\
                        extractor.__class__.__name__, textString, documentClass)
                featureSetList.append(featureSet)
        return featureSetList

def _extractFromEmail(extractorSelector, filepath, index=None):
    emailString = readFromFile(filepath)

    parser = TextParser(os.getcwd()+"/Parsers")
    email, isMultipart = parser.getEmailFromString(emailString)
    payload = email.get_payload()

    if index is not None:
        print "Email no. "+str(index)+": "

        print "---"
        for header in email.keys():
                print "\n"+header+": "+email.get(header)
        print "\nPayload: "+payload
        print "---"
    
    preProcessor = PreProcessor()
    processedEmail = preProcessor.removeEscapeChars(emailString)
    processedPayload = preProcessor.removeEscapeChars(payload)

    return selectExtractorAndProcess(extractorSelector,\
        processedEmail, email.get("Message-Id"), processedPayload)

def extractFromEmails(extractorSelector):
        featureSetList = []
        filepathPrefix = "./Emails/"
        
        i=0
        for filepath in listFilesInDirWithExtension(filepathPrefix, ".eml"):
                featureSetList.extend(_extractFromEmail(extractorSelector,\
                    filepathPrefix+filepath, index=i))
                i+=1
                
        return featureSetList


def main():
        ###Defaults###

        categoryList = ['text', 'html']
    
        indicatorDictionary = {'text':['From:', 'Date:', 'Message-ID', 'In-Reply-To:'],\
                              'html':['http://', 'www', '.com', '.co.uk']}

        extractorList = [(ImitationFeatureExtractor(), ObfuscationFeatureExtractor()),\
                         (ImitationFeatureExtractor(), ObfuscationFeatureExtractor())]

        featureMatrix = []
        documentPaths = []
        
        ###User arguments###
        #Text must be delimited by semi-colon, in 
            #each file passed into the program
        options, extras = getopt.getopt(sys.argv[1:], 'd:c:i:', ['documentlist=', 'categorylist=' 'indicatorlist='])
                
        for opt, arg in options:
                path = normpath(arg)
                if opt in ('-d', '--documentlist'):
                    documentListString = readFromFile(path)
                    documentFilePaths = documentListString.split(';')
                    
                    for path in documentFilePaths:
                        if isdir(path):
                            documentPaths.extend(listFilesInDir(path))
                        elif isfile(path):
                            documentPaths.append(path)

                if opt in ('-c', '--categorylist'):
                        categoryListString = readFromFile(path)
                        categoryList = categoryListString.split(';')

                        if opt in ('-y', '--indicatorlist'):
                                indicatorListString = readFromFile(path)
                                #For separating indicator to groups - one for each category
                                indicatorGroupsList = indicatorListString.split(';')

                                #For separating indicator words/phrases
                                if len(categoryList) == len(indicatorGroupsList):
                                        indicatorDictionary = {categoryList[x] : indicatorGroupsList[x].split(',') \
                                                               for x in len(range(categoryList))}
                                else:
                                        raise RuntimeError("\nTotal number of categories, is not equal to the number of indicator groups.\n")     
        
        extractorSelector = createExtractor(categoryList, indicatorDictionary, extractorList)
        
        ###Extracting emails from file(s):###
        if documentPaths: #List is not empty
                [featureMatrix.extend(_extractFromEmail(x)) for x in documentPaths]             

        ###Extracting###
        featureMatrix.extend(extractFromEmails(extractorSelector))

        matDict = OrderedDict() 
        for featureSet in featureMatrix:
                category = featureSet.documentCategory

                if category not in matDict:
                    matDict[category] = [[],[]]

                matDict[category][0].append(featureSet.getClass())
                matDict[category][1].append(featureSet.getVector())
                
        print "---"
        for k in matDict:
            print k
            print matDict[k] 
            print "---"

        #Test
        category = 'ImitationFeatureExtractor'
        matDict[category][0].append(0)
        matDict[category][1].append({0: 0.4, 1: 2.8, 2: 0.89, 3: 0.9, 4: 20, 5: 1})

        matDict[category][0].append(0)
        matDict[category][1].append({0: 0.4, 1: 2.8, 2: 0.89, 3: 0.9, 4: 30, 5: 1})

        matDict[category][0].append(0)
        matDict[category][1].append({0: 0.4, 1: 2.8, 2: 0.89, 3: 0.9, 4: 28, 5: 1})
                
        ###Testing Classifiers###
        svms = [GaussianSVM(matDict[category][0], matDict[category][1]) for category in matDict.keys()]
        dTrees = [DTree(matDict[category][0], matDict[category][1], documentGroupName=category) for category in matDict.keys()]

        print dTrees[1].classifyDocument({0: 0.4, 1: 2.8, 2: 0.89, 3: 0.9, 4: 26, 5: 1})
    
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
