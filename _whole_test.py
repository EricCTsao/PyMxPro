import numpy as np
import re
import matplotlib.pyplot as plt

#purpose: read the file and generate the figure (from NSRRC U9 ARPES beamline) 

#data pathway
path_input = "20180815_0001.txt"
path_output = "test.txt"

#generate the list with each line of the txt file
ListofData = []

def extract_data(path):
     with open (path, "r") as f:
          for line in f:
              Line_split = line.split('\n')[0]
              ListofData.append(Line_split)
          return ListofData

#modify the list since there is one space in the file, so remove it (the remaining one is delete in ".split('\n')")
Data_list = extract_data(path_input)
Data_list.pop()

#extract useful information from the file
d1_size = [int(Data_list[7]) for Data_list[7] in re.findall(r'-?\d+\.?\d*', Data_list[7])][-1]
kinetic_energy = [float(Data_list[8]) for Data_list[8] in re.findall(r'\d*[.]\d*', Data_list[8])]

d2_size = [int(Data_list[10]) for Data_list[10] in re.findall(r'-?\d+\.?\d*', Data_list[10])][-1]
angle = [float(Data_list[11]) for Data_list[11] in re.findall(r'\d*[.]\d*', Data_list[11])]

comments = [float(Data_list[38]) for Data_list[38] in re.findall(r'-?\d+\.?\d*', Data_list[38])]
theta = comments[0]
phi = comments[1]
temp = comments[-1]

#generate 2D matrix with 
value_list = []

def generate_value_list():
     for i in Data_list[47:]:
          i_new = list(map(float, i.split()))
          del i_new[0]
          value_list.append(i_new)
     return value_list

real_value_list = generate_value_list()
real_value_list_mx = np.array (real_value_list)

print(real_value_list_mx.shape)

#try to get second derivatives of the matrix
def hessian(x):
    """
    Calculate the hessian matrix with finite differences
    Parameters:
       - x : ndarray
    Returns:
       an array of shape (x.dim, x.ndim) + x.shape
       where the array[i, j, ...] corresponds to the seco nd derivative x_ij
    """
    x_grad = np.gradient(x) 
    hessian = np.empty((x.ndim, x.ndim) + x.shape, dtype=x.dtype) 
    for k, grad_k in enumerate(x_grad):
        # iterate over dimensions
        # apply gradient again to every component of the first derivative.
        tmp_grad = np.gradient(grad_k) 
        for l, grad_kl in enumerate(tmp_grad):
            hessian[k, l, :, :] = grad_kl
    return hessian


second_dev = hessian(real_value_list_mx)[0, 0, :, :, ]
#print(second_dev)
plt.subplot(1, 2, 1)
plt.imshow(real_value_list_mx, plt.cm.gray)
plt.colorbar()
plt.subplot(1, 2, 2)
plt.imshow(second_dev, plt.cm.gray)
plt.colorbar()
plt.show()

#print(value_list)
#print(len(value_list))
#print(Data_list[47].split())
#print(len(Data_list[47].split()))
#print(type(Data_list[47]))




#print(d1_size)
#print(kinetic_energy)
#print(type(kinetic_energy))
#print(len(kinetic_energy))
#print(type(len(kinetic_energy)))
#rint(theta)
#print(phi)
#print(temp)



#generate 2D matrix with coordinates







#d = {}
#with open(path_input, "r") as f:
#    for line in f.readlines():
#       (key, val) = ('kinetic_energy', kinetic_energy)
#       d[(key)] = val
#print(d)