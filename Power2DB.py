#This records data from the BKPrecision powermeter (connected via USB) to the mysql database.
#You need to run this as the root user and need to allow permission to the computer
#to access the connected device folder. For example, if the folder name is 'usbtmc0'
#and the computer name is 'inqnet', type the following command into terminal on
#linux: sudo chown inqnet:inqnet /dev/usbtmc0
#Requirements: Python3, mysql, packages listed below
import time
import math
import pymysql
import pyvisa as visa
from ThorlabsPM100 import ThorlabsPM100, USBTMC

db = pymysql.connect(host="<IP ADDRESS>",  #Replace <IP ADDRESS> with the IP of computer with database. Local host if is same computer.
					 user="<USERNAME>", #Replace <USERNAME> with your username
					 passwd="<PASSWORD>",  #Replace <PASSWORD> with your password
					 database="teleportcommission",
					 charset='utf8mb4',
					 cursorclass=pymysql.cursors.DictCursor) #name of the data

#Connect to device
inst = USBTMC(device="/dev/usbtmc0")
powermeter = ThorlabsPM100(inst=inst)

#Create mysql cursor
cur = db.cursor()
#Option to back up data to textfile
backup = False
print("Back up to text file: " + str(backup))
if backup:
	txtFile = open("PInterf.txt","w")

#Get max id for printing out data in terminal
query = "SELECT max(id) from Power"
cur.execute(query)
result = cur.fetchall()
resultDict = result[0]
maxid=resultDict["max(id)"]
if maxid is None:
	maxid = 0
i = maxid +1



print('Reading Powermeter values, press Ctrl-C to quit...')
# Print nice channel column headers.
line='  ID  |   Date/Time   |    Power   '.format(*range(3))
print(line)
if backup:
	txtFile.write(line+"\n")
line='-' * 50
print(line)
if backup:
	txtFile.write(line+"\n")
values = [0]*3

#Loop to write data to mysql
while True:
	try:
		values[0]=str(i)
		values[1] = str(time.ctime()) #Get current time
		p=powermeter.read #measure power
		values[2] = str(p)
		line = ' {0:>6} | {1:>6} |  {2:>6} '.format(*values) #print out values in terminal
		print(line)
		if(backup):
			txtFile.write(line+"\n")
		#Insert data into mysql data base
		query="INSERT INTO Power(P, datetimeP) values("+values[2]+", NOW());"
		cur.execute(query)
		db.commit()
		time.sleep(1) #wait 1 second
		i+=1
	except KeyboardInterrupt:
		print("")
		print("quit")
		break
if backup:
	txtFile.close()
db.close() #close database
