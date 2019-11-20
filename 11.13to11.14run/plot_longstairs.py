#!/usr/bin/python2.7

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.optimize
#import tkinter
#matplotlib.use('TkAgg')
import datetime
import math
import pymysql
import os

mpl.rcParams["savefig.directory"] = os.chdir(os.path.dirname("/home/inqnet1/Desktop/CQNET/CQNET-Interf"))



# #For 30min steps
# START_TIME = '2019-11-13 10:37:15'
# END_TIME = '2019-11-13 15:40:00'

#For 60min steps
START_TIME = '2019-11-13 17:39:26'
END_TIME = '2019-11-14 5:50:34'





#connect to database

db = pymysql.connect(host="192.168.0.125",  # this PC
					 user="inqnet1",
					 passwd="Teleport1536!",  # your password
					 db="teleportcommission",
					 charset='utf8mb4',
					 cursorclass=pymysql.cursors.DictCursor)






P = []
time_P =[]
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


print("Vmin: ", min(Vav))
print("Vmax: ", max(Vav))
Vmin=min(Vav)
Vmax=max(Vav)




minVav_index = np.argmin(Vav)
PatVmin=P[minVav_index]
maxVav_index = np.argmax(Vav)
PatVmax=P[maxVav_index]

Vavmin0=Vmin*P[0]/PatVmin
Vavmax0=Vmax*P[0]/PatVmax

VavmaxArr=[]
VavminArr=[]
#Check for noise level
for p in P:
	VavmaxArr.append(Vavmax0*p/PatVmin)
	VavminArr.append(Vavmin0*p/P[0])

VavmaxArr = np.array(VavmaxArr)
VavminArr = np.array(VavminArr)

visibility = (Vavmax0 - Vavmin0)/(Vavmax0 + Vavmin0)
print("Visibility: ", visibility)
print("")

Vavmax=max(Vav)
Vavmin=min(Vav)

#convert to phase
phase = []
for n in range(len(Vav)):
	v=Vav[n]
	#Vavmax=max(Vav)
	#Vavmin=min(Vav)
	#Vavmax=VavmaxArr[n]
	#Vavmin=VavminArr[n]
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
#print(minPhase_indices[0])
maxPhase_indices=np.where(phase==max(phase))
maxPhase_indices=maxPhase_indices[0]
#print("minphase vin: ",Vin[minPhase_indices[0]])
#print("minphase vap: ",Vap[minPhase_indices[0]])
#print("maxphase vin: ",Vin[maxPhase_indices[0]])
#print("maxphase vap: ",Vap[maxPhase_indices[0]])
print("")





#Stacked plot of all data
fig, axs = plt.subplots(6,1, num=238, sharex=True)
xmin=time_Vap_el_mins[0]
xmax=time_Vap_el_mins[-1]

#Vap
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


#Phase
axs[3].plot(time_Vav_el_mins, phase,  linestyle = 'none', marker = '.', markersize = 2)
axs[3].set_ylabel(r"Phase ($\degree$)")
axs[3].grid()

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
plt.show()




meanPhiArr = []
rangePhiArr = []
meanVavArr=[]
rangeVavArr=[]
minVavArr=[]
maxVavArr=[]
stdVavArr=[]
meanVapArr=[]
meanVinArr = []
meanTArr=[]


#phi = -2
t1 = 260
t2 = 300
ind1 = np.where(np.array(time_Vav_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vav_el_mins)==t2)
ind2=int(ind2[0])
print(phase[ind1])
print(phase[ind2])
meanphi = np.mean(phase[ind1:ind2])
rangephi = max(phase[ind1:ind2]) - min(phase[ind1:ind2])
print("mean phi: ", meanphi)
print("range phi: ", rangephi)
meanPhiArr.append(meanphi)
rangePhiArr.append(rangephi)

meanVav = np.mean(Vav[ind1:ind2])
rangeVav = max(Vav[ind1:ind2]) - min(Vav[ind1:ind2])
print("mean Vav: ", meanVav)
print("range Vav: ", rangeVav)
meanVavArr.append(meanVav)
minVavArr.append(min(Vav[ind1:ind2]))
maxVavArr.append(max(Vav[ind1:ind2]))
stdVavArr.append(np.std(Vav[ind1:ind2]))
rangeVavArr.append(rangeVav)

ind1 = np.where(np.array(time_Vap_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vap_el_mins)==t2)
ind2=int(ind2[0])
meanVap = np.mean(Vap[ind1:ind2])
meanVapArr.append(meanVap)

ind1 = np.where(np.array(time_Vin_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vin_el_mins)==t2)
ind2=int(ind2[0])
meanVin = np.mean(Vin[ind1:ind2])
meanVinArr.append(meanVin)

ind1 = np.where(np.array(time_T1_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_T1_el_mins)==t2)
ind2=int(ind2[0])
meanT = np.mean(T1[ind1:ind2])
meanTArr.append(meanT)
print("")

#phi = -32
t1 = 200
t2 = 240
ind1 = np.where(np.array(time_Vav_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vav_el_mins)==t2)
ind2=int(ind2[0])
print(phase[ind1])
print(phase[ind2])
meanphi = np.mean(phase[ind1:ind2])
rangephi = max(phase[ind1:ind2]) - min(phase[ind1:ind2])
print("mean phi: ", meanphi)
print("range phi: ", rangephi)
meanPhiArr.append(meanphi)
rangePhiArr.append(rangephi)

meanVav = np.mean(Vav[ind1:ind2])
rangeVav = max(Vav[ind1:ind2]) - min(Vav[ind1:ind2])
print("mean Vav: ", meanVav)
print("range Vav: ", rangeVav)
meanVavArr.append(meanVav)
rangeVavArr.append(rangeVav)
minVavArr.append(min(Vav[ind1:ind2]))
maxVavArr.append(max(Vav[ind1:ind2]))
stdVavArr.append(np.std(Vav[ind1:ind2]))


ind1 = np.where(np.array(time_Vap_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vap_el_mins)==t2)
ind2=int(ind2[0])
meanVap = np.mean(Vap[ind1:ind2])
meanVapArr.append(meanVap)

ind1 = np.where(np.array(time_Vin_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vin_el_mins)==t2)
ind2=int(ind2[0])
meanVin = np.mean(Vin[ind1:ind2])
meanVinArr.append(meanVin)

ind1 = np.where(np.array(time_T1_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_T1_el_mins)==t2)
ind2=int(ind2[0])
meanT = np.mean(T1[ind1:ind2])
meanTArr.append(meanT)
print("")

#phi = -56
t1=20
t2=60
ind1 = np.where(np.array(time_Vav_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vav_el_mins)==t2)
ind2=int(ind2[0])
print(phase[ind1])
print(phase[ind2])
meanphi = np.mean(phase[ind1:ind2])
rangephi = max(phase[ind1:ind2]) - min(phase[ind1:ind2])
print("mean phi: ", meanphi)
print("range phi: ", rangephi)
meanPhiArr.append(meanphi)
rangePhiArr.append(rangephi)

meanVav = np.mean(Vav[ind1:ind2])
rangeVav = max(Vav[ind1:ind2]) - min(Vav[ind1:ind2])
print("mean Vav: ", meanVav)
print("range Vav: ", rangeVav)
meanVavArr.append(meanVav)
rangeVavArr.append(rangeVav)
minVavArr.append(min(Vav[ind1:ind2]))
maxVavArr.append(max(Vav[ind1:ind2]))
stdVavArr.append(np.std(Vav[ind1:ind2]))


ind1 = np.where(np.array(time_Vap_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vap_el_mins)==t2)
ind2=int(ind2[0])
meanVap = np.mean(Vap[ind1:ind2])
meanVapArr.append(meanVap)


ind1 = np.where(np.array(time_Vin_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vin_el_mins)==t2)
ind2=int(ind2[0])
meanVin = np.mean(Vin[ind1:ind2])
meanVinArr.append(meanVin)

ind1 = np.where(np.array(time_T1_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_T1_el_mins)==t2)
ind2=int(ind2[0])
meanT = np.mean(T1[ind1:ind2])
meanTArr.append(meanT)
print("")


#phi = -60
t1=144
t2=184
ind1 = np.where(np.array(time_Vav_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vav_el_mins)==t2)
ind2=int(ind2[0])
print(phase[ind1])
print(phase[ind2])
meanphi = np.mean(phase[ind1:ind2])
rangephi = max(phase[ind1:ind2]) - min(phase[ind1:ind2])
print("mean phi: ", meanphi)
print("range phi: ", rangephi)
meanPhiArr.append(meanphi)
rangePhiArr.append(rangephi)

meanVav = np.mean(Vav[ind1:ind2])
rangeVav = max(Vav[ind1:ind2]) - min(Vav[ind1:ind2])
print("mean Vav: ", meanVav)
print("range Vav: ", rangeVav)
meanVavArr.append(meanVav)
rangeVavArr.append(rangeVav)
minVavArr.append(min(Vav[ind1:ind2]))
maxVavArr.append(max(Vav[ind1:ind2]))
stdVavArr.append(np.std(Vav[ind1:ind2]))


ind1 = np.where(np.array(time_Vap_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vap_el_mins)==t2)
ind2=int(ind2[0])
meanVap = np.mean(Vap[ind1:ind2])
meanVapArr.append(meanVap)

ind1 = np.where(np.array(time_Vin_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vin_el_mins)==t2)
ind2=int(ind2[0])
meanVin = np.mean(Vin[ind1:ind2])
meanVinArr.append(meanVin)

ind1 = np.where(np.array(time_T1_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_T1_el_mins)==t2)
ind2=int(ind2[0])
meanT = np.mean(T1[ind1:ind2])
meanTArr.append(meanT)
print("")




#phi = -85
t1=80
t2=120
ind1 = np.where(np.array(time_Vav_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vav_el_mins)==t2)
ind2=int(ind2[0])
print(phase[ind1])
print(phase[ind2])
meanphi = np.mean(phase[ind1:ind2])
rangephi = max(phase[ind1:ind2]) - min(phase[ind1:ind2])
print("mean phi: ", meanphi)
print("range phi: ", rangephi)
meanPhiArr.append(meanphi)
rangePhiArr.append(rangephi)

meanVav = np.mean(Vav[ind1:ind2])
rangeVav = max(Vav[ind1:ind2]) - min(Vav[ind1:ind2])
print("mean Vav: ", meanVav)
print("range Vav: ", rangeVav)
meanVavArr.append(meanVav)
rangeVavArr.append(rangeVav)
minVavArr.append(min(Vav[ind1:ind2]))
maxVavArr.append(max(Vav[ind1:ind2]))
stdVavArr.append(np.std(Vav[ind1:ind2]))


ind1 = np.where(np.array(time_Vap_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vap_el_mins)==t2)
ind2=int(ind2[0])
meanVap = np.mean(Vap[ind1:ind2])
meanVapArr.append(meanVap)

ind1 = np.where(np.array(time_Vin_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vin_el_mins)==t2)
ind2=int(ind2[0])
meanVin = np.mean(Vin[ind1:ind2])
meanVinArr.append(meanVin)

ind1 = np.where(np.array(time_T1_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_T1_el_mins)==t2)
ind2=int(ind2[0])
meanT = np.mean(T1[ind1:ind2])
meanTArr.append(meanT)
print("")


#phi = 25
t1=325
t2=326
ind1 = np.where(np.array(time_Vav_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vav_el_mins)==t2)
ind2=int(ind2[0])
print(phase[ind1])
print(phase[ind2])
meanphi = np.mean(phase[ind1:ind2])
rangephi = max(phase[ind1:ind2]) - min(phase[ind1:ind2])
print("mean phi: ", meanphi)
print("range phi: ", rangephi)
meanPhiArr.append(meanphi)
rangePhiArr.append(rangephi)

meanVav = np.mean(Vav[ind1:ind2])
rangeVav = max(Vav[ind1:ind2]) - min(Vav[ind1:ind2])
print("mean Vav: ", meanVav)
print("range Vav: ", rangeVav)
meanVavArr.append(meanVav)
rangeVavArr.append(rangeVav)
minVavArr.append(min(Vav[ind1:ind2]))
maxVavArr.append(max(Vav[ind1:ind2]))
stdVavArr.append(np.std(Vav[ind1:ind2]))

ind1 = np.where(np.array(time_Vap_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vap_el_mins)==t2)
ind2=int(ind2[0])
meanVap = np.mean(Vap[ind1:ind2])
meanVapArr.append(meanVap)

ind1 = np.where(np.array(time_Vin_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vin_el_mins)==t2)
ind2=int(ind2[0])
meanVin = np.mean(Vin[ind1:ind2])
meanVinArr.append(meanVin)

ind1 = np.where(np.array(time_T1_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_T1_el_mins)==t2)
ind2=int(ind2[0])
meanT = np.mean(T1[ind1:ind2])
meanTArr.append(meanT)
print("")


#phi = 26
t1=690
t2=730
ind1 = np.where(np.array(time_Vav_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vav_el_mins)==t2)
ind2=int(ind2[0])
print(phase[ind1])
print(phase[ind2])
meanphi = np.mean(phase[ind1:ind2])
rangephi = max(phase[ind1:ind2]) - min(phase[ind1:ind2])
print("mean phi: ", meanphi)
print("range phi: ", rangephi)
meanPhiArr.append(meanphi)
rangePhiArr.append(rangephi)

meanVav = np.mean(Vav[ind1:ind2])
rangeVav = max(Vav[ind1:ind2]) - min(Vav[ind1:ind2])
print("mean Vav: ", meanVav)
print("range Vav: ", rangeVav)
meanVavArr.append(meanVav)
rangeVavArr.append(rangeVav)
minVavArr.append(min(Vav[ind1:ind2]))
maxVavArr.append(max(Vav[ind1:ind2]))
stdVavArr.append(np.std(Vav[ind1:ind2]))

ind1 = np.where(np.array(time_Vap_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vap_el_mins)==t2)
ind2=int(ind2[0])
meanVap = np.mean(Vap[ind1:ind2])
meanVapArr.append(meanVap)

ind1 = np.where(np.array(time_Vin_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vin_el_mins)==t2)
ind2=int(ind2[0])
meanVin = np.mean(Vin[ind1:ind2])
meanVinArr.append(meanVin)

ind1 = np.where(np.array(time_T1_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_T1_el_mins)==t2)
ind2=int(ind2[0])
meanT = np.mean(T1[ind1:ind2])
meanTArr.append(meanT)
print("")


#phi = 46
t1=624
t2=664
ind1 = np.where(np.array(time_Vav_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vav_el_mins)==t2)
ind2=int(ind2[0])
print(phase[ind1])
print(phase[ind2])
meanphi = np.mean(phase[ind1:ind2])
rangephi = max(phase[ind1:ind2]) - min(phase[ind1:ind2])
print("mean phi: ", meanphi)
print("range phi: ", rangephi)
meanPhiArr.append(meanphi)
rangePhiArr.append(rangephi)

meanVav = np.mean(Vav[ind1:ind2])
rangeVav = max(Vav[ind1:ind2]) - min(Vav[ind1:ind2])
print("mean Vav: ", meanVav)
print("range Vav: ", rangeVav)
meanVavArr.append(meanVav)
rangeVavArr.append(rangeVav)
minVavArr.append(min(Vav[ind1:ind2]))
maxVavArr.append(max(Vav[ind1:ind2]))
stdVavArr.append(np.std(Vav[ind1:ind2]))

ind1 = np.where(np.array(time_Vap_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vap_el_mins)==t2)
ind2=int(ind2[0])
meanVap = np.mean(Vap[ind1:ind2])
meanVapArr.append(meanVap)

ind1 = np.where(np.array(time_Vin_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vin_el_mins)==t2)
ind2=int(ind2[0])
meanVin = np.mean(Vin[ind1:ind2])
meanVinArr.append(meanVin)

ind1 = np.where(np.array(time_T1_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_T1_el_mins)==t2)
ind2=int(ind2[0])
meanT = np.mean(T1[ind1:ind2])
meanTArr.append(meanT)
print("")

#phi = 67
t1=445
t2=485
ind1 = np.where(np.array(time_Vav_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vav_el_mins)==t2)
ind2=int(ind2[0])
print(phase[ind1])
print(phase[ind2])
meanphi = np.mean(phase[ind1:ind2])
rangephi = max(phase[ind1:ind2]) - min(phase[ind1:ind2])
print("mean phi: ", meanphi)
print("range phi: ", rangephi)
meanPhiArr.append(meanphi)
rangePhiArr.append(rangephi)

meanVav = np.mean(Vav[ind1:ind2])
rangeVav = max(Vav[ind1:ind2]) - min(Vav[ind1:ind2])
print("mean Vav: ", meanVav)
print("range Vav: ", rangeVav)
meanVavArr.append(meanVav)
rangeVavArr.append(rangeVav)
minVavArr.append(min(Vav[ind1:ind2]))
maxVavArr.append(max(Vav[ind1:ind2]))
stdVavArr.append(np.std(Vav[ind1:ind2]))

ind1 = np.where(np.array(time_Vap_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vap_el_mins)==t2)
ind2=int(ind2[0])
meanVap = np.mean(Vap[ind1:ind2])
meanVapArr.append(meanVap)

ind1 = np.where(np.array(time_Vin_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vin_el_mins)==t2)
ind2=int(ind2[0])
meanVin = np.mean(Vin[ind1:ind2])
meanVinArr.append(meanVin)

ind1 = np.where(np.array(time_T1_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_T1_el_mins)==t2)
ind2=int(ind2[0])
meanT = np.mean(T1[ind1:ind2])
meanTArr.append(meanT)
print("")



#phi = 68
t1=565
t2=605
ind1 = np.where(np.array(time_Vav_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vav_el_mins)==t2)
ind2=int(ind2[0])
print(phase[ind1])
print(phase[ind2])
meanphi = np.mean(phase[ind1:ind2])
rangephi = max(phase[ind1:ind2]) - min(phase[ind1:ind2])
print("mean phi: ", meanphi)
print("range phi: ", rangephi)
meanPhiArr.append(meanphi)
rangePhiArr.append(rangephi)

meanVav = np.mean(Vav[ind1:ind2])
rangeVav = max(Vav[ind1:ind2]) - min(Vav[ind1:ind2])
print("mean Vav: ", meanVav)
print("range Vav: ", rangeVav)
meanVavArr.append(meanVav)
rangeVavArr.append(rangeVav)
minVavArr.append(min(Vav[ind1:ind2]))
maxVavArr.append(max(Vav[ind1:ind2]))
stdVavArr.append(np.std(Vav[ind1:ind2]))

ind1 = np.where(np.array(time_Vap_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vap_el_mins)==t2)
ind2=int(ind2[0])
meanVap = np.mean(Vap[ind1:ind2])
meanVapArr.append(meanVap)

ind1 = np.where(np.array(time_Vin_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vin_el_mins)==t2)
ind2=int(ind2[0])
meanVin = np.mean(Vin[ind1:ind2])
meanVinArr.append(meanVin)

ind1 = np.where(np.array(time_T1_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_T1_el_mins)==t2)
ind2=int(ind2[0])
meanT = np.mean(T1[ind1:ind2])
meanTArr.append(meanT)
print("")

#phi = 85
t1=509
t2=549
ind1 = np.where(np.array(time_Vav_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vav_el_mins)==t2)
ind2=int(ind2[0])
print(phase[ind1])
print(phase[ind2])
meanphi = np.mean(phase[ind1:ind2])
rangephi = max(phase[ind1:ind2]) - min(phase[ind1:ind2])
print("mean phi: ", meanphi)
print("range phi: ", rangephi)
meanPhiArr.append(meanphi)
rangePhiArr.append(rangephi)
print(phase[ind1])
print(phase[ind2])



meanVav = np.mean(Vav[ind1:ind2])
rangeVav = max(Vav[ind1:ind2]) - min(Vav[ind1:ind2])
print("mean Vav: ", meanVav)
print("range Vav: ", rangeVav)
meanVavArr.append(meanVav)
rangeVavArr.append(rangeVav)
minVavArr.append(min(Vav[ind1:ind2]))
maxVavArr.append(max(Vav[ind1:ind2]))
stdVavArr.append(np.std(Vav[ind1:ind2]))

ind1 = np.where(np.array(time_Vap_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vap_el_mins)==t2)
ind2=int(ind2[0])
meanVap = np.mean(Vap[ind1:ind2])
meanVapArr.append(meanVap)

ind1 = np.where(np.array(time_Vin_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_Vin_el_mins)==t2)
ind2=int(ind2[0])
meanVin = np.mean(Vin[ind1:ind2])
meanVinArr.append(meanVin)

ind1 = np.where(np.array(time_T1_el_mins)==t1)
ind1=int(ind1[0])
ind2 = np.where(np.array(time_T1_el_mins)==t2)
ind2=int(ind2[0])
meanT = np.mean(T1[ind1:ind2])
meanTArr.append(meanT)
print("")

print(meanPhiArr)
print(rangePhiArr)
print(meanVavArr)
print(rangeVavArr)
print(meanVapArr)
print(meanVinArr)
print(meanTArr)





#Fit to sine curve
def fit_sin(tt, yy):
	'''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
	tt = np.array(tt)
	yy = np.array(yy)
	ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
	Fyy = abs(np.fft.fft(yy))
	guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
	guess_amp = np.std(yy) * 2.**0.5
	guess_offset = np.mean(yy)
	guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

	def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c
	popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
	A, w, p, c = popt
	print(A, w, p,c)
	f = w/(2.*np.pi)
	fitfunc = lambda t: A * np.sin(w*t + p) + c
	return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}

meanVapArr=np.array(meanVapArr)
meanVinArr=np.array(meanVinArr)
meanTArr=np.array(meanTArr)

fineVapArr= np.linspace(min(meanVapArr), max(meanVapArr), 100)
resVap=fit_sin(meanVapArr, meanVavArr)
VavfitArr_Vap = resVap["fitfunc"](fineVapArr)

fineVinArr= np.linspace(min(meanVinArr), max(meanVinArr), 100)
resVin=fit_sin(meanVinArr, meanVavArr)
VavfitArr_Vin = resVap["fitfunc"](fineVinArr)

fineTArr= np.linspace(min(meanTArr), max(meanTArr), 100)
resT=fit_sin(meanTArr, meanVavArr)
VavfitArr_T = resT["fitfunc"](fineTArr)


maxVavFit_Vap = max(VavfitArr_Vap)
minVavFit_Vap=min(VavfitArr_Vap)
visib_Vap = (maxVavFit_Vap-minVavFit_Vap)/(maxVavFit_Vap+minVavFit_Vap)

maxVavFit_Vin = max(VavfitArr_Vin)
minVavFit_Vin=min(VavfitArr_Vin)
visib_Vin = (maxVavFit_Vin-minVavFit_Vin)/(maxVavFit_Vin+minVavFit_Vin)


maxVavFit_T = max(VavfitArr_T)
minVavFit_T=min(VavfitArr_T)
visib_T = (maxVavFit_T-minVavFit_T)/(maxVavFit_T+minVavFit_T)

print(visib_Vap)
print(visib_Vin)
print(visib_T)

#Stacked plot of all data
fig, axs = plt.subplots(3,1, num=258)

#Phi vs Vap

Vavmaxfit = max(VavfitArr_Vap)
Vavminfit = min(VavfitArr_Vap)
axs[0].errorbar(meanVapArr, meanVavArr, yerr=stdVavArr, linestyle = 'none', marker = '.', markersize = 4)
axs[0].plot(fineVapArr,VavfitArr_Vap, '-r', label = "Visibility: {:.3f}".format(visib_Vap)+"\n"+"Min Vav Fit: {:.3f} mV".format(Vavminfit)+"\n"+"Max Vav Fit: {:.3f} mV".format(Vavmaxfit))
axs[0].set_ylabel(r"Mean $V_{av}$ (mV)")
axs[0].set_xlabel(r"Mean $V_{ap}$ (V)")
axs[0].legend()
axs[0].set_title("Phase vs. Voltage Sent to Power Supply "+ r"($V_{ap}$)")
axs[0].grid()

#Phi vs Vin
Vavmaxfit = max(VavfitArr_Vin)
Vavminfit = min(VavfitArr_Vin)
axs[1].errorbar(meanVinArr, meanVavArr, yerr=stdVavArr, linestyle = 'none', marker = '.', markersize = 4)
axs[1].plot(fineVinArr,VavfitArr_Vin, '-r', label = "Visibility: {:.3f}".format(visib_Vin)+"\n"+"Min Vav Fit: {:.3f} mV".format(Vavminfit)+"\n"+"Max Vav Fit: {:.3f} mV".format(Vavmaxfit))
axs[1].set_ylabel(r"Mean $V_{av}$ (mV)")
axs[1].set_xlabel(r"Mean $V_{in}$ (V)")
axs[1].legend()
axs[1].set_title("Phase vs. Actual Voltage of Power Supply "+ r"($V_{ap}$)")
axs[1].grid()

#Phi vs T
Vavmaxfit = max(VavfitArr_T)
Vavminfit = min(VavfitArr_T)
axs[2].errorbar(meanTArr, meanVavArr, yerr=stdVavArr, linestyle = 'none', marker = '.', markersize = 4)
axs[2].plot(fineTArr,VavfitArr_T, '-r',label = "Visibility: {:.3f}".format(visib_T)+"\n"+"Min Vav Fit: {:.3f} mV".format(Vavminfit)+"\n"+"Max Vav Fit: {:.3f} mV".format(Vavmaxfit))
axs[2].set_ylabel(r"Mean $V_{av}$ (mV)")
axs[2].set_xlabel(r"Mean T ($\degree$C)")
axs[2].set_title("Phase vs. Temp")
axs[2].legend()
axs[2].grid()

plt.subplots_adjust(hspace = 0.6)

#fig.suptitle(r"$\phi_{min}$"+" = {:.1f}".format(min(meanPhiArr)) + r", $\phi_{max}$"+" = {:.1f}".format(max(meanPhiArr)))
#fig.suptitle(r"$\phi_{min}$"+" = {:.1f}".format(phiminfit) + r", $\phi_{max}$"+" = {:.1f}".format(phimaxfit))
plt.show()
