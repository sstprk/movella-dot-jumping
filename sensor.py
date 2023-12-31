#Salih Toprak
import numpy as np

import scipy.signal as signal

import pandas as pd

class Sensor:
    sensor_count = 0
    def __init__(self, path, freq=60.0):
        self.freq = freq
        self.path = path
        self.df = pd.DataFrame(pd.read_excel(self.path))
        
        #Checking column headings
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

        self.reshape()
        self.timeAxis()
        self.filter()
        self.accToPoS()
        
        Sensor.sensor_count += 1

    def timeAxis(self):
        for i in range(self.frame_count):
            self.timeA.append(i/self.freq)

    def reshape(self):
        rawTemp = np.zeros(shape=(self.frame_count, 3))
        for t in range(self.frame_count):
            rawTemp[t] = [self.rawAcc[0][t], self.rawAcc[1][t], self.rawAcc[2][t]]
        self.rawAcc = rawTemp
    
    def filter(self):
        dfFilt = pd.DataFrame(self.rawAcc)
        window=2
        self.newAcc = np.array(dfFilt.rolling(window).mean())
        self.newAcc[0:window-1, :] = [0,0,0]
        

    def accToPoS(self):
        #Calculating acceleration magnitude
        newAcc = np.asmatrix(self.newAcc)
        sum = np.add(np.multiply(newAcc[:,0], newAcc[:,0]), np.multiply(newAcc[:,1], newAcc[:,1]))
        sum = np.add(sum, np.multiply(newAcc[:,2], newAcc[:,2]))
        accMag = np.sqrt(sum)

        #High pass filter
        samplePeriod = 1/60
        filtCutOff = 0.001
        b, a = signal.butter(1, (2*filtCutOff)/(1/samplePeriod), "high")
        magFilted = signal.filtfilt(b, a, np.ravel(accMag))
        magFilted = abs(magFilted)

        #Low pass filter
        filtCutOff = 5
        b, a = signal.butter(1,(2*filtCutOff)/(1/samplePeriod), "low")
        magFilted = signal.filtfilt(b, a, magFilted)
        
        #Stationary threshold 
        stationary = magFilted < 0.05
        stationary = stationary.astype(int)

        #Velocity list with zeros
        velocity = np.zeros(shape=(len(newAcc), 3))

        #Subtraction of acceleration drift in z axis
        newAcc[:,2] = newAcc[:, 2] - 0.2
        
        #Integrating acceleration for velocity
        t1=1
        for t1 in range(len(newAcc)):
            velocity[t1,:] = velocity[t1-1,:] + newAcc[t1,:] * samplePeriod
            if stationary[t1] == 1:
                velocity[t1,:] = [0, 0, 0]

 
        #Compute integral drift
        diff = np.diff(stationary)
        velDrift = np.zeros(shape=(self.frame_count, 3))
        stationary_start = np.argwhere(diff == -1)
        stationary_end = np.argwhere(diff == 1)
        
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

        #Integrating velocity for position
        pos = np.zeros(shape=(len(velocity), 3))
        t2=1
        for t2 in range(len(velocity)):
            pos[t2,:] = pos[t2-1,:] + velocity[t2,:] * samplePeriod
        self.Position = pos