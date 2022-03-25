"""
extract read_TD_variables_T
"""

import numpy as np
import re
import matplotlib.pyplot as plt
import os
import glob
import math
import xarray as xr

path_input = "D:\github\PyMxPro\_test_TD"

def read_TD_variables_T(data_dir):
    file_list = glob.glob(os.path.join(data_dir, "*.txt"))
    Result = {}
    for file in file_list:
        file_name = file.split("\\")[-1]
        if file_name != "_Settings.txt":
            ListofData = []
            with open (file, "r") as f:
                for line in f:
                    Line_split = line.split('\n')[0]
                    ListofData.append(Line_split)
            comments = [float(ListofData[38]) for ListofData[38] in re.findall(r'-?\d+\.?\d*', ListofData[38])]
            temp = comments[-1]
            Result[file_name] = temp
    return Result

print(read_TD_variables_T(path_input))




"""
step by step extract the info we need
"""

def data_read(path_input):
    with open (path_input, "r") as f:
         for line in f:
             #print (line)
             #if 'Region Name=SnSe'
             if "Dimension 1 scale" in line:
                 kinetic_energy = [float(kinetic_energy) for kinetic_energy in re.findall(r'\d*[.]\d*', line)]
                 #print (kinetic_energy)
             if "Dimension 2 scale" in line:
                 angle = [float(angle) for angle in re.findall(r'\d*[.]\d*', line)]
                 #print (angle)
             if "Comments=" in line:
                 s = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)]
                 theta = s[0]
                 phi = s[1]
                 temp = s[-1]
                 #print(theta)
                 #print(phi)
                 #print(temp)



#def read_temperature_variable(data_dir):
#    file_list = glob.glob(os.path.join(data_dir, "*.txt"))
#    file_list.remove(path_input + "\\" + "_Settings.txt")
#    temp_list = []
#    for f in file_list:
#
#    for line in txtfile:




"""
try

"""
#def read_temperature_variable(data_dir):
#    file_list = glob.glob(os.path.join(data_dir, "*.txt"))
#    for file in file_list:
#        #generate file_name in the data_dir
#        file_name = file.split("\\")[-1]
#        if file_name != "_Settings.txt":
#            temp_list = []
#            with open(file, "r") as f:
#                for line in f:
#                    if "Comments=" in line:
#                        s = [float(s) for s in re.findall(r'-?\d+\.?\d*', line)]
#                        temp = s[-1]
#        temp_list.append(temp)
#    print(temp_list)
                    


#print(read_temperature_variable(path_input))