import os, sys
sys.path.append("..")

from Utilities.FeatureSet import FeatureSet
from Utilities.Utils import writeToFile
import DecisionTree

class DTree(object):
    """docstring for DTree"""
    def __init__(self, classList, featureMatrix, filePath=None, documentGroupName=None):
        self.dt = None
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
            
            i = 1
            for label, vector in zip(classList, featureMatrix):
                
                if i == 1:
                    index = '"",'
                    classLabel = "%s%s,"  %(index, '"class_name"')
                    delimitedFeatures = classLabel + ''.join(['"feature_%s",' %feature for feature in vector.keys()])
                    writeToFile(self._decisionTreePath, "%s\n" %delimitedFeatures[:-1], "w")
                
                index = '"%d",' %i
                classLabel = "%s%s,"  %(index, str(label))
                
                delimitedFeatures = classLabel + ''.join(["%f," %feature for feature in vector.values()])
                writeToFile(self._decisionTreePath, "%s\n" %delimitedFeatures[:-1], "a")
                
                i+=1

            self.createDTree()

    def createDTree(self):
        self.dt = DecisionTree.DecisionTree( training_datafile = self._decisionTreePath,
                                csv_class_column_index = 1,
                                csv_columns_for_features = [x for x in range(len(self.featureMatrix[0])+1) if x > 1 ],
                                entropy_threshold = 0.01,
                                max_depth_desired = 8,
                                symbolic_to_numeric_cardinality_threshold = 10,
                              )
        
        self.dt.get_training_data()
        self.dt.calculate_first_order_probabilities()
        self.dt.calculate_class_priors()
    
        self.rootNode = self.dt.construct_decision_tree_classifier()
        self.dt.show_training_data()

    #Some code is from DecisionTree.py's examples
    def classifyDocument(self, featureVector):
        featureList = ['feature_%s = %0.2f' %(k, v) for k, v in featureVector.items()]
        print self.dt._feature_names
        print featureList
        classification = self.dt.classify(self.rootNode, featureList)

        classes = sorted(list( classification.keys() ),\
            key=lambda x: classification[x], reverse=True)

        classResult = ''.join(["\nClassification:\n",\
            "     "  + str.ljust("class name", 30) + "probability",\
            "     ----------                    -----------"])

        for cl in classes:
            if cl is not 'solution_path':
                classResult += ''.join("      %s%s" %(str.ljust(cl, 30),\
                                                      str(classification[cl])))
        return {'solution_path': classification['solution_path'],
                'no_of_nodes': self.rootNode.how_many_nodes(),
                'class_result': classResult} 
