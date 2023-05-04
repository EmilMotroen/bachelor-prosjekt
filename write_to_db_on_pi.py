"""
Write to the database on the Raspberry Pi.
"""

from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from configparser import ConfigParser

# Read influx login from config
config_object = ConfigParser()
config_object.read("config.ini")
login = config_object["INFLUXDB"]
url = login["url"]
bucket = login["bucket"]
token = login["token"]
org = login["org"]


with InfluxDBClient(url=url, token=token, org=org, timeout=30_000) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS) 
    AlpideID = 0x10
    seq = 1
    
    #amount of X,Y,Z set to be sent
    number_of_points = int(input("How many sets of (X,Y,Z) values? "))
    
    data = []
    
    for i in range(number_of_points):
        xGlobal = int(input(f"Set {i+1}: X: "))
        yGlobal = int(input(f"Set {i+1}: Y: "))
        zGlobal = int(input(f"Set {i+1}: Z: "))

        point = Point("Horten") \
                .tag(f"chipID={AlpideID}", f"seq={seq}") \
                .field("X", xGlobal) \
                .field("Y", yGlobal) \
                .field("Z", zGlobal) \
                .time(datetime.utcnow(), WritePrecision.NS)

        data.append(point)

    write_api.write(bucket, org, data)
    write_api.flush()

client.close()
