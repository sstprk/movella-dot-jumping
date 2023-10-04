#Salih Toprak
import numpy as np

from scipy.integrate import quad,cumtrapz
import scipy.signal as signal

import pandas as pd

import math as m

class Sensor:
    sensor_count = 0
    def __init__(self, path, freq=60.0):
        self.freq = freq
        self.path = path
        self.df = pd.DataFrame(pd.read_excel(self.path))

        if not "FreeAcc_X" in list(self.df.columns.values):
            self.rx = list(self.df.loc[:,"dv[1]"])
            self.ry = list(self.df.loc[:,"dv[2]"])
            self.rz = list(self.df.loc[:,"dv[3]"])
            self.rawAcc = [self.rx, self.ry, self.rz]

        else:
            self.rx = list(self.df.loc[:,"FreeAcc_X"])
            self.ry = list(self.df.loc[:,"FreeAcc_Y"])
            self.rz = list(self.df.loc[:,"FreeAcc_Z"])
            self.rawAcc = [self.rx, self.ry, self.rz]

        self.frame_count = len(self.rawAcc[0])
        self.frame_array = list(range(len(self.rawAcc[0])))
        self.newTime = []
        self.timeA = []

        self.newAcc = []
        self.Velocity = []
        self.Position = []

        self.organise()
        self.timeAxis()
        self.filter()
        
        Sensor.sensor_count += 1

    def filter(self):
        self.newAcc = np.asmatrix(self.newAcc)
        sum = np.add(np.multiply(self.newAcc[:,0], self.newAcc[:,0]), np.multiply(self.newAcc[:,1], self.newAcc[:,1]))
        sum = np.add(sum, np.multiply(self.newAcc[:,2], self.newAcc[:,2]))
        accMag = np.sqrt(sum)

        samplePeriod = 1/60
        filtCutOff = 0.001
        b, a = signal.butter(1, (2*filtCutOff)/(1/samplePeriod), "high")
        magFilted = signal.filtfilt(b, a, np.ravel(accMag))
        magFilted = abs(magFilted)

        filtCutOff = 5
        b, a = signal.butter(1,(2*filtCutOff)/(1/samplePeriod), "low")
        magFilted = signal.filtfilt(b, a, magFilted)
        
        stationary = magFilted < 0.05
        stationary = stationary.astype(int)

        self.newAcc = self.newAcc * 9.81
        self.newAcc[:,2] = self.newAcc[:,2] - 9.81
        t1=1

        velocity = np.zeros(shape=(len(self.newAcc), 3))

        for t1 in range(len(self.newAcc)):

            #acInterspace = [accFilted[t1], accFilted[t1-1]] 
            velocity[t1,:] = velocity[t1-1,:] + self.newAcc[t1,:] * samplePeriod
            if stationary[t1] == 1:
                velocity[t1,:] = [0, 0, 0]
 
        diff = np.diff(stationary)
        velDrift = np.zeros(shape=(self.frame_count, 3))
        stationary_start = np.argwhere(diff == -1)
        #stationary_start = np.insert(stationary_start, 0, 0)
        stationary_end = np.argwhere(diff == 1)
        #stationary_end = np.insert(stationary_end, 0, 0)

        for i in range(np.size(stationary_end)-1):
            drift_rate = velocity[stationary_end[i]-1, :]/ float(stationary_end[i] - stationary_start[i])

            enum = np.arange((stationary_end[i] - stationary_start[i]-1))

            drift = np.array([enum*drift_rate[0][0], enum*drift_rate[0][1], enum*drift_rate[0][2]])

            reshapedDrift = np.zeros((len(drift[0]), 3))
            for e in range(len(drift[0])):
                reshapedDrift[e][0] = drift[0][e]
                reshapedDrift[e][1] = drift[1][e]
                reshapedDrift[e][2] = drift[2][e]

            velDrift[stationary_start[i][0]:stationary_end[i][0]-1, :] = reshapedDrift
        
        self.Velocity = velocity = velocity - velDrift

        pos = np.zeros(shape=(np.size(velocity), 3))
        t2=1
        for t2 in range(len(velocity)):
            #velInterspace = [velocity[t2], velocity[t2-1]]
            pos[t2,:] = pos[t2-1,:] + velocity[t2,:]*samplePeriod
        
        

        self.Position = pos

    def integrate(self, filtD):
        results = []
        for data in filtD:
            tempResult = []
            rSum = 0
            i = 1
            tempResult = cumtrapz(data, initial=0)

            """for i in range(len(data)):  
                t1 = (i-1)/60
                t2 = i/60

                v = quad(func, t2, t1, args=(a[i]))
                Vx = v[1] - v[0]
                Vsum += Vx
                tempV.append(float(v[0]))

                p = quad(func, t2, t1, args=(v[0]))
                Psum += p[0]
                tempP.append(float(p[0]))

                interspaceData = [data[i-1], data[i]]

                res = cumtrapz(interspaceData, initial=0)
                r = res[1]
                rSum += r
                tempResult.append(rSum)"""
            results.append(tempResult)
        return results
    
    def timeAxis(self):
        for i in range(self.frame_count):
            self.timeA.append(i/self.freq)

    def organise(self):
        rawTemp = np.zeros(shape=(self.frame_count, 3))
        for t in range(self.frame_count):
            rawTemp[t] = [self.rawAcc[0][t], self.rawAcc[1][t], self.rawAcc[2][t]]
        self.newAcc = rawTemp