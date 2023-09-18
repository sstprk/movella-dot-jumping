import matplotlib.pyplot as plt
import matplotlib.animation as animation

from sensor import sensors

sensorLB = sensors("C:\\Users\\Salih\\OneDrive\\Desktop\\Data\\XDOT\\Sali\\1\\LowerBody.xlsx", 60)
sensorLUL = sensors("C:\\Users\\Salih\\OneDrive\\Desktop\\Data\\XDOT\\Sali\\1\\LeftUpperLeg.xlsx", 60)
sensorRUL = sensors("C:\\Users\\Salih\\OneDrive\\Desktop\\Data\\XDOT\\Sali\\1\\RightUpperLeg.xlsx", 60)

fig = plt.figure()

ax = fig.add_subplot(projection="3d")

line, = ax.plot(sensorLB.position[0][0], sensorLB.position[1][0], sensorLB.position[2][0], color="black", marker="o")

def update(num, data, line):
    line.set_data(data[0][:num], data[1][:num])
    line.set_3d_properties(data[2][:num]) 
    return line

ani = animation.FuncAnimation(fig, update, frames=sensorLB.frame_count, fargs=(sensorLB.position, line), interval=30, blit=False)

plt.show()