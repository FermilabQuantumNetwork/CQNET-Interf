#This plots data from a 36 hour test run of the interferometer. The test run
#corresponded to the applied voltage trace defined by `VoltageTestIntf(Vmin,Vmax,numSteps)`
#from IntfScanFunc.py
#It retrieves data stored from the corresponding table in the database and then plots the data.
#Requirements: Python3, mysql, packages listed below

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import math
import pymysql
import os

#Start and end datetimes that define range of data to retrieve from mysql table
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

#Connect to mysql database
db = pymysql.connect(host="<IP ADDRESS>",  #Replace <IP ADDRESS> with the IP of computer with database. Local host if is same computer.
					 user="<USERNAME>", #Replace <USERNAME> with your username
					 passwd="<PASSWORD>",  #Replace <PASSWORD> with your password
					 db="teleportcommission", #name of database
					 charset='utf8mb4',
					 cursorclass=pymysql.cursors.DictCursor)

#Arrays to fill with data from mysql table
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
Wavelength = []
time_w = []

try:
	#Create cursor to select data from mysql.
	with db.cursor() as cur:
		#Mysql commands to select data from each column
		queryVap = "SELECT Vap, datetimeVap FROM "+TABLE_NAME+" WHERE datetimeVap BETWEEN {ts %s} AND {ts %s}"
		queryVin = "SELECT Vin, datetimeVin FROM "+TABLE_NAME+" WHERE datetimeVin BETWEEN {ts %s} AND {ts %s}"
		queryW = "SELECT Wavelength, datetimeW FROM "+TABLE_NAME+" WHERE datetimeW BETWEEN {ts %s} AND {ts %s}"
		queryT1 = "SELECT T1, datetimeT1 FROM "+TABLE_NAME+" WHERE datetimeT1 BETWEEN {ts %s} AND {ts %s}"
		queryVav = "SELECT Vav, datetimeVav FROM "+TABLE_NAME+" WHERE datetimeVav BETWEEN {ts %s} AND {ts %s}"
		queryP = "SELECT P, datetimeP FROM "+TABLE_NAME+" WHERE datetimeP BETWEEN {ts %s} AND {ts %s}"

		#Execute query and store data in array from Vap (applied voltage) column
		cur.execute(queryVap,(START_TIME_Vap,END_TIME_Vap,))
		row = cur.fetchone() #Retrieves one row from column
		while row is not None:
			Vap.append(row["Vap"])
			time_Vap.append(row["datetimeVap"])
			row = cur.fetchone()

		#Execute query and store data in array from Vin (voltage as read from meter) column
		cur.execute(queryVin,(START_TIME_Vin,END_TIME_Vin,))
		row = cur.fetchone()
		while row is not None:
			Vin.append(row["Vin"])
			time_Vin.append(row["datetimeVin"])
			row = cur.fetchone()

		#Execute query and store data in array from P (Power) column
		cur.execute(queryP,(START_TIME_P,END_TIME_P,))
		row = cur.fetchone()
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
			time_w.append(row["datetimeW"])
			row = cur.fetchone()
finally: #Once store the data of each column in separate arrays, close the database
	db.close()

#Get the first and last datetimes of the Vap data. The retrieved data falls within the
#bounds of the start and end times that were specified, but may not be exactly the same.
#NOTE: You might want to print out the start and end times to verify that are selecting
#data across same time span for all the different tables, if not the times may not line up.
time_Vap_first = str(time_Vap[0])
time_Vap_last = str(time_Vap[-1])
first_time_Vap = datetime.datetime.strptime(time_Vap_first,'%Y-%m-%d %H:%M:%S') #Strips the time from the datetime entry
time_Vap_dt = [] #Array of just the times
time_Vap_el = [] #Array of elapsed times

#Get the first and last times of the Vin data.
time_Vin_first = str(time_Vin[0])
time_Vin_last = str(time_Vin[-1])
first_time_Vin = datetime.datetime.strptime(time_Vin_first,'%Y-%m-%d %H:%M:%S')
time_Vin_dt=[]
time_Vin_el=[]

#Get the first and last times of the P data.
time_P_first = str(time_P[0])
time_P_last = str(time_P[-1])
first_time_P = datetime.datetime.strptime(time_P_first,'%Y-%m-%d %H:%M:%S')
time_P_dt=[]
time_P_el=[]

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
time_w_first = str(time_w[0])
time_w_last = str(time_w[-1])
first_time_w = datetime.datetime.strptime(time_w_first,'%Y-%m-%d %H:%M:%S')
time_W_dt=[]
time_W_el=[]

#Create the elapsed time array for Vap
for t in time_Vap:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime- first_time_Vap
	time_Vap_dt.append(datime)
	time_Vap_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes

#Create the elapsed time array for Vin
for t in time_Vin:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime - first_time_Vin
	time_Vin_dt.append(datime)
	time_Vin_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes

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
for t in time_w:
	t=str(t)
	datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
	elapsed = datime - first_time_w
	time_W_dt.append(datime)
	time_W_el.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes


Vavmin = min(Vav)
Vavmax =max(Vav)
visibility = (Vavmax - Vavmin)/(Vavmax + Vavmin)
print(visibility)

#Convert output voltage to phase
phase = []
for v in Vav:
	ph = (2*v-Vavmax -Vavmin)/(Vavmax-Vavmin)
	if ph > 1 or ph <-1:
		print("sinph: ", ph)
		print("vav: ", v)
		ph=round(ph)
	ph = np.arcsin(ph)*180/np.pi
	phase.append(ph)


#Stacked plot of all data
fig, axs = plt.subplots(6,1, num=1, sharex=True)
#Vapplied Plot
axs[0].plot(time_Vap_el, Vap,  linestyle = 'none', marker = '.', markersize = 2, label = "Vap")
axs[0].set_ylabel(r"$V_{ap}$ (V)")
axs[0].grid()
#Vin Plot
axs[1].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2, label = "Vin")
axs[1].set_ylabel(r"$V_{in}$ (V)")
axs[1].grid()
#Phase Plot
axs[2].plot(time_Vav_el, phase,  linestyle = 'none', marker = '.', markersize = 2, label = "phase")
axs[2].set_ylabel(r"Phase ($\degree$)")
axs[2].grid()
#Temp plot
axs[3].plot(time_T1_el, T1,  linestyle = 'none', marker = '.', markersize = 2, label = "temp1")
axs[3].set_ylabel(r"T ($\degree C$)")
axs[3].grid()
#Power plot
axs[4].plot(time_P_el, P,  linestyle = 'none', marker = '.', markersize = 2, label = 'power')
axs[4].set_ylabel(r"P ($\mu$ W)")
axs[4].grid()
#Wavelength Plot
axs[5].plot(time_W_el, Wavelength,  linestyle = 'none', marker = '.', markersize = 2, label = 'wavelength')
axs[5].set_ylim(1536, 1537)
axs[5].set_ylabel(r"$\lambda$ (nm)")
axs[5].grid()
xlims=axs[5].get_xlim()
xmin1=xlims[0]
xmax1=xlims[1]
fig.suptitle("Monitoring Interferometer from \n"+str(time_Vap[0]+datetime.timedelta(minutes=xmin1))+" to "+str(time_Vap[0]+datetime.timedelta(minutes=xmax1)))
plt.xlabel('Elapsed time (min)', fontsize =16)
figname = "weekend36cyclefig_FullStacked.png"
plt.savefig(figname)
print(figname)


#Power vs time
fig, axs = plt.subplots(1,1, num="2", sharex=True)
stdP = np.std(P)
meanP=np.mean(P)
axs.plot(time_P_el, P,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{P}$" + r" = {:.3f} $\mu W$, $\sigma_P$ = {:.3f} $\mu W$".format(meanP,stdP))
axs.grid()
axs.set_ylabel(r"Power ($\mu$W)")
axs.set_xlabel("Elapsed time (min)")
axs.legend(prop={'size':10})
fig.suptitle("Power from 10/19 to 10/21")
figname = "weekend36cyclefig_Power.png"
plt.savefig(figname)
print(figname)


#(Power-mean(Power))/Power vs time ("Percent P")
fig, axs = plt.subplots(1,1, num="3", sharex=True)
stdP = np.std(P)
meanP=np.mean(P)
percentP=[]
for i in range(len(P)):
	percentP.append(100*(P[i]-meanP)/meanP)
percentP = np.array(percentP)
axs.plot(time_P_el, percentP,  linestyle = 'none', marker = '.', markersize = 2)
axs.plot(time_P_el, np.zeros(len(time_P_el)), label = r"$\overline{P}$"+r" = {:.3f} $\mu W$".format(meanP))
axs.grid()
axs.set_ylabel(r"$100\times \Delta P/\overline{P}$ ($\%$)")
axs.set_xlabel("Elapsed time (min)")
axs.legend(prop={'size':10})
fig.suptitle(r"$100 \times \Delta P/\overline{P}$"+" from 10/19 to 10/21")
figname = "weekend36cyclefig_PowerPercent.png"
plt.savefig(figname)
print(figname)


#Wavelength vs time
fig, axs = plt.subplots(1,1, num="4", sharex=True)
stdW = np.std(Wavelength)
meanW = np.mean(Wavelength)
axs.plot(time_W_el, Wavelength,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{\lambda}$"+r" = {:.3f} nm, $\sigma_\lambda$ = {:.3e} nm".format(meanW,stdW))
axs.grid()
axs.set_ylim(1536.35,1536.45)
axs.legend(prop={'size':10})
axs.set_ylabel("Wavelength (nm)")
axs.set_xlabel("Elapsed time (min)")
fig.suptitle("Wavelength from 10/19 to 10/21")
figname="weekend36cyclefig_lambda.png"
plt.savefig(figname)
print(figname)


#Stacked plot of Vin, Phase, Temp for subsection of data corresponding to Vin = 0.5V
fig, axs = plt.subplots(3,1, num="6", sharex=True)
xmin = 715
xmax = 1195
dtVinMinInd = time_Vin_el.index(xmin)
dtVavMinInd =time_Vav_el.index(xmin)
dtT1MinInd =time_T1_el.index(xmin)
dtVinMaxInd = time_Vin_el.index(xmax)
dtVavMaxInd =time_Vav_el.index(xmax)
dtT1MaxInd =time_T1_el.index(xmax)
#Vin
stdVin = np.std(Vin[dtVinMinInd:dtVinMaxInd])
meanVin = np.mean(Vin[dtVinMinInd:dtVinMaxInd])
axs[0].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{V_{in}}$"+r" = {:.3f}V, $\sigma_V$ = {:.3e}V".format(meanVin,stdVin))
axs[0].set_ylabel(r"$V_{in}$ (V)")
axs[0].grid()
axs[0].legend(prop={'size':10})
#Phase
stdPhase = np.std(phase[dtVavMinInd:dtVavMaxInd])
meanPhase = np.mean(phase[dtVavMinInd:dtVavMaxInd])
axs[1].plot(time_Vav_el, phase,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{\phi}$"+r" = {:.3f}$\degree$, $\sigma_\phi$ = {:.3f}$\degree$".format(meanPhase,stdPhase))
axs[1].set_ylabel(r"$\phi$ ($\degree$)")
axs[1].grid()
axs[1].legend(prop={'size':10})
#Temp
stdT=np.std(T1[dtT1MinInd:dtT1MaxInd])
meanT=np.mean(T1[dtT1MinInd:dtT1MaxInd])
axs[2].set_ylim(23.5,25)
axs[2].plot(time_T1_el, T1,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{T}$"+r" = {:.3f}$\degree$C, $\sigma_T$ = {:.3e}$\degree$C".format(meanT,stdT))
axs[2].set_ylabel(r"T ($\degree C$)")
axs[2].set_xlabel("Elapsed time (min)")
axs[2].grid()
axs[2].legend(prop={'size':10})
axs[2].set_xlim(xmin, xmax)
fig.suptitle(r"$V_{in}$ = 0.5V")
figname="weekend36cyclefig_Const1.png"
plt.savefig(figname)
print(figname)


#Stacked plot of Vin, Phase % fluctuation, Temp % percent fluctuation
#for subsection of data corresponding to Vin = 0.5V
fig, axs = plt.subplots(3,1, num="7", sharex=True)
xmin = 715
xmax = 1195
dtVinMinInd = time_Vin_el.index(xmin)
dtVavMinInd =time_Vav_el.index(xmin)
dtT1MinInd =time_T1_el.index(xmin)
dtVinMaxInd = time_Vin_el.index(xmax)
dtVavMaxInd =time_Vav_el.index(xmax)
dtT1MaxInd =time_T1_el.index(xmax)
#Vin
axs[0].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2)
axs[0].set_ylabel(r"$V_{in}$ (V)")
axs[0].grid()
#Percent Phase
percentPhase = []
for i in range(len(phase)):
	percentPhase.append(100*(phase[i]-meanPhase)/meanPhase)
percentPhase = np.array(percentPhase)
axs[1].plot(time_Vav_el, percentPhase,  linestyle = 'none', marker = '.', markersize = 2)
axs[1].plot(time_Vav_el, np.zeros(len(time_Vav_el)), label = r"$\overline{\phi}$"+r" = {:.3f}$\degree$".format(meanPhase))
axs[1].set_ylabel(r"$100\times \Delta \phi/\overline{\phi}$ ($\%$)")
axs[1].grid()
axs[1].set_ylim(-150,200)
axs[1].legend(prop={'size':10})
stdT=np.std(T1[dtT1MinInd:dtT1MaxInd])
meanT=np.mean(T1[dtT1MinInd:dtT1MaxInd])
#Percent T
percentT1 = []
for i in range(len(T1)):
	percentT1.append(100*(T1[i]-meanT)/meanT)
percentT1 = np.array(percentT1)
axs[2].plot(time_T1_el, percentT1,  linestyle = 'none', marker = '.', markersize = 2)
axs[2].plot(time_T1_el, np.zeros(len(time_T1_el)), label = r"$\overline{T}$"+r" = {:.3f}$\degree$C".format(meanT))
axs[2].set_ylabel(r"$100\times \Delta T/\overline{T}$ ($\%$)")
axs[2].set_xlabel("Elapsed time (min)")
axs[2].grid()
axs[2].legend(prop={'size':10})
axs[2].set_ylim(-1,2)
axs[2].set_xlim(xmin, xmax)
fig.suptitle(r"$V_{in}$ = 0.5V")
figname="weekend36cyclefig_Const1_percent.png"
plt.savefig(figname)
print(figname)



#Stacked plot of Vin, Phase, Temp for subsection of data corresponding to Vin = 1V
fig, axs = plt.subplots(3,1, num="8", sharex=True)
xmin = 1204
xmax = 1685
dtVinMinInd = time_Vin_el.index(xmin)
dtVavMinInd =time_Vav_el.index(xmin)
dtT1MinInd =time_T1_el.index(xmin)
dtVinMaxInd = time_Vin_el.index(xmax)
dtVavMaxInd =time_Vav_el.index(xmax)
dtT1MaxInd =time_T1_el.index(xmax)
#Vin
stdVin = np.std(Vin[dtVinMinInd:dtVinMaxInd])
meanVin = np.mean(Vin[dtVinMinInd:dtVinMaxInd])
axs[0].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{V_{in}}$"+r" = {:.3f}V, $\sigma_V$ = {:.3e}V".format(meanVin,stdVin))
axs[0].set_ylabel(r"$V_{in}$ (V)")
axs[0].grid()
#Phase
stdPhase = np.std(phase[dtVavMinInd:dtVavMaxInd])
meanPhase = np.mean(phase[dtVavMinInd:dtVavMaxInd])
axs[1].plot(time_Vav_el, phase,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{\phi}$"+r" = {:.3f}$\degree$, $\sigma_\phi$ = {:.3f}$\degree$".format(meanPhase,stdPhase))
axs[1].set_ylabel(r"$\phi$ ($\degree$)")
axs[1].grid()
axs[1].legend(prop={'size':10})
axs[1].set_ylim(10,90)
stdT=np.std(T1[dtT1MinInd:dtT1MaxInd])
#Temp
meanT=np.mean(T1[dtT1MinInd:dtT1MaxInd])
axs[2].plot(time_T1_el, T1,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{T}$"+r" = {:.3f}$\degree$C, $\sigma_T$ = {:.3e}$\degree$C".format(meanT,stdT))
axs[2].set_ylabel(r"T ($\degree C$)")
axs[2].set_xlabel("Elapsed time (min)")
axs[2].grid()
axs[2].legend(prop={'size':10})
axs[2].set_ylim(24,25)
axs[2].set_xlim(xmin, xmax)
fig.suptitle(r"$V_{in}$ = 1V")
figname="weekend36cyclefig_Const2.png"
plt.savefig(figname)
print(figname)


#Stacked plot of Vin, Phase % fluctuation, Temp % percent fluctuation
#for subsection of data corresponding to Vin = 1V
fig, axs = plt.subplots(3,1, num="9", sharex=True)
xmin = 1204
xmax = 1685
dtVinMinInd = time_Vin_el.index(xmin)
dtVavMinInd =time_Vav_el.index(xmin)
dtT1MinInd =time_T1_el.index(xmin)
dtVinMaxInd = time_Vin_el.index(xmax)
dtVavMaxInd =time_Vav_el.index(xmax)
dtT1MaxInd =time_T1_el.index(xmax)
#Vin
axs[0].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2)
axs[0].set_ylabel(r"$V_{in}$ (V)")
axs[0].grid()
#Percent Phase
percentPhase = []
for i in range(len(phase)):
	percentPhase.append(100*(phase[i]-meanPhase)/meanPhase)
percentPhase = np.array(percentPhase)
axs[1].plot(time_Vav_el, percentPhase,  linestyle = 'none', marker = '.', markersize = 2)
axs[1].plot(time_Vav_el,np.zeros(len(time_Vav_el)),label = r"$\overline{\phi}$"+r" = {:.3f}$\degree$".format(meanPhase))
axs[1].set_ylabel(r"$100 \times \Delta \phi / \overline{\phi}$ ($\% $)")
axs[1].grid()
axs[1].set_ylim(-80,40)
axs[1].legend(prop={'size':10})
stdT=np.std(T1[dtT1MinInd:dtT1MaxInd])
meanT=np.mean(T1[dtT1MinInd:dtT1MaxInd])
#Percent T
percentT1 = []
for i in range(len(T1)):
	percentT1.append(100*(T1[i]-meanT)/meanT)
percentT1 = np.array(percentT1)
axs[2].plot(time_T1_el, percentT1,  linestyle = 'none', marker = '.', markersize = 2)#, label = r"$\overline{T}$"+r" = {:.3f}$\degree$C, $\sigma_T$ = {:.3e}$\degree$C".format(meanT,stdT))
axs[2].plot(time_T1_el,np.zeros(len(time_T1_el)),label = r"$\overline{T}$"+r" = {:.3f}$\degree$C".format(meanT))
axs[2].set_ylabel(r"$100\times \Delta T/\overline{T}$ ($\%$)")
axs[2].set_xlabel("Elapsed time (min)")
axs[2].grid()
axs[2].legend(prop={'size':10})
axs[2].set_ylim(-2,1)
axs[2].set_xlim(xmin, xmax)
fig.suptitle(r"$V_{in}$ = 1V")
figname="weekend36cyclefig_Const2_percent.png"
plt.savefig(figname)
print(figname)



#Stacked plot of Vin, Phase, Temp for zoomed in subsection of data
#corresponding to Vin = 1V
fig, axs = plt.subplots(3,1, num="10", sharex=True)
xmin = 1400
xmax = 1685
dtVinMinInd = time_Vin_el.index(xmin)
dtVavMinInd =time_Vav_el.index(xmin)
dtT1MinInd =time_T1_el.index(xmin)
dtVinMaxInd = time_Vin_el.index(xmax)
dtVavMaxInd =time_Vav_el.index(xmax)
dtT1MaxInd =time_T1_el.index(xmax)
#Vin
stdVin = np.std(Vin[dtVinMinInd:dtVinMaxInd])
meanVin = np.mean(Vin[dtVinMinInd:dtVinMaxInd])
axs[0].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{V_{in}}$"+r" = {:.3f}V, $\sigma_V$ = {:.3e}V".format(meanVin,stdVin))
axs[0].set_ylabel(r"$V_{in}$ (V)")
axs[0].grid()
axs[0].legend(prop={'size':10})
#Phase
stdPhase = np.std(phase[dtVavMinInd:dtVavMaxInd])
meanPhase = np.mean(phase[dtVavMinInd:dtVavMaxInd])
axs[1].plot(time_Vav_el, phase,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{\phi}$"+r" = {:.3f}$\degree$, $\sigma_\phi$ = {:.3f}$\degree$".format(meanPhase,stdPhase))
axs[1].set_ylabel(r"$\phi$ ($\degree$)")
axs[1].grid()
axs[1].legend(prop={'size':10})
axs[1].set_ylim(50,90)
stdT=np.std(T1[dtT1MinInd:dtT1MaxInd])
#Temp
meanT=np.mean(T1[dtT1MinInd:dtT1MaxInd])
axs[2].plot(time_T1_el, T1,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{T}$"+r" = {:.3f}$\degree$C, $\sigma_T$ = {:.3e}$\degree$C".format(meanT,stdT))
axs[2].set_ylabel(r"T ($\degree C$)")
axs[2].set_xlabel("Elapsed time (min)")
axs[2].grid()
axs[2].legend(prop={'size':10})
axs[2].set_xlim(xmin, xmax)
axs[2].set_ylim(24.2,24.6)
fig.suptitle(r"$V_{in}$ = 1V")
figname="weekend36cyclefig_Const2_Zoom.png"
plt.savefig(figname)
print(figname)

#Stacked plot of Vin, Phase % fluctuation, Temp % percent fluctuation
#for zoomed in subsection of data corresponding to Vin = 1V
fig, axs = plt.subplots(3,1, num="11", sharex=True)
xmin = 1400
xmax = 1685
dtVinMinInd = time_Vin_el.index(xmin)
dtVavMinInd =time_Vav_el.index(xmin)
dtT1MinInd =time_T1_el.index(xmin)
dtVinMaxInd = time_Vin_el.index(xmax)
dtVavMaxInd =time_Vav_el.index(xmax)
dtT1MaxInd =time_T1_el.index(xmax)
#Vin
axs[0].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2)
axs[0].set_ylabel(r"$V_{in}$ (V)")
axs[0].grid()
#Percent Phase
percentPhase = []
for i in range(len(phase)):
	percentPhase.append(100*(phase[i]-meanPhase)/meanPhase)
percentPhase = np.array(percentPhase)
axs[1].plot(time_Vav_el, percentPhase,  linestyle = 'none', marker = '.', markersize = 2)#, label = r"$\overline{\phi}$"+r" = {:.3f}$\degree$, $\sigma_\phi$ = {:.3f}$\degree$".format(meanPhase,stdPhase))
axs[1].plot(time_Vav_el,np.zeros(len(time_Vav_el)),label = r"$\overline{\phi}$"+r" = {:.3f}$\degree$".format(meanPhase))
axs[1].set_ylabel(r"$100 \times \Delta \phi/\overline{\phi}$ ($\%$)")
axs[1].grid()
axs[1].set_ylim(-10,20)
axs[1].legend(prop={'size':10})
stdT=np.std(T1[dtT1MinInd:dtT1MaxInd])
meanT=np.mean(T1[dtT1MinInd:dtT1MaxInd])
#Percent T
percentT1 = []
for i in range(len(T1)):
	percentT1.append(100*(T1[i]-meanT)/meanT)
percentT1 = np.array(percentT1)
axs[2].plot(time_T1_el, percentT1,  linestyle = 'none', marker = '.', markersize = 2)#, label = r"$\overline{T}$"+r" = {:.3f}$\degree$C, $\sigma_T$ = {:.3e}$\degree$C".format(meanT,stdT))
axs[2].plot(time_T1_el,np.zeros(len(time_T1_el)),label = r"$\overline{T}$"+r" = {:.3f}$\degree$C".format(meanT))
axs[2].set_ylabel(r"$100\times \Delta T/\overline{T}$ ($\%$)")
axs[2].set_xlabel("Elapsed time (min)")
axs[2].grid()
axs[2].set_ylim(-1,2)
axs[2].legend(prop={'size':10})
axs[2].set_xlim(xmin, xmax)
fig.suptitle(r"$V_{in}$ = 1V")
figname="weekend36cyclefig_Const2_percent_Zoom.png"
plt.savefig(figname)
print(figname)


#Stacked plot of Vin, Phase, Temp for subsection of data corresponding to Vin = 2V
fig, axs = plt.subplots(3,1, num="12", sharex=True)
xmin = 1690
xmax = 2170
dtVinMinInd = time_Vin_el.index(xmin)
dtVavMinInd =time_Vav_el.index(xmin)
dtT1MinInd =time_T1_el.index(xmin)
dtVinMaxInd = time_Vin_el.index(xmax)
dtVavMaxInd =time_Vav_el.index(xmax)
dtT1MaxInd =time_T1_el.index(xmax)
#Vin
stdVin = np.std(Vin[dtVinMinInd:dtVinMaxInd])
meanVin = np.mean(Vin[dtVinMinInd:dtVinMaxInd])
axs[0].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{V_{in}}$"+r" = {:.3f}V, $\sigma_V$ = {:.3e}V".format(meanVin,stdVin))
axs[0].set_ylabel(r"$V_{in}$ (V)")
axs[0].grid()
axs[0].legend(prop={'size':10})
#Phase
stdPhase = np.std(phase[dtVavMinInd:dtVavMaxInd])
meanPhase = np.mean(phase[dtVavMinInd:dtVavMaxInd])
axs[1].plot(time_Vav_el, phase,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{\phi}$"+r" = {:.3f}$\degree$, $\sigma_\phi$ = {:.3f}$\degree$".format(meanPhase,stdPhase))
axs[1].set_ylabel(r"$\phi$ ($\degree$)")
axs[1].grid()
axs[1].legend(prop={'size':10})
stdT=np.std(T1[dtT1MinInd:dtT1MaxInd])
#Temp
meanT=np.mean(T1[dtT1MinInd:dtT1MaxInd])
axs[2].plot(time_T1_el, T1,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{T}$"+r" = {:.3f}$\degree$C, $\sigma_T$ = {:.3e}$\degree$C".format(meanT,stdT))
axs[2].set_ylabel(r"T ($\degree C$)")
axs[2].set_xlabel("Elapsed time (min)")
axs[2].grid()
axs[2].legend(prop={'size':10})
axs[2].set_xlim(xmin, xmax)
axs[2].set_ylim(24.2,26)
fig.suptitle(r"$V_{in}$ = 1V")
figname="weekend36cyclefig_Const3.png"
plt.savefig(figname)
print(figname)


#Stacked plot of Vin, Phase % fluctuation, Temp % percent fluctuation
#for subsection of data corresponding to Vin = 2V
fig, axs = plt.subplots(3,1, num="13", sharex=True)
xmin = 1690
xmax = 2170
dtVinMinInd = time_Vin_el.index(xmin)
dtVavMinInd =time_Vav_el.index(xmin)
dtT1MinInd =time_T1_el.index(xmin)
dtVinMaxInd = time_Vin_el.index(xmax)
dtVavMaxInd =time_Vav_el.index(xmax)
dtT1MaxInd =time_T1_el.index(xmax)
stdPhase = np.std(phase[dtVavMinInd:dtVavMaxInd])
meanPhase = np.mean(phase[dtVavMinInd:dtVavMaxInd])
#Vin
axs[0].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2)
axs[0].set_ylabel(r"$V_{in}$ (V)")
axs[0].grid()
#Percent Phase
percentPhase = []
for i in range(len(phase)):
	percentPhase.append(100*(phase[i]-meanPhase)/meanPhase)
percentPhase = np.array(percentPhase)
axs[1].plot(time_Vav_el, percentPhase,  linestyle = 'none', marker = '.', markersize = 2)
axs[1].plot(time_Vav_el,np.zeros(len(time_Vav_el)),label = r"$\overline{\phi}$"+r" = {:.3f}$\degree$".format(meanPhase))
axs[1].set_ylabel(r"$100\times \Delta \phi/\overline{\phi}$ ($\%$)")
axs[1].grid()
axs[1].legend(prop={'size':10})
stdT=np.std(T1[dtT1MinInd:dtT1MaxInd])
meanT=np.mean(T1[dtT1MinInd:dtT1MaxInd])
#Percent T
percentT1 = []
for i in range(len(T1)):
	percentT1.append(100*(T1[i]-meanT)/meanT)
percentT1 = np.array(percentT1)
axs[2].plot(time_T1_el, percentT1,  linestyle = 'none', marker = '.', markersize = 2)#, label = r"$\overline{T}$"+r" = {:.3f}$\degree$C, $\sigma_T$ = {:.3e}$\degree$C".format(meanT,stdT))
axs[2].plot(time_T1_el,np.zeros(len(time_T1_el)),label = r"$\overline{T}$"+r" = {:.3f}$\degree$C".format(meanT))
axs[2].set_ylabel(r"$100 \times \Delta T)/\overline{T}$ ($\%$)")
axs[2].set_xlabel("Elapsed time (min)")
axs[2].grid()
axs[2].set_ylim(-4,1)
axs[2].legend(prop={'size':10})
axs[2].set_xlim(xmin, xmax)
fig.suptitle(r"$V_{in}$ = 2V")
figname="weekend36cyclefig_Const3_percent.png"
plt.savefig(figname)
print(figname)


#Stacked plot of Vin, Phase, Temp for zoomed in subsection of data
#corresponding to Vin = 2V
fig, axs = plt.subplots(3,1, num="14", sharex=True)
xmin = 1900
xmax = 2170
dtVinMinInd = time_Vin_el.index(xmin)
dtVavMinInd =time_Vav_el.index(xmin)
dtT1MinInd =time_T1_el.index(xmin)
dtVinMaxInd = time_Vin_el.index(xmax)
dtVavMaxInd =time_Vav_el.index(xmax)
dtT1MaxInd =time_T1_el.index(xmax)
#Vin
stdVin = np.std(Vin[dtVinMinInd:dtVinMaxInd])
meanVin = np.mean(Vin[dtVinMinInd:dtVinMaxInd])
axs[0].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{V_{in}}$"+r" = {:.3f}V, $\sigma_V$ = {:.3e}V".format(meanVin,stdVin))
axs[0].set_ylabel(r"$V_{in}$ (V)")
axs[0].grid()
#Phase
stdPhase = np.std(phase[dtVavMinInd:dtVavMaxInd])
meanPhase = np.mean(phase[dtVavMinInd:dtVavMaxInd])
axs[1].plot(time_Vav_el, phase,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{\phi}$"+r" = {:.3f}$\degree$, $\sigma_\phi$ = {:.3f}$\degree$".format(meanPhase,stdPhase))
axs[1].set_ylabel(r"$\phi$ ($\degree$)")
axs[1].grid()
axs[1].legend(prop={'size':10})
axs[1].set_ylim(25, 50)
stdT=np.std(T1[dtT1MinInd:dtT1MaxInd])
#Temp
meanT=np.mean(T1[dtT1MinInd:dtT1MaxInd])
axs[2].plot(time_T1_el, T1,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\overline{T}$"+r" = {:.3f}$\degree$C, $\sigma_T$ = {:.3e}$\degree$C".format(meanT,stdT))
axs[2].set_ylabel(r"T ($\degree C$)")
axs[2].set_xlabel("Elapsed time (min)")
axs[2].grid()
axs[2].legend(prop={'size':10})
axs[2].set_xlim(xmin, xmax)
axs[2].set_ylim(25, 26)
fig.suptitle(r"$V_{in}$ = 2V")
figname="weekend36cyclefig_Const3_Zoom.png"
plt.savefig(figname)
print(figname)



#Stacked plot of Vin, Phase % fluctuation, Temp % percent fluctuation
#for zoomed in subsection of data corresponding to Vin = 2V
fig, axs = plt.subplots(3,1, num="15", sharex=True)
xmin = 1900
xmax = 2170
dtVinMinInd = time_Vin_el.index(xmin)
dtVavMinInd =time_Vav_el.index(xmin)
dtT1MinInd =time_T1_el.index(xmin)
dtVinMaxInd = time_Vin_el.index(xmax)
dtVavMaxInd =time_Vav_el.index(xmax)
dtT1MaxInd =time_T1_el.index(xmax)
#Vin
axs[0].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2)
axs[0].set_ylabel(r"$V_{in}$ (V)")
axs[0].grid()
#axs[0].legend(prop={'size':10})
#Percent Phase
percentPhase = []
for i in range(len(phase)):
	percentPhase.append(100*(phase[i]-meanPhase)/meanPhase)
percentPhase = np.array(percentPhase)
axs[1].plot(time_Vav_el, percentPhase,  linestyle = 'none', marker = '.', markersize = 2)
axs[1].plot(time_Vav_el,np.zeros(len(time_Vav_el)),label = r"$\overline{\phi}$"+r" = {:.3f}$\degree$".format(meanPhase))
axs[1].set_ylabel(r"$100 \times \Delta \phi/\overline{\phi}$ ($\%$)")
axs[1].grid()
axs[1].set_ylim(-20,20)
axs[1].legend(prop={'size':10})
stdT=np.std(T1[dtT1MinInd:dtT1MaxInd])
meanT=np.mean(T1[dtT1MinInd:dtT1MaxInd])
#Percent T
percentT1 = []
for i in range(len(T1)):
	percentT1.append(100*(T1[i]-meanT)/meanT)
percentT1 = np.array(percentT1)
axs[2].plot(time_T1_el, percentT1,  linestyle = 'none', marker = '.', markersize = 2)
axs[2].plot(time_T1_el,np.zeros(len(time_T1_el)), label=r"$\overline{T}$"+r" = {:.3f}$\degree$C".format(meanT))
axs[2].set_ylabel(r"$100 \times \Delta T/\overline{T}$ $\%$")
axs[2].set_xlabel("Elapsed time (min)")
axs[2].grid()
axs[2].set_ylim(-0.5,0.5)
axs[2].legend(prop={'size':10})
axs[2].set_xlim(xmin, xmax)
fig.suptitle(r"$V_{in}$ = 2V")
figname="weekend36cyclefig_Const3_percent_Zoom.png"
plt.savefig(figname)
print(figname)


#Plot of data used to determine visibility
fig, axs = plt.subplots(3,1, num="16", sharex=True)
xmin = 0
xmax = 710
dtVinMinInd = time_Vin_el.index(xmin)
dtVavMinInd =time_Vav_el.index(xmin)
dtT1MinInd =time_T1_el.index(xmin)
dtVinMaxInd = time_Vin_el.index(xmax)
dtVavMaxInd =time_Vav_el.index(xmax)
dtT1MaxInd =time_T1_el.index(xmax)
#Vin
axs[0].plot(time_Vin_el, Vin,  linestyle = 'none', marker = '.', markersize = 2)
axs[0].set_ylabel(r"$V_{in}$ (V)")
axs[0].grid()
#Phase
minPhase = np.nanmin(phase[dtVavMinInd:dtVavMaxInd])
maxPhase = np.nanmax(phase[dtVavMinInd:dtVavMaxInd])
axs[1].set_title(r"$\phi_{min}$ = "+r"{:.3f}$\degree$, ".format(minPhase) +"$\phi_{max}$ = "+r"{:.3f}$\degree$".format(maxPhase), fontsize=10)
axs[1].plot(time_Vav_el, phase,  linestyle = 'none', marker = '.', markersize = 2, label = r"$\phi_{min}$ = "+r"{:.3f}$\degree$".format(minPhase) +"\n"+r"$\phi_{max}$ = "+r"{:.3f}$\degree$".format(maxPhase))
axs[1].grid()
#Temp
minT=np.min(T1[dtT1MinInd:dtT1MaxInd])
maxT=np.max(T1[dtT1MinInd:dtT1MaxInd])
axs[2].set_title(r"$T_{min}$ = "+r"{:.3f}$\degree C$, ".format(minT)+ r"$T_{max}$ = "+r"{:.3f}$\degree C$".format(maxT), fontsize=10)
axs[2].plot(time_T1_el, T1,  linestyle = 'none', marker = '.', markersize = 2, label =  r"$T_{min}$ = "+r"{:.3f}$\degree C$".format(minT) +"\n"+r"$T_{max}$ = "+r"{:.3f}$\degree C$".format(maxT))
axs[2].set_ylabel(r"T ($\degree C$)")
axs[2].set_xlabel("Elapsed time (min)")
axs[2].grid()
axs[2].set_xlim(xmin, xmax)
fig.suptitle(r"max($V_{av}$)"+" = {:.3f}V,".format(Vavmin)+r" max($V_{av}$)"+" = {:.3f}V".format(Vavmax)+", Visibility = {:.3f}".format(visibility))
figname="weekend36cyclefig_Visib.png"
plt.savefig(figname)
print(figname)
