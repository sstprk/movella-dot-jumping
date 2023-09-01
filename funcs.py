#Salih Toprak
import numpy as np
from scipy.integrate import cumtrapz, quad
import scipy.signal as signal
import math as m

class functions:
    def __init__(self):
        pass

    def accFilter(acc, freq, Fs=20):
        [b,a]=signal.butter(2,Fs/freq,'low'); 
        ac=signal.lfilter(b,a,acc);
        return ac

    def accTodist(a, t):
        def func(x, ac):
            return ac
        loc = 0
        location = []
        Vo = 0
        Po = 0
        i = 1
        for i in range(t):  
            t1 = (i-1)/60
            t2 = i/60      
            v = quad(func, t1, t2, args=(a[i]))
            Vo += v[0]
            p = quad(func, t1, t2, args=(Vo))
            location.append(float(p[0]))
        return location
    
    def timeAxis(frame_count, freq):
        timeAx = []
        for i in range(frame_count):
            timeAx.append(i/freq)
        return timeAx