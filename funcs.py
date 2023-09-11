#Salih Toprak
import numpy as np
from scipy.integrate import quad,cumtrapz
import scipy.signal as signal
import math as m
import pandas as pd

class functions:
    def __init__(self, path):
        self.path = path
        self.df = pd.DataFrame(pd.read_excel(self.path))

        self.rawAcc_x = list(self.df.loc[:,"FreeAcc_X"])
        self.rawAcc_y = list(self.df.loc[:,"FreeAcc_Y"])
        self.rawAcc_z = list(self.df.loc[:,"FreeAcc_Z"])

        self.filteredAccX = functions.accFilter(self.rawAcc_x)
        self.filteredAccY = functions.accFilter(self.rawAcc_y)
        self.filteredAccZ = functions.accFilter(self.rawAcc_z)

        self.locationX, self.velocityX = functions.accTodist(self.filteredAccX, len(self.filteredAccX))
        self.locationY, self.velocityY = functions.accTodist(self.filteredAccY, len(self.filteredAccY))
        self.locationZ, self.velocityZ = functions.accTodist(self.filteredAccZ, len(self.filteredAccZ))

        self.pos = [self.locationX, self.locationY, self.locationZ]

        self.timeA = functions.timeAxis(len(self.filteredAccY), 60)

    def accFilter(acc):
        fs = 30.0 
        cutoff = 2
        nyq = 0.5 * fs  
        order = 2
        normal_cutoff = cutoff/nyq
        y = signal.medfilt(acc, 21)
        b, a = signal.butter(order, normal_cutoff, btype="low", analog=False)
        ac = signal.filtfilt(b, a, y)
        return ac

    def accTodist(a, t):
        func = lambda x, ac: ac
        
        position = []
        velocity = []
        i = 1
        for i in range(t):  
            t1 = (i-1)/60
            t2 = i/60
            Vsum = 0
            Psum = 0

            v = quad(func, t1, t2, args=(a[i]))
            Vx = v[0] - v[1]
            Vsum += Vx
            p = quad(func, t1, t2, args=(Vsum))
            velocity.append(float(Vx))
            Px = p[0] - p[1]
            Psum += Px
            position.append(float(Psum))
        return position, velocity
    
    def timeAxis(frame_count, freq):
        timeAx = []
        for i in range(frame_count):
            timeAx.append(i/freq)
        return timeAx