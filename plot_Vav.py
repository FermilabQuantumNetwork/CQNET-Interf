"""
This plots data from the Vav column of a table in our database.
It retrieves data stored from the corresponding table in the database and then plots the data.
For more detailed comments, see plot_36hours.py

Requirements: Python3, mysql, packages listed below
OS: CentOS7
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import math
import pymysql
import os

#Start and end datetimes that define range of data to retrieve from mysql table
START_TIME_Vav = '2019-10-09 23:00:00'
END_TIME_Vav = '2019-10-10 02:59:00'

START_TIME_T1 = '2019-10-09 23:00:00'
END_TIME_T1 = '2019-10-10 02:59:00'

START_TIME_W = '2019-10-10 23:00:00'
END_TIME_W = '2019-10-11 02:59:00'

TABLE_NAME = 'interf4'


#Connect to mysql database
db = pymysql.connect(host="<IP ADDRESS>",  #Replace <IP ADDRESS> with the IP of computer with database. Local host if is same computer.
					 user="<USERNAME>", #Replace <USERNAME> with your username
					 passwd="<PASSWORD>",  #Replace <PASSWORD> with your password
					 db="teleportcommission", #name of the database
					 charset='utf8mb4',
					 cursorclass=pymysql.cursors.DictCursor)

#Arrays to fill with data from mysql table
Vav=[]
time_Vav=[]
T1 = []
time_T1 = []
wavelength = []
time_w = []

try:
	#Create cursor to select data from mysql.
	with db.cursor() as cur:
		#Mysql command to select data from each column
		queryVav = "SELECT Vav, datetimeVav FROM "+TABLE_NAME+" WHERE id BETWEEN %s AND %s"
		#Execute query and store data in array from Vav column
		cur.execute(queryVav,(str(76503),str(134896),))
		row = cur.fetchone()
		while row is not None:
			Vav.append(row["Vav"])
			time_Vav.append(row["datetimeVav"])
			row = cur.fetchone()
finally: #Once store the data of each column in separate arrays, close the database
	db.close()


#Get the first and last datetimes of the Vav data. The retrieved data falls within the
#bounds of the start and end times that were specified, but may not be exactly the same.
time_Vav_first = str(time_Vav[0])
time_Vav_last = str(time_Vav[-1])
first_time_Vav = datetime.datetime.strptime(time_Vav_first,'%Y-%m-%d %H:%M:%S')
time_Vav_dt = []
time_Vav_el = []

#Create the elapsed time array for Vav
for t in time_Vav:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime- first_time_Vav
	time_Vav_dt.append(datime)
	time_Vav_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes

#Plot data
fig = plt.figure(1)
plt.title("Vav from "+time_Vav_first+" to "+time_Vav_last)
plt.plot(time_Vav_el, Vav,  linestyle = 'none', marker = '.', markersize = 2, label = "Vav")
plt.grid()
plt.xlabel('Elapsed time (min)', fontsize =16)
plt.ylim(0,0.1)
plt.tight_layout()
plt.show()
