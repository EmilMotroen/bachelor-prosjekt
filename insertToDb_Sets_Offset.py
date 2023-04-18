"""
Send data to Influx in sets of X,Y,Z values and add offset to values with json
"""
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import json


#token is the authentication token for authenticating the client with the server
#org stores the name of the organisasion assosiated with the Influx server
#bucket stores the name of the Influx bucket

token = "ATwnh3qV6l95VXlCNJcnjQbpMiyyY3kpwn7JlluvhFLy4e_cPeB2HuqaEXJNxFXfldqcwKjcAVNh5zYGRFFFAA=="
org = "usn"
bucket = "AlpideData"


#setting up connection to Influx instance
with InfluxDBClient(url="http://127.0.0.1:8086", token=token, org=org, timeout=30_000) as client:
    
    #creating API object to write
    write_api = client.write_api(write_options=SYNCHRONOUS) 
    AlpideID = 0x10
    seq = 1
    
    #opening json file with offset values
    f = open('data.json')
      
    #returns JSON object as a dictionary
    jsondata = json.load(f)
    
    #amount of X,Y,Z sets to be sent
    number_of_points = int(input("How many sets of (X,Y,Z) values? "))
    
    #empty list for data to be appended to
    data = []
    

    for i in range(number_of_points):
        
        #setting XYZ values before the offset
        xGlobal = float(input(f"Set {i+1}: X: "))
        yGlobal = float(input(f"Set {i+1}: Y: "))
#         zGlobal = float(input(f"Set {i+1}: Z: "))
        
        #setting Z to 0, ALPIDEs sends X,Y values and ALPIDE ID
        zGlobal = float(0)
        
        
        #adding offset from json
        xGlobal += float(jsondata["offset"][0]["layer"][i]["X"])
        yGlobal += float(jsondata["offset"][0]["layer"][i]["Y"])
        zGlobal += float(jsondata["offset"][0]["layer"][i]["Z"])

        print(f"Set {i+1} after offset: X: ", xGlobal)
        print(f"Set {i+1} after offset: Y: ", yGlobal)
        print(f"Set {i+1} after offset: Z: ", zGlobal)
        

        #creating data point for measurment Horten, tags data with corresponding values from ALPIDE and sequence
        point = Point("Horten") \
                .tag(f"chipID={AlpideID}", f"seq={seq}") \
                .field("X", xGlobal) \
                .field("Y", yGlobal) \
                .field("Z", zGlobal) \
                .time(datetime.utcnow(), WritePrecision.NS)

        #points appended to the empty list
        data.append(point)

    #writes the points in the data list assosiated with bucket and org
    write_api.write(bucket, org, data)
    #Flush() forces all pending writes from the buffer to be sent
    write_api.flush()

client.close()
