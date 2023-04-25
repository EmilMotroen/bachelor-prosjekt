"""
Reads data from database then saves it to a file where it can get
used by Unity for the tracking sim.
"""
#%% Imports
from influxdb_client import InfluxDBClient
import pandas as pd

token = "9kt0L7AyIAESu9GJo80cj9rZFju-idt-GLpwIRxqDphIPgmHvcy7zTyIstBaKkyZrXUrr2RUa1nlldWNQy-R-g=="
org = "USN"
bucket = "tracking-data"
client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
query_api = client.query_api()

data_frame = query_api.query_data_frame(f'from(bucket:"{bucket}")'
                                        '|> range(start: -10h)'
                                        '|> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")'
                                        '|> keep(columns: ["X", "Z", "Y"])')

pd_data_frame = pd.DataFrame(data_frame)  # Bruke Pandas for å behandle data

pd_data_frame.drop('result', inplace=True, axis=1); 
pd_data_frame.drop('table', inplace=True, axis=1)  # Fjern unødvendige kolonner

with open('C:/Users/emotr/AppData/LocalLow/DefaultCompany/ParticleDetector/dataFile.txt', 'w') as file:
    dfAsString = pd_data_frame.to_string(header=False, index=False)
    file.write(dfAsString)

print('... Done getting data from database')