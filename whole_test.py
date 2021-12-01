import numpy as np
import re

#data pathway
path_input = "20180815_0001_mod.txt"
path_output = "test.txt"

sample_name = []
theta = []
phi = []
temp = []
kinetic_energy = []
angle = []
delay_time = []


#read the file (from NSRRC U9 ARPES beamline) 
with open (path_input, "r") as f:
    for line in f:
        #print(line)
        #if 'Region Name=SnSe'
        if "Dimension 1 size" in line: 
             s = [int(s) for s in re.findall(r'-?\d+\.?\d*', line)]
             d1_size = s[-1]
             #print(d1_size)
        if "Dimension 2 size" in line: 
             s = [int(s) for s in re.findall(r'-?\d+\.?\d*', line)]
             d2_size = s[-1]
             #print(d2_size)
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


with open (path_input, "r") as f:
    for line in f.readlines(2):
        print(line)
             #value = [float(value) for value in re.findall(r'\d*[.]\d*', line)]
             #print(value)

#generate 2D matrix with coordinates







#d = {}
#with open(path_input, "r") as f:
#    for line in f.readlines():
#       (key, val) = ('kinetic_energy', kinetic_energy)
#       d[(key)] = val
#print(d)