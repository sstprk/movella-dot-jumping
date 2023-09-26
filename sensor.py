#Salih Toprak
import numpy as np

from scipy.integrate import quad,cumtrapz
import scipy.signal as signal
import scipy.interpolate as interpolate

import pandas as pd

import math as m

from pykalman import KalmanFilter
#from kalman import KalmanFilter

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
            dt = 0.01
            F = np.array([[1, dt, 0.5*dt**2], [0, 1, dt], [0, 0, 1]])
            H = np.array([0, 0, 1]).reshape(1, 3)
            Q = np.array([[0.2, 0.0, 0.0], [0.0, 0.1, 0.0], [0.0, 0.0, 10e-4]])
            R = 0.0020
            P0 = np.array([[0, 0, 0], [0, 0, 0], [0, 0, R]])
            X0 = np.array([0, 0, data[0]])

            kf = KalmanFilter(transition_matrices=F, observation_matrices=H, transition_covariance=Q, observation_covariance=R, initial_state_mean=X0, initial_state_covariance=P0)
            predictions = []
            n_timesteps = len(data)
            n_dim_state = 3
            filtered_state_means = np.zeros((n_timesteps, n_dim_state))
            filtered_state_covariances = np.zeros((n_timesteps, n_dim_state, n_dim_state))
            
            for t in range(n_timesteps):
                if t == 0:
                    filtered_state_means[t] = X0
                    filtered_state_covariances[t] = P0
                else:
                    filtered_state_means[t], filtered_state_covariances[t] = kf.filter_update()

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
