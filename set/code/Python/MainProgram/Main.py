import sys, shlex, os, getopt

from Extractors.ObfuscationFeatureExtractor import ObfuscationFeatureExtractor
from Extractors.ImitationFeatureExtractor import ImitationFeatureExtractor
from Extractors.HTMLFeatureExtractor import HTMLFeatureExtractor

from Utilities.PreProcessor import PreProcessor
from Utilities.ExtractorSelector import ExtractorSelector
from Utilities.Utils import readFromFile
from Utilities.Utils import startProcess
from Utilities.Utils import listFilesInDirWithExtension
from Utilities.listen import startFakeSMTPServer
from Parsers.TextParser import TextParser

def main():

        extractorSelector = None

        ###Defaults###
        documentFilePath = 'test_email'
        documentCategory = 'text'

        categoryList = ['text', 'html']
        extractorList = [(ImitationFeatureExtractor(), ObfuscationFeatureExtractor()), HTMLFeatureExtractor()]
        indicatorDictionary = {'text':['From:', 'Date:', 'Message-ID', 'In-Reply-To:'],\
                              'html':['http://', 'www', '.com', '.co.uk']}

        featureMatrix = []
        
        ###User arguments###

        options, extras = getopt.getopt(sys.argv[1:], 'd:c:e:i:', ['docpath=', 'category=' 'categoriesfilepath=', 'indicatorsfilepath='])
                
        for opt, arg in options:
                if opt in ('-d', '--docpath'):
                        documentFilePath = arg.replace("\\", "/")
                elif opt in ('-c', '--category'):
                        documentCategory = arg
                elif opt in ('-x', '--categoriesfilepath'):
                        categoryList = shlex.split(readFromFile(arg))
                        categoryFileExists = True
                elif opt in ('-y', '--indicatorsfilepath'):
                        #Must change to allow file to contain
                        #multiple document names, which map to multiple indicators
                        #use 'indicatorDictionary' - maps docname to text features
                        indicatorList = shlex.split(readFromFile(arg))
                        indicatorFileExists = True

        extractorSelector = ExtractorSelector(categoryList, extractorList)

        for category in categoryList:
                extractorSelector.addExtractorIdentifierSet(category, indicatorDictionary[category])                   

        ###Extracting###

        ###Email Test###

        emailList = []

        parser = TextParser(os.getcwd()+"/Parsers")
        filepathPrefix = "./Emails/"
        
        for filepath in listFilesInDirWithExtension(filepathPrefix, ".eml"):
                emailString = readFromFile(filepathPrefix+filepath)
                emailList.append(parser.getEmailFromString(emailString))
                i=0
                
                for email, isMultipart in emailList:
                        payload = email.get_payload()
                        
                        print "Email no. "+str(i)+": "

                        print "---"
                        for header in email.keys():
                                print "\n"+header+": "+email.get(header)
                        print "\nPayload: "+email.get_payload()
                        print "---"

                        preProcessor = PreProcessor()
                        
                        processedEmail = preProcessor.removeEscapeChars(emailString)
                        processedPayload = preProcessor.removeEscapeChars(payload)
                        
                        selectedExtractorTuple = extractorSelector.\
                                                 determineBestExtractor(processedEmail.split())

                        if selectedExtractorTuple[0] is None:
                                documentName = "DEFAULT - TEXT "+str(i)
                                documentCategory = "DEFAULT - TEXT"
                        elif selectedExtractorTuple[0] is 'text':
                                documentName = email.get("Message-Id")
                                documentCategory = "text"
                        elif selectedExtractorTuple[0] is 'html':
                                documentName = "DEFAULT - HTML "+str(i)
                                documentCategory = "html"


                        #Start parsing using the chosen extractor(s)
                        extractorTuple = selectedExtractorTuple[1]
                        print selectedExtractorTuple[0], "---", extractorTuple

                        
                        for extNum in range(len(extractorTuple)):
                                featureSet = extractorTuple[extNum].getFeatureSet(\
                                        documentName+": "+str(extNum), documentCategory, processedPayload)
                                featureMatrix.append(featureSet)
                                print featureSet
                        i+=1
                        
        print "---"
        for featureSet in featureMatrix:
                print featureSet.documentName
                print featureSet.vector
                print "---"

        startFakeSMTPServer()

        """
        if sys.platform == 'win32':
                #startProcess("python ./Utilities/listen.py")
        else:
                #startProcess("sudo chmod +x ./Utilities/listen.py")
                #startProcess("./Utilities/listen.py")
        """
        
if __name__ == "__main__":
        main()
