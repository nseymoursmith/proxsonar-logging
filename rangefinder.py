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
import MySQLdb
import settings

class rangefinder(object):
    #default port def should work for linux & mac
    def __init__(self):
        self.debug = False
        self.status = 0;

        #DB initialisation
        self.db = MySQLdb.connect(
            db = settings.DATABASE,
            host = settings.HOST,
            user = settings.USER,
            passwd = settings.PASS
        )

        self.cur = self.db.cursor()
        self.cur.execute("SELECT VERSION()")
        ver = self.cur.fetchone()
        print "Server version: ", ver[0]
        
        self.sqlUpdate = '''
        UPDATE mccglc_seebri_motiondetect
        SET active = (%s)
        WHERE id = (%s)
        '''
        self.sqlRead = '''
        SELECT active 
        FROM mccglc_seebri_motiondetect
        WHERE id = (%s)
        '''

        if settings.LOG:
            date = "".join(time.strftime("%x").split("/"))
            clock = "".join(time.strftime("%X").split(":"))
            logname = "rangefinderlog_%s_%s.log" % (date, clock)
            logging.basicConfig(filename = logname, 
                                format='%(levelname)s:%(message)s', 
                                level=logging.DEBUG)
            print "Logging data to file %s." % (logname,)

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
        if settings.LOG:
            logging.info("Serial initialised to port: %s \n\
Threshold set to: %s inches\nSample taken every %s seconds\n" % 
                     (port,settings.THRESHOLD,settings.RATE))
        print ("Serial initialised to port: %s \n\
Threshold set to: %s inches\nSample taken every %s seconds\nPress \"Ctrl-c\" to quit" % 
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

    def stop(self):
        self.status = 0

    def record(self):
        #Start recording:
        self.status = 1
        while self.status:
            try: 
                self.cur.execute(self.sqlRead, (settings.COLUMN_ID,))
                dbValue = self.cur.fetchone()
                received_line = self.get_message()[:-1] #strip \cr
                temp = received_line.split(" ")
                try:
                    distance = int(temp[0][1:])
                except ValueError:
                    if not settings.SILENT:
                        print "Serial error, skipping measurement"
                    pass
                activeValue = int(temp[1][1:])
                if distance > settings.THRESHOLD:
                    logging.info(received_line)
                    self.cur.execute(self.sqlUpdate, (activeValue, settings.COLUMN_ID))
                if not settings.SILENT:
                    print "activeValue on database: ", (dbValue[0],)
                    print "sensor data: " + received_line + "\n"
                time.sleep(settings.RATE)
            except (KeyboardInterrupt, SystemExit):
                self.cur.close()
                self.db.close()
                raise

if __name__ == "__main__":
    rangefinder = rangefinder().record()
