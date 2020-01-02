import numpy as np
#import matplotlib
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import tkinter
#matplotlib.use('TkAgg')
import datetime
import math
import pymysql
import os

TABLE_NAME = 'interf6'


#connect to database

db = pymysql.connect(host="192.168.0.125",  # this PC
		             user="inqnet1",
                     passwd="Teleport1536!",  # your password
                     db="teleportcommission",
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)
cur = db.cursor()


while(True):
#Update where timestamp = Vin timestamp
    #update where timestamp = now and index of last query
    query="SELECT datetime, test from testTable where datetime = NOW();"
    cur.execute(query)
    query = "update testTable set datetime=NOW(), test = 0 where datetime=NOW()"
    print(query)
    cur.execute(query)
    db.commit()
    time.sleep(1)
db.close()
