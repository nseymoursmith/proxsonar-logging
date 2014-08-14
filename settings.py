# CONFIGURABLE VALUES

THRESHOLD = 10 #Minimum distance (inches) included in log 

RATE = 1 #Seconds between readings

SILENT = 0 #If not set, readings will be printed to terminal

WINDOWS = True #Set to "False" if in Mac/Linux

PORT = "/dev/tty*USB*" #Regex used to identify serial port in Mac/linux
                       #You can replace this with specific name if you
                       #have multiple serial devices

WINPORT = "COM1" #Serial port of the rangefinder in windows

