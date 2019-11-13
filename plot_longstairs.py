#!/usr/bin/python2.7

import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import tkinter
#matplotlib.use('TkAgg')
import datetime
import math
import pymysql
import os

figname = "stairsNov13.png"

START_TIME = '2019-11-13 10:37:15'
END_TIME = '2019-11-14 1:40:00'





#connect to database

db = pymysql.connect(host="192.168.0.125",  # this PC
					 user="inqnet1",
					 passwd="Teleport1536!",  # your password
					 db="teleportcommission",
					 charset='utf8mb4',
					 cursorclass=pymysql.cursors.DictCursor)
#Initial visibility
Vavmin = 0.3
Vavmax0 =222.5

print(Vavmin)
print(Vavmax0)
visibility = (Vavmax0 - Vavmin)/(Vavmax0 + Vavmin)
print(visibility)
print("")


P = []
time_P = []
Vav=[]
time_Vav=[]
T1 = []
time_T1 = []
Vap = []
time_Vap = []
Vin=[]
time_Vin = []

try:
	with db.cursor() as cur:
		TABLE_NAME = "VapVin"
		queryVapVin = "SELECT Vap, Vin,datetimeVap,datetimeVin FROM "+TABLE_NAME+" WHERE datetimeVap BETWEEN {ts %s} AND {ts %s}"
		TABLE_NAME = "Temp"
		queryT1 = "SELECT T1, datetimeT1 FROM "+TABLE_NAME+" WHERE datetimeT1 BETWEEN {ts %s} AND {ts %s}"
		TABLE_NAME = "Vav"
		queryVav = "SELECT Vav, datetimeVav FROM "+TABLE_NAME+" WHERE datetimeVav BETWEEN {ts %s} AND {ts %s}"
		TABLE_NAME = "Power"
		queryP = "SELECT P, datetimeP FROM "+TABLE_NAME+" WHERE datetimeP BETWEEN {ts %s} AND {ts %s}"


		cur.execute(queryP,(START_TIME,END_TIME,))
		row = cur.fetchone()
		while row is not None:
			P.append(10**6*row["P"])
			time_P.append(row["datetimeP"])
			row = cur.fetchone()

		cur.execute(queryVav,(START_TIME,END_TIME,))
		row = cur.fetchone()
		while row is not None:
			Vav.append(1000*row["Vav"]) #sometimes the scope give me a crazy number like 99999999999 so I replace those values by the first measurement
			time_Vav.append(row["datetimeVav"])
			row = cur.fetchone()


		cur.execute(queryT1,(START_TIME,END_TIME,))
		row = cur.fetchone()
		while row is not None:
			T1.append(row["T1"])
			time_T1.append(row["datetimeT1"])
			row = cur.fetchone()

		cur.execute(queryVapVin,(START_TIME,END_TIME,))
		row = cur.fetchone()
		while row is not None:
			Vap.append(row["Vap"])
			time_Vap.append(row["datetimeVap"])
			Vin.append(row["Vin"])
			time_Vin.append(row["datetimeVin"])
			row = cur.fetchone()

finally:
	db.close()


time_P_first = str(time_P[0])
print("time_P_first=",time_P_first )
time_P_last = str(time_P[-1])
print("time_P_last=",time_P_last )
first_time_P = datetime.datetime.strptime(time_P_first,'%Y-%m-%d %H:%M:%S')
time_P_dt=[]
time_P_el_mins=[]

time_T1_first = str(time_T1[0])
print("time_T1_first=",time_T1_first )
time_T1_last = str(time_T1[-1])
print("time_T1_last=",time_T1_last )
first_time_T1 = datetime.datetime.strptime(time_T1_first,'%Y-%m-%d %H:%M:%S')
time_T1_dt=[]
time_T1_el_mins=[]

time_Vav_first = str(time_Vav[0])
print("time_Vav_first=",time_Vav_first )
time_Vav_last = str(time_Vav[-1])
print("time_Vav_last=",time_Vav_last )
first_time_Vav = datetime.datetime.strptime(time_Vav_first,'%Y-%m-%d %H:%M:%S')
time_Vav_dt = []
time_Vav_el_mins = []


time_Vap_first = str(time_Vap[0])
print("time_Vap_first=",time_Vap_first )
time_Vap_last = str(time_Vap[-1])
print("time_Vap_last=",time_Vap_last )
first_time_Vap = datetime.datetime.strptime(time_Vap_first,'%Y-%m-%d %H:%M:%S')
time_Vap_dt = []
time_Vap_el_mins = []

time_Vin_first = str(time_Vin[0])
print("time_Vin_first=",time_Vin_first )
time_Vin_last = str(time_Vin[-1])
print("time_Vin_last=",time_Vin_last )
first_time_Vin = datetime.datetime.strptime(time_Vin_first,'%Y-%m-%d %H:%M:%S')
time_Vin_dt = []
time_Vin_el_mins = []




for t in time_P:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime - first_time_P
	time_P_dt.append(datime)
	time_P_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
for t in time_Vav:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime- first_time_Vav
	time_Vav_dt.append(datime)
	time_Vav_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
for t in time_Vap:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime- first_time_Vap
	time_Vap_dt.append(datime)
	time_Vap_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
for t in time_Vin:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime- first_time_Vin
	time_Vin_dt.append(datime)
	time_Vin_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
for t in time_T1:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime - first_time_T1
	time_T1_dt.append(datime)
	time_T1_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes


VavmaxArr=[]
P0=P[0]
for p in P:
	VavmaxArr.append(Vavmax0*p/P0)


#convert to phase
phase = []
for n in range(len(Vav)):
	v=Vav[n]
	Vavmax=VavmaxArr[n]
	ph = (2*v-Vavmax -Vavmin)/(Vavmax-Vavmin)
	if ph >1 or ph<-1:
		print("sinph: ",ph)
		print("vav: ",v)
		if ph>1:
			ph=1
		if ph<-1:
			ph=-1

	ph = np.arcsin(ph)*180/np.pi
	phase.append(ph)
print(min(phase))
print(max(phase))


phase_unscaled = []
for n in range(len(Vav)):
	v=Vav[n]
	Vavmax=Vavmax0
	ph = (2*v-Vavmax -Vavmin)/(Vavmax-Vavmin)
	if ph >1 or ph<-1:
		print("sinph: ",ph)
		print("vav: ",v)
		if ph>1:
			ph=1
		if ph<-1:
			ph=-1

	ph = np.arcsin(ph)*180/np.pi
	phase_unscaled.append(ph)



minPhase_indices = np.where(phase==min(phase))
minPhase_indices=minPhase_indices[0]
print(minPhase_indices[0])
maxPhase_indices=np.where(phase==max(phase))
maxPhase_indices=maxPhase_indices[0]
print("minphase vin: ",Vin[minPhase_indices[0]])
print("minphase vap: ",Vap[minPhase_indices[0]])
print("maxphase vin: ",Vin[maxPhase_indices[0]])
print("maxphase vap: ",Vap[maxPhase_indices[0]])


#Stacked plot of all data
fig, axs = plt.subplots(6,1, num=238, sharex=True)
xmin=time_Vap_el_mins[0] #40
xmax=time_Vap_el_mins[-1] #60
#Vin
axs[0].plot(time_Vap_el_mins, Vap,  linestyle = 'none', marker = '.', markersize = 2)
axs[0].set_ylabel(r"$V_{ap}$ (V)")
axs[0].grid()

#Vin
axs[1].plot(time_Vin_el_mins, Vin,  linestyle = 'none', marker = '.', markersize = 2)
axs[1].set_ylabel(r"$V_{in}$ (V)")
axs[1].grid()

#Vav
axs[2].plot(time_Vav_el_mins, Vav,  linestyle = 'none', marker = '.', markersize = 2)
axs[2].set_ylabel(r"Vav (mV)")
axs[2].grid()
#axs[2].set_ylim(210,220)

#Phase
axs[3].plot(time_Vav_el_mins, phase,  linestyle = 'none', marker = '.', markersize = 2)
axs[3].set_ylabel(r"Phase ($\degree$)")
axs[3].grid()
#axs[3].set_ylim(60,80)

#Temp
axs[4].plot(time_T1_el_mins, T1,  linestyle = 'none', marker = '.', markersize = 2)
axs[4].set_ylabel(r"T ($\degree C$)")
axs[4].grid()

#Power
axs[5].plot(time_P_el_mins, P,  linestyle = 'none', marker = '.', markersize = 2)
axs[5].set_ylabel(r"P ($\mu$ W)")
axs[5].grid()
axs[5].set_xlim(xmin,xmax)

xlims=axs[5].get_xlim()
xmin1=xlims[0]
xmax1=xlims[1]
fig.suptitle("Monitoring Interferometer from \n"+str(time_Vav[0]+datetime.timedelta(minutes=xmin1))+" to "+str(time_Vav[0]+datetime.timedelta(minutes=xmax1)))
plt.xlabel('Elapsed time (min)', fontsize =16)
plt.savefig(figname)
plt.show()
print(figname)
