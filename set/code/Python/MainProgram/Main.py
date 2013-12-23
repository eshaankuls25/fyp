from PreProcessor import PreProcessor
from ParserSelector import ParserSelector
from TextParser import TextParser
from FeatureSet import FeatureSet

import sys, shlex, os, getopt

def main():

        parserSelector = None
        textParser = TextParser()

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
                        categoryList = shlex.split(textParser.readFromFile(arg))
                        categoryFileExists = True
                elif opt in ('-y', '--indicatorsfilepath'):
                        indicatorList = shlex.split(textParser.readFromFile(arg))
                        indicatorFileExists = True

        ###Determining Parser and Config###

        if categoryFileExists:
                parserSelector = ParserSelector(*categoryList)
        else:
                parserSelector = ParserSelector('html', 'text')

        if indicatorFileExists:
                #From file
                parserSelector.addParserIdentifierSet(documentCategory, indicatorList)
                #Otherwise, defaults to an empty set
                

        #Default text
        documentText = textParser.readFromFile(documentFilePath)+'\x001\x034'
        print documentText

        #Processed text
        processedText = PreProcessor().removeEscapeChars(documentText)
        print processedText

        selectedParserTuple = parserSelector.determineBestParser(processedText.split(' '))

        if selectedParserTuple[0] is None:
                #Start parsing using the 'TextParser' Class
                selectedParser = textParser
        else:
                #Use the returned parser object
                selectedParser = selectedParserTuple[1]

        ###Parsing###

        if isinstance(selectedParser, TextParser):
                selectedParser.tagText(documentFilePath.split('/')[-1], processedText)
                print selectedParser.taggedText[documentFilePath.split('/')[-1]]

if __name__ == "__main__":
        main()
