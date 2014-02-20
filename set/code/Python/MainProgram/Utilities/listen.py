#!/usr/bin/env python
# My Source: http://www.technoreply.com/finally-a-dummy-smtp-for-linux/
# Original Source: http://muffinresearch.co.uk/archives/2010/10/15/fake-smtp-server-with-python/
"""A noddy fake smtp server."""

import smtpd, asyncore, time, os
from optparse import OptionParser

class FakeSMTPServer(smtpd.SMTPServer):
    """A Fake smtp server"""

    def __init__(*args, **kwargs):
        smtpd.SMTPServer.__init__(*args, **kwargs)

    def process_message(*args, **kwargs):

        directory = "Emails/"

        try:
            os.stat(directory)
        except:
            os.mkdir(directory)

        mail = open(directory+str(time.time())+".eml", "w")
        print "New mail from " + args[2]
        mail.write(args[4])
        mail.close
        pass

#A function
def startFakeSMTPServer(options=None, args=None):

    if (options is None) or (args is None):
        smtp_server = FakeSMTPServer(('localhost', 3333), None)
        print "Running fake smtp server on port 3333\n"
    else:
        portnum = int(options.portnumber)
        smtp_server = FakeSMTPServer(('localhost', portnum), None)
        print "Running fake smtp server on port %d\n" %(portnum)
        
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-p", "--port", dest="portnumber",
                  help="Provide a port number to listen with.\nDefault = port 3333\n", default=3333)
    (options, args) = parser.parse_args()
    startFakeSMTPServer(options, args)
    

