#Salih Toprak
import funcs
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import pandas as pd

#funcs.py
cls = funcs.functions("C:\\Users\\Salih\\Desktop\\Data\\XDOT\\Sali\\Walk2\\Walk2.xlsx")

#Figure for comparison between raw and filtered data
plt.figure(1)

plt.subplot(2,3,1)
plt.title("rAcc X")
plt.plot(cls.timeA, cls.rawAcc_x, color="green")
plt.subplot(2,3,2)
plt.title("rAcc Y")
plt.plot(cls.timeA, cls.rawAcc_y, color="blue")
plt.subplot(2,3,3)
plt.title("rAcc Z")
plt.plot(cls.timeA, cls.rawAcc_z, color="red")
plt.subplot(2,3,4)
plt.title("fAcc X")
plt.plot(cls.timeA, cls.filteredAccX, color="green")
plt.subplot(2,3,5)
plt.title("fAcc Y")
plt.plot(cls.timeA, cls.filteredAccY, color="blue")
plt.subplot(2,3,6)
plt.title("fAcc Z")
plt.plot(cls.timeA, cls.filteredAccZ, color="red")

#Figure for position on each axis
plt.figure(2)

plt.subplot(1,3,1)
plt.plot(cls.timeA, cls.locationX , color="green")
plt.subplot(1,3,2)
plt.plot(cls.timeA, cls.locationY, color="blue")
plt.subplot(1,3,3)
plt.plot(cls.timeA, cls.locationZ, color="red")

#Figure for 3D displacement
fig = plt.figure(3)

ax = fig.add_subplot(111, projection="3d")
ax.plot(cls.locationX, cls.locationY, cls.locationZ, color="black")

plt.show()

#Deneme1 = 33.5 cm
#Deneme2 = 13 cm
#Deneme3 = 32.5 cm