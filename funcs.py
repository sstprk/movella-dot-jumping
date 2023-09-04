#Salih Toprak
import numpy as np
from scipy.integrate import quad
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

        self.locationX = functions.accTodist(self.filteredAccX, len(self.filteredAccX))
        self.locationY = functions.accTodist(self.filteredAccY, len(self.filteredAccY))
        self.locationZ = functions.accTodist(self.filteredAccZ, len(self.filteredAccZ))

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
        def func(x, ac):
            return ac
        position = []
        i = 1
        for i in range(t):  
            t1 = (i-1)/60
            t2 = i/60      
            v = quad(func, t1, t2, args=(a[i]-0.55))
            p = quad(func, t1, t2, args=(v[0]))
            position.append(float(p[0]))
        return position
    
    def timeAxis(frame_count, freq):
        timeAx = []
        for i in range(frame_count):
            timeAx.append(i/freq)
        return timeAx