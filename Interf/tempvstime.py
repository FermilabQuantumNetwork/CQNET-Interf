# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time
import math
# Import the ADS1x15 module.
import Adafruit_ADS1x15
import mysql.connector
#import MySQLdb

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

db = mysql.connector.connect(host = "192.168.0.125", #Wired IPv4 Address
                             user ="rbpi2", # this user only has access to CPTLAB database
                             passwd="Teleport1536!", # your password
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

#action: whether are inserting new data or are updating the table
#action = "update"
#print "action = ", action
#if action = update, specify which row to update data
#id=76654
#if action == "update":
#       print "start id number = ", id

txtFile = open("T1Interf.txt","w")
cur = db.cursor(buffered=True)
flag = True
while(True):
        try:
                query = "SELECT max(id) from interf6"
                cur.execute(query)
                result = cur.fetchall()
                resultDict=result[0]
                print(resultDict)
                maxid = resultDict[0] #resultDict["max(id)"]
                if maxid is None:
                        maxid = 0
                if maxid == 0:
                        action = "i"
                else:
                        action = raw_input("Inserting new data or updating table? (enter 'i' for insert or 'u' for update) ")
                        print("action = ", action)

   try:
                query = "SELECT max(id) from interf6"
                cur.execute(query)
                result = cur.fetchall()
                resultDict=result[0]
                print(resultDict)
                maxid = resultDict[0] #resultDict["max(id)"]
                if maxid is None:
                        maxid = 0
                if maxid == 0:
                        action = "i"
                else:
                        action = raw_input("Inserting new data or updating table? (enter 'i' for insert or 'u' for update) ")
                        print("action = ", action)
                #if action = update, specify with row to update data
                if action == "u":
                        rowNum = raw_input("Which row number to start inputing data? ")
                        i = int(rowNum.rstrip())
                        break
                if action == "i":
                        i = maxid+1
                        break
                print("invalid entry, try again")
        except KeyboardInterrupt:
                print("")
                flag = False
                print("quit")
                break

if flag:



        #Constants
        bitToVolt=4.096/32767

        #Connect to db
        #cur = db.cursor(buffered=True)
        #cur.execute("SHOW TABLES")

        #for x in cur:
        #       print(x)


        print('Reading ADS1x15 values, press Ctrl-C to quit...')
        # Print nice channel column headers.
        line = '  ID  |   Date/Time   |   Temp (C)  '.format(*range(3))
        print(line)
        txtFile.write(line+"\n")
        line = '-' * 50
        print(line)
        txtFile.write(line+"\n")
        # Main loop.
        #print(time.clock())
        values = [0]*3
        starttime = time.time()
        R0 = 10000
        T0=25+273.15
        beta=3895
        rInf = R0*math.exp(-beta/T0)

        while True:
                try:
                #for i in range(4):
                        #if action == "u" and i>maxid:
                        #       action = "i"
                        values[0]=str(i);
                        values[1]=str(time.ctime());
                        #values[1]=time.time()-starttime
                        # Read the specified ADC channel using the previously set gain value.
                        data=adc.read_adc(0, gain=GAIN)
                        Vin = data*bitToVolt
                        Rt= Vin*10000/(3.3-Vin)
                        #values[1]=Rt
                        T=beta/(math.log(Rt/rInf))
                        values[2]=str(T-273.15)

                # Note you can also pass in an optional data_rate parameter that controls
                # the ADC conversion time (in samples/second). Each chip has a different
                # set of allowed data rate values, see datasheet Table 9 config register
                # DR bit values.
                #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
                # Each value will be a 12 or 16 bit signed integer value depending on the
                # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
                # Print the ADC values.
                        line=' {0:>6} | {1:>6} |{2:>6} '.format(*values)
                        print(line)
                        txtFile.write(line+"\n")


                        #update table
                        if action == "u":
                                query="SELECT T1, datetimeT1 from interf6 where id = "+values[0]+";"
                                cur.execute(query)
                                query = "update interf6 set T1 = "+values[2]+", datetimeT1 = NOW() where id = "+values[0]+";"
                                cur.execute(query)
                        #insert into table
                        if action == "i":
                                query="INSERT INTO interf6(T1, datetimeT1) values("+str(values[2])+", NOW());"
                                cur.execute(query)
                        db.commit()
                        i+=1

                        # Pause for a second.
                        time.sleep(1)


                except KeyboardInterrupt:
                        print "\n"
                        print "quit"
                        break


txtFile.close()
db.close()
