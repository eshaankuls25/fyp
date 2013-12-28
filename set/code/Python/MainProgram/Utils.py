import os, sys, pickle

class Utils:

    def pickleObject(self, filepath, object):
        directory = os.path.dirname(filepath)

        try:
            os.stat(directory)
        except:
            os.mkdir(directory)   

        try:
            with open(filepath, "wb") as f:
                pickle.dump(object, f)
        except IOError:
            sys.stderr.write("Could not pickle object.\n")
            return False

    def unpickleObject(self, filepath, object):
        directory = os.path.dirname(filepath)
        try:
            with open(filepath, "rb") as f:
                return pickle.load(object, f)
        except IOError:
            sys.stderr.write("Could not load object.\n")
            return False

    def readFromFile(self, filename):
        self.filepath = os.getcwd() + "/" + filename
        try:
            with open(self.filepath, 'r') as f:
                fileContents = f.read()
                f.close()
            return fileContents
        except IOError:
            sys.stderr.write("Could not read file.\n")
            return False

    def writeToFile(self, filename, data, accessType):
        self.filepath = os.getcwd() + "/" + filename
        try:
            with open(self.filepath, accessType) as f:
                f.write(data + "\n")
                f.close()
            return True
        except IOError:
            sys.stderr.write("Could not write file.\n")
            return False
