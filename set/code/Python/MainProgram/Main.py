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

class Detector(object):
        """docstring for Detector"""
        def __init__(self, *args):
                ###Defaults###

                self.categoryList = ['text', 'html']

                self.indicatorDictionary = {'text':['From:', 'Date:', 'Message-ID', 'In-Reply-To:'],\
                              'html':['http://', 'www', '.com', '.co.uk']}

                self.extractorList = [(ImitationFeatureExtractor(), ObfuscationFeatureExtractor()),\
                         (ImitationFeatureExtractor(), ObfuscationFeatureExtractor())]

                self.documentPaths = []
                self.extractorSelector = None

                self.matrixDict = OrderedDict()
                self.svms = None
                self.dTrees = None
                

                ###User arguments###
                #Text must be delimited by semi-colon, in 
                #each file passed into the program
                options, extras = getopt.getopt(args, 'd:c:i:', ['documentlist=', 'categorylist=' 'indicatorlist='])
                
                for opt, arg in options:
                        path = normpath(arg)
                
                        if opt in ('-d', '--documentlist'):
                                documentListString = readFromFile(path)
                                documentFilePaths = documentListString.split(';')[:-1]
                                print documentFilePaths
                                documentClassAndPaths = [pair.split(',') for pair in documentFilePaths]

                                for label, path in documentClassAndPaths:
                                        if isdir(path):
                                            self.documentPaths.extend([(label, os.path.join(path, document)) for document in listFilesInDir(path)])
                                        elif isfile(path):
                                            self.documentPaths.append((label, document))
                                print "Documents: ", self.documentPaths

                        if opt in ('-c', '--categorylist'):
                                categoryListString = readFromFile(path)
                                self.categoryList = categoryListString.split(';')

                                print self.categoryList

                        if opt in ('-i', '--indicatorlist'):
                                indicatorListString = readFromFile(path)
                                #For separating indicator to groups - one for each category
                                indicatorGroupsList = indicatorListString.split(';')

                                #For separating indicator words/phrases
                                if len(categoryList) == len(indicatorGroupsList):
                                        self.indicatorDictionary = {categoryList[x] : indicatorGroupsList[x].split(',') \
                                                               for x in len(range(categoryList))}
                                else:
                                        raise RuntimeError("\nTotal number of categories, is not equal to the number of indicator groups.\n")     

                                print self.indicatorList
        
                self.extractorSelector = self._createExtractor(self.categoryList, self.indicatorDictionary, self.extractorList)
                                

        def _createExtractor(self, categoryList, indicatorDictionary, extractorList):
                extractorSelector = ExtractorSelector(categoryList, extractorList)
                for category in categoryList:
                        extractorSelector.addExtractorIdentifierSet(category, indicatorDictionary[category])
                return extractorSelector

        def _selectExtractorAndProcess(self, processedText,\
                              documentClass, email_ID=None, emailPayload=None):
                featureSetList = []
                selectedExtractorTuple = self.extractorSelector.\
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
                extractorTuple = selectedExtractorTuple[1]
                
                for extractor in extractorTuple:
                        urlList = HTMLParser().getEmailURLs(textString) #Get all urls in email
                        if urlList != list(): #Get first url, if one exists in email
                                extractor.scrapeWebsiteFromURL(urlList[0], documentName=None)
                        
                        featureSet = extractor.getFeatureSet(\
                                documentName+": "+documentCategory,\
                                extractor.__class__.__name__, textString, documentClass)

                        featureSetList.append(featureSet)
                return featureSetList

        def _extractFromDocument(self, filepath, documentClass, index=None):    
                documentString = readFromFile(filepath)

                print "---\n", documentString, "\n---"

                preProcessor = PreProcessor()
                processedDocument = preProcessor.removeEscapeChars(documentString)

                parser = TextParser(os.getcwd()+"/Parsers")
                email, isMultipart = parser.getEmailFromString(documentString)
                payload = email.get_payload()

                if index is not None:
                        print "Email no. "+str(index)+": "

                        print "---"
                        for header in email.keys():
                                print "\n"+header+": "+email.get(header)
                        print "\nPayload: "+payload
                        print "---"

                if index is not None:
                        processedPayload = preProcessor.removeEscapeChars(payload)
                        return self._selectExtractorAndProcess(processedDocument,\
                                                         documentClass,\
                                                         email.get("Message-Id"),\
                                                               processedPayload)
                else:
                        return self._selectExtractorAndProcess(processedDocument,\
                                                         documentClass)
                        
                    
        def extractFromEmails(self, documentClass):
                featureSetList = []
                filepathPrefix = "./Emails/"
        
                i=0
                for filepath in listFilesInDirWithExtension(filepathPrefix, ".eml"):
                        featureSetList.extend(self._extractFromDocument(filepathPrefix+filepath,\
                                                                   documentClass,\
                                                                   index=i))
                i+=1
                
                return featureSetList

        def extractAllDocuments(self):
                featureMatrix = []
                ###Extracting emails from file(s):###
                if self.documentPaths: #List is not empty
                        [featureMatrix.extend(self._extractFromDocument(document, label)) for label, document in self.documentPaths]
                else:
                        ###Extracting###
                        featureMatrix.extend(self.extractFromEmails(documentClass=0))

                for featureSet in featureMatrix:
                        category = featureSet.documentCategory

                        if category not in self.matrixDict:
                                self.matrixDict[category] = [[],[]]

                        self.matrixDict[category][0].append(featureSet.getClass())
                        self.matrixDict[category][1].append(featureSet.getVector())
                
                print "---"
                for k in self.matrixDict:
                        print k
                        print self.matrixDict[k] 
                        print "---"

        def trainClassifiers(self):
                mkeys = self.matrixDict.keys()
                mdict = self.matrixDict
                self.svms = {category: GaussianSVM(mdict[category][0], mdict[category][1]) for category in mkeys}
                self.dTrees = {category: DTree(mdict[category][0], mdict[category][1], documentGroupName=category) for category in mkeys}


        def classifyDocument(self, classifierName, label, dictVector):
                return(self.svms[classifierName].classifyDocument(label, dictVector),
                       self.dTrees[classifierName].classifyDocument(dictVector))

        def startClassificationLoop(self):
                while True:
                        option = None
                        documentClass = None
                        documentPath = None
                        print "SET Deception Detector:\n"
                        print "Press a number associated with the following options."
                        print "1) Classify document\n2) Train program with documents\n3) Exit"
                        
                        while (not isinstance(option, (int))\
                                   and (option < 1 or option > 3)):
                                option = int(raw_input("Please choose a valid option.\n"))
                                print option
                                
                        if option is 1:
                                while (not isinstance(documentClass, (int))\
                                       and (documentClass < 1)):
                                        documentClass = int(raw_input("Please enter a class integer, equal to or greater than 1.\n"))
                                print documentClass
                                documentPath = normpath(raw_input("Now enter the filepath of the document to classify.\n"))
                                
                                while not isfile(documentPath):
                                        documentPath = normpath(raw_input("Please enter a valid filepath.\n"))
                                #Must change default classifier group name - imitation, obfuscation etc.
                                self.classifyDocument('ImitationFeatureExtractor', documentClass, self._extractFromDocument(documentPath, documentClass)) 

                        elif option is 2:
                                detector.extractAllDocuments()
                                detector.trainClassifiers()
                        elif option is 3:
                                sys.exit(0)
                
if __name__ == "__main__":
        detector = Detector(*sys.argv[1:])
        detector.startClassificationLoop()
        """
        detector.classifyDocument('ImitationFeatureExtractor', 0, {0: 0.4, 1: 2.8, 2: 0.89, 3: 0.9, 4: 26,\
                                      5: 1, 6:0, 7:56, 8:3, 9:2, 10:1, 11:0})

        """

        
