"""
GUI for sending X,Y,Z offset values to JSON file
"""
import tkinter as tk
import json


#method gets X,Y,Z offset values
def get_offset():

    #create the root window
    window = tk.Tk()

    #configure the root window
    window.title("Offset values to JSON/Influx")


    #set size of window
#     window.geometry("500x200")


    #creating rows, columns and labels of X,Y,Z with entries
    x_label = tk.Label(window, text = "X offset: ")
    x_label.grid(row = 0, column = 0)

    x_entry = tk.Entry(window)
    x_entry.grid(row = 0, column = 1)


    y_label = tk.Label(window, text = "Y offset: ")
    y_label.grid(row = 1, column = 0)

    y_entry = tk.Entry(window)
    y_entry.grid(row= 1 , column = 1)


    z_label = tk.Label(window, text = "Z offset: ")
    z_label.grid(row = 2, column = 0)

    z_entry = tk.Entry(window)
    z_entry.grid(row = 2, column = 1)



    #method to get offset values, sends to json file and close window
    def submit_offset():
        
        #gets values from entries
        x = int(x_entry.get())
        y = int(y_entry.get())
        z = int(z_entry.get())
        

        #structure of json file
        data = {
            "offset": [
                {
                    "layer": [
                        {"X": x, "Y": y, "Z": z},
                        {"X": x, "Y": y, "Z": z}
                    ]
                }
            ]
        }
        
        #opens json file and dumps data
        with open('data_json_test.json', 'w') as f:
            json.dump(data, f, indent = 4)
        
        #close window        
        window.destroy()


    #submit button that calls the submit_values function
    tk.Button(window, text = "Submit", command = submit_offset).grid(row = 3, column = 1)

    #start the main event loop
    window.mainloop()
    
#call method to get the offset values
get_offset()



