#This records data from our oscilloscope to the mysql database.
#This code will open socket port 5025 and send commands to the oscilloscope
#to retrieve output voltage data (Vav) from the interferometer.

#Requirements: Python3, mysql, packages listed below
import time
import socket
import math
import sys
import pymysql

db = pymysql.connect(host="192.168.0.125",  #IP of computer with database or "local host" if same computer
		     user="inqnet1",         # user
             password="Teleport1536!",  # your password
		     database="teleportcommission", #database name
             charset='utf8mb4',
             cursorclass=pymysql.cursors.DictCursor) # name of the data base

#Create cursor to select data from mysql.
with db.cursor() as cur:
	#Option to back up data to textfile
	backup = False
	print("Back up to text file: " + str(backup))
	if backup:
		txtFile = open("VavInterf.txt","w")
	#Get max id for printing out data in terminal
	query = "SELECT max(id) from Vav"
	cur.execute(query)
	result = cur.fetchall()
	resultDict = result[0]
	maxid = resultDict["max(id)"]
	if maxid is None:
		maxid = 0
	i = maxid+1;

	#Connect to oscilloscope
	input_buffer = 4096 #Temp buffer for rec data.
	exRat = 0
	pna = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	pna.connect(("192.168.0.177", 5025))
	#Check connection
	st = "*idn?" + "\n"
	byt = st.encode()
	pna.send(byt)
	id = pna.recv(input_buffer)
	print(id.decode('utf-8')) #Print response from oscilloscope in terminal


	print('Reading Voltage from oscilloscope, press Ctrl-C to quit...')
	# Print nice channel column headers.
	line = '    ID    |       Date/Time       |     Vav (V)    '.format(*range(3))
	print(line)
	if backup:
		txtFile.write(line+"\n")
	line = '-' * 50
	print(line)
	if backup:
		txtFile.write(line+"\n")

	#Loop to write data to mysql
	while True:
		try:
			#Ask scope for current average voltage
			st = "meas:vav? display,channel1" + "\n"
			byt = st.encode()
			pna.send(byt)
			vav = pna.recv(input_buffer)
			vav=vav.decode("utf-8")
			vav=vav.rstrip() #Get rid of termination character from scope response
			values=[0]*3
			values[0] = str(i)
			values[1] = str(time.ctime())
			values[2] = str(vav)
			line = '{0:>6} | {1:>6} |{2:>6}'.format(*values) #print out values in terminal
			print(line)
			if backup:
				txtFile.write(line+"\n")
			#SQL command to insert data into database
			query = "INSERT INTO Vav(Vav, datetimeVav) values("+values[2]+", NOW());"
			cur.execute(query)
			db.commit()
			time.sleep(1) #Wait 1 second
			i+=1
		except KeyboardInterrupt:
			print("")
			print("quit")
			break
if backup:
	txtFile.close()
pna.close()
db.close()
