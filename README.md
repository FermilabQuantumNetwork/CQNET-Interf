# CQNETInterf
Code for monitoring interferometer.

## Overview
1. `IntfScanFunc.py` (Documented) -- Contains functions for remotely controlling power supply
2. `plot_36hours.py` (Documented) -- plots data from database for a 36 hour interferometer run
3. `plot_interf.py` (Not documented) -- plots data from a table in the database
4. `plot_stableTemp.py` (Documented) -- plots data from database for an overnight run at constant applied voltage with stabilized temperature.
5. `plot_Vav.py` (Documented) -- plots data from the Vav table (output voltage of interferometer) in the database
6. `Power2DB.py` (Documented) -- Records power from powermeter and writes to database. This needs to be run on a computer where the powermeter is connected. At CQNET, we've been running this on the INQNET4 computer.
7. `run_DAQ_interf.py` (Documented) -- Records output voltage of interferometer from oscilloscope and writes to database. This needs to be run on a computer in the database network, such as the INQNET1 computer at CQNET.
8. `run_W_interf.py` (Not documented) -- for recording wavelength data and writing to database in real time using API. Not finished.
9. `runIntfVapScan.py` (Documented) -- Controls the power supply, records the voltage sent to the interferometer as reported by the power supply and writes to the database. Needs to be run on computer where the powersupply is connected (USB). At CQNET, we've been running this on INQNET4.
10. `tempvstime.py` (Documented) -- Records temp of thermistor attached to body of interferometer through an ADC. At CQNET, we run this script on a raspberry pi and ssh to the raspberry pi through a computer on the database network, such as the INQNET1 at CQNET.
11. `write_W_interf.py` (Documented) -- Writes the wavelength vs. time data to the database from a .lta file.  Since the wavelength recording software isn't very compatible with linux, I wrote this script to as a work-around: save the data as recorded by the software as a '.lta' file (at CQNET, the software is run on the INQNET3 computer), send to a computer on the database network (such as INQNET1 at CQNET), and use this script to write the data to the database. In principle, there is an API that can be set up to write the data directly to the database as it is being recorded (see `run_W_interf.py`).

This code was written by Sam Davis at CQNET. Contact me at s1dav1s@alumni.stanford.edu if you have any questions.

## Tips
* If you are on Centos, install tkinter to use graphical interface for viewing matplotlib plots:
`sudo yum install python3-tkinter`

## Useful mysql syntax

### Login to mysql
From computer with database:
```
mysql -u root -p
```

From computer in network:
```
mysql -u <username> -h '<IP address>' -p
```

These commands will prompt for password.

### Create database
```create database teleportcommission;```

### Create user
For more info, look up "MySQL 6.2.8 Adding Accounts, Assigning Privileges, and Dropping Accounts"
```
create user '<username>'@'<IP address>' 
	identified by '<password>';

grant all on *.*
	to '<username>'@'<IP address>'  
	with grant option;
```
On terminal of computer with database:

```
grant all privileges on *.* to '<username>'@'<IP address>' with grant option;
flush privileges;
```

### Drop user

```
drop user '<username>'@'<IP address>'
```


### Create table
Example: create table called interf with five columns and diff datatypes.

```
create table interf(id int not null primary key auto_increment, 
                         Vmax0 float, 
                         Vmax1 float, 
                         Vmax2 float, 
                         datetime datetime); //create a new table
```

### Select single row of table
Example:

```
select *
from MyTable
where MyPrimaryKey = 123;
```


### Select multiple rows of table
Example:

```
select * from interf4 limit 55719,76063;
```

### Rename table
Example:

```
ALTER TABLE old_table RENAME new_table; 
```


### Rename column of table
Example:

```
alter table testTable rename column T1 to test; 
```

### Add column
The square bracket terms are optional.

```
ALTER TABLE table ADD [COLUMN] column_name_1 column_1_definition [FIRST|AFTER existing_column];  ```

