#Salih Toprak
import numpy as np
from scipy.integrate import cumtrapz
class functions:
    def __init__(self):
        pass
    def accTodist(a, t):
        loc = 0
        location = []
        for i in range(t):        
            v = cumtrapz(a[i], x=i)
            displc = cumtrapz(v, i)
            loc += displc
            location.append(loc)
        return location