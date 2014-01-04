import sys, shlex, os, getopt

from Extractors.TextFeatureExtractor import TextFeatureExtractor
from Extractors.HTMLFeatureExtractor import HTMLFeatureExtractor

from Utilities.PreProcessor import PreProcessor
from Utilities.ExtractorSelector import ExtractorSelector
from Utilities.Utils import readFromFile
from Utilities.Utils import startProcess
from Utilities.Utils import listFilesInDirWithExtension
from Parsers.TextParser import TextParser

def main():

        extractorSelector = None

        ###Defaults###
        documentFilePath = 'test_email'
        documentCategory = 'text'

        categoryList = ['html', 'text']
        extractorList = [TextFeatureExtractor(), HTMLFeatureExtractor()]
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
                emailList.append(parser.getEmailFromString(emailString));
                i = 0
                
                for email, isMultipart in emailList:
                        payload = email.get_payload()
                        
                        print "Email no: "+str(i)+": "

                        print "---"
                        for header in email.keys():
                                print "\n"+header+": "+email.get(header)
                        print "\nPayload: "+email.get_payload()
                        print "---"
                        
                        processedEmail = PreProcessor().removeEscapeChars(emailString)
                        processedPayload = PreProcessor().removeEscapeChars(payload)
                        selectedExtractorTuple = extractorSelector.determineBestExtractor(processedEmail.split(' '))

                        if selectedExtractorTuple[0] is None:
                                #Start parsing using the 'TextFeatureExtractor' Class
                                selectedExtractor = TextFeatureExtractor()
                                featureSet = selectedExtractor.getFeatureSet(email.get("Message-Id"), documentCategory, processedPayload)
                        else:
                                #Use the returned parser object
                                selectedExtractor = selectedExtractorTuple[1]
                                featureSet = selectedExtractor.getFeatureSet(email.get("Message-Id"), selectedExtractorTuple[0], processedPayload)
                                
                        featureMatrix.append(featureSet.vector)
                        i+=1

        for vector in featureMatrix:
                print vector

        if sys.platform == 'win32':
                startProcess("python ./Utilities/listen.py")
        else:
                startProcess("sudo chmod +x ./Utilities/listen.py")
                startProcess("./Utilities/listen.py")
if __name__ == "__main__":
        main()
