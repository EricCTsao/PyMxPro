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

#d = {}
#with open(path_input, "r") as f:
#    for line in f.readlines():
#       (key, val) = line.split('=')
#       d[int(key)] = val


#read the file (from NSRRC U9 ARPES beamline) 
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


    




    