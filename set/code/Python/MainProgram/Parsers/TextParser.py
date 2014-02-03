from nltk.tag.stanford import POSTagger
from nltk.internals import config_java
from email.parser import Parser
import os, sys
sys.path.append("..")

from Utilities.Utils import readFromFile

class TextParser:
        taggedText = {}
        tagCriteria = ('DT', 'EX', 'JJ', 'MD', 'NN',
                       'POS', 'PRP', 'RB', 'VB', 'VBD',
                       'VBG', '#', '$', "'", ',')
        stanfordTagger = None
        #config_java("C:\Program Files\Java\jdk1.6.0_37\\bin\java.exe") 

        def __init__(self, pathToParser=None, javaHeapOptions='-Xmx2g'):

                if pathToParser is None:
                        taggerLibraryPath = os.getcwd() + "/sp/jar/" + "stanford-postagger.jar"
                        taggerModelPath = os.getcwd() + "/sp/models/" + "english-bidirectional-distsim.tagger"
                else:
                        taggerLibraryPath = pathToParser + "/sp/jar/" + "stanford-postagger.jar"
                        taggerModelPath = pathToParser + "/sp/models/" + "english-bidirectional-distsim.tagger"

                self.stanfordTagger = POSTagger(taggerModelPath,
                        taggerLibraryPath, java_options=javaHeapOptions)

                print "---"
                print "Tagger library path: " + taggerLibraryPath
                print "Tagger model path: " + taggerModelPath
                print "---" 

        def tagTextFile(self, documentName, textFilePath):
                tempTaggedText = self.stanfordTagger.tag(readFromFile(textFilePath).split())
                finalList = []
                
                for x, y in tempTaggedText:
                        if y in self.tagCriteria:
                                finalList.append((x, y))
                                

                self.taggedText[documentName] = finalList

        def tagText(self, documentName, textString):
                tempTaggedText = self.stanfordTagger.tag(textString.split())
                finalList = []
                
                for x, y in tempTaggedText:
                        if y in self.tagCriteria:
                                finalList.append((x, y))
                                

                self.taggedText[documentName] = finalList

        def getEmailFromString(self, emailString):
                message = Parser().parsestr(emailString)
                return (message, message.is_multipart())

	
