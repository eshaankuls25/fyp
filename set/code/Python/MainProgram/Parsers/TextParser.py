import os, sys
from nltk.tag.stanford  import POSTagger
from nltk.internals     import config_java
from nltk.util          import ngrams
from email.parser       import Parser
from os.path            import normpath

sys.path.append("..")
from Utilities.Utils    import readFromFile
import  Utilities.PreProcessor as PreProcessor


class TextParser:
        taggedText = {}
        tagCriteria = ('DT', 'EX', 'JJ', 'MD', 'NN',
                       'POS', 'PRP', 'RB', 'VB', 'VBD',
                       'VBG', '#', '$', "'", ',')
        stanfordTagger = None
        #config_java("C:\Program Files\Java\jdk1.6.0_37\\bin\java.exe") 

        def __init__(self, pathToParser=None, javaHeapOptions='-Xmx4g -XX:-UseGCOverheadLimit'):

                if pathToParser is None:
                        taggerLibraryPath = normpath(os.path.join(os.getcwd(), "sp/jar/stanford-postagger.jar"))
                        taggerModelPath = normpath(os.path.join(os.getcwd(), "sp/models/english-bidirectional-distsim.tagger"))
                else:
                        taggerLibraryPath = normpath(os.path.join(pathToParser, "sp/jar/stanford-postagger.jar"))
                        taggerModelPath = normpath(os.path.join(pathToParser, "sp/models/english-bidirectional-distsim.tagger"))

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

        def ngram(self, textString, n=3): #Defaults to tri-gram
                return ngrams(textString.split(), n)



	
