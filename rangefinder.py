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
import os
import json
import shutil
 
class rangefinder(object):
    def __init__(self):
        self.debug = False
        self.status = 0;

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
%s. Try setting it manually in \"settings.py\"" % (settings.PORT,))
                raise Exception(settings.PORT + " does not exist!")
            try:
                self.serial = serial.Serial(port, 57600, timeout=None)
            except:
                logging.exception("Error opening serial port for rangefinder:\
%s. Try setting it manually in \"settings.py\"" % (port,))
                raise
        if settings.LOG:
            logging.info("Serial initialised to port: %s \n\
Threshold set to: %s inches\nSample taken every %s seconds\n" %
                                 (port,settings.DMAX,settings.RATE))
        print ("Serial initialised to port: %s \n\
Threshold set to: %s inches\nSample taken every %s seconds\nPress \"Ctrl-c\" to quit" % (port,settings.DMAX,settings.RATE))
                    
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
                
    def stop(self):
        self.status = 0
    
    def record(self):
        #Start recording:
        self.status = 1
        while self.status:
            try:
                received_line = self.get_message()[:-1] #strip \cr
                temp = received_line.split(" ")
                distance = int(temp[0][1:])
                activeValue = int(temp[1][1:])
                if distance > settings.DMAX:
                    activeValue = 0
                else:
                    activeValue = 1
                logging.info(received_line)
                
                # Write to a temp file then rename to the final file,
                # on mac, linux and unix this is atomic and on windows
                # it's pretty fast
                open(settings.OUPTUT_FILE + ".temp", "wb").write(json.dumps([{"active": activeValue}]))
                shutil.move(settings.OUPTUT_FILE + ".temp", settings.OUPTUT_FILE)
                if not settings.SILENT:
                    print "\nsensor data: " + received_line
                    print "Max distance: %s in." % (settings.DMAX,)

                time.sleep(settings.RATE)
            except ValueError:
                if not settings.SILENT:
                    print "Serial error, skipping measurement"
            except (KeyboardInterrupt, SystemExit):
                self.cur.close()
                self.db.close()
                raise
 
 
if __name__ == "__main__":
    rangefinder = rangefinder().record()
