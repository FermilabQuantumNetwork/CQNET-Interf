#!/usr/bin/python2.7

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import datetime
import math
import pymysql
import os

def string_to_date(time):
    return time[2:4]+time[5:7]+time[8:10]+time[11:13]+time[14:16]+time[17:19]
#parameters
# START_TIME_Vav = '2019-10-09 19:00:00'
# END_TIME_Vav = '2019-10-10 09:30:00'
#
# START_TIME_T1 = '2019-10-09 19:00:00'
# END_TIME_T1 = '2019-10-10 09:30:00'

START_TIME_Vav = '2019-10-09 23:00:00'
END_TIME_Vav = '2019-10-10 02:59:00'

START_TIME_T1 = '2019-10-09 23:00:00'
END_TIME_T1 = '2019-10-10 02:59:00'

START_TIME_W = '2019-10-10 23:00:00'
END_TIME_W = '2019-10-11 02:59:00'

TABLE_NAME = 'interf4'


#connect to database

db = pymysql.connect(host="localhost",  # this PC
		             user="root",
                     passwd="Teleport1536!",  # your password
                     db="teleportcommission",
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need

Vav=[]
time_Vav=[]
T1 = []
time_T1 = []
wavelength = []
time_w = []

try:
    with db.cursor() as cur:
        queryVav = "SELECT Vav, datetimeVav FROM "+TABLE_NAME+" WHERE id BETWEEN %s AND %s"
        cur.execute(queryVav,(str(76503),str(134896),))
        row = cur.fetchone()
        while row is not None:
            Vav.append(row["Vav"]) #sometimes the scope give me a crazy number like 99999999999 so I replace those values by the first measurement
            time_Vav.append(row["datetimeVav"])
            row = cur.fetchone()


finally:
    db.close()

time_Vav_first = str(time_Vav[0])
time_Vav_last = str(time_Vav[-1])
first_time_Vav = datetime.datetime.strptime(time_Vav_first,'%Y-%m-%d %H:%M:%S')
time_Vav_dt = []
time_Vav_el = []

# time_wav_first = str(time_w[0])
# first_time_wav = datetime.datetime.strptime(time_wav_first,'%Y-%m-%d %H:%M:%S')
# time_wav_s=[]

for t in time_Vav:
    t=str(t)
    datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    elapsed = datime- first_time_Vav
    time_Vav_dt.append(datime)
    time_Vav_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes




#figure(1)
fig = plt.figure(1)
plt.title("Vav from "+time_Vav_first+" to "+time_Vav_last)
plt.plot(time_Vav_el, Vav,  linestyle = 'none', marker = '.', markersize = 2, label = "Vav")
plt.grid()

plt.xlabel('Elapsed time (min)', fontsize =16)
plt.ylim(0,0.1)
plt.tight_layout()
plt.show()
