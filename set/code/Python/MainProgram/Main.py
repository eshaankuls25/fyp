import PreProcessor
import ParserSelector
import TextParser
import FeatureSet

def main():

	#Allow user to pass document types, document name/file,
	#and parser identifier set(s) in as parameters.

	#documentTypes = None
	documentTypes = initialiseDocumentTypes(['fake', 'list', 'of', 'document', 'types', 'example:', 'html', 'text'])



	preprocessor = PreProcessor()
	ps = ParserSelector()
	textParser = TextParser()

def initialiseDocumentTypes(*sequential, **named):	#From StackOverflow - http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    	return dict(zip(sequential, range(len(sequential))), **named)


if __name__ == "__main__":
    main()