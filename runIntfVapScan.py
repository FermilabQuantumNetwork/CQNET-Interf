"""
This sends and receives voltages to the BK Precision power supply.
Vap is the voltage that is sent to power supply by this script.
Once Vap is received by the power supply, the current channel is set to Vap.
Vin is the voltage that the current channel is set to as reported by the
power supply.

Requirements: Python3, pymysql, IntfScanFunc.py (in same directory)
OS: CentOS7
"""
from IntfScanFunc import *
import pymysql


db = pymysql.connect(host="<IP ADDRESS>",  #Replace <IP ADDRESS> with the IP of computer with database. Local host if is same computer.
					 user="<USERNAME>", #Replace <USERNAME> with your username
					 passwd="<PASSWORD>",  #Replace <PASSWORD> with your password
					 database="teleportcommission",
					 charset='utf8mb4',
					 cursorclass=pymysql.cursors.DictCursor) #name of the data

numSteps=10
Vmin=0 #in Volts
Vmax=2 #in Volts

#Find all devices (resources) that can be detected with VISA
VISAInstance=pyvisa.ResourceManager('@py')
#Prompts for resource
Resource=InitiateResource()
#Sets channel of powersupply
SetChannel(Resource)

#Create cursor to select data from mysql.
cur = db.cursor()
#Option to back up data to textfile
backup = False
print("Back up to text file: " + str(backup))
if backup:
	txtFile = open("VapVinInterf.txt","w")

#Get max id for printing out data in terminal
query = "SELECT max(id) from VapVin"
cur.execute(query)
result = cur.fetchall()
resultDict = result[0]
maxid=resultDict["max(id)"]
if maxid is None:
	maxid=0
i = maxid +1


try:
	values = [0]*4
	#Returns array of Vap elements
	Vapplied=VoltageTestIntf(Vmin,Vmax,numSteps)
	#Examples of other Vap arrays (see 'IntfScanFunc.py')
	#Vapplied = VoltageRamp(0.5,1.5,30)
	#Vapplied=VoltageStairs(2,0,5,5)

	#Plot of what will be sent to power supply
	t=np.arange(1,1+len(Vapplied))
	plt.plot(t/3600,Vapplied)
	plt.xlabel("Hours")
	plt.ylabel("Voltage (V)")
	plt.title("Applied Voltage vs. Time")
	plt.show()
	Vin=[]
	print('Writing and reading applied/input voltage values, press Ctrl-C to quit...')
	# Print nice channel column headers.
	line='  ID  |   Date/Time   |    Voltage Applied (V)    |    Voltage Measured (V)    '.format(*range(4))
	print(line)
	if backup:
		txtFile.write(line+"\n")
	line='-' * 75
	print(line)
	if backup:
		txtFile.write(line+"\n")

	#Loops through elements in Vapplied array, sets power supply to each element.
	for Vap in Vapplied:
		time.sleep(1) #Wait 1 second
		values[0]=str(i)
		values[1]= str(time.ctime()) #Get current time
		values[2]="{0:.3f}".format(Vap) #Current Vap
		values[3]=SetVoltage(Resource,Vap) #Set voltage of power supply to Vap. Returns Vin, the voltage reported by power supply
		Vin.append(values[3])
		values[3]=str(values[3])
		line=' {0:>6} | {1:>6} | {2:>6} | {3:>6} '.format(*values)
		print(line)
		if backup:
			txtFile.write(line+"\n")
		#SQL command to insert data into database
		query="INSERT INTO VapVin(Vap, Vin, datetimeVap, datetimeVin) values("+values[2]+","+values[3]+", NOW(), NOW());"
		cur.execute(query)
		db.commit()
		i+=1
	Vin = np.array(Vin)
	#Plot of Vap, Vin at the end of the scan.
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
if backup:
	txtFile.close()
plt.show()
db.close()
