from inputoutput import InputOutput
from collections import OrderedDict
import shlex, os

class ExtractData:
    ioInstance = None
    streams = (0, 1, 2)
    argsList = []
    cmdLine = ""
    filename = ""
    
    filepath = None
    optionDict = OrderedDict(); #Maps menu option , to a list of sub-options    

    # e.g. programName = 'setoolkit'
    def __init__(self):
        self.filename = "auto.dat"
                

    #From here: http://jimmyg.org/blog/2009/working-with-python-subprocess.html#id13
    def whereis(self, program):
        for path in os.environ.get('PATH', '').split(':'):
            if os.path.exists(os.path.join(path, program)) and \
               not os.path.isdir(os.path.join(path, program)):
                return os.path.join(path, program)
        return None

    def sendMessage(self, message=""):
        cmdList = shlex.split(message)
        print "\nCommand: " + message + "\n"

        while cmdList:
            print "--"
            print self.ioInstance.sendMessage(cmdList.pop(0), 0)
            print "--\n"

    def sendCommands(self):
        while True:
            print "\nEnter some commands to send to the running process.\n"
            self.cmdLine = raw_input()
            self.sendMessage(self.cmdLine)

    def createCategory(self, name, optionList):
        self.optionDict[name] = optionList

    def writeToFile(self, filename, data):
        self.filepath = os.getcwd() + "/" + filename
        with open(self.filepath, 'w') as f:
                f.write(data + "\n")


    def writeToFile(self, filename, data, accessType):
        self.filepath = os.getcwd() + "/" + filename
        with open(self.filepath, accessType) as f:
                f.write(data + "\n")

    def writeToFileCmd(self, filename):
        self.filepath = os.getcwd() + "/" + filename

        print "\nEnter some options for automation, leaving spaces between them:\n"
        self.cmdLine = raw_input()
        self.argsList = shlex.split(self.cmdLine)
        
        #f = open(self.filepath, 'a')
        #for option in argsList:
        #    f.write(option + "\n")
        #f.close()

        for option in self.argsList:
            self.writeToFile(filename, option, "a")

    def runAttack(self):
        self.writeToFileCmd(self.filename)
        self.runProcess()

    def runProcess(self):
        print "\nEnter a program to run, with some arguments, if required.\n"
        self.cmdLine = raw_input()
        self.argsList = shlex.split(self.cmdLine)
        
        #location = whereis(argsList[0])
        #if location is not None:
        #   argsList.pop(0)
        #   argsList.reverse()
        #   argsList.append(location)
        #   argsList.reverse()
        #self.ioInstance = InputOutput(argsList)
        
        self.ioInstance = InputOutput(self.argsList)
        
        #self.argsList = []



    
        
    
