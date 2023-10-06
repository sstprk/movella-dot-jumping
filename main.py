#Salih Toprak
from sensor import Sensor

import matplotlib.pyplot as plt

sensorOther = Sensor("C:\\Users\\Salih\\OneDrive\\Desktop\\Data\\XDOT\\Sali\\Swing1\\Swing1.xlsx")
sensorLB = Sensor("C:\\Users\\Salih\\OneDrive\\Desktop\\Data\\XDOT\\Sali\\Walking\\LowerBody.xlsx")
sensorLUL = Sensor("C:\\Users\\Salih\\OneDrive\\Desktop\\Data\\XDOT\\Sali\\Walking\\LeftUpperLeg.xlsx")
sensorRUL = Sensor("C:\\Users\\Salih\\OneDrive\\Desktop\\Data\\XDOT\\Sali\\Walking\\RightUpperLeg.xlsx")

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
plt.plot(sensorLB.newAcc[:, 0], color="green", lw=1)
plt.subplot(2,3,5)
plt.title("fAcc Y")
plt.plot(sensorLB.newAcc[:, 1], color="blue", lw=1)
plt.subplot(2,3,6)
plt.title("fAcc Z")
plt.plot(sensorLB.newAcc[:, 2], color="red", lw=1)

#Figure for position on each axis
plt.figure(2)

plt.subplot(2,3,1)
plt.title("Pos X")
plt.plot(sensorOther.Position[:, 0], color="green", lw=1)
plt.subplot(2,3,2)
plt.title("Pos Y")
plt.plot(sensorOther.Position[:, 1],  color="blue", lw=1)
plt.subplot(2,3,3)
plt.title("Pos Z")
plt.plot(sensorOther.Position[:, 2], color="red", lw=1)
plt.subplot(2,3,4)
plt.title("Vel X")
plt.plot(sensorOther.Velocity[:, 0], color="green", lw=1)
plt.subplot(2,3,5)
plt.title("Vel Y")
plt.plot(sensorOther.Velocity[:, 1], color="blue", lw=1)
plt.subplot(2,3,6)
plt.title("Vel Z")
plt.plot(sensorOther.Velocity[:, 2], color="red", lw=1)

#Figure for 3D displacement
fig = plt.figure(3)

ax = fig.add_subplot(111, projection="3d")
plt.title("LB")

ax.plot(sensorLB.Position[:,0], sensorLB.Position[:,1], sensorLB.Position[:,2], color="black", lw=1)
ax.set(xlabel="X Axis(m)")
ax.set(ylabel="Y Axis(m)")
ax.set(zlabel="Z Axis(m)")

fig = plt.figure(4)

ax = fig.add_subplot(111, projection="3d")
plt.title("LUL")

ax.plot(sensorLUL.Position[:,0], sensorLUL.Position[:,1], sensorLUL.Position[:,2], color="green", lw=1)
ax.set(xlabel="X Axis(m)")
ax.set(ylabel="Y Axis(m)")
ax.set(zlabel="Z Axis(m)")

fig = plt.figure(5)

ax = fig.add_subplot(111, projection="3d")
plt.title("RUL")

ax.plot(sensorRUL.Position[:,0], sensorRUL.Position[:,1], sensorRUL.Position[:,2], color="red", lw=1)
ax.set(xlabel="X Axis(m)")
ax.set(ylabel="Y Axis(m)")
ax.set(zlabel="Z Axis(m)")

fig = plt.figure(6)

ax = fig.add_subplot(111, projection="3d")
plt.title("Other")

ax.plot(sensorOther.Position[:,0], sensorOther.Position[:,1], sensorOther.Position[:,2], color="black", lw=1)
ax.set(xlabel="X Axis(m)")
ax.set(ylabel="Y Axis(m)")
ax.set(zlabel="Z Axis(m)")

plt.show()
