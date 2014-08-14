<<<<<<< HEAD
# CONFIGURABLE VALUES:
=======
# CONFIGURABLE VALUES
>>>>>>> 1a0db0850b107cc561adc2460424b37ac7a29cbb

THRESHOLD = 10 #Minimum distance (inches) included in log 

RATE = 1 #Seconds between readings

<<<<<<< HEAD
SILENT = 0 #If set, readings will not be printed to terminal

LOG = 0 #If set, readings will be written to logfile
=======
SILENT = 0 #If not set, readings will be printed to terminal

WINDOWS = True #Set to "False" if in Mac/Linux
>>>>>>> 1a0db0850b107cc561adc2460424b37ac7a29cbb

PORT = "/dev/tty*USB*" #Regex used to identify serial port in Mac/linux
                       #You can replace this with specific name if you
                       #have multiple serial devices

<<<<<<< HEAD
WINDOWS = True #Set to "False" if in Mac/Linux

WINPORT = "COM1" #Serial port of the rangefinder in windows


#DATABASE VARIABLES:

DATABASE = "test" 

HOST = "localhost"

USER = "root"

PASS = "root"

COLUMN_ID = 2 
=======
WINPORT = "COM1" #Serial port of the rangefinder in windows

>>>>>>> 1a0db0850b107cc561adc2460424b37ac7a29cbb
