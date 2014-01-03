#!/usr/bin/env python
# My Source: http://www.technoreply.com/finally-a-dummy-smtp-for-linux/
# Original Source: http://muffinresearch.co.uk/archives/2010/10/15/fake-smtp-server-with-python/
"""A noddy fake smtp server."""

import smtpd
import asyncore
import time

class FakeSMTPServer(smtpd.SMTPServer):
    """A Fake smtp server"""

    def __init__(*args, **kwargs):
        print "Running fake smtp server on port 25"
        smtpd.SMTPServer.__init__(*args, **kwargs)

    def process_message(*args, **kwargs):

        directory = "mails/"

        try:
            os.stat(directory)
        except:
            os.mkdir(directory)

        mail = open(directory+str(time.time())+".eml", "w")
        print "New mail from " + args[2]
        mail.write(args[4])
        mail.close
        pass

if __name__ == "__main__":
    smtp_server = FakeSMTPServer(('localhost', 25), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()
