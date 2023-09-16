#Salih Toprak
from sensor import sensors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import pandas as pd
import numpy as np

#funcs.py
sensorLB = sensors("C:\\Users\\Salih\\Desktop\\Data\\XDOT\\Sali\\Swing1\\Swing1.xlsx", 60)
#sensorLUL = sensor()
#sensorRUL = sensor()

#Figure for comparison between raw and filtered data
plt.figure(1)

plt.subplot(2,3,1)
plt.title("rAcc X")
plt.plot(sensorLB.rawAcc[0], color="green", lw=1)
plt.subplot(2,3,2)
plt.title("rAcc Y")
plt.plot(sensorLB.rawAcc[1], color="blue", lw=1)
plt.subplot(2,3,3)
plt.title("rAcc Z")
plt.plot(sensorLB.rawAcc[2], color="red", lw=1)
plt.subplot(2,3,4)
plt.title("fAcc X")
plt.plot(sensorLB.newTime, sensorLB.filteredAcc[0], color="green", lw=1)
plt.subplot(2,3,5)
plt.title("fAcc Y")
plt.plot(sensorLB.newTime, sensorLB.filteredAcc[1], color="blue", lw=1)
plt.subplot(2,3,6)
plt.title("fAcc Z")
plt.plot(sensorLB.newTime, sensorLB.filteredAcc[2], color="red", lw=1)

#Figure for position on each axis
plt.figure(2)

plt.subplot(2,3,1)
plt.title("Pos X")
plt.plot(sensorLB.newTime, sensorLB.position[0], color="green", lw=1)
plt.subplot(2,3,2)
plt.title("Pos Y")
plt.plot(sensorLB.newTime, sensorLB.position[1],  color="blue", lw=1)
plt.subplot(2,3,3)
plt.title("Pos Y")
plt.plot(sensorLB.newTime, sensorLB.position[2], color="red", lw=1)
plt.subplot(2,3,4)
plt.title("Vel X")
plt.plot(sensorLB.newTime, sensorLB.velocity[0], color="green", lw=1)
plt.subplot(2,3,5)
plt.title("Vel Y")
plt.plot(sensorLB.newTime, sensorLB.velocity[1], color="blue", lw=1)
plt.subplot(2,3,6)
plt.title("Vel Z")
plt.plot(sensorLB.newTime, sensorLB.velocity[2], color="red", lw=1)

#Figure for 3D displacement
fig = plt.figure(3)

ax = fig.add_subplot(111, projection="3d")
ax.plot(sensorLB.position[0], sensorLB.position[1], sensorLB.position[2], color="black", lw=1)
ax.set(xlabel="X Axis(m)")
ax.set(ylabel="Y Axis(m)")
ax.set(zlabel="Z Axis(m)")


plt.show()

#Deneme1 = 33.5 cm
#Deneme2 = 13 cm
#Deneme3 = 32.5 cm