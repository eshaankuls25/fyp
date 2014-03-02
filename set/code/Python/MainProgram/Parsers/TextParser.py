import os, sys
from nltk.tag.stanford  import POSTagger
from nltk.internals     import config_java
from nltk.util          import ngrams
from email.parser       import Parser
from os.path            import normpath
sys.path.append("..")

from Utilities.Utils            import readFromFile
from Parsers.Stemming.lovins    import stem as lovins_stem
from nltk.stem.porter           import PorterStemmer
from nltk.stem.lancaster        import LancasterStemmer
from nltk.stem.snowball         import EnglishStemmer
from nltk.stem                  import WordNetLemmatizer


class TextParser:
        taggedText = {}
        _wnl = WordNetLemmatizer()
        _porter = PorterStemmer()
        _snowball = EnglishStemmer()
        _lancs = LancasterStemmer()
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

        def stem(self, textString, stemmerType="porter"): #Defaults to Porter stemmer
                if not (isinstance(stemmerType, basestring)\
                        and isinstance(textString, basestring)):
                        raise TypeError("Both 'textString' and 'stemmerType' must be strings.")
                
                if stemmerType == "lovins":
                        return lovins_stem(textString)
                elif stemmerType == "lancaster":
                        return _lancs.stem(textString)
                elif stemmerType == "porter":
                        return _porter.stem(textString)
                elif stemmerType == "snowball":
                        return _snowball.stem(textString)

        def lemmatise(self, textString):
                self._wnl.lemmatize(textString)



	
