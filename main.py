#Salih Toprak
from funcs import functions
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import pandas as pd

path = "C:\\Users\\Salih\\Desktop\\Data\\XDOT\\Sali\\DenemeFreeAcc3\\Deneme3.xlsx"

df = pd.DataFrame(pd.read_excel(path))

acc_x = list(df.loc[:,"FreeAcc_X"])
acc_y = list(df.loc[:,"FreeAcc_Y"])
acc_z = list(df.loc[:,"FreeAcc_Z"])

locationX= functions.accTodist(acc_x, len(acc_x))
locationY = functions.accTodist(acc_y, len(acc_y))
locationZ = functions.accTodist(acc_z, len(acc_z))

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.plot(locationX, locationY, locationZ)
plt.show()

#Deneme1 = 33.5 cm
#Deneme2 = 13 cm
#Deneme3 = 32.5 cm
