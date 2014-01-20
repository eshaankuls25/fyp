import os, sys
sys.path.append("..")

from Utilities.FeatureSet import FeatureSet
from Utilities.Utils import writeToFile
import DecisionTree

class DTree(object):
    """docstring for DTree"""
    def __init__(self, classList, featureMatrix, filePath=None, documentGroupName=None):
        self.rootNode = None
        self._decisionTreePath = None
        self.classes = classList
        self.featureMatrix = featureMatrix
              
        _filePathSuffix = "/Classifiers/DecisionTree/training_data.csv"
        if documentGroupName is not None:
             _filePathSuffix = "/Classifiers/DecisionTree/training_data_%s.csv" %documentGroupName

        if filePath is not None:
            self._decisionTreePath = filePath
        else:    
            self._decisionTreePath = os.getcwd() + _filePathSuffix

            writeToFile(self._decisionTreePath, '', "w")
            i = 0
            for label, vector in zip(classList, featureMatrix):

                if i == 0:
                    index = '"",'
                    classLabel = "%s%s,"  %(index, '"class_name"')
                    delimitedFeatures = classLabel + ''.join(['"%s",' %label for label in vector.keys()])
                else:
                    index = '"%d",' %i
                    classLabel = "%s%s,"  %(index, str(label))
                    delimitedFeatures = classLabel + ''.join(["%f," %feature for feature in vector.values()])

                writeToFile(self._decisionTreePath, "%s\n" %delimitedFeatures[:-1], "a")
                i+=1

            self.createDTree()

    def createDTree(self):
        dt = DecisionTree.DecisionTree( training_datafile = self._decisionTreePath,
                                csv_class_column_index = 1,
                                csv_columns_for_features = [x for x in range(len(self.classes))],
                                entropy_threshold = 0.01,
                                max_depth_desired = 8,
                                symbolic_to_numeric_cardinality_threshold = 10,
                              )
        
        dt.get_training_data()
        dt.calculate_first_order_probabilities()
        dt.calculate_class_priors()
    
        self.rootNode = dt.construct_decision_tree_classifier()

    #Some code is from DecisionTree.py's examples
    def classifyDocument(self, featureVector):
        featureString = ''.join(["%s = %f" %(k, v) for k, v in featureVector.items()])
        classification = dt.classify(self.rootNode, featureString)

        classes = sorted(list( classification.keys() ),\
            key=lambda x: classification[x], reverse=True)

        classResult = ''.join(["\nClassification:\n",\
            "     "  + str.ljust("class name", 30) + "probability",\
            "     ----------                    -----------"])

        for which_class in which_classes:
            if which_class is not 'solution_path':
                classResult += ''.join("     ",\
                    str.ljust(which_class, 30), \
                    str(classification[which_class]))

        return {'solution_path': classification['solution_path'],
                'no_of_nodes': self.rootNode.how_many_nodes(),
                'class_result': classResult} 
