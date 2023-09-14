#Salih Toprak
import numpy as np
from scipy.integrate import quad,cumtrapz
import scipy.signal as signal
import scipy.interpolate as interpolate
import pandas as pd

class functions:
    def __init__(self, path):
        self.path = path
        self.df = pd.DataFrame(pd.read_excel(self.path))

        #self.rawAcc_x = list(self.df.loc[:,"dv[1]"])
        #self.rawAcc_y = list(self.df.loc[:,"dv[2]"])
        #self.rawAcc_z = list(self.df.loc[:,"dv[3]"])

        self.rawAcc_x = list(self.df.loc[:,"FreeAcc_X"])
        self.rawAcc_y = list(self.df.loc[:,"FreeAcc_Y"])
        self.rawAcc_z = list(self.df.loc[:,"FreeAcc_Z"])

        self.frame_count = list(range(len(self.rawAcc_x)))

        self.filteredAccX = functions.accFilter(self.rawAcc_x, self.frame_count)
        self.filteredAccY = functions.accFilter(self.rawAcc_y, self.frame_count)
        self.filteredAccZ = functions.accFilter(self.rawAcc_z, self.frame_count)

        self.locationX, self.velocityX = functions.accTodist(self.filteredAccX, len(self.filteredAccX))
        self.locationY, self.velocityY = functions.accTodist(self.filteredAccY, len(self.filteredAccY))
        self.locationZ, self.velocityZ = functions.accTodist(self.filteredAccZ, len(self.filteredAccZ))

        self.pos = [self.locationX, self.locationY, self.locationZ]

        self.timeA = functions.timeAxis(len(self.locationX), 60)

    def accFilter(acc, t):
        newTime = np.linspace(0, len(t)-1, (len(t)-1)*2)
        f = interpolate.interp1d(t, acc, kind="cubic")
        aa = f(newTime)

        fs = 30.0 
        cutoff = 2
        nyq = 0.5 * fs  
        order = 2
        normal_cutoff = cutoff/nyq
        y = signal.medfilt(aa, 21)
        b, a = signal.butter(order, normal_cutoff, btype="low")
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
            #t = (t1, t2)
            #aa = (a[i-1], a[i])
            Vsum = 0
            Psum = 0

            #v = cumtrapz(aa, t)
            v = quad(func, t1, t2, args=(a[i]))
            Vx = v[0] - v[1]
            Vsum += Vx
            #p = cumtrapz(aa, t)
            p = quad(func, t1, t2, args=(Vsum))
            Px = p[0] - p[1]
            Psum += Px
            velocity.append(float(Vsum))
            position.append(float(-Psum))
        return position, velocity
    
    def timeAxis(frame_count, freq):
        timeAx = []
        for i in range(frame_count):
            timeAx.append(i/freq)
        return timeAx