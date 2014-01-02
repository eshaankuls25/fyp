import os, sys
sys.path.append("..")

from Utilities.FeatureSet import FeatureSet
sys.path.append(os.getcwd()+'/libsvm/python')

from svmutil import *

class GaussianSVM(object):
	"""docstring for GaussianSVM"""
	param_C = 5
	svmModel = None
	labels = None
	featureMatrix = None

	#featureMatrix is a list of featureSet vectors:
	##e.g. [featureSet1.vector, featureSet2.vector, fe5.vector ...]

	def __init__(self, labelList, featureMatrix):
		super(GaussianSVM, self).__init__()
		self.labels = labelList
		self.featureMatrix = featureMatrix

		svmProb = svm_problem(self.labels, self.featureMatrix)

		#t = 2 model type Gaussian/RBF
		#s = 0 C-SVC multi-class classifier
		#c = cost parameter of C-SVC
		params 	= svm_parameter('-s 0 -t 2 -c '+str(param_C)+' -b 1')
		self.svmModel = svm_train(svmProb, params)

		self.saveModel('gaussianSVM_model.bak', svmModel)

	def __init__(self, labelList, featureMatrix, costParam):
		super(GaussianSVM, self).__init__()
		self.param_C = costParam
		self.labels = labelList
		self.featureMatrix = featureMatrix

		svmProb = svm_problem(self.labels, self.featureMatrix)

		#t = 2 model type Gaussian/RBF
		#s = 0 C-SVC multi-class classifier
		#c = cost parameter of C-SVC
		params 	= svm_parameter('-s 0 -t 2 -c '+str(self.param_C)+' -b 1')
		self.svmModel = svm_train(svmProb, params)

		self.saveModel('gaussianSVM_model.bak', svmModel)

	def saveModel(filename, model):
		try:
			svm_save_model(filename, model)
		except Exception, e:
			raise e

	def loadModel(filename):
		try:
			svm_load_model(filename)
		except Exception, e:
			raise e

	def classifyDocument(featureSet, newFeatureMatrix):
		if isinstance(featureSet, FeatureSet):
			p_labels, p_acc, p_vals = svm_predict(self.labels, [featureSet.vector], self.svmModel)
			#Do stuff with variables
			return True
		else:
			return False

		
