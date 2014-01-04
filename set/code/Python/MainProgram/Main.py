import sys, shlex, os, getopt

from Utilities.PreProcessor import PreProcessor
from Utilities.ExtractorSelector import ExtractorSelector
from Extractors.TextFeatureExtractor import TextFeatureExtractor
from Utilities.Utils import readFromFile
from Utilities.Utils import startProcess

def main():

        extractorSelector = None

        ###Defaults###
        documentFilePath = 'test.txt'
        documentCategory = 'text'
        categoryFileExists = False
        indicatorFileExists = False
        
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
                        indicatorList = shlex.split(readFromFile(arg))
                        indicatorFileExists = True

        ###Determining Parser and Config###

        if categoryFileExists:
                extractorSelector = ExtractorSelector(*categoryList)
        else:
                extractorSelector = ExtractorSelector('html', 'text')

        if indicatorFileExists:
                #From file
                extractorSelector.addExtractorIdentifierSet(documentCategory, indicatorList)
                #Otherwise, defaults to an empty set
                

        #Default text
        documentText = readFromFile(documentFilePath)+'\x001\x034'
        print documentText

        #Processed text
        processedText = PreProcessor().removeEscapeChars(documentText)
        print processedText

        selectedExtractorTuple = extractorSelector.determineBestExtractor(processedText.split(' '))

        if selectedExtractorTuple[0] is None:
                #Start parsing using the 'TextFeatureExtractor' Class
                selectedExtractor = TextFeatureExtractor()
        else:
                #Use the returned parser object
                selectedExtractor = selectedExtractorTuple[1]

        ###Extracting###

        featureSet = selectedExtractor.getFeatureSet(processedText, documentFilePath, documentCategory)
        print featureSet.documentName, ":  ", featureSet.documentCategory, "\n\n", featureSet.vector

        if sys.platform == 'win32':
                startProcess("python ./Utilities/listen.py -p 333")
        else:
		startProcess("sudo chmod +x ./Utilities/listen.py")
                startProcess("sudo ./Utilities/listen.py -p 333")
if __name__ == "__main__":
        main()
