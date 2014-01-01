from nltk.tag.stanford import POSTagger
from nltk.internals import config_java
import os
from Utils import readFromFile

class TextParser:
        taggedText = {}
        tagCriteria = ('DT', 'EX', 'JJ', 'MD', 'NN',
                       'POS', 'PRP', 'RB', 'VB', 'VBD',
                       'VBG', '#', '$', "'", ',')
        stanfordTagger = None
        #config_java("C:\Program Files\Java\jdk1.6.0_37\\bin\java.exe")
        
        def __init__(self):

                taggerLibraryPath = os.getcwd() + "/sp/jar/" + "stanford-postagger.jar"
                taggerModelPath = os.getcwd() + "/sp/models/" + "english-bidirectional-distsim.tagger"

                self.stanfordTagger = POSTagger(taggerModelPath,
                        taggerLibraryPath)

                print "---"
                print "Tagger library path: " + taggerLibraryPath
                print "Tagger model path: " + taggerModelPath
                print "---" 
                
                #print self.stanfordTagger.tag('What is the airspeed of an unladen swallow ?'.split()) 
                
                #print("File: " + readFromFile("test.txt") + "\n\n") 
                #self.tagTextFile("testDocument", "test.txt")
                #print("Tagged Text: ", self.taggedText["testDocument"]) 

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
