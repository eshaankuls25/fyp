class HTML_FeatureParser:
	featureDictionary = {}
	
	#def parseGraph(self, ):


	def __init__(self, featureSet):
		self.featureDictionary = {feature:0 for feature in featureSet}

	def 