import socket
import time
import math
import pymysql

import pyvisa as visa
from ThorlabsPM100 import ThorlabsPM100, USBTMC
#Need to allow permission: sudo chown inqnet4:inqnet4 /dev/usbtmc0
txtFile = open("PInterf.txt","w")

db = pymysql.connect(host = "192.168.0.125", #Wired IPv4 Address
							 user ="INQNET4", # this user only has access to CP
							 password="Teleport1536!", # your password
							 database="teleportcommission",
							 charset='utf8mb4',
							 #port = 5025,
							 cursorclass=pymysql.cursors.DictCursor) #name of the data


inst = USBTMC(device="/dev/usbtmc0")
powermeter = ThorlabsPM100(inst=inst)

cur = db.cursor()
flag = True

while(True):
	try:
		query = "SELECT max(id) from interf6"
		cur.execute(query)
		result = cur.fetchall()
		resultDict = result[0]
		print(resultDict)
		maxid=resultDict["max(id)"]
		if maxid is None:
			maxid = 0
		if maxid == 0:
			action = "i"
		else:
			action = input("Inserting new data or updating table? (enter 'i' for insert or 'u' for update) ")
			print("action = ", action)
		# if action = update, specify with row to update data
		if action == "u":
			rowNum = input("Which row number to start inputing data? ")
			i = int(rowNum)
			break
		if action == "i":
			i = maxid +1
			break
		print("invalid entry, try again")
	except KeyboardInterrupt:
		print("")
		flag = False
		print("quit")
		break


if flag:
	print('Reading Powermeter values, press Ctrl-C to quit...')
	# Print nice channel column headers.
	line='  ID  |   Date/Time   |    Power   '.format(*range(3))
	print(line)
	txtFile.write(line+"\n")
	line='-' * 50
	print(line)
	txtFile.write(line+"\n")
	values = [0]*3


	while True:
		try:

			#if action == "u" and i > maxid:
			#	action = "i"
			values[0]=str(i)
			values[1] = str(time.ctime())
			p=powermeter.read
			values[2] = str(p)
			line = ' {0:>6} | {1:>6} |  {2:>6} '.format(*values)
			print(line)
			txtFile.write(line+"\n")
			if action == "u":
				query="SELECT P, datetimeP from interf6 where id = "+values[0]+";"
				cur.execute(query)
				query = "update interf6 set P = "+values[2]+", datetimeP = NOW() where id = "+values[0]+";"
				cur.execute(query)
			if action == "i": # insert into table
				query="INSERT INTO interf6(P, datetimeP) values("+values[2]+", NOW());"
				cur.execute(query)
			db.commit()
			time.sleep(1)
			i+=1
		except KeyboardInterrupt:
			print("")
			print("quit")
			break
txtFile.close()
db.close()
