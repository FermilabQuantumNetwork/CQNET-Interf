"""
This plots data from a 36 hour test run of the interferometer. The test run
corresponded to the applied voltage trace defined by `VoltageTestIntf(Vmin,Vmax,numSteps)`
from IntfScanFunc.py
It retrieves data stored from the corresponding table in the database and then plots the data.

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


START_TIME_Vap = '2019-10-19 15:40:00'
END_TIME_Vap = '2019-10-21 04:10:00'

START_TIME_Vin = START_TIME_Vap
END_TIME_Vin = END_TIME_Vap

START_TIME_Vav = START_TIME_Vap
END_TIME_Vav = END_TIME_Vap

START_TIME_T1 = START_TIME_Vap
END_TIME_T1 = END_TIME_Vap


START_TIME_P = START_TIME_Vap
END_TIME_P = END_TIME_Vap


START_TIME_W = START_TIME_Vap
END_TIME_W = END_TIME_Vap

TABLE_NAME = 'interf6'


#connect to database

db = pymysql.connect(host="<IP ADDRESS>",  #Replace <IP ADDRESS> with the IP of computer with database. Local host if is same computer.
					 user="<USERNAME>", #Replace <USERNAME> with your username
					 passwd="<PASSWORD>",  #Replace <PASSWORD> with your password
					 db="teleportcommission",
					 charset='utf8mb4',
					 cursorclass=pymysql.cursors.DictCursor)        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need

Vap=[]
time_Vap=[]
Vin = []
time_Vin = []
P = []
time_P = []
Vav=[]
time_Vav=[]
T1 = []
time_T1 = []
wavelength = []
time_w = []

try:
	with db.cursor() as cur:
		queryVap = "SELECT Vap, datetimeVap FROM "+TABLE_NAME+" WHERE datetimeVap BETWEEN {ts %s} AND {ts %s}"
		queryVin = "SELECT Vin, datetimeVin FROM "+TABLE_NAME+" WHERE datetimeVin BETWEEN {ts %s} AND {ts %s}"
		queryW = "SELECT Wavelength, datetimeW FROM "+TABLE_NAME+" WHERE datetimeW BETWEEN {ts %s} AND {ts %s}"
		queryT1 = "SELECT T1, datetimeT1 FROM "+TABLE_NAME+" WHERE datetimeT1 BETWEEN {ts %s} AND {ts %s}"
		queryVav = "SELECT Vav, datetimeVav FROM "+TABLE_NAME+" WHERE datetimeVav BETWEEN {ts %s} AND {ts %s}"
		queryP = "SELECT P, datetimeP FROM "+TABLE_NAME+" WHERE datetimeP BETWEEN {ts %s} AND {ts %s}"

		cur.execute(queryVap,(START_TIME_Vap,END_TIME_Vap,))
		row = cur.fetchone()
		while row is not None:
			Vap.append(row["Vap"]) #sometimes the scope give me a crazy number like 99999999999 so I replace those values by the first measurement
			time_Vap.append(row["datetimeVap"])
			row = cur.fetchone()


		cur.execute(queryVin,(START_TIME_Vin,END_TIME_Vin,))
		row = cur.fetchone()
		while row is not None:
			Vin.append(row["Vin"])
			time_Vin.append(row["datetimeVin"])
			row = cur.fetchone()

		cur.execute(queryP,(START_TIME_P,END_TIME_P,))
		row = cur.fetchone()
		while row is not None:
			P.append(row["P"])
			time_P.append(row["datetimeP"])
			row = cur.fetchone()

		cur.execute(queryVav,(START_TIME_Vav,END_TIME_Vav,))
		row = cur.fetchone()
		while row is not None:
			Vav.append(row["Vav"]) #sometimes the scope give me a crazy number like 99999999999 so I replace those values by the first measurement
			time_Vav.append(row["datetimeVav"])
			row = cur.fetchone()


		cur.execute(queryT1,(START_TIME_T1,END_TIME_T1,))
		row = cur.fetchone()
		while row is not None:
			T1.append(row["T1"])
			time_T1.append(row["datetimeT1"])
			row = cur.fetchone()

		cur.execute(queryW,(START_TIME_W,END_TIME_W,))
		row = cur.fetchone()
		while row is not None:
			wavelength.append(row["Wavelength"])
			time_w.append(row["datetimeW"])
			row = cur.fetchone()





finally:
	db.close()

time_Vap_first = str(time_Vap[0])
time_Vap_last = str(time_Vap[-1])
first_time_Vap = datetime.datetime.strptime(time_Vap_first,'%Y-%m-%d %H:%M:%S')
time_Vap_dt = []
time_Vap_el = []

time_Vin_first = str(time_Vin[0])
time_Vin_last = str(time_Vin[-1])
first_time_Vin = datetime.datetime.strptime(time_Vin_first,'%Y-%m-%d %H:%M:%S')
time_Vin_dt=[]
time_Vin_el=[]

time_P_first = str(time_P[0])
time_P_last = str(time_P[-1])
first_time_P = datetime.datetime.strptime(time_P_first,'%Y-%m-%d %H:%M:%S')
time_P_dt=[]
time_P_el=[]

time_Vav_first = str(time_Vav[0])
time_Vav_last = str(time_Vav[-1])
first_time_Vav = datetime.datetime.strptime(time_Vav_first,'%Y-%m-%d %H:%M:%S')
time_Vav_dt = []
time_Vav_el = []

time_T1_first = str(time_T1[0])
time_T1_last = str(time_T1[-1])
first_time_T1 = datetime.datetime.strptime(time_T1_first,'%Y-%m-%d %H:%M:%S')
time_T1_dt=[]
time_T1_el=[]

time_w_first = str(time_w[0])
time_w_last = str(time_w[-1])
first_time_w = datetime.datetime.strptime(time_w_first,'%Y-%m-%d %H:%M:%S')
time_w_dt=[]
time_w_el=[]

for t in time_Vap:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime- first_time_Vap
	time_Vap_dt.append(datime)
	time_Vap_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
for t in time_Vin:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime - first_time_Vin
	time_Vin_dt.append(datime)
	#time_T1_s.append(elapsed.total_seconds())
	time_Vin_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
for t in time_P:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime - first_time_P
	time_P_dt.append(datime)
	#time_T1_s.append(elapsed.total_seconds())
	time_P_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes

for t in time_Vav:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime- first_time_Vav
	time_Vav_dt.append(datime)
	time_Vav_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
for t in time_T1:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime - first_time_T1
	time_T1_dt.append(datime)
	#time_T1_s.append(elapsed.total_seconds())
	time_T1_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
for t in time_w:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime - first_time_w
	time_w_dt.append(datime)
	#time_T1_s.append(elapsed.total_seconds())
	time_w_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes


#second parameter is the variable to be ploted



Vavmin = min(Vav)
Vavmax =max(Vav)


phase = []
for v in Vav:
	# ph = v-Vavmin
	# rangeVav = Vavmax-Vavmin
	# ph=np.arcsin(ph/rangeVav)*180/np.pi
	ph = (2*v-Vavmax +Vavmin)/(Vavmax-Vavmin)
	#ph =(Vavmax+3*Vavmin - 2*v)/(Vavmax + Vavmin)
	#print(ph)
	ph = np.arcsin(ph)*180/np.pi
	#print(ph)
	phase.append(ph)




xmin = 1300
xmax = 1680

#figure(1)
fig, axs = plt.subplots(5,1, num="1")

#axs[0].title.set_text("Applied Voltage from "+time_Vap_first+" to "+time_Vap_last)
# axs[0].plot(time_Vap_el, Vap,  linestyle = 'none', marker = '.', markersize = 2, label = "Vap")
# axs[0].grid()

#axs[1].title.set_text("Vin from "+time_Vin_first+" to "+time_Vin_last)
axs[0].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2, label = "Vin")
axs[0].set_xlim(xmin, xmax)
axs[0].grid()

#axs[2].title.set_text("Vav from "+time_Vav_first+" to "+time_Vav_last)
# axs[2].plot(time_Vav_el, Vav,  linestyle = 'none', marker = '.', markersize = 2, label = "Vav")
# axs[2].grid()

axs[1].plot(time_Vav_el, phase,  linestyle = 'none', marker = '.', markersize = 2, label = "phase")
axs[1].set_xlim(xmin,xmax)
axs[1].grid()


#axs[3].title.set_text("Temp from "+time_T1_first+" to "+time_T1_last)
axs[2].plot(time_T1_el, T1,  linestyle = 'none', marker = '.', markersize = 2, label = "temp1")
axs[2].set_xlim(xmin, xmax)
axs[2].grid()

#axs[4].title.set_text("Power from "+time_P_first+" to "+time_P_last)
axs[3].plot(time_P_el, P,  linestyle = 'none', marker = '.', markersize = 2, label = 'power')
axs[3].set_xlim(xmin, xmax)
axs[3].grid()



#axs[4].title.set_text("Wavelength from "+time_w_first+" to "+time_w_last)
axs[4].plot(time_w_el, wavelength,  linestyle = 'none', marker = '.', markersize = 2, label = 'wavelength')
axs[4].set_ylim(1536, 1537)
axs[4].grid()




for nn, ax in enumerate(axs):
	ax.legend(prop={'size':10})


plt.xlabel('Elapsed time (min)', fontsize =16)
plt.tight_layout()



fig, axs = plt.subplots(1,1, num="2")

axs.plot(time_Vav_el, phase,  linestyle = 'none', marker = '.', markersize = 2, label = "phase")
axs.set_xlim(xmin, xmax)
axs.grid()


axs.legend(prop={'size':10})


fig, axs = plt.subplots(1,1, num="3")
axs.set_xlim(xmin,xmax)
axs.plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2, label = "Vin")
axs.grid()


axs.legend(prop={'size':10})



plt.show()
