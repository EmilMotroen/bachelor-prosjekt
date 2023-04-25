"""
Reads file with hits from the Unity tracking sim, then if there's new hits
pass those to a database
"""
#%% Imports
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import numpy as np
import os

#%% Open file and check if there is any data in it
currentFile = 'C:/Users/emotr/AppData/LocalLow/DefaultCompany/ParticleDetector/25.04.2023 00.00.00_hits.txt'

if os.stat(currentFile).st_size == 0:
    print(f'ERROR! No data in file: {currentFile}. \nExiting...')
    raise SystemExit

#%% Database connection
token = "9kt0L7AyIAESu9GJo80cj9rZFju-idt-GLpwIRxqDphIPgmHvcy7zTyIstBaKkyZrXUrr2RUa1nlldWNQy-R-g=="
org = "USN"
bucket = "tracking-data"
client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

#%% Open file and save coordinates
x = []
z = []
y = []

file = open(currentFile)
line = file.readline()[:-1]
while line:
    splitLine = line.split('_')
    x.append(int(splitLine[0]))
    z.append(int(splitLine[1]))
    y.append(int(splitLine[2]))
    line = file.readline()[:-1]
file.close()

#%% Pass coordinates to database
for i in range(len(x)):
    point = Point("Coordinates")\
        .tag("Location", "Horten")\
        .field("X", x[i])\
        .field("Z", z[i])\
        .field("Y", y[i])\
        .time(datetime.utcnow(), WritePrecision.NS)
    try:
        write_api.write(bucket, org, point)  # Skriver til database
    except Exception as e:
        print(f'Exception caught: {e}')

open(currentFile, 'w').close()  # Delete the contents of the file to avoid duplicates on next run
print('... done')