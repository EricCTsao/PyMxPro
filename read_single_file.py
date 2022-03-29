import numpy as np
import re
import math
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
    
path_input = "20180815_0001.txt"
path_output = "test.txt"  

def read_single_file(data_dir):
    """
    Read single .txt file of NSRRC U9 and convert it into dataarray.
    """

    #generate the list with each line of the txt file
    ListofData = []

    #open single .txt file
    with open (data_dir, "r") as f:
        for line in f:
            Line_split = line.split('\n')[0]
            ListofData.append(Line_split)

        #extract useful information from the file
        #kinetic_energy size and value
        d1_size = [int(ListofData[7]) for ListofData[7] in re.findall(r'-?\d+\.?\d*', ListofData[7])][-1]
        kinetic_energy = [float(ListofData[8]) for ListofData[8] in re.findall(r'\d*[.]\d*', ListofData[8])]
        
        #angle size and value
        d2_size = [int(ListofData[10]) for ListofData[10] in re.findall(r'-?\d+\.?\d*', ListofData[10])][-1]
        angle = [float(ListofData[11]) for ListofData[11] in re.findall(r'\S\d*[.]\d*', ListofData[11])]
        
        #photon energy
        photon_energy = [int(ListofData[15]) for ListofData[15] in re.findall(r'-?\d+\.?\d*', ListofData[15])][-1]
        
        #convert angle into crystal momentum
        p_momentum = []
        for ang in angle:
            p_momentum_element =  0.5123*math.sqrt(photon_energy)*math.sin(math.radians(ang))
            p_momentum.append(p_momentum_element)
        
        #comment info, theta, phi, and temp
        comments = [float(ListofData[38]) for ListofData[38] in re.findall(r'-?\d+\.?\d*', ListofData[38])]
        theta = comments[0]
        phi = comments[1]
        temp = comments[-1]

        #generate data value
        value_list = []
        data_list = [x for x in ListofData[47:] if x != ""]
        print(data_list)
        for i in data_list:
            i_new = list(map(float, i.split()))
            print(i_new)
            del i_new[0]
            value_list.append(i_new) 
        #create dict including useful information
        Data_Info = {"name": path_input, "size of kinetic energy": d1_size, "size of angle": d2_size, "theta": theta,
        "phi": phi, "temperature": temp}

        #create dataarray
        da = xr.DataArray(
            name = Data_Info["name"],
            data = value_list, 
            dims = ["kinetic_energy", "p_momentum"], 
            coords = {"p_momentum": p_momentum, "kinetic_energy": kinetic_energy},
            attrs = Data_Info
        )
    return da

a = read_single_file(path_input)
print (type(a))
a.plot()
plt.show()
