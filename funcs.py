#Salih Toprak
import numpy as np
from scipy.integrate import cumtrapz, quad
import math as m

class functions:
    def __init__(self):
        pass

    def accFilter(acc):
        pass

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
            Vo += v[1]
            p = quad(func, t1, t2, args=(Vo))
            Po += p[1]
            location.append(float(Po))
        return location