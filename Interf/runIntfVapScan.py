from IntfScanFunc import *
import pymysql

txtFile = open("VapVinInterf.txt","w")
db = pymysql.connect(host = "192.168.0.125", #Wired IPv4 Address
					user ="INQNET4", # this user only has access to CP
					password="Teleport1536!", # your password
					database="teleportcommission",
					charset='utf8mb4',
					#port = 5025,
					cursorclass=pymysql.cursors.DictCursor) #name of the data

cur = db.cursor()
flag = True

numSteps=10
Vmin=0 #in Volts
Vmax=2 #in Volts
VISAInstance=pyvisa.ResourceManager('@py')
Resource=InitiateResource()
SetChannel(Resource)

while(True):
	try:
		query = "SELECT max(id) from interf6"
		cur.execute(query)
		result = cur.fetchall()
		resultDict = result[0]
		print(resultDict)
		maxid=resultDict["max(id)"]
		if maxid is None:
			maxid=0
		if maxid == 0:
			action = "i"
		else:
			action = input("Inserting new data or updating table? (enter 'i' for insert or 'u' for update) ")
			print("action = ", action)

		# if action = update, specify with row to update data
		if action == "u":
			rowNum = input("Which row number to start inputing data? ")
			i = int(rowNum.rstrip())
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
	try:
		values = [0]*4
		Vapplied=VoltageTestIntf(Vmin,Vmax,numSteps)
		#Vapplied = VoltageRamp(0.5,1.5,30)
		#Vapplied=VoltageStairs(2,0,5,5)
		t=np.arange(1,1+len(Vapplied))
		plt.plot(t/3600,Vapplied)
		plt.xlabel("Hours")
		plt.ylabel("Voltage (V)")
		plt.title("Applied Voltage vs. Time")
		plt.show()
		Vin=[]
		print('Writing and reading applied/input voltage values, press Ctrl-C to quit...')
		line='  ID  |   Date/Time   |    Voltage Applied (V)    |    Voltage Measured (V)    '.format(*range(4))
		print(line)
		txtFile.write(line+"\n")
		line='-' * 75
		print(line)
		txtFile.write(line+"\n")
		for Vap in Vapplied:
			if action == "u" and i > maxid:
				action = "i"
			time.sleep(1) #Wait 1 second
			values[0]=str(i)
			values[1]= str(time.ctime())
			values[2]="{0:.3f}".format(Vap)
			values[3]=SetVoltage(Resource,Vap)
			Vin.append(values[3])
			values[3]=str(values[3])
			line=' {0:>6} | {1:>6} | {2:>6} | {3:>6} '.format(*values)
			print(line)
			txtFile.write(line+"\n")
			if action == "u":
				query="SELECT Vap, Vin, datetimeVap, datetimeVin from interf6 where id = "+values[0]+";"
				cur.execute(query)
				query = "update interf6 set Vap = "+values[2]+", Vin = "+values[3]+", datetimeVap = NOW(), datetimeVin = NOW() where id = "+values[0]+";"
				cur.execute(query)
			if action == "i": # insert into table
				query="INSERT INTO interf6(Vap, Vin, datetimeVap, datetimeVin) values("+values[2]+","+values[3]+", NOW(), NOW());"
				cur.execute(query)
			db.commit()
			i+=1
		Vin = np.array(Vin)
		plt.plot(t/3600,Vapplied, label = "Applied Voltage")
		plt.plot(t/3600,Vin, label = "Vin")
		plt.xlabel("Hours")
		plt.ylabel("Voltage (V)")
		plt.legend()
		plt.title("Voltage vs. Time")
	except KeyboardInterrupt:
		print("")
		print("Quit")
		DisableLVOutput(Resource)

txtFile.close()
plt.show()
db.close()
