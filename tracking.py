"""
Connect tracking program to InfluxDB on RPi or PC 
    Make sure you are on the same network as RPi
    Can make error if no points on each layer
    Tracking from layer 0 to pixel_layers
    See config.ini for configuration
    Visualisation is upside down from real life

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from configparser import ConfigParser


num_points = 100000
search_diameter = 50

# Size of close points on the plot
close_point_size = 5


# Information from 'config.ini', change file before running
config_object = ConfigParser()
config_object.read("config.ini")
login = config_object["INFLUXDB"]
url = login["url"]
bucket = login["bucket"]
token = login["token"]
org = login["org"]

layersdata = config_object["LAYERS"]
num_layers = layersdata["pixel_layers"]


# Create client object to connect to Influx server
client = InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Make it possible to preform queries from Influx
query_api = client.query_api()


# Execute Influx query and retrieve result as Pandas DataFrame
# '|> range(start: -<10>)' is the time from now to the first data you want. "10" is value and "d" is unit (m=minutes, d=days, w=week)
data_frame = query_api.query_data_frame(f'from(bucket:"{bucket}")'
                                        '|> range(start: -10d)'
                                        '|> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")'
                                        '|> keep(columns: ["X", "Y", "Z"])')

# Remove unnecessary columns
pd_data_frame = pd.DataFrame(data_frame)  
pd_data_frame.drop('result', inplace=True, axis=1); pd_data_frame.drop('table', inplace=True, axis=1)  
pd_data_frame.columns = ['X', 'Y', 'Z']
print(f'\n{pd_data_frame}')


def create_value(layer):
    """
    Finds all values for layer in the stack
    """
    values = pd_data_frame.loc[pd_data_frame['Z'] == layer]
    if len(values) == 0:
        print(f"Error! No points on layer: {layer}")
        exit()
    return values


# Find all values where Z = 0
values_layer_0 = create_value(0)
# Select random point with Z = 0
point_layer_0 = values_layer_0.sample(n=1).iloc[0]
# Change point to test program
# point_layer_0.X = 0
# point_layer_0.Y = 0
# point_layer_0.Z = 0

# Find all values where Z = 1
values_layer_1 = create_value(1)
# Select random point with Z = 0
point_layer_1 = values_layer_1.sample(n=1).iloc[0]
# Change point to test program
# point_layer_1.X = 100
# point_layer_1.Y = 50
# point_layer_1.Z = 1


# Find direction vector from layer 0 to layer 1
direction_vector = np.array([point_layer_1.X - point_layer_0.X, point_layer_1.Y - point_layer_0.Y, point_layer_1.Z - point_layer_0.Z])

# Use direction vector to expand the line 
extended_point = point_layer_0 + direction_vector * num_layers


# Gets all values from each layer
for layer in range(2, num_layers):
    values = f"values_layer_{layer}"
    exec(f"{values} = create_value({layer})")


def find_xy_values(values_layer):
    """
    Find all X,Y-values from values in a layer
    """
    x_values = values_layer['X']
    y_values = values_layer['Y']
    return x_values, y_values


for layer in range(2, num_layers):
    values = globals()[f"values_layer_{layer}"]
    x_values, y_values = find_xy_values(values)
    exec(f"x{layer}_values = x_values")
    exec(f"y{layer}_values = y_values")


def interp_xy(layer, point_layer_0, extended_point):
    """
    Find where X and Y hit layer with linear interpolation
    """
    x = np.interp(layer, [point_layer_0['Z'], extended_point[2]], [point_layer_0['X'], extended_point[0]])
    y = np.interp(layer, [point_layer_0['Z'], extended_point[2]], [point_layer_0['Y'], extended_point[1]])
    return x, y


for layer in range(2, num_layers):
    x, y = interp_xy(layer, point_layer_0, extended_point)
    exec(f"x{layer} = x")
    exec(f"y{layer} = y")


def find_close_points(values_layer, x, y):
    """
    Find close points on layer within search diameter
    """
    close_points = values_layer[((values_layer['X'] - x)**2 + (values_layer['Y'] - y)**2) < (search_diameter / 2)**2]
    return close_points


for layer in range(2, num_layers):
    
    values_layer = globals()[f"values_layer_{layer}"]

    x = globals()[f"x{layer}"]

    y = globals()[f"y{layer}"]

    close_points = find_close_points(values_layer, x, y)
    exec(f"close_points_layer_{layer} = close_points")


# Check if a layer has no points close to line 
for layer in range(2, num_layers):
    close = f"close_points_layer_{layer}"
    close_point_list = globals()[close]
    if close_point_list.empty:
        print(f"Dataframe {close} is empty. No close points on layer {layer}")
        

def make_plot(layer):
    """
    2D figures of all points on a layer and close points to the line
    """
    fig = plt.figure()
    
    x_values = globals()[f'x{layer}_values']
    y_values = globals()[f'y{layer}_values']
    close_points = globals()[f'close_points_layer_{layer}']

    plt.scatter(x_values, y_values)
    plt.scatter(close_points.X, close_points.Y)
    plt.title(f'points where Z={layer}')
    plt.xlabel('X')
    plt.ylabel('Y')
    
    # Comment out to see save 2D plot
#     plt.savefig(f"image_layer_{layer}.png")
    
# Comment out to see plot each layer
# for layer in range(2, num_layers):
#     plot = make_plot(layer)
    
    
"""
3D plot of ALPIDE stack
The starting points have a line between them and is extended
Points within search diameter of the line are highlighted on each layer
"""
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Comment out to see all points
# ax.scatter(dataframe.X, dataframe.Y, dataframe.Z) 

ax.scatter(point_layer_0.X, point_layer_0.Y, point_layer_0.Z, color = 'green', s = 50, label = f"Start point ({point_layer_0.X}, {point_layer_0.Y}, {point_layer_0.Z})")
ax.scatter(point_layer_1.X, point_layer_1.Y, point_layer_1.Z, color = 'red', s = 50, label = f"Next point ({point_layer_1.X}, {point_layer_1.Y}, {point_layer_1.Z})")
ax.scatter(extended_point[0], extended_point[1], extended_point[2], color = 'purple', s = 50)

def scatter_close_points(layer):
    """
    Plot close points in 3D 
    """
    close_points = globals()[f"close_points_layer_{layer}"]
    ax.scatter(close_points.X, close_points.Y, close_points.Z, s = close_point_size)

for layer in range(2, num_layers):
    scatter_close_points(layer)


# Set axis view limit same as ALPIDE stack size
ax.set_xlim(0,1023)
ax.set_ylim(0,511) 
ax.set_zlim(0,num_layers-1)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# Line between points
# ax.plot([point_layer_0.X, point_layer_1.X], [point_layer_0.Y, point_layer_1.Y], [point_layer_0.Z, point_layer_1.Z], c='black')
line_points = np.array([[point_layer_0.X, point_layer_0.Y, point_layer_0.Z], [point_layer_1.X, point_layer_1.Y, point_layer_1.Z], [extended_point[0], extended_point[1], extended_point[2]]])
ax.plot(line_points[:, 0], line_points[:, 1], line_points[:, 2], c='orange')

ax.legend()
# Comment out to save 3D plot
# plt.savefig("image_3D_plot.png")
plt.show()
