import subprocess
import os
import sys

class InputOutput:
    inputData = ""
    outputData = None
    process = None

    def __init__(self, argsList): #Starts self.process with argument list like
                                    #this: ['programName', 'arg1', 'arg2, 'arg3' etc...]
        print "--"
        print argsList
        print "--\n"
        self.process = subprocess.Popen(argsList, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def sendMessage(self, inputData="", stream=1):
        #self.inputData = inputData
        if stream == 0: #Send input and get response (stdout)

            #return self.process.communicate(inputData)[0]

            for line in iter(self.process.stdout.readline, ''):
                inputData.append(line)
            self.process.stdout.close()
            
            #while True:
            #    outputData = self.process.stdout.read(1)
            #    if outputData == '' and self.process.poll() != None:
            #        break
            #    if outputData != '':
            #        sys.stdout.write(outputData)
            #        sys.stdout.flush()
                
            
        elif stream == 1:
            sys.stdout.write(inputData) #Write to stdout
        elif stream == 2:
            sys.stderr.write(inputData) #Write to stdin
        else:
            return None
        

    
        
        
        
        
        
