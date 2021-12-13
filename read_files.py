import numpy as np
import re
import matplotlib.pyplot as plt
import os
import glob
import math
import xarray as xr
import logging

__all__ = ["read_settings", "batch_read_TD_experiment"]
#__name__ = ["read_settings"]
logger = logging.getLogger(__name__)

#purpose: read the file and generate the figure (from NSRRC U9 ARPES beamline) 

#data pathway
path_input = "D:\github\PyMxPro\_test_TD"

#distinguish the dataset is time-resolved, temperature dependent, or XXXX
def classification(data_dir):
    data_dir_split = data_dir.split("_")
    if "TD" in data_dir_split:
        return batch_read_TD_experiment(data_dir) 
    elif "TR" in data_dir_split:
        print("hihi")
    else:
        print("unknown dataset")


#generate the list with each line of the txt file and get the information we need
def read_settings(data_dir):
    """
    Read setting file.
    Returns: Data_Info dictrionary
             "d1_size", "kinetic energy", "d2_size", "angle", "theta", "phi", "temp"
    """
    #search and read Settings.txt
    file_list = glob.glob(os.path.join(data_dir, "*_Settings.txt"))
    setting_path = file_list[0]
    #if len(file_list) > 1:
        #logger.warning("found multiple setting file, ignored")
    
    #generate the list with each line of the txt file
    ListofData = []
    # parse 
    with open (setting_path, "r") as f:
        for line in f:
            Line_split = line.split('\n')[0]
            ListofData.append(Line_split)
        #print(ListofData)

        #extract useful information from the file
        #kinetic_energy size and value
        d1_size = [int(ListofData[7]) for ListofData[7] in re.findall(r'-?\d+\.?\d*', ListofData[7])][-1]
        kinetic_energy = [float(ListofData[8]) for ListofData[8] in re.findall(r'\d*[.]\d*', ListofData[8])]
        
        #angle size and value
        d2_size = [int(ListofData[10]) for ListofData[10] in re.findall(r'-?\d+\.?\d*', ListofData[10])][-1]
        angle = [float(ListofData[11]) for ListofData[11] in re.findall(r'\S\d*[.]\d*', ListofData[11])]
        photon_energy = [int(ListofData[15]) for ListofData[15] in re.findall(r'-?\d+\.?\d*', ListofData[15])][-1]
        p_momentum = []
        for ang in angle:
            p_momentum_element =  0.5123*math.sqrt(photon_energy)*math.sin(math.radians(ang))
            p_momentum.append(p_momentum_element)
        #comment info, theta, phi, and temp
        comments = [float(ListofData[38]) for ListofData[38] in re.findall(r'-?\d+\.?\d*', ListofData[38])]
        theta = comments[0]
        phi = comments[1]
        temp = comments[-1]
    if __name__ == '__main__':
        #generate dictionary
        Data_Info = {"d1_size": d1_size, "kinetic energy": kinetic_energy, "d2_size": d2_size, "angle": angle, 
        "p_momentum": p_momentum, "theta": theta, "phi": phi, "temperature": temp}
    return Data_Info


def batch_read_TD_experiment(data_dir):
    """
    Batch Read the .txt files in the data_dir and capture the [data1]
    Returns: Result dictrionary
            each file with each 2D matrix
    """
    settings_dict = read_settings(data_dir)
    p_momentum = settings_dict["p_momentum"]
    kinetic_energy =settings_dict["kinetic energy"]
    #search and read experimental *.txt
    file_list = glob.glob(os.path.join(data_dir, "*.txt"))
    
    #create dictionary
    Result = {}
    for file in file_list:
        #generate file_name in the data_dir
        file_name = file.split("\\")[-1]
        
        #for other files, generate ListofData and value_list
        if file_name != "_Settings.txt":
            ListofData = []
            value_list = []
            with open(file, "r") as f:
                #generate ListofData
                for line in f:
                    Line_split = line.split('\n')[0]
                    ListofData.append(Line_split)
                    
                comments = [float(ListofData[38]) for ListofData[38] in re.findall(r'-?\d+\.?\d*', ListofData[38])]
                temp = comments[-1]
                print(temp)
                #extract [data1] information and generate a matrix for each file
                #generate dictionary for each file and [data1]
                for i in ListofData[47:]:
                    #ignore the "" in the list
                    if i != "":
                        i_new = list(map(float, i.split()))
                        del i_new[0]
                        value_list.append(i_new)
                        value_list_mx = np.array(value_list)
            da = xr.DataArray(
                data = value_list_mx, 
                dims = ["kinetic_energy", "p_momentum"], 
                coords = dict(p_momentum = (["p_momentum"], p_momentum), 
                kinetic_energy = (["kinetic_energy"], kinetic_energy),
                temp = temp
                )
            )
                
                #Result.append(value_list)
                #value_list_mx = np.array(Result)            
    
                #print(value_list_mx.shape)
                #da = embed_info_2_xarray(value_list_mx)
                #Result.append = da
            Result[file_name] = da
    return Result

def embed_info_2_xarray(nparray):
    p_momentum = read_settings(path_input)["p_momentum"] #list
    kinetic_energy = read_settings(path_input)["kinetic energy"] #list
    #temperature = read_TD_variables_T(path_input)["temperature"]

    print(len(p_momentum))
    print(len(kinetic_energy))
    da = xr.DataArray(
        data = nparray, 
        dims = ["kinetic_energy", "p_momentum"], 
        coords = dict(p_momentum = (["p_momentum"], p_momentum), 
        kinetic_energy = (["kinetic_energy"], kinetic_energy)
        )
    )
    return da


print(classification(path_input))




#print(batch_read_experiment(path_input))

#a = batch_read_experiment(path_input)["20180815_0001.txt"]
#print(a.dims[0])


