#Salih Toprak
from funcs import functions
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import pandas as pd

path = "C:\\Users\\Salih\\Desktop\\Data\\XDOT\\Sali\\Swing1\\Swing1.xlsx"

df = pd.DataFrame(pd.read_excel(path))

rawAcc_x = list(df.loc[:,"FreeAcc_X"])
rawAcc_y = list(df.loc[:,"FreeAcc_Y"])
rawAcc_z = list(df.loc[:,"FreeAcc_Z"])

filteredAccX = functions.accFilter(rawAcc_x, 60)
filteredAccY = functions.accFilter(rawAcc_y, 60)
filteredAccZ = functions.accFilter(rawAcc_z, 60)

locationX = functions.accTodist(filteredAccX, len(filteredAccX))
locationY = functions.accTodist(filteredAccY, len(filteredAccY))
locationZ = functions.accTodist(filteredAccZ, len(filteredAccZ))

timeAxis = functions.timeAxis(len(filteredAccY), 60)
plt.figure(1)

plt.subplot(2,3,1)
plt.title("Pos X")
plt.plot(timeAxis, locationX , color="green")
plt.subplot(2,3,2)
plt.title("Pos Y")
plt.plot(timeAxis, locationY, color="blue")
plt.subplot(2,3,3)
plt.title("Pos Z")
plt.plot(timeAxis, locationZ, color="red")
plt.subplot(2,3,4)
plt.title("Acc X")
plt.plot(timeAxis, filteredAccX, color="green")
plt.subplot(2,3,5)
plt.title("Acc Y")
plt.plot(timeAxis, filteredAccY, color="blue")
plt.subplot(2,3,6)
plt.title("Acc Z")
plt.plot(timeAxis, filteredAccZ, color="red")

fig = plt.figure(2)
ax = fig.add_subplot(111, projection="3d")
ax.plot(locationX, locationY, locationZ, color="black")
plt.show()

#Deneme1 = 33.5 cm
#Deneme2 = 13 cm
#Deneme3 = 32.5 cm
