import sys, shlex, os, getopt, uuid, time
import cPickle as pickle
import threading
from collections import OrderedDict

from os.path import normpath, isfile, isdir
from uuid import uuid4

from Extractors.DeceptionFeatureExtractor import DeceptionFeatureExtractor as dfe
#from Extractors.HTMLDeceptionFeatureExtractor import HTMLDeceptionFeatureExtractor as hfe
from Extractors.TextFeatureExtractor import TextFeatureExtractor as tfe
from Extractors.HTMLFeatureExtractor import HTMLFeatureExtractor
from Extractors.HTMLScraper.items import HTMLScraperItem

import Utilities.PreProcessor as PreProcessor
from Utilities import ParallelExtractor, ListProcessor
from Utilities.Utils import downloadNLTKData
from Utilities.Utils import readFromFile, listFilesInDirWithExtension,\
     unpickleObject, unpickleHTMLScraperItem, listFilesInDir
from Utilities.listen import startFakeSMTPServer
from Utilities.ExtractorSelector import ExtractorSelector
from Utilities.ParallelExtractor import _extractFromDocument

from Parsers.HTMLParser_ import HTMLParser
from Parsers.TextParser import TextParser

from Classifiers.GaussianSVM import GaussianSVM
from Classifiers.DecisionTree.DTree import DTree

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  #Python 3.x

io_q = Queue()

class Detector(object):
        """docstring for Detector"""
        def __init__(self, *args):
                ###Defaults###

                self.extractorDictionary = {'text':tfe(), 'html':tfe()}

                self.documentPaths = []
                self.extractorSelector = None

                self.matrixDict = OrderedDict()
                self.svms = None
                self.dTrees = None

                ###Dependency checks###

                if not (downloadNLTKData('punkt') and downloadNLTKData('cmudict')):
                        raise RuntimeError("\n\nCould not download the required nltk dependencies\n('punkt' or 'cmudict' dictionaries).\n")                

                ###User arguments###
                #Text must be delimited by semi-colon, in 
                #each file passed into the program
                options, extras = getopt.getopt(args, 'd:i:', ['documentlist=', 'indicatorlist='])
                
                for opt, arg in options:
                        path = normpath(arg)
                
                        if opt in ('-d', '--documentlist'):
                                documentListString = readFromFile(path)
                                self.documentPaths = self._getDocumentPaths(documentListString)
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

                                #self.extractorDictionary = {category:None for category in self.extractorDictionary}
                                        ###Must add FeatureExtractor instances, somehow...
                
        
                self.extractorSelector = self._createExtractor(self.extractorDictionary)

        def _getDocumentPaths(self, documentListString):
                documentPaths = []
                try:
                        documentFilePaths = documentListString.split(';')[:-1]
                        documentClassAndPaths = [pair.split(',') for pair in documentFilePaths]
                except AttributeError, IndexError:
                        sys.stderr.write("\nYour document list has been formatted incorrectly.\n"\
                                         +"Follow this format:\n[class integer],[directory path];\n"\
                                         +"----------------------------\nYou can enter in as many of these lines, as you'd like.\n")
                        sys.exit(1)
                for label, path in documentClassAndPaths:
                        if isdir(path):
                                documentPaths.extend([(int(label), os.path.join(path, document)) for document in listFilesInDir(path)])
                        elif isfile(path):
                                documentPaths.append((int(label), path))
                print "\n-------------------------\nPaths: ", documentFilePaths
                print "Documents: ", documentPaths if len(documentPaths) <= 20 else "More than 20 documents.", "\n-------------------------\n"

                return documentPaths

        def _createExtractor(self, extractorDictionary):
                return ExtractorSelector(extractorDictionary)

        def extractAllDocuments(self):
                featureMatrix = []
                if self.documentPaths:  #List is not empty
                        argsList = [(pickle.dumps(self.extractorSelector), document, label)\
                                                                 for label, document in self.documentPaths]
                        
                        documentList = [pickle.loads(item) for item in\
                                        ListProcessor.map( ParallelExtractor, argsList, options=[('popen', 2)] )]

                        for l in documentList:
                            featureMatrix.extend(l)
                        
                else:                   #No documents found
                        sys.stderr.write("Could not find any documents.\nPlease try again, or enter another file, or directory path.\n")
                        return
                
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
                
                self.svms = {category: GaussianSVM(mdict[category][0],\
                                                   mdict[category][1]) for category in mkeys}
                
                self.dTrees = {category: DTree(mdict[category][0],\
                                               mdict[category][1],\
                                               documentGroupName=category) for category in mkeys}


        def classifyDocument(self, classifierName, label, dictVector):
                if self.svms is None or self.dTrees is None:    #SVM
                        self.svms = {classifierName: GaussianSVM()} #Loads pre-computed model
                        return self.svms[classifierName].classifyDocument(label, dictVector)
                else:                                           #SVM and decision tree
                        return(self.svms[classifierName].classifyDocument(label, dictVector),
                               self.dTrees[classifierName].classifyDocument(dictVector))
                
        def startFakeSMTPServerThread(self):
            smtpThread = threading.Thread(target=startFakeSMTPServer, name='smtp-watcher',
                        args=())

            smtpThread.daemon = True
            smtpThread.start()
                

        def startClassificationThread(self, documentClass):
                classificationThread = threading.Thread(target=_classifyEmailsInFolder,\
                                                        name='email-watcher',args=(self.extractorSelector, documentClass, 10))

                classificationThread.daemon = True
                classificationThread.start()

        def startMainMenu(self):
                time.sleep(0.5);
                while True:
                        option = -1
                        documentClass = -1
                        documentPath = None
                        
                        print "\n-------------------------\nSET Deception Detector:\n-------------------------\n"
                        print "Press a number associated with the following options."
                        print "1) Classify document\n2) Train program with documents\n3) Exit"
                        #print "\n\nNOTE: New documents added to the './Emails' folder\nwill be processed in the background, ***AND then deleted***.\n"
                        
                        while not isinstance(option, (int))\
                                   or (option < 1 or option > 3):
                                try:
                                    option = int(raw_input("Please choose a valid option.\n"))
                                except ValueError:
                                    option = -1
                                
                        if option is 1:

                                while not isinstance(documentClass, (int))\
                                       or documentClass < 0:
                                        try:
                                                documentClass = int(raw_input("Please enter a class integer, equal to or greater than 0.\n"))
                                        except ValueError:
                                                documentClass = None  

                                documentPath = normpath(raw_input("Now enter the filepath of the document to classify.\n"))
                                while (not isinstance(documentPath, basestring)) or (not isfile(documentPath)):
                                        documentPath = normpath(raw_input("Please enter a valid filepath.\n"))

                                featureSetList = _extractFromDocument(documentPath, documentClass)
                                for featureSet in featureSetList:
                                        print self.classifyDocument(featureSet.documentCategory,\
                                                              documentClass, featureSet.getVector())
                                
                        elif option is 2:

                                documentPaths = None
                                path = None
                                if len(sys.argv) is 1: #No arguments passed
                                        message = "\nNow enter the directory path or filepath of the document(s) "\
                                                  +"to classify, using the following format:\n[class integer],[directory path];\n"\
                                         +"----------------------------\nYou can enter in as many of these lines, as you'd like.\n"
                                        
                                        while not isinstance(path, basestring) or not (isfile(path) or isdir(path)):
                                                documentPaths = normpath(raw_input(message))
                                                try:
                                                        path = documentPaths.split(',')[1].split(';')[0]
                                                except IndexError:
                                                        path = None
                                        self.documentPaths = self._getDocumentPaths(documentPaths) #If entering in the document list, on the fly...
                                detector.extractAllDocuments()		
                                detector.trainClassifiers()
                                
                        elif option is 3:
                                sys.exit(0)

def _classifyEmailsInFolder(extractorSelector, documentClass, maxQueueLength):
        currentQueueLength = 0
        maxQueueLength = maxQueueLength if maxQueueLength > 1 else 1

        while True:
        
                while currentQueueLength < maxQueueLength:
                        emailList = listFilesInDirWithExtension(filepathPrefix, ".eml")
                        for filepath in emailList:
                                io_q.put(_extractFromDocument(extractorSelector,\
                                                              filepathPrefix+filepath,\
                                                              documentClass,\
                                                              index=-1))
                                os.remove(filepath)
                                currentQueueLength += 1

                [self.svms[model].updateModel([documentClass], [io_q.get()]) for model in self.svms]
                currentQueueLength -= 1
                #Delete email, when not in access. Otherwise wait/locked out...
                
                
if __name__ == "__main__":
        detector = Detector(*sys.argv[1:])
        detector.startFakeSMTPServerThread()
        detector.startMainMenu()

        
