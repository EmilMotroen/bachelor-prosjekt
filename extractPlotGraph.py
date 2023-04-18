"""
Read data from influxdb database using dataframes
"""
import pandas as pd
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import matplotlib.pyplot as plt


#bucket stores the name of the Influx bucket
#org stores the name of the organisasion assosiated with the Influx server
#token is the authentication token for authenticating the client with the server
#url stores the URL for the Influx server to connect to

bucket = "AlpideData"
org = "usn"
token = "ATwnh3qV6l95VXlCNJcnjQbpMiyyY3kpwn7JlluvhFLy4e_cPeB2HuqaEXJNxFXfldqcwKjcAVNh5zYGRFFFAA=="
url = "http://localhost:8086"


#creating client object to connect to Influx server
client = InfluxDBClient(
    url=url,
    token=token,
    org=org
)

#makes it possible to preform queries from Influx
query_api = client.query_api()

#execute Influx query and retrieve result as Pandas DataFrame
#"1h" in line 33 is the time from now to the first data you want
data_frame = query_api.query_data_frame(f'from(bucket:"{bucket}")'
                                        '|> range(start: -1h)'
                                        '|> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")'
                                        '|> keep(columns: ["X", "Y", "Z"])')

#using Pandas to process data with a new DataFrame of the query results
pd_data_frame = pd.DataFrame(data_frame)  

#remove unnecessary columns
pd_data_frame.drop('result', inplace=True, axis=1); pd_data_frame.drop('table', inplace=True, axis=1)  

#writes X instead of x-coord, same with Y and Z
pd_data_frame.columns = ['X', 'Y', 'Z']

#prints the Pandas DataFrame to console, with retrieved data
print(f'\n{pd_data_frame}')


#plotting 3D graph of data from DataFrame using Matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot(pd_data_frame.X, pd_data_frame.Y, pd_data_frame.Z)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.show()



