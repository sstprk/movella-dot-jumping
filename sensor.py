#Salih Toprak
import numpy as np

from scipy.integrate import quad,cumtrapz
import scipy.signal as signal
import scipy.interpolate as interpolate

import pandas as pd

import math as m

from kalman import KalmanFilter

class sensors:
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
        self.filteredAcc = []
        self.velocity = []
        self.position = []
        self.timeA = []

        self.dt = 1.0/60
        self.F = np.array([[1, self.dt, 0.5*self.dt**2], [0, 1, self.dt], [0, 0, 1]])
        self.H = np.array([0, 0, 1]).reshape(1, 3)
        self.Q = np.array([[0.2, 0.0, 0.0], [0.0, 0.1, 0.0], [0.0, 0.0, 10e-4]])
        self.R = 0.0020

        self.timeAxis()
        self.accFilter()
        self.accTodist()
        
        sensors.sensor_count += 1

    def accFilter(self):
        fs = self.freq 
        cutoff = 2
        nyq = 0.5 * fs  
        order = 2
        normal_cutoff = cutoff/nyq

        for nAcc in self.rawAcc:
            """y = signal.medfilt(nAcc, 3)
            b, a = signal.butter(order, normal_cutoff, btype="low")
            ac = signal.filtfilt(b, a, y)

            self.newTime = np.linspace(0, self.frame_count-1, (self.frame_count-1)*10)
            
            f = interpolate.CubicSpline(self.frame_array, ac)
            aa = f(self.newTime)"""

            self.X0 = np.array([0, 0, nAcc[0]])
            self.P0 = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0.0020]])

            kf = KalmanFilter(F=self.F, H=self.H, Q=self.Q, R=self.R, x0=self.X0, P=self.P0)
            predictions = []
            
            for z in nAcc:
                predictions.append(np.dot(self.H, kf.predict())[0])
                kf.update(z)
            self.filteredAcc.append(predictions)

    def accTodist(self):
        func = lambda x, ac: ac
        for a in self.filteredAcc:
            tempV = []
            tempP = []
            Vsum = 0
            Psum = 0
            i = 1
            for i in range(len(a)):  
                t1 = (i-1)/60
                t2 = i/60

                v = quad(func, t2, t1, args=(a[i]))
                Vx = v[1] - v[0]
                Vsum += Vx
                tempV.append(float(Vsum))

                p = quad(func, t2, t1, args=(v[0]))
                Px = p[1] - p[0]
                Psum += Px
                tempP.append(float(Psum))

                """aaa = [a[i-1], a[i]]
                t = [t1, t2]

                v = cumtrapz(aaa, initial=0)
                Vx = v[1]
                Vsum += Vx
                tempV.append(Vx)

                p = cumtrapz(v)
                Psum += p
                tempP.append(p)"""

            self.velocity.append(tempV)
            self.position.append(tempP)
    
    def timeAxis(self):
        for i in range(self.frame_count):
            self.timeA.append(i/self.freq)
