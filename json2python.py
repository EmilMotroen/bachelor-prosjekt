#python program to read json file

import json
  
#open JSON file
f = open('data.json')
  
#returns JSON object as a dictionary
data = json.load(f)

  
# #iterating through the json list
# for i in data['offset']:
#     print(i)
#   

#get value Z from index 0 
print(data["offset"][0]["Z"])

#closing file
f.close()
