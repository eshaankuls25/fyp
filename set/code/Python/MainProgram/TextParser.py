from nltk.tag.stanford import POSTagger
import os

class TextParser:
        taggedText = {}
        tagCriteria = ('DT', 'EX', 'JJ', 'MD', 'NN',
                       'POS', 'PRP', 'RB', 'VB', 'VBD',
                       'VBG', '#', '$', "'", ',')
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
                
                #print("File: " + self.readFromFile("test.txt") + "\n\n") 
                #self.tagTextFile("testDocument", "test.txt")
                #print("Tagged Text: ", self.taggedText["testDocument"]) 


        def readFromFile(self, filename):
                self.filepath = os.getcwd() + "/" + filename
                with open(self.filepath, 'r') as f:
                        fileContents = f.read()
                f.close()
                return fileContents

        def writeToFile(self, filename, data, accessType):
                self.filepath = os.getcwd() + "/" + filename
                with open(self.filepath, accessType) as f:
                        f.write(data + "\n")

        def tagTextFile(self, documentName, textFilePath):
                tempTaggedText = self.stanfordTagger.tag(self.readFromFile(textFilePath).split())
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
