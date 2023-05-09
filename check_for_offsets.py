"""
Check over the hits passed to the database and see if offsets need to be added.
Works with multiple particles, but they cannot hit at the same time. Once a particle
hits the first alpide, it must finish hitting all the alpides in the stack.
"""

import os
import math
import numpy as np
from configparser import ConfigParser

currentFile = 'dataFile.txt'
if os.stat(currentFile).st_size == 0:
    print(f'ERROR! No data in file: {currentFile}. \nExiting...')
    raise SystemExit

config_object = ConfigParser()
config_object.read("config.ini")
config_layers = config_object["LAYERS"]
NUMBER_OF_LAYERS = int(config_layers["pixel_layers"])
NUMBER_OF_STACKS = int(config_layers["pixel_stacks"])

file = open(currentFile)
layer1 = []  # Sort all hits into lists based on the layer numbers
layer2 = []
layer3 = []
layer4 = []

lines = file.readlines()
# The last number in every line is the ALPIDE-ID or layernumber
for line in lines:
    if int(line.strip()[-1]) == 0:   layer1.append(line.strip())
    elif int(line.strip()[-1]) == 1: layer2.append(line.strip())
    elif int(line.strip()[-1]) == 2: layer3.append(line.strip())
    elif int(line.strip()[-1]) == 3: layer4.append(line.strip())
    else:                            continue

file.close()

"""
Assuming the top two layers have correct hit values, a line can be drawn by finding the angle
between the two layers.
"""

# Split the strings to individiual values
def split_string(data):
    data = data[:-2]  # Remove chip-ID/layernumber
    space_split = data.split(' ')
    points = (int(space_split[0]), int(space_split[1]))
    return points

# Get the points assosiated with the layers using the chip-ID/layernumber
layer1_points = []
layer2_points = []
layer3_points = []
layer4_points = []

for index in range(NUMBER_OF_STACKS):
    layer1_points.append(split_string(layer1[index]))
    layer2_points.append(split_string(layer2[index]))
    layer3_points.append(split_string(layer3[index]))
    layer4_points.append(split_string(layer4[index]))

for index in range(NUMBER_OF_STACKS):
    # Use math.atan() to find the angles
    angle_top_two_sensors = np.rad2deg(math.atan2(layer2_points[index][1] - layer1_points[index][1], 
                                                layer2_points[index][0] - layer1_points[index][0]))

    angle_bottom_two_sensors = np.rad2deg(math.atan2(layer4_points[index][1] - layer3_points[index][1], 
                                                layer4_points[index][0] - layer3_points[index][0]))

    angle_middle_two_sensors = np.rad2deg(math.atan2(layer3_points[index][1] - layer2_points[index][1], 
                                                layer3_points[index][0] - layer2_points[index][0]))

    print(f'Angle top on stack {index}: {angle_top_two_sensors}')
    print(f'Angle middle on stack {index}: {angle_middle_two_sensors}')
    print(f'Angle bottom on stack {index}: {angle_bottom_two_sensors}\n')

# What to do with the angle?
