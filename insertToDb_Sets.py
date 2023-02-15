from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# You can generate an API token from the "API Tokens Tab" in the UI
token = "ATwnh3qV6l95VXlCNJcnjQbpMiyyY3kpwn7JlluvhFLy4e_cPeB2HuqaEXJNxFXfldqcwKjcAVNh5zYGRFFFAA=="
org = "usn"
bucket = "AlpideData"

with InfluxDBClient(url="http://127.0.0.1:8086", token=token, org=org, timeout=30_000) as client:
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
