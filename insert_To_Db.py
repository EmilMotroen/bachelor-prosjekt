
"""
Send data to Influx in sets of X,Y,Z values and add offset to values with json
"""
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import json
from configparser import ConfigParser


# Information from 'config.ini', change file before running
config_object = ConfigParser()
config_object.read("config.ini")
login = config_object["INFLUXDB"]
url = login["url"]
bucket = login["bucket"]
token = login["token"]
org = login["org"]


# Setting up connection to Influx instance
with InfluxDBClient(url=url, token=token, org=org, timeout=30_000) as client:
    
    # Create API object to write
    write_api = client.write_api(write_options=SYNCHRONOUS) 
    AlpideID = 0x10
    seq = 1
    
    # Open json file with offset values
    f = open("offset.json")
      
    # Returns JSON object as a dictionary
    jsondata = json.load(f)
    
    # Amount of X,Y,Z sets to be sent
    number_of_points = int(input("How many sets of (X,Y,Z) values? "))
    
    # Empty list for data to be appended to
    data = []
    

    for i in range(number_of_points):
        
        # Setting XYZ values before the offset
        xGlobal = int(input(f"Set {i+1}: X: "))
        yGlobal = int(input(f"Set {i+1}: Y: "))
#         zGlobal = float(input(f"Set {i+1}: Z: "))
        
        # Setting Z to 0, ALPIDEs sends X,Y values and ALPIDE ID
        zGlobal = int(0)
        
        
        # Adding offset from JSON
        xGlobal += int(jsondata["offset"][0]["layer"][i]["X"])
        yGlobal += int(jsondata["offset"][0]["layer"][i]["Y"])
        zGlobal += int(jsondata["offset"][0]["layer"][i]["Z"])

        print(f"Set {i+1} after offset: X: ", xGlobal)
        print(f"Set {i+1} after offset: Y: ", yGlobal)
        print(f"Set {i+1} after offset: Z: ", zGlobal)
        

        # Creating data point for measurment Horten, tags data with corresponding values from ALPIDE and sequence
        point = Point("Horten") \
                .tag(f"chipID={AlpideID}", f"seq={seq}") \
                .field("X", xGlobal) \
                .field("Y", yGlobal) \
                .field("Z", zGlobal) \
                .time(datetime.utcnow(), WritePrecision.NS)

        # Points appended to the empty list
        data.append(point)

    # Writes the points in the data list assosiated with bucket and org
    write_api.write(bucket, org, data)
    # Flush() forces all pending writes from the buffer to be sent
    write_api.flush()

client.close()
