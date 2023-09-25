#Salih Toprak
from sensor import Sensor

import matplotlib.pyplot as plt

sensorOther = Sensor("C:\\Users\\Salih\\OneDrive\\Desktop\\Data\\XDOT\\Sali\\Swing1\\Swing1.xlsx")
sensorLB = Sensor("C:\\Users\\Salih\\OneDrive\\Desktop\\Data\\XDOT\\Sali\\2\\LowerBody.xlsx")
sensorLUL = Sensor("C:\\Users\\Salih\\OneDrive\\Desktop\\Data\\XDOT\\Sali\\2\\LeftUpperLeg.xlsx")
sensorRUL = Sensor("C:\\Users\\Salih\\OneDrive\\Desktop\\Data\\XDOT\\Sali\\2\\RightUpperLeg.xlsx")

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
plt.plot(sensorLB.timeA, sensorLB.filteredAcc[0], color="green", lw=1)
plt.subplot(2,3,5)
plt.title("fAcc Y")
plt.plot(sensorLB.timeA, sensorLB.filteredAcc[1], color="blue", lw=1)
plt.subplot(2,3,6)
plt.title("fAcc Z")
plt.plot(sensorLB.timeA, sensorLB.filteredAcc[2], color="red", lw=1)

#Figure for position on each axis
plt.figure(2)

plt.subplot(2,3,1)
plt.title("Pos X")
plt.plot(sensorLB.timeA, sensorLB.rawPosition[0], color="green", lw=1)
plt.subplot(2,3,2)
plt.title("Pos Y")
plt.plot(sensorLB.timeA, sensorLB.rawPosition[1],  color="blue", lw=1)
plt.subplot(2,3,3)
plt.title("Pos Z")
plt.plot(sensorLB.timeA, sensorLB.rawPosition[2], color="red", lw=1)
plt.subplot(2,3,4)
plt.title("Vel X")
plt.plot(sensorLB.timeA, sensorLB.filteredPos[0], color="green", lw=1)
plt.subplot(2,3,5)
plt.title("Vel Y")
plt.plot(sensorLB.timeA, sensorLB.filteredPos[1], color="blue", lw=1)
plt.subplot(2,3,6)
plt.title("Vel Z")
plt.plot(sensorLB.timeA, sensorLB.filteredPos[2], color="red", lw=1)

plt.figure(3)

plt.subplot(2,3,1)
plt.title("Pos X")
plt.plot(sensorLB.timeA, sensorLB.rawVelocity[0], color="green", lw=1)
plt.subplot(2,3,2)
plt.title("Pos Y")
plt.plot(sensorLB.timeA, sensorLB.rawVelocity[1],  color="blue", lw=1)
plt.subplot(2,3,3)
plt.title("Pos Z")
plt.plot(sensorLB.timeA, sensorLB.rawVelocity[2], color="red", lw=1)
plt.subplot(2,3,4)
plt.title("Vel X")
plt.plot(sensorLB.timeA, sensorLB.filteredVel[0], color="green", lw=1)
plt.subplot(2,3,5)
plt.title("Vel Y")
plt.plot(sensorLB.timeA, sensorLB.filteredVel[1], color="blue", lw=1)
plt.subplot(2,3,6)
plt.title("Vel Z")
plt.plot(sensorLB.timeA, sensorLB.filteredVel[2], color="red", lw=1)

#Figure for 3D displacement
fig = plt.figure(4)

ax = fig.add_subplot(111, projection="3d")
plt.title("LB")

ax.plot(sensorLB.filteredPos[0], sensorLB.filteredPos[1], sensorLB.filteredPos[2], color="black", lw=1)
ax.set(xlabel="X Axis(m)")
ax.set(ylabel="Y Axis(m)")
ax.set(zlabel="Z Axis(m)")

fig = plt.figure(5)

ax = fig.add_subplot(111, projection="3d")
plt.title("LUL")

ax.plot(sensorLUL.filteredPos[0], sensorLUL.filteredPos[1], sensorLUL.filteredPos[2], color="green", lw=1)
ax.set(xlabel="X Axis(m)")
ax.set(ylabel="Y Axis(m)")
ax.set(zlabel="Z Axis(m)")

fig = plt.figure(6)

ax = fig.add_subplot(111, projection="3d")
plt.title("RUL")

ax.plot(sensorRUL.filteredPos[0], sensorRUL.filteredPos[1], sensorRUL.filteredPos[2], color="red", lw=1)
ax.set(xlabel="X Axis(m)")
ax.set(ylabel="Y Axis(m)")
ax.set(zlabel="Z Axis(m)")

fig = plt.figure(7)

ax = fig.add_subplot(111, projection="3d")
plt.title("Other")

ax.plot(sensorOther.filteredPos[0], sensorOther.filteredPos[1], sensorOther.filteredPos[2], color="black", lw=1)
ax.set(xlabel="X Axis(m)")
ax.set(ylabel="Y Axis(m)")
ax.set(zlabel="Z Axis(m)")

plt.show()
