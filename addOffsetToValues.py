#python program to read json file

import json

xGlobal = 10
yGlobal = 20
zGlobal = 0
  
#open JSON file
f = open('data.json')
  
#returns JSON object as a dictionary
data = json.load(f)

  
#iterate json layers, getting Z value
for i in range(4):


    xGlobal += float(data["offset"][0]["layer"][i]["X"])
    yGlobal += float(data["offset"][0]["layer"][i]["Y"])
    zGlobal += float(data["offset"][0]["layer"][i]["Z"])
    print("X: ", xGlobal, "\tY: ", yGlobal, "\tZ: ", zGlobal)

#closing file
f.close()
