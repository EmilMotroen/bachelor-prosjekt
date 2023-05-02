"""
    ***Description***
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


search_diameter = 100
num_points = 100000
#size of points on the plot
close_point_size = 2

#random data
data = {
    'X': np.random.randint(low=0, high=512, size=num_points),
    'Y': np.random.randint(low=0, high=1024, size=num_points),
    'Z': np.random.randint(low=0, high=8, size=num_points),
}

#make dataframe of X,Y,Z data
dataframe = pd.DataFrame(data)


#find all values on Z = 0
z0_values = dataframe.loc[dataframe['Z'] == 0]
if len(z0_values) == 0:
    print("error! no points with 0 on z-axis")
    exit()
    
#select random point with Z = 0
#contains all the idx in dataframe where z=1, sample selects one random and iloc[0] returns row with the idx
z0_point = z0_values.sample(n=1).iloc[0]
#z0_point['X'] = z0_point[0], z0_point['Y'] = z0_point[1]

#change values to 0 for the test
z0_point.X = 0
z0_point.Y = 0
z0_point.Z = 0


#select random point with Z = 1
z1_values = dataframe.loc[dataframe['Z'] == 1]
if len(z1_values) == 0:
    print("error! no points with 1 on z-axis")
    exit()
#select point on z-axis with z = 1
z1_point = z1_values.sample(n=1).iloc[0]

#change values for the test
z1_point.X = 50
z1_point.Y = 100
z1_point.Z = 1


#find direction vector from Z = 0 to Z = 1
direction_vector = np.array([z1_point.X - z0_point.X, z1_point.Y - z0_point.Y, z1_point.Z - z0_point.Z])

#use direction vector to expand the line from Z = 0 to Z = 1 
extended_point = z0_point + direction_vector * 16


#find all values on Z = z
#			*** make for loop to go through all instead ***
z2_values = dataframe.loc[dataframe['Z'] == 2]
if len(z2_values) == 0:
    print("error! no points with 2 on z-axis")
    exit()
    
z3_values = dataframe.loc[dataframe['Z'] == 3]
if len(z3_values) == 0:
    print("error! no points with 3 on z-axis")
    exit()

z4_values = dataframe.loc[dataframe['Z'] == 4]
if len(z4_values) == 0:
    print("error! no points with 4 on z-axis")
    exit()
    
z5_values = dataframe.loc[dataframe['Z'] == 5]
if len(z5_values) == 0:
    print("error! no points with 5 on z-axis")
    exit()
    
z6_values = dataframe.loc[dataframe['Z'] == 6]
if len(z6_values) == 0:
    print("error! no points with 6 on z-axis")
    exit()
    
z7_values = dataframe.loc[dataframe['Z'] == 7]
if len(z7_values) == 0:
    print("error! no points with 7 on z-axis")
    exit()


#find Xn and Yn values from Zn
#			*** make for loop to go through all instead ***
x2_values = z2_values['X']
y2_values = z2_values['Y']

x3_values = z3_values['X']
y3_values = z3_values['Y']

x4_values = z4_values['X']
y4_values = z4_values['Y']

x5_values = z5_values['X']
y5_values = z5_values['Y']

x6_values = z6_values['X']
y6_values = z6_values['Y']

x7_values = z7_values['X']
y7_values = z7_values['Y']


#find where Xn and Yn hit layer Zn
#			*** make for loop to go through all instead ***
x2 = np.interp(2, [z0_point['Z'], extended_point[2]], [z0_point['X'], extended_point[0]])
y2 = np.interp(2, [z0_point['Z'], extended_point[2]], [z0_point['Y'], extended_point[1]])

x3 = np.interp(3, [z0_point['Z'], extended_point[2]], [z0_point['X'], extended_point[0]])
y3 = np.interp(3, [z0_point['Z'], extended_point[2]], [z0_point['Y'], extended_point[1]])

x4 = np.interp(4, [z0_point['Z'], extended_point[2]], [z0_point['X'], extended_point[0]])
y4 = np.interp(4, [z0_point['Z'], extended_point[2]], [z0_point['Y'], extended_point[1]])

x5 = np.interp(5, [z0_point['Z'], extended_point[2]], [z0_point['X'], extended_point[0]])
y5 = np.interp(5, [z0_point['Z'], extended_point[2]], [z0_point['Y'], extended_point[1]])

x6 = np.interp(6, [z0_point['Z'], extended_point[2]], [z0_point['X'], extended_point[0]])
y6 = np.interp(6, [z0_point['Z'], extended_point[2]], [z0_point['Y'], extended_point[1]])

x7 = np.interp(7, [z0_point['Z'], extended_point[2]], [z0_point['X'], extended_point[0]])
y7 = np.interp(7, [z0_point['Z'], extended_point[2]], [z0_point['Y'], extended_point[1]])

#find close points on layes Zn within search diameter
#			*** make for loop to go through all instead ***
close_points_z2 = z2_values[((z2_values['X'] - x2)**2 + (z2_values['Y'] - y2)**2) < (search_diameter / 2)**2]
close_points_z3 = z3_values[((z3_values['X'] - x3)**2 + (z3_values['Y'] - y3)**2) < (search_diameter / 2)**2]
close_points_z4 = z4_values[((z4_values['X'] - x4)**2 + (z4_values['Y'] - y4)**2) < (search_diameter / 2)**2]
close_points_z5 = z5_values[((z5_values['X'] - x5)**2 + (z5_values['Y'] - y5)**2) < (search_diameter / 2)**2]
close_points_z6 = z6_values[((z6_values['X'] - x6)**2 + (z6_values['Y'] - y6)**2) < (search_diameter / 2)**2]
close_points_z7 = z7_values[((z7_values['X'] - x7)**2 + (z7_values['Y'] - y7)**2) < (search_diameter / 2)**2]


#print if there are no points close to line
for i in range(2, 8):
    close = f"close_points_z{i}"
    close_point_list = globals()[close]
    if close_point_list.empty:
        print(f"Dataframe {close} is empty. No close points on layer {i}")
        

#2D figures of close points for layer Z = z
"""
#plot all points on Z = 2
fig = plt.figure()
plt.scatter(x2_values, y2_values)
plt.scatter(close_points_z2.X, close_points_z2.Y)
plt.title('Points where Z=2')
plt.xlabel('X')
plt.ylabel('Y')

#plot all points on Z = 3
fig = plt.figure()
plt.scatter(x3_values, y3_values)
plt.scatter(close_points_z3.X, close_points_z3.Y)
plt.title('Points where Z=3')
plt.xlabel('X')
plt.ylabel('Y')

#plot all points on Z = 7
fig = plt.figure()
plt.scatter(x7_values, y7_values)
plt.scatter(close_points_z7.X, close_points_z7.Y)
plt.title('Points where Z=7')
plt.xlabel('X')
plt.ylabel('Y')
"""


#3D plot of ALPIDE stack with 8 layers.
#points within search diameter are highlighted on each layer
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
# ax.scatter(dataframe.X, dataframe.Y, dataframe.Z)

#plot starting points and close points
ax.scatter(z0_point.X, z0_point.Y, z0_point.Z, color = 'green', s = 50, label = 'Start point (layer 0)')
ax.scatter(z1_point.X, z1_point.Y, z1_point.Z, color = 'red', s = 50, label = 'Next point (layer 1)')
ax.scatter(extended_point[0], extended_point[1], extended_point[2], color = 'purple', s = 50, label = 'Extended')

#plot close points
ax.scatter(close_points_z2.X, close_points_z2.Y, close_points_z2.Z, color = 'magenta', s = close_point_size)
ax.scatter(close_points_z3.X, close_points_z3.Y, close_points_z3.Z, color = 'aquamarine', s = close_point_size)
ax.scatter(close_points_z4.X, close_points_z4.Y, close_points_z4.Z, color = 'yellow', s = close_point_size)
ax.scatter(close_points_z5.X, close_points_z5.Y, close_points_z5.Z, color = 'green', s = close_point_size)
ax.scatter(close_points_z6.X, close_points_z6.Y, close_points_z6.Z, color = 'pink', s = close_point_size)
ax.scatter(close_points_z7.X, close_points_z7.Y, close_points_z7.Z, color = 'khaki', s = close_point_size)

#set axis view limit same as ALPIDE stack size
ax.set_xlim(0,511)
ax.set_ylim(0,1023) 
ax.set_zlim(0,7)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

#line between points
# ax.plot([z0_point.X, z1_point.X], [z0_point.Y, z1_point.Y], [z0_point.Z, z1_point.Z], c='black')
line_points = np.array([[z0_point.X, z0_point.Y, z0_point.Z], [z1_point.X, z1_point.Y, z1_point.Z], [extended_point[0], extended_point[1], extended_point[2]]])
ax.plot(line_points[:, 0], line_points[:, 1], line_points[:, 2], c='orange')

ax.legend()

plt.show()






