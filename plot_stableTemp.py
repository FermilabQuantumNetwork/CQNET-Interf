#This plots data from an overnight test run of the interferometer. The test run
#corresponded to a constant applied voltage trace to test the long term stability
#using a peltier thermal feedback control.
#It retrieves data stored from the corresponding tables in the database and then plots the data.
#Whereas `plot_36hours.py` retrieves data all from the same table, this retrieves
#data from separate tables, one for each parameter.
#Requirements: Python3, mysql, packages listed below

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import math
import pymysql
import os

#Start and end datetimes that define range of data to retrieve from mysql table
START_TIME_Vap = '2019-10-23 18:19:00'
END_TIME_Vap = '2019-10-24 07:19:00'

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


#Connect to mysql database
db = pymysql.connect(host="192.168.0.125",  # this PC
		             user="inqnet1",
                     passwd="Teleport1536!",  # your password
                     db="teleportcommission", #Name of database
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

#Arrays to fill with data from mysql table
P = []
time_P = []
Vav=[]
time_Vav=[]
T1 = []
time_T1 = []
Wavelength = []
time_W = []

try:
    #Create cursor to select data from mysql.
    with db.cursor() as cur:
        #Mysql commands to select data from each column
        TABLE_NAME = "Wavelength"
        queryW = "SELECT Wavelength, datetimeW FROM "+TABLE_NAME+" WHERE datetimeW BETWEEN {ts %s} AND {ts %s}"
        TABLE_NAME = "Temp"
        queryT1 = "SELECT T1, datetimeT1 FROM "+TABLE_NAME+" WHERE datetimeT1 BETWEEN {ts %s} AND {ts %s}"
        TABLE_NAME = "Vav"
        queryVav = "SELECT Vav, datetimeVav FROM "+TABLE_NAME+" WHERE datetimeVav BETWEEN {ts %s} AND {ts %s}"
        TABLE_NAME = "Power"
        queryP = "SELECT P, datetimeP FROM "+TABLE_NAME+" WHERE datetimeP BETWEEN {ts %s} AND {ts %s}"

        #Execute query and store data in array from P (Power) column
        cur.execute(queryP,(START_TIME_P,END_TIME_P,))
        row = cur.fetchone() #Retrieves one row from column
        while row is not None:
            P.append(1000000*row["P"])
            time_P.append(row["datetimeP"])
            row = cur.fetchone()

        #Execute query and store data in array from Vav (Average output voltage) column
        cur.execute(queryVav,(START_TIME_Vav,END_TIME_Vav,))
        row = cur.fetchone()
        while row is not None:
            Vav.append(row["Vav"])
            time_Vav.append(row["datetimeVav"])
            row = cur.fetchone()

        #Execute query and store data in array from T1 (Temperature) column
        cur.execute(queryT1,(START_TIME_T1,END_TIME_T1,))
        row = cur.fetchone()
        while row is not None:
            T1.append(row["T1"])
            time_T1.append(row["datetimeT1"])
            row = cur.fetchone()

        #Execute query and store data in array from Wavelength column
        cur.execute(queryW,(START_TIME_W,END_TIME_W,))
        row = cur.fetchone()
        while row is not None:
            Wavelength.append(row["Wavelength"])
            time_W.append(row["datetimeW"])
            row = cur.fetchone()
finally: #Once store the data of each column in separate arrays, close the database
    db.close()

#Get the first and last datetimes of the P data. The retrieved data falls within the
#bounds of the start and end times that were specified, but may not be exactly the same.
time_P_first = str(time_P[0])
print(time_P_first)
time_P_last = str(time_P[-1])
first_time_P = datetime.datetime.strptime(time_P_first,'%Y-%m-%d %H:%M:%S') #Strips the time from the datetime entry
time_P_dt=[] #Array of just the times
time_P_el=[] #Array of elapsed times

#Get the first and last times of the Vav data.
time_Vav_first = str(time_Vav[0])
time_Vav_last = str(time_Vav[-1])
first_time_Vav = datetime.datetime.strptime(time_Vav_first,'%Y-%m-%d %H:%M:%S')
time_Vav_dt = []
time_Vav_el = []

#Get the first and last times of the T1 data.
time_T1_first = str(time_T1[0])
time_T1_last = str(time_T1[-1])
first_time_T1 = datetime.datetime.strptime(time_T1_first,'%Y-%m-%d %H:%M:%S')
time_T1_dt=[]
time_T1_el=[]

#Get the first and last times of the Wavelength data.
time_W_first = str(time_W[0])
time_W_last = str(time_W[-1])
first_time_W = datetime.datetime.strptime(time_W_first,'%Y-%m-%d %H:%M:%S')
time_W_dt=[]
time_W_el=[]


#Create the elapsed time array for P
for t in time_P:
    t=str(t)
    datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    elapsed = datime - first_time_P
    time_P_dt.append(datime)
    time_P_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
#Create the elapsed time array for Vav
for t in time_Vav:
    t=str(t)
    datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    elapsed = datime- first_time_Vav
    time_Vav_dt.append(datime)
    time_Vav_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
#Create the elapsed time array for T1
for t in time_T1:
    t=str(t)
    datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    elapsed = datime - first_time_T1
    time_T1_dt.append(datime)
    time_T1_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
#Create the elapsed time array for Wavelength
for t in time_W:
    t=str(t)
    datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    elapsed = datime - first_time_W
    time_W_dt.append(datime)
    time_W_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes



Vavmin = min(Vav)
Vavmax =max(Vav)
print(Vavmin)
print(Vavmax)
visibility = (Vavmax - Vavmin)/(Vavmax + Vavmin)
print(visibility)
print("")

#Convert output voltage to phase
phase = []
for v in Vav:
    ph = (2*v-Vavmax -Vavmin)/(Vavmax-Vavmin)
    if ph >1 or ph<-1:
        print("sinph: ",ph)
        print("vav: ",v)
    ph = np.arcsin(ph)*180/np.pi
    phase.append(ph)


#Stacked plot of all data
fig, axs = plt.subplots(5,1, num=1, sharex=True)
#Vav plot
axs[0].plot(time_Vav_el, Vav,  linestyle = 'none', marker = '.', markersize = 2, label = "phase")
axs[0].set_ylabel(r"Vav (V)")
axs[0].grid()
#Phase plot
axs[1].plot(time_Vav_el, phase,  linestyle = 'none', marker = '.', markersize = 2, label = "phase")
axs[1].set_ylabel(r"Phase ($\degree$)")
axs[1].grid()
#Temp plot
axs[2].plot(time_T1_el, T1,  linestyle = 'none', marker = '.', markersize = 2, label = "temp1")
axs[2].set_ylabel(r"T ($\degree C$)")
axs[2].grid()
#Power plot
axs[3].plot(time_P_el, P,  linestyle = 'none', marker = '.', markersize = 2, label = 'power')
axs[3].set_ylabel(r"P ($\mu$ W)")
axs[3].grid()
#Wavelength
axs[4].plot(time_W_el, Wavelength,  linestyle = 'none', marker = '.', markersize = 2, label = 'wavelength')
axs[4].set_ylim(1536, 1537)
axs[4].set_ylabel(r"$\lambda$ (nm)")
axs[4].grid()
xlims=axs[3].get_xlim()
xmin1=xlims[0]
xmax1=xlims[1]
fig.suptitle("Monitoring Interferometer from \n"+str(time_Vav[0]+datetime.timedelta(minutes=xmin1))+" to "+str(time_Vav[0]+datetime.timedelta(minutes=xmax1)))
plt.xlabel('Elapsed time (min)', fontsize =16)
figname = "constTempOvernight.png"
plt.savefig(figname)
print(figname)
fig, axs = plt.subplots(5,1, num=1, sharex=True)


#Stable region plot
fig, axs = plt.subplots(3,1, num="6", sharex=True)
xmin = 100
xmax = 425
dtVavMinInd =time_Vav_el.index(xmin)
dtT1MinInd =time_T1_el.index(xmin)
dtPMinInd = time_P_el.index(xmin)
dtVavMaxInd =time_Vav_el.index(xmax)
dtT1MaxInd =time_T1_el.index(xmax)
dtPMaxInd = time_P_el.index(xmax)
#Phase
stdPhase = np.std(phase[dtVavMinInd:dtVavMaxInd])
meanPhase = np.mean(phase[dtVavMinInd:dtVavMaxInd])
axs[0].plot(time_Vav_el, phase,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{\phi}$"+r" = {:.3f}$\degree$, $\sigma_\phi$ = {:.3f}$\degree$".format(meanPhase,stdPhase))
axs[0].set_ylabel(r"$\phi$ ($\degree$)")
axs[0].set_ylim(50,90)
axs[0].grid()
axs[0].legend(prop={'size':10})
#Temp
stdT=np.std(T1[dtT1MinInd:dtT1MaxInd])
meanT=np.mean(T1[dtT1MinInd:dtT1MaxInd])
axs[1].set_ylim(17,18)
axs[1].plot(time_T1_el, T1,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{T}$"+r" = {:.3f}$\degree$C, $\sigma_T$ = {:.3e}$\degree$C".format(meanT,stdT))
axs[1].set_ylabel(r"T ($\degree C$)")
axs[1].set_xlabel("Elapsed time (min)")
axs[1].grid()
axs[1].legend(prop={'size':10})
axs[1].set_xlim(xmin, xmax)
#Power
stdP=np.std(P[dtPMinInd:dtPMaxInd])
meanP=np.mean(P[dtPMinInd:dtPMaxInd])
axs[2].set_ylim(1065,1070)
axs[2].plot(time_P_el, P,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{P}$"+r" = {:.3f}$\mu$W, $\sigma_P$ = {:.3e}$\mu$W".format(meanP,stdP))
axs[2].set_ylabel(r"P ($\mu W$)")
axs[2].set_xlabel("Elapsed time (min)")
axs[2].grid()
axs[2].legend(prop={'size':10})
axs[2].set_xlim(xmin, xmax)
fig.suptitle(r"Stable Region")
figname="constTempOvernight_stable.png"
plt.savefig(figname)
print(figname)
