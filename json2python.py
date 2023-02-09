#python program to read json file

import json
  
#open JSON file
f = open('data.json')
  
#returns JSON object as a dictionary
data = json.load(f)

  
#iterating through the json list
# for i in data['offset']:
#     print(i)
  

#get value Z at offset index 0 and layer index 1 
print(data["offset"][0]["layer"][1]["Z"])


#closing file
f.close()
