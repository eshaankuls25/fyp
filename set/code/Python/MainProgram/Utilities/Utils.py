import os, sys, pickle, nltk, shlex, glob

from subprocess import Popen, PIPE
from threading import Thread

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  #Python 3.x

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

def addToNLTKPath(directoryPath):
  if not isinstance(directoryPath, basestring) or \
        directoryPath is None:
        raise TypeError("ERROR: The parameter must be a string.")
  nltk.data.path.append(directoryPath)

#Source: Stack Overflow - http://stackoverflow.com/questions/5843817/programmatically-install-nltk-corpora-models-i-e-without-the-gui-downloader
def downloadNLTKData(packageList):

    isDirectoryInPath = None
    directory = ''

    if sys.platform == 'win32':
        directory = r'C:\nltk_data'
    elif sys.platform.startswith('linux') or sys.platform == 'darwin':
        directory = os.path.expanduser('~')+r'/nltk_data'
    else:
        print 'ERROR: Operating System Not Supported'
        sys.exit()

    isDirectoryInPath = any((directory in item) for item in nltk.data.path)
    if not isDirectoryInPath: nltk.data.path.append(directory)

    downloader = nltk.downloader.Downloader(download_dir=directory)
    return downloader.download(packageList)

#'startProcess' method uses Threaded printing of stdout and stderr, frome here:
#http://sharats.me/the-ever-useful-and-neat-subprocess-module.html#popen-class
# And here:
#http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
def stream_watcher(identifier, stream):
    global io_q
    
    for line in stream:
        io_q.put((identifier, line))

    if not stream.closed:
        stream.close()

def startProcess(programNameAndArgsString):

    argsList = None 

    if not isinstance(programNameAndArgsString, basestring) or \
        programNameAndArgsString is None:
        raise TypeError("ERROR: The parameter must be a string.")

    if " " in programNameAndArgsString:
        if sys.platform == 'win32':
            argsList = _cmdline2list(programNameAndArgsString)
        elif sys.platform.startswith('linux') or sys.platform == 'darwin':
            argsList = shlex.split(programNameAndArgsString)
            argsList[1] = os.path.normpath(argsList[1])
        else:
            print 'ERROR: Operating System Not Supported'
            sys.exit()  
    else:
        argsList = [programNameAndArgsString]

    ON_POSIX = 'posix' in sys.builtin_module_names
    
    process = Popen(argsList, shell=False, stdout=PIPE, stderr=PIPE, close_fds=ON_POSIX)

    #Start stdout and stderr reading threads

    t1 = Thread(target=stream_watcher, name='stdout-watcher',
        args=('STDOUT', process.stdout))

    t1.daemon = True
    t1.start()

    t2 = Thread(target=stream_watcher, name='stderr-watcher',
        args=('STDERR', process.stderr))

    t2.daemon = True
    t2.start()

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
            #print 'Nothing yet.'
        else:
            identifier, line = item
            print identifier + ':', line

def _threadStreamPrinter(process, blockingTimeout=1):
    Thread(target=_threadPrinter, name='printer', args=(process, blockingTimeout)).start()

def listFilesInDir(directoryPath):
    fileList = []
    
    if not isinstance(directoryPath, basestring) or \
        directoryPath is None:
        raise TypeError("ERROR: The parameter must be a string.")

    for file_ in os.listdir(directoryPath):
        fileList.append(file_)
    return fileList

def listFilesInDirWithExtension(directoryPath, extension):
    fileList = []
    
    if not isinstance(directoryPath, basestring) or \
        directoryPath is None:
        raise TypeError("ERROR: The parameter must be a string.")

    for file_ in os.listdir(directoryPath):
        if file_.endswith(extension):
            fileList.append(file_)
    return fileList

"Source: Jython - https://fisheye3.atlassian.com/browse/jython/trunk/jython/Lib/subprocess.py?r=6636#to566"
def _cmdline2list(cmdline):
       """Build an argv list from a Microsoft shell style cmdline str
 
        The reverse of list2cmdline that follows the same MS C runtime
        rules.
 
        Java's ProcessBuilder takes a List<String> cmdline that's joined
        with a list2cmdline-like routine for Windows CreateProcess
        (which takes a String cmdline). This process ruins String
        cmdlines from the user with escapes or quotes. To avoid this we
        first parse these cmdlines into an argv.
 
        Runtime.exec(String) is too naive and useless for this case.
        """
       whitespace = ' \t'
       # count of preceding '\'
       bs_count = 0
       in_quotes = False
       arg = []
       argv = []
 
       for ch in cmdline:
           if ch in whitespace and not in_quotes:
               if arg:
                   # finalize arg and reset
                   argv.append(''.join(arg))
                   arg = []
               bs_count = 0
           elif ch == '\\':
               arg.append(ch)
               bs_count += 1
           elif ch == '"':
               if not bs_count % 2:
                   # Even number of '\' followed by a '"'. Place one
                   # '\' for every pair and treat '"' as a delimiter
                   if bs_count:
                       del arg[-(bs_count / 2):]
                   in_quotes = not in_quotes
               else:
                   # Odd number of '\' followed by a '"'. Place one '\'
                   # for every pair and treat '"' as an escape sequence
                   # by the remaining '\'
                   del arg[-(bs_count / 2 + 1):]
                   arg.append(ch)
               bs_count = 0
           else:
               # regular char

               arg.append(ch)
               bs_count = 0
 
       # A single trailing '"' delimiter yields an empty arg
       if arg or in_quotes:
           argv.append(''.join(arg))
 
       return argv

    
