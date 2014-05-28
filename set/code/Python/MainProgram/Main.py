import sys, shlex, os, getopt, uuid,\
       time, threading, multiprocessing
import cPickle as pickle
from math           import ceil 
from collections    import OrderedDict

from os.path        import normpath, isfile, isdir

from    Extractors.InitialFeatureExtractor     import InitialFeatureExtractor      as ife
from    Extractors.DeceptionFeatureExtractor   import DeceptionFeatureExtractor    as dfe
from    Extractors.GeneralFeatureExtractor     import GeneralFeatureExtractor      as gfe
from    Extractors.TextFeatureExtractor        import TextFeatureExtractor         as tfe
from    Extractors.BaseExtractor               import BaseExtractor                as be
from    Extractors.HTMLScraper.items           import HTMLScraperItem

from    Extractors.POSFeatureExtractor         import _getTagCountVector           as getTagVec

from    Utilities                              import ParallelExtractor, ListProcessor
from    Utilities.Utils                        import downloadNLTKData, readFromFile,\
                                                                    listFilesInDir, writeWekaArffFile
from    Utilities.PreProcessor                 import convertString
from    Utilities.listen                       import startFakeSMTPServer
from    Utilities.ExtractorSelector            import ExtractorSelector
from    Utilities.ParallelExtractor            import _extractFromDocument
from    Utilities.FeatureSet                   import FeatureSet
from    Parsers.TextParser                     import TextParser

import  Utilities.PreProcessor as PreProcessor
from    Utilities.PreProcessor                 import stem, lemmatiseText
from    Classifiers.DecisionTree.DTree         import DTree
from    Classifiers.SupportVectorMachine.SVM   import SVM
from    Classifiers.NaiveBayes                 import NaiveBayes

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  #Python 3.x

io_q = Queue()

class Detector(object):
        """docstring for Detector"""
        def __init__(self, *args):
                ###Defaults###

                cpuCount = multiprocessing.cpu_count()
                self.maxParallelCoreCount = int(ceil(float(cpuCount)/2)) if cpuCount <= 8\
                                            else int(ceil(0.75*cpuCount)) #Core count ranges from 1 to ceil(num_of_cores/2), if core count <= 8,
                                                                                #else is approx. or exactly 3/4 of the total CPU count.
                self.extractorDictionary = {'text':gfe(), 'html':gfe()}
                self.documentPaths = []
                self.extractorSelector = None
                self.isParallel = True

                self.matrixDict = OrderedDict()
                self.svms = None
                self.dTrees = None
                self.naiveBayes = None

                ###Dependency checks###

                if not (downloadNLTKData('punkt') and downloadNLTKData('cmudict')
                        and downloadNLTKData('wordnet')):
                        raise RuntimeError("\n\nCould not download the required nltk dependencies.\n")                

                ###User arguments###
                #Text must be delimited by semi-colon, in 
                #each file passed into the program
                options, extras = getopt.getopt(args, 'd:p:', ['documentlist=', 'parallel='])
                
                for opt, arg in options:
                        path = normpath(arg)
                
                        if opt in ('-d', '--documentlist'):
                                documentListString = readFromFile(path)
                                
                                for ch in ('\n', '\t', ' '): #Removes unnecessary characters
                                    if ch in documentListString:
                                        documentListString = documentListString.replace(ch, '')

                                self.documentPaths = self._getDocumentPaths(documentListString)
                                
                        if opt in ('-p', '--parallel'):
                                if isinstance(arg, basestring) and len(arg) == 1:
                                    option = int(arg)
                                    
                                    if option == 0:
                                        self.isParallel = False
                                    elif option == 1:
                                        self.isParallel = True
                                
        
                self.extractorSelector = self._createExtractor(self.extractorDictionary)

        def _getDocumentPaths(self, documentListString):
                documentPaths = []
                try:
                        documentFilePaths = documentListString.split(';')[:-1]
                        documentClassAndPaths = [pair.split(',') for pair in documentFilePaths]

                        for label, path in documentClassAndPaths:
                            convertedLabel = int(label)
                            if (not isinstance(convertedLabel, int)) or (convertedLabel not in (0, 1)):
                                raise ValueError
                        
                except (AttributeError, IndexError, ValueError):
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
                        """
                        tp = TextParser("./Parsers/")
                        exDict = self.extractorSelector.extractorDictionary
                        for label, document in self.documentPaths:
                            for ex in exDict:
                                exDict[ex].setFunctionArgTuple( (getTagVec, [tp, readFromFile(document)]) )
                        """

                        if self.isParallel: #Parallel execution
                            argsList = [(pickle.dumps(self.extractorSelector), convertString(document), label)\
                                                                     for label, document in self.documentPaths]

                            if len(argsList) < self.maxParallelCoreCount: #Less documents than available cores...
                                self.maxParallelCoreCount = len(argsList) #Reduce core count == no. of documents                      
                            
                            documentList = [pickle.loads(item) for item in\
                                            ListProcessor.map( ParallelExtractor, argsList, options=[('popen', self.maxParallelCoreCount )] )]

                        else:               #Sequential execution
                            argsList = [(self.extractorSelector, convertString(document), label)\
                                        for label, document in self.documentPaths]

                            documentList = [pickle.loads(_extractFromDocument(arg[0], *arg[1:])) for arg in argsList]
                
                        
                        for l in documentList:
                            featureMatrix.extend(l)
                        
                        
                else:   #No documents found
                        sys.stderr.write("Could not find any documents.\nPlease try again, or enter another file, or directory path.\n")
                        return
                
                for featureSet in featureMatrix:
                        category = featureSet.documentCategory #category = FeatureExtractor name, e.g. 'TextFeatureExtractor'

                        if category not in self.matrixDict:
                                self.matrixDict[category] = [[],[]] #[[classes/labels][associated vectors]]

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

                #category = FeatureExtractor name
                [writeWekaArffFile("set_%s"%category, mdict[category][1][0].keys(), mdict[category]) for category in mkeys]

                print "\n-------------------------\nTRAINING...\n-------------------------\n"

                self.naiveBayes = {category: NaiveBayes(mdict[category][0],\
                                                        mdict[category][1]) for category in mkeys}
                
                self.svms = {category: SVM(mdict[category][0],\
                                           mdict[category][1]) for category in mkeys}
                
                self.dTrees = {category: DTree(mdict[category][0],\
                                               mdict[category][1],\
                                               documentGroupName=category) for category in mkeys}


        def classifyDocument(self, classifierName, label, dictVector):
                if self.svms is None or self.dTrees is None:                 
                        self.svms = {classifierName: SVM()}                                     #Loads pre-computed SVM model
                        self.dTrees = {classifierName: DTree(documentGroupName=classifierName)} #Loads pre-computed Decision Tree CSV
                        return (self.svms[classifierName].classifyDocument(label, dictVector),
                                self.dTrees[classifierName].classifyDocument(dictVector))
                    
                else:   #Display results of SVM and Decision Tree
                        #self.naiveBayes[classifierName].classifyDocument(label, dictVector)
                    
                        return (self.svms[classifierName].classifyDocument(label, dictVector),
                                self.dTrees[classifierName].classifyDocument(dictVector))

        
        def startFakeSMTPServerThread(self):
            smtpThread = threading.Thread(target=startFakeSMTPServer, name='smtp-watcher',
                        args=())

            smtpThread.daemon = True
            smtpThread.start()
            

        def startMainMenu(self):
                time.sleep(0.5); #Wait for Fake SMTP Server to start...
                while True:
                        option = -1
                        documentClass = -1
                        documentPath = None
                        
                        print "\n-------------------------\nSET Deception Detector:\n-------------------------"
                        if self.isParallel:
                            print "CPU Cores to be in use: %d\n" %self.maxParallelCoreCount
                        print "Press a number associated with the following options."
                        print "1) Classify document\n2) Train program with documents\n3) Exit"
                        
                        while not isinstance(option, (int))\
                                   or (option < 1 or option > 3):
                                try:
                                    option = int(raw_input("Please choose a valid option.\n"))
                                except ValueError:
                                    option = -1
                                
                        if option is 1:     #Classify a document

                                while not isinstance(documentClass, (int))\
                                       or (documentClass not in (0, 1)):
                                        inputMessage = raw_input("Please enter a valid class.\n0 = You consider the document to "+\
                                                                              "be deceptive.\n1 = You consider the document to be non-deceptive.\nPress 'b' or 'back' to exit data entry.\n")
                                        if inputMessage in ('b', 'back'):
                                            documentClass = None
                                            break
                                        
                                        try:
                                                documentClass = int(inputMessage)
                                        except ValueError:
                                                documentClass = None

                                if documentClass is not None:
                                    inputMessage = raw_input("Now enter the filepath of the document to classify.\nPress 'b' or 'back' to exit data entry.\n")
                                    documentPath = normpath(inputMessage)
                                    
                                    while (not isinstance(documentPath, basestring)) or (not isfile(documentPath)):

                                            if inputMessage in ('b', 'back'):
                                                documentPath = None
                                                break

                                            inputMessage = raw_input("Please enter a valid filepath.\nPress 'b' or 'back' to exit data entry.\n")
                                            documentPath = normpath(inputMessage)

                                    if documentPath is not None:
                                        featureSetList = pickle.loads(_extractFromDocument(self.extractorSelector, documentPath, documentClass))
                                        for featureSet in featureSetList:
                                                for each_classification in self.classifyDocument(\
                                                    featureSet.documentCategory, documentClass, featureSet.getVector()):
                                                    print each_classification
                                
                        elif option is 2:   #Train classifiers with data from documents

                                inputMessage = None
                                documentPaths = None
                                paths = None
                                
                                if len(sys.argv) is 1 or\
                                   (len(sys.argv) == 3 and '-p' in sys.argv): #No arguments passed to program
                                                                              # OR Parallel/Sequential processing selection argument
                                        message = "\nNow enter the directory path or filepath of the document(s) "\
                                                  +"to use for training, using the following format:\n[class integer],[directory/file path];\n"\
                                         +"----------------------------\nThe class integer represents the expected classification of the associated document/file:\n"\
                                         +"deceptive = 0, non-deceptive = 1.\n"\
                                         +"\nYou can enter in as many of these lines, as you'd like.\nPress 'b' or 'back' to exit data entry.\n"
                                        
                                        while not isinstance(paths, basestring) or not (isfile(paths) or isdir(paths)):
                                                inputMessage = raw_input(message)

                                                if inputMessage in ('b', 'back'):
                                                    documentPaths = None
                                                    break
                                                
                                                documentPaths = normpath(inputMessage)
                                                try:
                                                        paths = documentPaths.split(',')[1].split(';')[0] #Separate classes and file/directory paths
                                                except IndexError:
                                                        paths = None

                                        if documentPaths is not None: #If file/directory paths exist...
                                            for ch in ('\n', '\t', ' '): #Removes unnecessary characters
                                                if ch in documentPaths:
                                                    documentPaths = documentPaths.replace(ch, '')
                                                            
                                            self.documentPaths = self._getDocumentPaths(documentPaths) #If entering in the document list, on the fly...

                                if inputMessage not in ('b', 'back'): #If not leaving data entry...
                                    detector.extractAllDocuments()      
                                    detector.trainClassifiers()
                                
                        elif option is 3:   #Quit program
                                sys.exit(0)
                
                
if __name__ == "__main__":
        detector = Detector(*sys.argv[1:])      #Initialise program
        detector.startFakeSMTPServerThread()    #Start Fake SMTP Server
        detector.startMainMenu()                #Start rest of program

        
