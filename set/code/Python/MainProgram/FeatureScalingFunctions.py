#Scaling functions

def numberOfCommas(textString):
	if isInstance(textString, String) and textString not None:
		num = 0
		return len(textString.split(','))
	else
		return -1