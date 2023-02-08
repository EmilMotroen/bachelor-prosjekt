# Python program to read json file

import json
  
#open JSON file
f = open('data.json')
  
#returns JSON object as a dictionary
data = json.load(f)
  
#iterating through the json list
for i in data['coordinates']:
    print(i)
  
#closing file
f.close()