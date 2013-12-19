from nltk.tag.stanford import POSTagger
import os

class TextParser:
        taggedText = {}
        stanfordTagger = None

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
                print("File: " + self.readFromFile("test.txt") + "\n\n") 
                self.tagTextFile("testDocument", "test.txt")
                print("Tagged Text: ", self.taggedText["testDocument"]) 


        def readFromFile(self, filename):
                self.filepath = os.getcwd() + "/" + filename
                with open(self.filepath, 'r') as f:
                        fileContents = f.read()
                f.close()
                return fileContents

        def tagTextFile(self, documentName, textFilePath):
                self.taggedText[documentName] = self.stanfordTagger.tag(self.readFromFile(textFilePath).split())

        def tagText(self, documentName, textString):
                self.taggedText[documentName] = self.stanfordTagger.tag(textString.split())                

TextParser()