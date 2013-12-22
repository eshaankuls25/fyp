import PreProcessor
import ParserSelector
import TextParser
import FeatureSet

import sys
import getopt

def main():

	#Allow user to pass document types, document name/file,
	#and parser identifier set(s) in as parameters.

	options, extras = getopt.getopt(sys.argv[1:], 'd:t:', ['docname=',
															'type='])
	
	for opt, arg in options:
    if opt in ('-d', '--docname'):
        documentName = arg
    elif opt in ('-t', '--type'):
        documentType = arg

	preprocessor = PreProcessor()
	ps = ParserSelector('fake', 'list', 'of', 'document', 'categories', 'example:', 'html', 'text')
	textParser = TextParser()


if __name__ == "__main__":
    main()