# CQNET-Interf
Code for monitoring the interferometer at Caltech.


## Overview
1. `IntfScanFunc.py` (Python3, Commented, INQNET4) -- Contains functions for remotely controlling power supply
2. `plot_36hours.py` (Python3, Commented, INQNET1) -- plots data from database for a 36 hour interferometer run
3. `plot_interf.py` (Python3, Not Commented, QuTagPC) -- plots data from a table in the database
4. `plot_longstairs.py` (Python3, Not Commented, INQNET1) -- plots data from database for overnight run of interferometer with long steps
5. `plot_realtime.py` (Python3, Not Commented, INQNET1) -- plots data from database for interferometer in real time.
Currently very slow and inefficient because redownloads data from whole table each time instead of just fetching most recent data entry.
6. `plot_stableTemp.py` (Python3, Commented, INQNET1) -- plots data from database for an overnight run at constant applied voltage with stabilized temperature.
7. `plot_Vav.py` (Python3, Commented, QuTagPC) -- plots data from the Vav table (output voltage of interferometer) in the database
8. `Power2DB.py` (Python3, Commented, INQNET4) -- Records power from powermeter and writes to database. This needs to be run on a computer where the powermeter is connected.
9. `run_DAQ_interf.py` (Python3, Commented, INQNET1) -- Records output voltage of interferometer from oscilloscope and writes to database. This needs to be run on a computer in the database network.
10. `run_W_interf.py` (Python3, Not documented) -- for recording wavelength data and writing to database in real time using API. Not finished.
11. `runIntfVapScan.py` (Python3, Commented, INQNET4) -- Controls the power supply, records the voltage sent to the interferometer as reported by the power supply and writes to the database. Needs to be run on computer where the power supply is connected (USB).
12. `tempvstime.py` (Python2, Commented, rbpi2) -- Records temp of thermistor attached to body of interferometer through an ADC. At CQNET, we run this script on a raspberry pi and ssh to the raspberry pi through a computer on the database network (QuTagPC or INQNET1).
13. `write_W_interf.py` (Python3, Commented, QuTagPC) -- Writes the wavelength vs. time data to the database from a .lta file.  Since the wavelength recording software is run on Windows, I wrote this script to as a work-around: save the data as recorded by the software as a '.lta' file (on INQNET3), send to a computer on the database network (INQNET1), and use this script to write the data to the database. In principle, there is an API that can be set up to write the data directly to the database as it is being recorded (see `run_W_interf.py`).

* The "...run(s)" folders feature data and code edited for specific data collections.

### Notes
* To get started on the API for the wavemeter, here is an email from an exchange with a company representative:
    > the API (wlmData.dll) is included in the software. The dll is installed
    > to the windows/system32 (/sysWow64) folder.
    >
    > In the installation path of the wavemeter you will find a subfolder
    > /projects, in this folder you will find some simple examples.
    >
    > If you tell us the programming language you want to use we can send you
    > also some more "sophisticated" examples.
    
    - For INQNET3, the API is located in `This PC > Windows(C:) > Windows > System32 > wlmData.dll`


## Requirements
### Mysql
The scripts here store and collect data from mysql tables from local mysql databases. If you don't have
mysql installed, you first need to install it (see https://www.mysql.com/downloads/) and create databases, tables, and users. Unless you set up the exact same databases and tables, you will probably have to change the database, table, and column names/specs in the scripts.

### Python packages
Below are listed all the packages that are used in this repo. Some may already be installed on your computer, but otherwise you should install them.
#### Python3:
* pymysql
* ast
* datetime
* time
* numpy
* getpass
* os
* subprocess
* sockets
* sys
* glob
* pipes
* argparse
* pyvisa
* matplotlib
* math
* ThorlabsPM100
* re
* pandas
* statistics
* itertools
* ctypes

#### Python2
* time
* math
* Adafruit_ADS1x15
* mysql.connector

You can look up the packages and their installation commands on pypi.org.

### Installation commands
To install python packages, use:
* `python -m pip install --user <package1> <package2> ...`
* `python3 -m pip install --user <package1> <package2> ...`

##### For tips and other useful commands for getting started, see the CQNET repo's README.
---
This code was written by Sam Davis at Caltech. Contact me at s1dav1s@alumni.stanford.edu if you have any questions.
