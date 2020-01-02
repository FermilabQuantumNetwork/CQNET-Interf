# CQNET-Interf
Code for monitoring the interferometer at Caltech.


## Overview
1. `IntfScanFunc.py` (Python3, Documented) -- Contains functions for remotely controlling power supply
2. `plot_36hours.py` (Python3, Documented) -- plots data from database for a 36 hour interferometer run
3. `plot_interf.py` (Python3, Not documented) -- plots data from a table in the database
4. `plot_stableTemp.py` (Python3, Documented, INQNET1) -- plots data from database for an overnight run at constant applied voltage with stabilized temperature.
5. `plot_Vav.py` (Python3, Documented, QTagPC) -- plots data from the Vav table (output voltage of interferometer) in the database
6. `Power2DB.py` (Python3, Documented, INQNET4) -- Records power from powermeter and writes to database. This needs to be run on a computer where the powermeter is connected.
7. `run_DAQ_interf.py` (Python3, Documented, INQNET1) -- Records output voltage of interferometer from oscilloscope and writes to database. This needs to be run on a computer in the database network.
8. `run_W_interf.py` (Python3, Not documented) -- for recording wavelength data and writing to database in real time using API. Not finished.
9. `runIntfVapScan.py` (Python3, Documented, INQNET4) -- Controls the power supply, records the voltage sent to the interferometer as reported by the power supply and writes to the database. Needs to be run on computer where the power supply is connected (USB).
10. `tempvstime.py` (Python2, Documented, rbpi2) -- Records temp of thermistor attached to body of interferometer through an ADC. At CQNET, we run this script on a raspberry pi and ssh to the raspberry pi through a computer on the database network (QTagPC or INQNET1).
11. `write_W_interf.py` (Python3, Documented, QTagPC) -- Writes the wavelength vs. time data to the database from a .lta file.  Since the wavelength recording software is run on Windows, I wrote this script to as a work-around: save the data as recorded by the software as a '.lta' file (on INQNET3), send to a computer on the database network (INQNET1), and use this script to write the data to the database. In principle, there is an API that can be set up to write the data directly to the database as it is being recorded (see `run_W_interf.py`).


## Requirements
All of files included in this repository require Python 3, except for `tempvstime.py` which requires python 2.

### Python packages
Below are listed all the packages that are used in this repo. Many may already be installed on your computer, but otherwise you need to install them.
#### Python3:
* pymysql
* ast
* datetime
* time
* numpy
* getpass
* os
* subprocess
* socket
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

To install python packages, use:
* `python -m pip install --user <package1> <package2> ...`
* `python3 -m pip install --user <package1> <package2> ...`


## Tips
* If you are on Centos 7, install tkinter to use graphical interface for viewing matplotlib plots:
`sudo yum install python3-tkinter`

## Useful mysql syntax
Angle bracket terms should be replaced with your inputs.

### Login to mysql
These commands will prompt for password.

* From computer with database:
```
mysql -u root -p
```

* From computer in network:
```
mysql -u <username> -h '<IP address>' -p
```



### Create database
```create database <database name>;```

### Create user
```
create user '<username>'@'<IP address>'
	identified by '<password>';

grant all on *.*
	to '<username>'@'<IP address>'  
	with grant option;
```
* On terminal of computer with database:

```
grant all privileges on *.* to '<username>'@'<IP address>' with grant option;
flush privileges;
```

For more info, look up "MySQL 6.2.8 Adding Accounts, Assigning Privileges, and Dropping Accounts"
### Drop user

```
drop user '<username>'@'<IP address>'
```


### Create table
Example: create table called myTable with five columns and different datatypes.

```
create table myTable(id int not null primary key auto_increment,
                         Vmax0 float,
                         Vmax1 float,
                         Vmax2 float,
                         datetime datetime); //create a new table
```

### Select single row of table
Example:

```
select *
from <table name>
where <primary key name> = 123;
```


### Select multiple rows of table
Example:

```
select * from <table name> limit 55719,76063;
```

### Rename table
```
ALTER TABLE <old_table> RENAME <new_table>;
```


### Rename column of table

```
alter table <table name> rename column <old name> to <new name>;
```

### Add column

```
ALTER TABLE table ADD [COLUMN] <column_name_1> <column_1_definition> [FIRST|AFTER existing_column];
```
The square bracket terms are optional.

---
This code was written by Sam Davis at Caltech. Contact me at s1dav1s@alumni.stanford.edu if you have any questions.
