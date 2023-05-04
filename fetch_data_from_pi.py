"""
Fetches the data from the Raspberry Pi database.
"""
from influxdb_client import InfluxDBClient
from configparser import ConfigParser
import pandas as pd

# Read influx login from config
config_object = ConfigParser()
config_object.read("config.ini")
login = config_object["INFLUXDB"]
url = login["url"]
bucket = login["bucket"]
token = login["token"]
org = login["org"]

# Connect to the database
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# Fetch data to a dataframe
try:
    data_frame = query_api.query_data_frame(f'from(bucket:"{bucket}")'
                                            '|> range(start: -30d)'
                                            '|> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")'
                                            '|> keep(columns: ["X", "Y", "Z"])')
except Exception as e:
    print(e)
    #print('Error fetching data... Exiting')
    raise SystemExit

pd_data_frame = pd.DataFrame(data_frame)

# Remove unnecessary columns
pd_data_frame.drop('result', inplace=True, axis=1) 
pd_data_frame.drop('table', inplace=True, axis=1)

# Write the dataframe to a file for further use
with open('dataFile.txt', 'w') as file:
    dfAsString = pd_data_frame.to_string(header=False, index=False)
    file.write(dfAsString)

print('... done getting data from database')