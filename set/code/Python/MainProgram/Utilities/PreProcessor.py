class PreProcessor:

	#def __init__(self):

	def removeEscapeChars(self, string):
		return string.encode('string_escape').decode('string_escape') #Python 2
		#return string.encode('encode_escape').decode("unicode_escape") #Python3

	def getASCIIChars(self, string):
                return unicode(string, 'ascii', 'ignore')
 
