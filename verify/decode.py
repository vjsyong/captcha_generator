import os
import numpy as np
import pandas as pd

current_file = os.path.dirname(os.path.abspath(__file__))
print(current_file)
folder = "labels"

label_dir = os.path.join(current_file, folder)
print(label_dir)

# filename = 

# f = open(os.path.join(label_dir, filename))

for filename in os.listdir(label_dir):
    # f = open(os.path.join(label_dir,filename), "r")
    char_list = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    predicted_string = ""
    # with f as openfile:
    #     for line in openfile:
    #         entry = line.split()
    #         predicted_chars.append(char_list[entry[0]])
    #         print(line)
    data = pd.read_csv(os.path.join(label_dir,filename), sep=" ", header=None, names=["key", "x", "y", "w", "h"])
    data.sort_values(by=["x"], ascending=True, inplace=True)
    for index, row in data.iterrows():
        predicted_string += char_list[int(row["key"])]
    print(filename, predicted_string)
    # print(data)
