import os, sys, pickle, nltk

def pickleObject(filepath, object):
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

def unpickleObject(filepath, object):
    directory = os.path.dirname(filepath)
    try:
        with open(filepath, "rb") as f:
            return pickle.load(object, f)
    except IOError:
        sys.stderr.write("Could not load object.\n")
        return False

def readFromFile(filename):
    filepath = os.getcwd() + "/" + filename
    try:
        with open(filepath, 'r') as f:
            fileContents = f.read()
            f.close()
        return fileContents
    except IOError:
        sys.stderr.write("Could not read file.\n")
        return None

def writeToFile(filename, data, accessType):
    filepath = os.getcwd() + "/" + filename
    try:
        with open(filepath, accessType) as f:
            f.write(data + "\n")
            f.close()
        return True
    except IOError:
        sys.stderr.write("Could not write file.\n")
        return False

#Source: Stack Overflow - http://stackoverflow.com/questions/5843817/programmatically-install-nltk-corpora-models-i-e-without-the-gui-downloader
def downloadNLTKData(packageList):
    directory = ''
    if sys.platform == 'win32':
        directory = r'C:\nltk_data'
    elif sys.platform.startswith('linux') or sys.platform == 'darwin':
        directory = r'/usr/share/nltk_data'
    else:
        print 'ERROR: Operating System Not Supported'
        sys.exit()

    downloader = nltk.downloader.Downloader(download_dir=directory)
    return downloader.download(packageList)




