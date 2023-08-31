#Salih Toprak
from funcs import functions
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import pandas as pd

path = "C:\\Users\\Salih\\Desktop\\Data\\XDOT\\Sali\\DenemeFreeAcc2\\Deneme2.xlsx"

df = pd.DataFrame(pd.read_excel(path))

acc_x = list(df.loc[:,"FreeAcc_X"])
acc_y = list(df.loc[:,"FreeAcc_Y"])
acc_z = list(df.loc[:,"FreeAcc_Z"])

locationX = functions.accTodist(acc_x, len(acc_x))
locationY = functions.accTodist(acc_y, len(acc_y))
locationZ = functions.accTodist(acc_z, len(acc_z))

plt.figure(1)

plt.subplot(2,3,1)
plt.title("Pos X")
plt.plot(locationX, color="green")
plt.subplot(2,3,2)
plt.title("Pos Y")
plt.plot(locationY, color="blue")
plt.subplot(2,3,3)
plt.title("Pos Z")
plt.plot(locationZ, color="red")
plt.subplot(2,3,4)
plt.title("Acc X")
plt.plot(acc_x, color="green")
plt.subplot(2,3,5)
plt.title("Acc Y")
plt.plot(acc_y, color="blue")
plt.subplot(2,3,6)
plt.title("Acc Z")
plt.plot(acc_z, color="red")

fig = plt.figure(2)
ax = fig.add_subplot(111, projection="3d")
ax.plot(locationX, locationY, locationZ, color="black")
plt.show()

#Deneme1 = 33.5 cm
#Deneme2 = 13 cm
#Deneme3 = 32.5 cm
