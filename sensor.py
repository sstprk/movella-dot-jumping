#Salih Toprak
import numpy as np

from scipy.integrate import quad,cumtrapz
import scipy.signal as signal
import scipy.interpolate as interpolate

import pandas as pd

import math as m

from pykalman import KalmanFilter

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

        self.timeAxis()
        self.kalmanF()
        """self.accFilter()
        self.accTodist()"""
        
        sensors.sensor_count += 1

    def accFilter(self):
        fs = self.freq 
        cutoff = 2
        nyq = 0.5 * fs  
        order = 2
        normal_cutoff = cutoff/nyq

        for nAcc in self.rawAcc:
            y = signal.medfilt(nAcc, 3)
            b, a = signal.butter(order, normal_cutoff, btype="low")
            ac = signal.filtfilt(b, a, y)

            self.newTime = np.linspace(0, self.frame_count-1, (self.frame_count-1)*10)
            
            f = interpolate.CubicSpline(self.frame_array, ac)
            aa = f(self.newTime)
            self.filteredAcc.append(aa)

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

                """v = quad(func, t2, t1, args=(a[i]))
                Vx = v[0] - v[1]
                Vsum += Vx
                tempV.append(float(Vx))

                p = quad(func, t2, t1, args=(v[0]))
                Px = p[0] - p[1]
                Psum += Px
                tempP.append(float(Px))"""

                aaa = [a[i], a[i-1]]
                t = [t2, t1]

                v = cumtrapz(aaa, t, initial=0)
                Vx = v[1]
                Vsum += Vx
                tempV.append(float(Vx))

                p = cumtrapz(v, t)
                Psum += p
                tempP.append(float(p))

            self.velocity.append(tempV)
            self.position.append(tempP)
    
    def timeAxis(self):
        for i in range(self.frame_count):
            self.timeA.append(i/self.freq)
    
    def kalmanF(self):
        use_HP_signal = 0
        for idx in range(3):
            if use_HP_signal:
                #AccX_Value = AccX_HP
                AccX_Variance = 0.0007
            else:    
                AccX_Value = np.array(self.rawAcc[idx])
                AccX_Variance = 0.0020

            # time step
            dt = 1/60

            # transition_matrix  
            F = [[1, dt, 0.5*dt**2], 
                [0,  1,       dt],
                [0,  0,        1]]

            # observation_matrix   
            H = [0, 0, 1]

            # transition_covariance 
            Q = [[0.2,    0,      0], 
                [  0,  0.1,      0],
                [  0,    0,  10e-4]]

            # observation_covariance 
            R = AccX_Variance

            # initial_state_mean
            X0 = [0,
                0,
                AccX_Value[0, 0]]

            # initial_state_covariance
            P0 = [[  0,    0,               0], 
                [  0,    0,               0],
                [  0,    0,   AccX_Variance]]

            n_timesteps = AccX_Value.shape[0]
            n_dim_state = 3
            filtered_state_means = np.zeros((n_timesteps, n_dim_state))
            filtered_state_covariances = np.zeros((n_timesteps, n_dim_state, n_dim_state))

            kf = KalmanFilter(transition_matrices = F, 
                            observation_matrices = H, 
                            transition_covariance = Q, 
                            observation_covariance = R, 
                            initial_state_mean = X0, 
                            initial_state_covariance = P0)
            
            for t in range(n_timesteps):
                if t == 0:
                    filtered_state_means[t] = X0
                    filtered_state_covariances[t] = P0
                else:
                    filtered_state_means[t], filtered_state_covariances[t] = (
                    kf.filter_update(
                    filtered_state_means[t-1],
                    filtered_state_covariances[t-1],
                    AccX_Value[t, 0]
                    )
                )
            self.filteredAcc.append(filtered_state_means[:, 2])
            self.velocity.append(filtered_state_means[:, 1])
            self.position.append(filtered_state_means[:, 0])