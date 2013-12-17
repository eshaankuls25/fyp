class PreProcessor:

	#def __init__(self):

	def removeEscapeChars(self, string):
		return string.decode('string_escape') #Python 2
		#return bytes(string, "utf-8").decode("unicode_escape") #Python3

	