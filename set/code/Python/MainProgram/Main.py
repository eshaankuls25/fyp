import sys, shlex, os, getopt

import Utilities.Utils
import Utilities.PreProcessor
import Utilities.ParserSelector
import Utilities.FeatureSet

import Parsers.TextParser

from Utils import readFromFile

def main():

        parserSelector = None

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
                parserSelector = ParserSelector(*categoryList)
        else:
                parserSelector = ParserSelector('html', 'text')

        if indicatorFileExists:
                #From file
                parserSelector.addParserIdentifierSet(documentCategory, indicatorList)
                #Otherwise, defaults to an empty set
                

        #Default text
        documentText = readFromFile(documentFilePath)+'\x001\x034'
        print documentText

        #Processed text
        processedText = PreProcessor().removeEscapeChars(documentText)
        print processedText

        selectedParserTuple = parserSelector.determineBestParser(processedText.split(' '))

        if selectedParserTuple[0] is None:
                #Start parsing using the 'TextParser' Class
                selectedParser = TextParser()
        else:
                #Use the returned parser object
                selectedParser = selectedParserTuple[1]

        ###Parsing###

        if isinstance(selectedParser, TextParser):
                selectedParser.tagText(documentFilePath.split('/')[-1], processedText)
                print selectedParser.taggedText[documentFilePath.split('/')[-1]]

if __name__ == "__main__":
        main()
