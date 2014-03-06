import sys, os
from BaseExtractor import BaseExtractor as be

class POSFeatureExtractor(be):
        def __init__(self, documentName="currentWebsite", indicators=[]):
                be.__init__(self, documentName, indicators)
                pass

    
