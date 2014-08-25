USAGE:
=====

From the command line: 

> python rangefinder.py

On mac, you can also just double click "rangefinder_logging.command".

To quit, press "Ctrl-c" in the terminal window 

REQUIREMENTS:
============

Python2.7: 
----------

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

+ Install Python and tools

   - From Terminal: brew install python
   - Make sure all is good with by typing brew doctor (should just output "Your system is ready to brew." again)
   - Type python --version and ensure that it gives the same version as Brew reported installing (2.7.8 at the time of writing)



pySerial: 
---------

Windows: http://www.askives.com/pyserial-64-bit-windows.html

Mac: 
> pip install pyserial

