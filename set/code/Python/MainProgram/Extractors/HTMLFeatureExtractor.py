from collections import *
import re, sys
sys.path.append("..")

from Utilities.Utils import downloadNLTKData
from BaseExtractor import BaseExtractor

#Use scrapy code here - items, spiders etc.
class HTMLFeatureExtractor(BaseExtractor):

        def __init__(self):
        	BaseExtractor.__init__(self)
        	pass 

