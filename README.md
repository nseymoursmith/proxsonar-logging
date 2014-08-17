USAGE:
=====

In windows or linux, from the command line: 

> python rangefinder.py

On mac, just double click "rangefinder_logging.command".

To quit, press "Ctrl-c" in the terminal window 

REQUIREMENTS:
============

Python2.7: 
=========

Windows: https://www.python.org/download/releases/2.7/

Mac (if Python is not already installed): 
	
+ Install homebrew (instructions from http://brew.sh/):
   - Got to Terminal and type `ruby -e "$(curl -fsSL
     https://raw.github.com/Homebrew/homebrew/go/install)"`
   - Hit return when prompted
   - Enter system admin password
   - Wait for it to install
   - Type `brew doctor` and it should reply `Your system is ready to
     brew`
   - IMPORTANT: Make sure that Brew installed things are used instead
     of default installs by typing: `echo export PATH='/usr/local/bin:$PATH' >> ~/.bash_profile`
     then `source ~/.bash_profile`

pySerial: 
========

Windows: http://www.askives.com/pyserial-64-bit-windows.html

Mac: 
> pip install pyserial

MySQLdb: 
=======

Windows: http://www.codegood.com/archives/129

Mac:
> pip install MySQLdb-python

