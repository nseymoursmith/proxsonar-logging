"""
Python serial interface to USB-ProxSonar®-EZ2™
logs data from the rangefinder to file
N. Seymour-Smith 11/09/14
"""
""" 
    From the Documentation:
======================================================================
    The sensor output is provided over the COM port (or equivalent) in
an ASCII character format. If a target is detected at 8 inches the
output appears as follows: “R008 P1<carriage return>”. The output is
an ASCII capital “R”, followed by three ASCII character digits
representing the range in inches up to a maximum of 125 inches. This
is followed by an ASCII space and the ASCII character “P”, followed by
one ASCII digit “1 or 0” corresponding to the “True or False”
proximity information, followed by a carriage return. A proximity
value of “1” signifies that a target is present in the detection
zone. A proximity value of “0” signifies that no target has been
detected in the detection zone."""

import serial
import glob
import time
import logging

class rangefinder(object):
    #default port def should work for linux & mac
    def __init__(self, port="/dev/tty*USB*"):
        self.debug = False
        self.status = 0;
        #Look for the first port that matches the glob given
        try:
            port = glob.glob(port)[0]
        except IndexError:
           logger.error("Could not find the serial port for the rangefinder:
                         %s" % (port,))
           raise Exception(port + "does not exist!")
        try:
            self.serial = serial.Serial(port, 9600, timeout=None)
        except:
            logger.exception("Error opening serial port for rangefinder:
                              %s" % (port,))
            raise
        logger.debug("Serial initialised to port: %s \n" % (port,))

    def get_message(self, timeout = 10): #timeout in seconds
        start_time = time.time()
        while not self.serial.inWaiting(): #wait for message from rangefinder
            time.sleep(0.1)
            if time.time() - start_time > timeout:
                logger.error("Serial communication timed out")
                raise Exception("Serial timeout")
            received_line = self.serial.readline() 
            return received_line

    def interpret(self, received_line):
        if self.debug:
            print "Received line :", received_line,
        range, status = received_line.split(" ")
        range = range.lsplit('R')
        status = status.rsplit('\r')
        return range, status

    def stop(self):
        self.status = 0

    def record(self, silent = False, filename = ""):
        if not filename:
            date = "".join(time.strftime("%x").split("/"))
            clock = "".join(time.strftime("%X").split(":"))
            logname = "rangefinderlog_%s_%s.log" % (date, clock)
        logging.basicConfig(filename = logname, 
                            format='%(levelname)s:%(message)s', 
                            level=logging.DEBUG)
        print "Logging data to file %s. \"Ctrl-c Ctrl-c\" to stop" % (logname,)
        
        #Start recording:
        self.status = 1
        while self.status:
            received_line = self.get_message()
            range, status = self.interpret(received_line)
            clock = time.strftime("%X")
            output = ("time: " + clock + ", distance: " + range 
                      + ", object in range: " + status)
            logging.info(output)
            if not silent:
                print output

