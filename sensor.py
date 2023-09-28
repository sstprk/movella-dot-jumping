#Salih Toprak
import numpy as np

from scipy.integrate import quad,cumtrapz
import scipy.signal as signal
import scipy.interpolate as interpolate

import pandas as pd

import math as m

#from pykalman import KalmanFilter
from kalman import KalmanFilter

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

        self.filteredAcc = []
        self.Velocity = []
        self.Position = []

        self.organise()
        self.timeAxis()
        self.filter()
        
        Sensor.sensor_count += 1

    def filter(self):
        self.rawAcc = np.asmatrix(self.rawAcc)
        mag = [np.multiply(self.rawAcc[:,0], self.rawAcc[:,0])+
               np.multiply(self.rawAcc[:,1], self.rawAcc[:,1])+
               np.multiply(self.rawAcc[:,2], self.rawAcc[:,2])]
        accMag = np.sqrt(mag)

        samplePeriod = 1/256
        filtCutOff = 0.001
        b, a = signal.butter(1, (2*filtCutOff)/(1/samplePeriod), "high")
        magFilted = signal.filtfilt(b, a, np.ravel(accMag))
        magFilted = abs(magFilted)

        filtCutOff = 5
        b, a = signal.butter(1,(2*filtCutOff)/(1/samplePeriod), "low")
        magFilted = signal.filtfilt(b, a, magFilted)
        
        stationary = magFilted < 0.05
        stationary = stationary.astype(int)

        self.rawAcc = self.rawAcc * 9.81
        t=1

        velocity = np.zeros(shape=(len(self.rawAcc), 3))

        for t1 in range(len(velocity)):

            #acInterspace = [accFilted[t1], accFilted[t1-1]] 
            velocity[t1,:] = velocity[t1-1,:] + self.rawAcc[t,:] * samplePeriod
            for ix in range(2):
                if stationary[t1] == 1:
                    velocity[t1] = [0, 0, 0]
        print(velocity)
        self.Velocity = velocity
        velDrift = np.zeros(np.shape(velocity))
        print(velDrift)
        stationary_start = np.where(np.diff(stationary) == -1)
        stationary_start = np.insert(stationary_start, 0, 0)
        stationary_end = np.where(np.diff(stationary) == 1)
        stationary_end = np.insert(stationary_end, 0, 0)

        for i in range(np.size(stationary_end)):
            drift_rate = velocity[stationary_end[i], :]/ (stationary_end[i] - stationary_start[i])

            enum = np.array(range(1, stationary_end[i] - stationary_start[i]))

            drift = [np.transpose(enum*drift_rate[0]), np.transpose(enum*drift_rate[1]), np.transpose(enum*drift_rate[2])]

            velDrift[stationary_start[i]:stationary_end[i]-1, :] = drift

        velocity = velocity - velDrift

        pos = np.zeros(shape=(len(velocity), 3))
        for t2 in range(np.size(pos)):
            #velInterspace = [velocity[t2], velocity[t2-1]]
            pos[t2,:] = pos[t2-1,:] + velocity[t2,:]*samplePeriod

        self.Position.append(pos)

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
        self.rawAcc = rawTemp