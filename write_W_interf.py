"""
This writes wavelength vs time data from a '.lta' file
to the database.

Requirements: Python3, mysql, packages listed below.
OS: CentOS7
"""

import time
import math
import pymysql
import numpy as np
import re
import sys
import datetime
import pandas as pd
from statistics import mean
from itertools import groupby



#Parse data from file
FILENAME="weekend36Scan.lta"
wavelength=[]
deltat_wavelength=[]
datetime_wavelength=[]
wavelength_float=[]
with open(FILENAME,'r') as f:
    line = f.readline()
    linesplit = line.split()
    while "[Measurement data]" not in line:
        line = f.readline()
        if "Measurements" in line:
            linesplit = line.split()
            numPts = int(linesplit[1])
            line = f.readline()
            linesplit=line.split()
            start_date = linesplit[1]
            start_date_split=re.split('[.,]',start_date)
            print(start_date_split)
            start_date_str = datetime.date(int(start_date_split[2]),int(start_date_split[1]),int(start_date_split[0]))
            print(start_date_str)
            start_time=linesplit[2]
            start_time_split=re.split('[:.]',start_time)
            print(start_time_split)
            start_time_str=datetime.time(int(start_time_split[0]),int(start_time_split[1]),int(start_time_split[2]),1000*int(start_time_split[3]))
            startdatetime = datetime.datetime(int(start_date_split[2]),int(start_date_split[1]),int(start_date_split[0]),int(start_time_split[0]),int(start_time_split[1]),int(start_time_split[2]),1000*int(start_time_split[3]))

            line = f.readline()
            linesplit=line.split()
            end_date = linesplit[1]
            end_date_split=re.split('[.,]',end_date)
            end_date_str = datetime.date(int(end_date_split[2]),int(end_date_split[1]),int(end_date_split[0]))
            end_time=linesplit[2]
            end_time_split=re.split('[:.]',end_time)
            end_time_str=datetime.time(int(end_time_split[0]),int(end_time_split[1]),int(end_time_split[2]),1000*int(end_time_split[3]))
            enddatetime=datetime.datetime(int(end_date_split[2]),int(end_date_split[1]),int(end_date_split[0]),int(end_time_split[0]),int(end_time_split[1]),int(end_time_split[2]),1000*int(end_time_split[3]))
    print(start_date_split)
    print(start_time_split)
    print(start_time_str)
    print(startdatetime)
    line = f.readline()
    line = f.readline()
    while line:
        line = f.readline()
        linesplit = line.split()
        if len(linesplit)==2:
            deltat_wavelength.append(linesplit[0])
            wavelength.append(linesplit[1])


#Round microsecond precision to nearest second
def roundSeconds(dateTimeObject):
    newDateTime=dateTimeObject
    if newDateTime.microsecond >= 500000:
        newDateTime = newDateTime + datetime.timedelta(seconds=1)
    return newDateTime.replace(microsecond=0)




#action: whether are inserting new data or are upating the table in the database
action = "update"
print("action = ", action)
#if action = update, specify with row to update data
i = 60000
if action == "update":
	print("start id number = ", i)


db = pymysql.connect(host="localhost",  # this PC
		     user="root",         # this user only has access to CPTLAB database
             password="Teleport1536!",  # your password
		     #auth_plugin='mysql_native_password',
		     database="teleportcommission",
             charset='utf8mb4',
             cursorclass=pymysql.cursors.DictCursor) # name of the data base

#Bin data by seconds
for w in range(len(wavelength)):
    wav=float(wavelength[w])
    dt = float(deltat_wavelength[w])-float(deltat_wavelength[0])
    wavdt=startdatetime + datetime.timedelta(milliseconds=dt)
    wavdt=roundSeconds(wavdt)
    wavelength_float.append(wav)
    datetime_wavelength.append(wavdt)
df=pd.DataFrame()
df['datetime']=datetime_wavelength
df['datetime'] = pd.to_datetime(df['datetime'])
df.index = df['datetime']
df['wavelength']=wavelength_float
#Take mean of each bin
df=df.resample('S').mean()
datetime_data=df.index.values
wav_data=df['wavelength'].values


try:
    #Create mysql cursor
    with db.cursor() as cur:
        for t in range(len(datetime_data)):
            wav=str(wav_data[t])
            dt=str(datetime_data[t])
            #update table
            if action == "update":
                query = "SELECT `Wavelength`, `datetimeW` from `interf6` where `id` = %s;"
                cur.execute(query,(str(i)))
                query = "update interf6 set Wavelength = %s, datetimeW = %s where id = %s;"
                cur.execute(query,(wav,dt,str(i)))
            #insert into table
            if action == "insert":
                query = "INSERT INTO interf6(Wavelength, datetimeW) values(%s, %s);"
                cur.execute(query,(wav,dt))
                #print(cur.rowcount, "record inserted.")

            i+=1
    db.commit()
finally:
    db.close()
