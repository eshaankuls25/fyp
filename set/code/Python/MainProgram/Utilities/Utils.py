import os, sys, pickle, nltk, shlex

from subprocess import Popen, PIPE
from threading import Thread
from Queue import Queue, Empty

io_q = Queue()

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

#'startProcess' method uses Threaded printing of stdout and stderr, frome here:
#http://sharats.me/the-ever-useful-and-neat-subprocess-module.html#popen-class

def stream_watcher(identifier, stream):
    global io_q
    
    for line in stream:
        io_q.put((identifier, line))

    if not stream.closed:
        stream.close()

def startProcess(programNameAndArgsString):

    if not isinstance(programNameAndArgsString, basestring) or \
        programNameAndArgsString is None:
        raise TypeError("ERROR: The parameter must be a string.")


    argsList = programNameAndArgsString.split(" ")

    process = Popen(argsList, shell=False, stdout=PIPE, stderr=PIPE)

    #Start stdout and stderr reading threads

    Thread(target=stream_watcher, name='stdout-watcher',
        args=('STDOUT', process.stdout)).start()

    Thread(target=stream_watcher, name='stderr-watcher',
        args=('STDERR', process.stderr)).start()

    _threadStreamPrinter(process)

def _threadPrinter(process, blockingTimeout):
    global io_q
    
    while True:
        try:
            # Block for 1 second.
            item = io_q.get(True, 1)
        except Empty:
            # No output in either streams for a second. Are we done?
            if process.poll() is not None:
                break
        else:
            identifier, line = item
            print identifier + ':', line

def _threadStreamPrinter(process, blockingTimeout=1):
    Thread(target=_threadPrinter, name='printer', args=(process, blockingTimeout)).start()




    
