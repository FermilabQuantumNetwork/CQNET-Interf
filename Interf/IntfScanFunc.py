import requests
import ast
from datetime import datetime
import time
import numpy as np
import getpass
import os
import subprocess as sp
import socket
import sys
import glob
import subprocess
from subprocess import Popen, PIPE
import pipes
from pipes import quote
import argparse
import pyvisa
import matplotlib.pyplot as plt

def InitiateResource():
    VISAInstance=pyvisa.ResourceManager('@py')
    ResourceList=VISAInstance.list_resources()
    print(ResourceList)
    for index in range(len(ResourceList)):
        print("Device number " + str(index) + " - " + ResourceList[index])
    DeviceNumber = input("Which device would you like to use? ")
    resourceName=ResourceList[int(DeviceNumber)]
    Resource = VISAInstance.open_resource(resourceName)#,write_termination='\n',read_termination='\r')
    print(Resource.query("*IDN?"))
    print("Set remote access")
    Resource.write("SYSTEM:REMOTE") #Set device to remote control
    return Resource

def SetChannel(Resource):
    Resource.write("outp on")
    ChannelNumber = input("Which channel? ")
    ChannelNumber=int(ChannelNumber)
    if ChannelNumber == 1:
        cmd1 = "inst CH1"
    elif ChannelNumber == 2:
        cmd1 = "inst CH2"
    elif ChannelNumber == 3:
        cmd1 = "inst CH3"
    Resource.write(cmd1)
    print("Set channel to "+str(ChannelNumber)+"\n")
#Safety check -- if true, then check that set voltage between 0 and 2.
def SetVoltage(Resource, ChVoltage, safetyCheck=True):
    cmd2 = "volt " + str(ChVoltage) + "V"
    if ChVoltage <= 2 and ChVoltage >= 0 or not safetyCheck:
        Resource.write(cmd2)
    else:
        print ('[WARNING] : The voltage is out of the bounds [0-2V], not changing the low voltage supply output')

    return float(Resource.query("MEAS:VOLT?").rstrip())

def VoltageStairs(V1,V2,numSteps,durStep):
    vArray = np.linspace(V1,V2,numSteps)
    vStairs=[]
    for Vap in vArray:
        for s in range(durStep):
            vStairs.append(Vap)
    return np.array(vStairs)

def VoltageRamp(V1,V2,dur):
    return np.linspace(V1,V2,dur)

def VoltageConst(V,dur):
    return V*np.ones(dur)

def VoltageTestIntf(Vmin,Vmax,numSteps):
    durStartBuff = 120
    VStartBuff = VoltageConst(Vmin,durStartBuff)

    upStairs1 = VoltageStairs(Vmin,Vmax,numSteps,300)
    downStairs1 = VoltageStairs(Vmax,Vmin,numSteps,300)
    hill1 = np.append(upStairs1,downStairs1)
    upStairs2 = VoltageStairs(Vmin,Vmax,numSteps,600)
    downStairs2 = VoltageStairs(Vmax,Vmin,numSteps,600)
    hill2 = np.append(upStairs2,downStairs2)
    upStairs3 = VoltageStairs(Vmin,Vmax,numSteps,1200)
    downStairs3 = VoltageStairs(Vmax,Vmin,numSteps,1200)
    hill3 = np.append(upStairs3,downStairs3)


    ramp1 = VoltageRamp(Vmin,Vmax/4,30)
    Vconst1 = VoltageConst(Vmax/4,3600*8)
    ramp2 = VoltageRamp(Vmax/4,Vmax/2,30)
    Vconst2 = VoltageConst(Vmax/2,3600*8)
    ramp3 = VoltageRamp(Vmax/2,Vmax,60)
    Vconst3 = VoltageConst(Vmax,3600*8)
    ramp4 = VoltageRamp(Vmax,0,60)

    voltageArray = np.append(VStartBuff,hill1)
    voltageArray = np.append(voltageArray,hill2)
    voltageArray = np.append(voltageArray,hill3)
    voltageArray=np.append(voltageArray,ramp1)
    voltageArray=np.append(voltageArray,Vconst1)
    voltageArray=np.append(voltageArray,ramp2)
    voltageArray=np.append(voltageArray,Vconst2)
    voltageArray=np.append(voltageArray,ramp3)
    voltageArray=np.append(voltageArray,Vconst3)
    voltageArray=np.append(voltageArray,ramp4)
    durEndBuff = 36*3600 - len(voltageArray)
    VEndBuff = VoltageConst(Vmin,durEndBuff)

    voltageArray=np.append(voltageArray,VEndBuff)
    return voltageArray

def DisableLVOutput(Resource):
    Resource.write("outp off")
    #Resource.read()
    print("Disabled LV Output")
