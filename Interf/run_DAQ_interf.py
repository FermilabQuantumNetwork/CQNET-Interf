#!/usr/bin/python



#This code will open socket port 5025 and send *IDN to instrument.

import time
import socket
import math
import sys
#import mysql.connector
import pymysql
txtFile = open("VavInterf.txt","w")

db = pymysql.connect(host="localhost",  # this PC
		     user="root",         # this user only has access to CPTLAB database
             password="Teleport1536!",  # your password
		     #auth_plugin='mysql_native_password',
		     database="teleportcommission",
             charset='utf8mb4',
             cursorclass=pymysql.cursors.DictCursor) # name of the data base

flag = True
with db.cursor() as cur1:
	#action: whether are inserting new data or are upating the table
	while(True):
		try:
			query = "SELECT max(id) from interf6"
			cur1.execute(query)
			result = cur1.fetchall()
			resultDict = result[0]
			print(resultDict)
			maxid = resultDict["max(id)"]
			if maxid is None:
				maxid = 0
				action = "i"
			else:
				action = input("Inserting new data or updating table? (enter 'i' for insert or 'u' for update) ")
				print("action = ", action)
			#if action = update, specify with row to update data
			if action == "u":
				rowNum = input("Which row number to start inputing data? ")
				i = int(rowNum)
				break
			if action == "i":
				i = maxid + 1
				break
			print("invalid entry, try again")
		except KeyboardInterrupt:
			print("")
			print("quit")
			flag = False
			break
if flag:


	input_buffer = 4096 #Temp buffer for rec data.
	exRat = 0


	pna = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#pna.connect(("192.168.0.136", 5025))
	#pna.connect(("192.168.0.142", 5025))
	pna.connect(("192.168.0.177", 5025))

	st = "*idn?" + "\n"
	byt = st.encode()
	pna.send(byt)

	id = pna.recv(input_buffer)

	print(id.decode('utf-8'))
	#cur = db.cursor(buffered = "True", dictionary = True)
	# db.close()
	# pna.close()

	with db.cursor() as cur:
		print('Reading Voltage from oscilloscope, press Ctrl-C to quit...')
		line = '    ID    |       Date/Time       |     Vav (V)    '.format(*range(3))
		print(line)
		txtFile.write(line+"\n")
		line = '-' * 50
		print(line)
		txtFile.write(line+"\n")

		while True:
			try:
				st = "meas:vav? display,channel1" + "\n"
				#st="meas:vav? func1" + "\n"
				byt = st.encode()
				pna.send(byt)
				vav = pna.recv(input_buffer)
				vav=vav.decode("utf-8")
				vav=vav.rstrip()

				#print(vav)
				values=[0]*3
				values[0] = str(i)
				values[1] = str(time.ctime())
				values[2] = str(vav)
				line = '{0:>6} | {1:>6} |{2:>6}'.format(*values)
				print(line)
				txtFile.write(line+"\n")
				#update table
				if action == "u":
					query = "SELECT Vav, datetimeVav from interf6 where id = "+values[0]+";"
					cur.execute(query)
					query = "update interf6 set Vav = "+values[2]+", datetimeVav = NOW() where id = "+values[0]+";"
					cur.execute(query)
				#insert into table
				if action == "i":
					query = "INSERT INTO interf6(Vav, datetimeVav) values("+values[2]+", NOW());"
					cur.execute(query)
				db.commit()
				time.sleep(1)
				i+=1
			except KeyboardInterrupt:
				print("")
				print("quit")
				break

txtFile.close()
pna.close()
db.close()
