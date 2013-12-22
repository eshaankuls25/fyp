from PreProcessor import PreProcessor
from ParserSelector import ParserSelector
from TextParser import TextParser
from FeatureSet import FeatureSet

import sys
import os
import getopt

def main():

        parserSelector = None
        textParser = TextParser()

        ###Defaults###
        documentFilePath = 'test.txt'
        documentType = 'text'
        categoryFileExists = False
        
        #Allow user to pass document types, document name/file,
        #and parser identifier set(s) in as parameters.

        options, extras = getopt.getopt(sys.argv[1:], 'd:t:c:', ['docpath=', 'type=', 'categoryfilepath='])
                
        for opt, arg in options:
                if opt in ('-d', '--docpath'):
                        documentFilePath = arg
                elif opt in ('-t', '--type'):
                        documentType = arg
                elif opt in ('-c', '--categoryfilepath'):
                        categoryList = shlex.split(textParser.readFromFile(arg))
                        categoryFileExists = True

        if categoryFileExists:
                parserSelector = ParserSelector(*categoryList)
        else:
                parserSelector = ParserSelector('html', 'text')

        #Default text
        documentText = textParser.readFromFile(documentFilePath)
        print documentText

        #Processed text
        documentText = PreProcessor().removeEscapeChars(documentText+'\x01')
        print documentText
        

if __name__ == "__main__":
        main()
