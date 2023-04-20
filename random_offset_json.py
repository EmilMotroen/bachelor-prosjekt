import json
import random

#how many sets/layers of X,Y,Z values
num_layers = int(input("How many layers in json? "))

layer = {}

#generating random values for each X,Y,Z value for each layer
for i in range(num_layers):
    for j in range(1, 4):
        position = f"variable_{i + 1}_{j}"
        
        #giving X,Y,Z random values from 1-9
        random_value = random.randint(1, 9)

        #adding the variable to the list
        layer[position] = random_value


#sending to JSON file
def submit_offset():
    
    layers_list = []
    
    for i in range(num_layers):
        x = layer[f"variable_{i + 1}_1"]
        y = layer[f"variable_{i + 1}_2"]
        z = layer[f"variable_{i + 1}_3"]
        
        layers_list.append({"X": x, "Y": y, "Z": z})
        
        #if we dont want X,Y offsets
#         layers_list.append({"X": 0, "Y": 0, "Z": z})


    #structure of json file
    data = {
                "offset": [
                    {
                        "layer": layers_list
                    }
                ]
        }


    #opens json file and dumps data
    with open('data_json_test.json', 'w') as f:
        json.dump(data, f, indent = 4)


#call method
submit_offset()
