#Salih Toprak
import numpy as np

from scipy.integrate import quad,cumtrapz
import scipy.signal as signal
import scipy.interpolate as interpolate

import pandas as pd

import math as m

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
        
        self.timeAxis()

        self.filteredAcc = self.filter(self.rawAcc)
        self.rawVelocity = self.integrate(self.filteredAcc)
        self.filteredVel = self.filter(self.rawVelocity)
        self.rawPosition = self.integrate(self.filteredVel)
        self.filteredPos = self.filter(self.rawPosition)
        
        Sensor.sensor_count += 1

    def filter(self, rawD):
        fs = self.freq 
        cutoff = 2
        nyq = 0.5 * fs  
        order = 2
        normal_cutoff = cutoff/nyq
        final = []

        for data in rawD:
            dt = 1/60
            F = np.array([[1, dt, 0.5*dt**2], [0, 1, dt], [0, 0, 1]])
            H = np.array([0, 0, 1]).reshape(1, 3)
            Q = np.array([[0.2, 0.0, 0.0], [0.0, 0.1, 0.0], [0.0, 0.0, 10e-4]])
            R = 0.0020
            P0 = np.array([[0, 0, 0], [0, 0, 0], [0, 0, R]])
            X0 = np.array([0, 0, data[0]])

            kf = KalmanFilter(F=F, H=H, Q=Q, R=R, x0=X0, P=P0)
            predictions = []
            
            for z in data:
                predictions.append(np.dot(H, kf.predict())[0])
                kf.update(z)
            #y = signal.medfilt(predictions, 3)
            #b, a = signal.butter(order, normal_cutoff, btype="low")
            #ac = signal.filtfilt(b, a, predictions)

            final.append(predictions)
        return final

    def integrate(self, filtD):
        #func = lambda x, ac: ac
        results = []
        for data in filtD:
            tempResult = []
            rSum = 0
            i = 1

            for i in range(len(data)):  
                t1 = (i-1)/60
                t2 = i/60

                """v = quad(func, t2, t1, args=(a[i]))
                Vx = v[1] - v[0]
                Vsum += Vx
                tempV.append(float(v[0]))

                p = quad(func, t2, t1, args=(v[0]))
                Psum += p[0]
                tempP.append(float(p[0]))"""

                interspaceData = [data[i-1], data[i]]

                res = cumtrapz(interspaceData, initial=0)
                r = res[1]
                rSum += r
                tempResult.append(r)
            results.append(tempResult)
        return results
    
    def timeAxis(self):
        for i in range(self.frame_count):
            self.timeA.append(i/self.freq)
