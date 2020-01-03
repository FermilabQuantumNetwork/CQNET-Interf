"""
Records temperature of a thermistor from an ADC.
Modified from simple demo of reading each analog input from the ADS1x15 and printing it to
the screen (Author: Tony DiCola, License: Public Domain)

Requirements: Python2
OS: Raspberry Pi
"""
import time
import math
# Import the ADS1x15 module.
import Adafruit_ADS1x15
import mysql.connector

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

db = mysql.connector.connect(host="<IP ADDRESS>",  #Replace <IP ADDRESS> with the IP of computer with database. Local host if is same computer.
							 user="<USERNAME>", #Replace <USERNAME> with your username
							 passwd="<PASSWORD>",  #Replace <PASSWORD> with your password
							 #auth_plugin='mysql_native_password',
							 database="teleportcommission") #name of the data base


# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

#Create cursor to select data from mysql.
cur = db.cursor(buffered=True)
#Option to back up data to textfile
backup = False
if backup:
	txtFile = open("T1Interf.txt","w")
#Get max id for printing out data in terminal
query = "SELECT max(id) from Temp"
cur.execute(query)
result = cur.fetchall()
resultDict = result[0]
maxid=resultDict["max(id)"]
if maxid is None:
	maxid = 0
i = maxid +1


#Constants
bitToVolt=4.096/32767
R0 = 10000
T0=25+273.15
beta=3895
rInf = R0*math.exp(-beta/T0)

print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
line = '  ID  |   Date/Time   |   Temp (C)  '.format(*range(3))
print(line)
if backup:
	txtFile.write(line+"\n")
line = '-' * 50
print(line)
if backup:
	txtFile.write(line+"\n")
values = [0]*3
starttime = time.time()


while True:
		try:
			values[0]=str(i);
			values[1]=str(time.ctime()); #Current time
			# Read the specified ADC channel using the previously set gain value.
			data=adc.read_adc(0, gain=GAIN)
			Vin = data*bitToVolt
			#Convert voltage to resistance
			Rt= Vin*10000/(3.3-Vin)
			#Convert resistance to temp
			T=beta/(math.log(Rt/rInf))
			values[2]=str(T-273.15)
#Convert celsius to kelvin
T0=25+273.15
beta=3895
rInf = R0*math.exp(-beta/T0)can also pass in an optional data_rate parameter that controls
			# the ADC conversion time (in samples/second). Each chip has a different
			# set of allowed data rate values, see datasheet Table 9 config register
			# DR bit values.
			#values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
			# Each value will be a 12 or 16 bit signed integer value depending on the
			# ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
			# Print the ADC values.
			line=' {0:>6} | {1:>6} |{2:>6} '.format(*values)
			print(line)
			if backup:
				txtFile.write(line+"\n")
			#SQL command to insert data into database
			query="INSERT INTO Temp(T1, datetimeT1) values("+str(values[2])+", NOW());"
			cur.execute(query)
			db.commit()
			i+=1
			time.sleep(1) # Pause for a second.
			except KeyboardInterrupt:
					print "\n"
					print "quit"
					break

if backup:
	txtFile.close()
db.close() #Close database
