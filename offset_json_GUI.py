"""
GUI for sending X,Y,Z offset values to JSON file
    JSON filename: offset.json
"""
import tkinter as tk
import json

# Method gets X,Y,Z offset values
def get_offset():

    # Create the root window
    window = tk.Tk()

    # Configure the root window
    window.title("Offset values to JSON/Influx")


    # Set size of window
#     window.geometry("500x200")


    # Creating rows, columns and labels of X,Y,Z with entries
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


    # Method to get offset values, sends to json file and close window
    def submit_offset():
        
        # Gets values from entries
        x = int(x_entry.get())
        y = int(y_entry.get())
        z = int(z_entry.get())
        

        # Structure of json file
        data = {
            "offset": [
                {
                    "layer": [
                        {"X": x, "Y": y, "Z": z},
                        {"X": x, "Y": y, "Z": z},
                        {"X": x, "Y": y, "Z": z},
                        {"X": x, "Y": y, "Z": z}
                    ]
                }
            ]
        }
        
        # Opens json file and dumps data. Structured with tab width
        with open('offset.json', 'w') as f:
            json.dump(data, f, indent = 4)
        
        # Close window        
        window.destroy()


    # Submit button that calls the submit_values function
    tk.Button(window, text = "Submit", command = submit_offset).grid(row = 3, column = 1)

    # Start the main event loop
    window.mainloop()
    
# Call method to get the offset values
get_offset()


