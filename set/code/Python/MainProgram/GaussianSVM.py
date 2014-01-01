import os
sys.path.append(os.getcwd()+'/libsvm/python')

from svmutil import *

class GaussianSVM(object):
	"""docstring for GaussianSVM"""
	param_C = None

	def __init__(self, featureVector):
		super(GaussianSVM, self).__init__()

		