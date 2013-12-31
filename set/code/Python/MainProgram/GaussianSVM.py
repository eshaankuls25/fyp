import os
sys.path.append(os.getcwd()+'/libsvm/python')

class GaussianSVM(object):
	"""docstring for GaussianSVM"""
	param_C = None

	def __init__(self):
		super(GaussianSVM, self).__init__()
		