import matplotlib.pyplot as plt
import matplotlib.animation as animation
from funcs import functions

cls = functions("C:\\Users\\Salih\\Desktop\\Data\\XDOT\\Sali\\Swing1\\Swing1.xlsx")
fig = plt.figure()

ax = fig.add_subplot(projection="3d")
line, = ax.plot(cls.locationX[0], cls.locationY[0], cls.locationZ[0], color="black", marker="o")

def update(num, data, line):
    line.set_data(data[0][:num], data[1][:num])
    line.set_3d_properties(data[2][:num])
    return line
ax.set(xlim3d=(-10, 10), xlabel='X')
ax.set(ylim3d=(-10, 10), ylabel='Y')
ax.set(zlim3d=(-10, 10), zlabel='Z')

ani = animation.FuncAnimation(fig, update, frames=len(cls.locationX), fargs=(cls.pos, line), interval=30, blit=False)

plt.show()