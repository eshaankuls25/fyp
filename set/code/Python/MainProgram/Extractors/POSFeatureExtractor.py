import sys, os
from BaseExtractor import BaseExtractor as be

class POSFeatureExtractor(be):
        def __init__(self, documentName="currentWebsite", indicators=[], functionArgTuple=None):
                be.__init__(self, documentName, indicators)
                self.setFunctionArgTuple(functionArgTuple)  

def _getTagCountVector(textParserInstance, textString):
        return textParserInstance.getTagCountVector(textString)

        

    
