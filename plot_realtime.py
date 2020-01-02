#!/usr/bin/python2.7

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import tkinter
#matplotlib.use('TkAgg')
import datetime
import math
import pymysql
import os
import time

figname = "plot_realtime.png"

START_TIME = '2019-11-19 16:31:00'
END_TIME = 'NOW()'




#connect to database


T1 = []
time_T1 = []
Vap = []
time_Vap = []
Vin=[]
time_Vin = []

try:
	n=0
	while True:
		db = pymysql.connect(host="192.168.0.125",  # this PC
							 user="inqnet1",
							 passwd="Teleport1536!",  # your password
							 db="teleportcommission",
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)
		n=n+1
		with db.cursor() as cur:

			TABLE_NAME = "VapVin"
			queryVapVin = "SELECT Vap, Vin,datetimeVap,datetimeVin FROM "+TABLE_NAME+" WHERE datetimeVap BETWEEN {ts %s} AND NOW()"
			TABLE_NAME = "Temp"
			queryT1 = "SELECT T1, datetimeT1 FROM "+TABLE_NAME+" WHERE datetimeT1 BETWEEN {ts %s} AND NOW()"


			cur.execute(queryT1, (START_TIME,))
			row = cur.fetchone()
			while row is not None:
				T1.append(row["T1"])
				time_T1.append(row["datetimeT1"])
				row = cur.fetchone()

			cur.execute(queryVapVin, (START_TIME,))
			row = cur.fetchone()
			while row is not None:
				Vap.append(row["Vap"])
				time_Vap.append(row["datetimeVap"])
				Vin.append(row["Vin"])
				time_Vin.append(row["datetimeVin"])
				row = cur.fetchone()



			time_T1_first = str(time_T1[0])
			if n==1:
				print("time_T1_first=",time_T1_first )
			time_T1_last = str(time_T1[-1])
			first_time_T1 = datetime.datetime.strptime(time_T1_first,'%Y-%m-%d %H:%M:%S')
			time_T1_dt=[]
			time_T1_el_mins=[]




			time_Vap_first = str(time_Vap[0])
			if n==1:
				print("time_Vap_first=",time_Vap_first )
			time_Vap_last = str(time_Vap[-1])
			# if n==1:
			# 	print("time_Vap_last=",time_Vap_last )
			first_time_Vap = datetime.datetime.strptime(time_Vap_first,'%Y-%m-%d %H:%M:%S')
			time_Vap_dt = []
			time_Vap_el_mins = []

			time_Vin_first = str(time_Vin[0])
			if n==1:
				print("time_Vin_first=",time_Vin_first )
			time_Vin_last = str(time_Vin[-1])
			# if n==1:
			# 	print("time_Vin_last=",time_Vin_last )
			first_time_Vin = datetime.datetime.strptime(time_Vin_first,'%Y-%m-%d %H:%M:%S')
			time_Vin_dt = []
			time_Vin_el_mins = []



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



			#Stacked plot of all data


			plt.ion()
			fig, axs = plt.subplots(3,1, num=238, sharex=True)



			# #plt.clf()

			plt.draw()

			xmin=time_Vap_el_mins[0] #40
			xmax=time_Vap_el_mins[-1] #60
			#Vap
			axs[0].plot(time_Vap_el_mins, Vap,  linestyle = 'none', marker = '.', markersize = 2)
			axs[0].set_ylabel(r"$V_{ap}$ (V)")
			axs[0].grid()

			#Vin
			axs[1].plot(time_Vin_el_mins, Vin,  linestyle = 'none', marker = '.', markersize = 2)
			axs[1].set_ylabel(r"$V_{in}$ (V)")
			axs[1].grid()

			#Temp
			axs[2].plot(time_T1_el_mins, T1,  linestyle = 'none', marker = '.', markersize = 2)
			axs[2].set_ylabel(r"T ($\degree C$)")
			axs[2].grid()


			xlims=axs[2].get_xlim()
			xmin1=xlims[0]
			xmax1=xlims[1]
			fig.suptitle("Monitoring Interferometer from \n"+str(time_Vap[0]+datetime.timedelta(minutes=xmin))+" to "+str(time_Vap[0]+datetime.timedelta(minutes=xmax)))
			plt.xlabel('Elapsed time (min)', fontsize =16)
			plt.savefig(figname)
			plt.pause(0.001)
			plt.clf()
			db.close()


except KeyboardInterrupt:
	print("")
	print("time_T1_last=",time_T1_last )
	print("time_Vap_last=",time_Vap_last )
	print("time_Vin_last=",time_Vin_last )
	db.close()
