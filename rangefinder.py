"""
Python serial interface to USB-ProxSonar
logs data from the rangefinder to file
N. Seymour-Smith 11/09/14
"""
import sys
import serial
import glob
import time
import logging
import settings

class rangefinder(object):
    #default port def should work for linux & mac
    def __init__(self):
        self.debug = False
        self.status = 0;

        #Logging initialisation:
        date = "".join(time.strftime("%x").split("/"))
        clock = "".join(time.strftime("%X").split(":"))
        logname = "rangefinderlog_%s_%s.log" % (date, clock)
        logging.basicConfig(filename = logname, 
                            format='%(levelname)s:%(message)s', 
                            level=logging.DEBUG)
        print "Logging data to file %s. \"Ctrl-c\" to stop" % (logname,)

        #Open serial port:
        if settings.WINDOWS:
            port = settings.WINPORT
            try:
                self.serial = serial.Serial(port, 57600, timeout=None)
            except:
                logging.exception("Error opening serial port %s" % (port,))
        else:
            #Look for the first port that matches the glob given
            try:
                port = glob.glob(settings.PORT)[0]
            except IndexError:
                logging.error("Could not find the serial port for the rangefinder:\
                         %s" % (port,))
                raise Exception(port + " does not exist!")
            try:
                self.serial = serial.Serial(port, 57600, timeout=None)
            except:
                logging.exception("Error opening serial port for rangefinder:\
                              %s" % (port,))
                raise
        logging.info("Serial initialised to port: %s \n\
Threshold set to: %s inches\nSample taken every %s seconds\n" % 
                     (port,settings.THRESHOLD,settings.RATE))
        print ("Serial initialised to port: %s \n\
Threshold set to: %s inches\nSample taken every %s seconds\n" % 
        (port,settings.THRESHOLD,settings.RATE))

    def get_message(self, timeout = 10): #timeout in seconds
        self.serial.flushInput()
        start_time = time.time()
        while not self.serial.inWaiting(): #wait for message from rangefinder
            time.sleep(0.1)
            if time.time() - start_time > timeout:
                logging.error("Serial communication timed out")
                raise Exception("Serial timeout")
        received_line = self.serial.read(8) 
        if self.debug:
            print "Received line :", received_line
        return received_line

    def interpret(self, received_line):
        range, status = received_line.split(" ")
        range = range[1:] #All but first character (R)
        status = status[1:-1] #All but first (P) and
                              #last character (carriage return)
        if self.debug:
            print "distance: " + range + ", in-range: " + status + "\n"
        return range, status

    def stop(self):
        self.status = 0

    def record(self):
        #Start recording:
        self.status = 1
        start = round(time.time(), 0)
        while self.status:
            try: 
                received_line = self.get_message()[:-1] #strip \cr
                temp = received_line.split(" ")
                distance = int(temp[0][1:])
                if distance > settings.THRESHOLD:
                    logging.info(received_line)
                if not settings.SILENT:
                    print received_line + "\n"
                time.sleep(settings.RATE)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                logging.exception("Exception encountered while recording")

if __name__ == "__main__":
    rangefinder = rangefinder().record()
