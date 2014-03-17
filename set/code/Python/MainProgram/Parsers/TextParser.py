import os, sys
from nltk.tag.stanford          import POSTagger
from nltk.internals             import config_java
from nltk.util                  import ngrams
from email.parser               import Parser
from os.path                    import normpath
from collections                import Counter, OrderedDict

sys.path.append("..")
from    Utilities.Utils         import readFromFile
import  Utilities.PreProcessor  as PreProcessor


class TextParser:
        taggedText = Counter()
        tagList = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR',
                   'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS',
                   'PDT', 'POS', 'PRP', 'RB', 'RBR', 'RBS', 'RP',
                   'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN',
                   'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB'] #Penn treebank tags
        
        tagCriteria = ('DT', 'EX', 'JJ', 'MD', 'NN',
                       'POS', 'PRP', 'RB', 'VB', 'VBD',
                       'VBG', '#', '$', "'", ',')
        stanfordTagger = None
        #config_java("C:\Program Files\Java\jdk1.6.0_37\\bin\java.exe") 

        def __init__(self, pathToParser=None, javaHeapOptions='-Xmx4g -XX:+UseParallelGC -XX:-UseGCOverheadLimit'):

                if pathToParser is None:
                        taggerLibraryPath = normpath(os.path.join(os.getcwd(), "sp/jar/stanford-postagger.jar"))
                        taggerModelPath = normpath(os.path.join(os.getcwd(), "sp/models/english-bidirectional-distsim.tagger"))
                else:
                        taggerLibraryPath = normpath(os.path.join(pathToParser, "sp/jar/stanford-postagger.jar"))
                        taggerModelPath = normpath(os.path.join(pathToParser, "sp/models/english-bidirectional-distsim.tagger"))

                self.stanfordTagger = POSTagger(taggerModelPath,
                        taggerLibraryPath, java_options=javaHeapOptions)

                """
                print "---"
                print "Tagger library path: " + taggerLibraryPath
                print "Tagger model path: " + taggerModelPath
                print "---"
                """

        def tagTextFile(self, documentName, textFilePath, useCriteria=False):
                tempTaggedText, finalList = [], []
                textFile = readFromFile(textFilePath)
                
                for line in textFile.splitlines():
                        tempTaggedText.extend(self.stanfordTagger.tag(line.split()))

                if useCriteria:
                        for x, y in tempTaggedText:
                                if y in self.tagCriteria:
                                        finalList.append((x, y))
                else:
                        for x, y in tempTaggedText:
                                finalList.append((x, y))
                                

                self.taggedText[documentName] = finalList

        def getTagCountVector(self, textString):
                splitString = textString.split()
                numberOfWords = len(splitString)
                tempTaggedText = self.stanfordTagger.tag(splitString)
                counterVector = Counter([y for x, y in tempTaggedText if y in self.tagList]) #Get tags

                resultantVector = OrderedDict()

                for k in self.tagList:
                        if k in counterVector:
                                resultantVector[k] = float(counterVector[k])/numberOfWords
                        else:
                                resultantVector[k] = 0

                return resultantVector
                

        def tagText(self, documentName, textString, useCriteria=False):
                tempTaggedText, finalList = [], []
                
                for line in textString.splitlines():
                        tempTaggedText.extend(self.stanfordTagger.tag(line.split()))
                
                if useCriteria:
                        for x, y in tempTaggedText:
                                if y in self.tagCriteria:
                                        finalList.append((x, y))
                else:
                        for x, y in tempTaggedText:
                                finalList.append((x, y))                

                self.taggedText[documentName] = finalList

        def getEmailFromString(self, emailString):
                message = Parser().parsestr(emailString)
                return (message, message.is_multipart())

        def ngram(self, textString, n=3): #Defaults to tri-gram
                return ngrams(textString.split(), n)



	
