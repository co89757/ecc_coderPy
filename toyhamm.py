
# Author:Colin 
# Date Nov 18 2013 
# Testing simple Hamming code for C(39,32),C(72,64),C(137,128),C(266,256) 
# UPDATE: Nov 20 2013: Include DED functionality by overall parity bit ;
# use error_status_code to switch to error scenarios detected 
#TODO: larger G/H for wider information word length 


# Notations:
# H: check matrix H = [rxn] = [NameMatrix[rxk]|I] ; 





import numpy
import random
from itertools import izip 
import math 

####### NEW: Hsiao optimum odd-column-weight SECDED name matrices table for 16,32,64. ##################
# NOTE: definiton of name matrix: check matrix H[rxn]=[name_matrix, I] ; name_matrix[rxk]  

HsiaoName16=numpy.array(
[[1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,0],
[1,1,1,0,0,0,1,1,1,1,0,0,1,0,0,0],
[1,0,0,0,1,0,1,1,1,0,0,0,0,1,1,1],
[0,0,0,0,0,1,1,0,0,1,1,1,0,1,1,1],
[0,1,0,1,0,0,0,1,0,1,1,1,1,1,0,0],
[0,0,1,1,1,1,0,0,1,0,0,1,1,0,0,1],
], dtype=int 
)

HsiaoName32=numpy.array(
[[1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,1,1],
[0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0],
[0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,1,1,0,1,1,0],
[0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
[0,1,1,0,0,1,0,1,0,1,0,0,1,0,0,1,0,0,0,0,1,1,1,1,0,1,1,0,1,0,0,0],
[1,0,0,0,0,1,1,0,1,0,0,0,1,1,1,0,1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0],
[1,1,0,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,1],
], dtype=int 
)

HsiaoName64=numpy.array(
[[1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0],
[1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,1,0,0],
[0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1],
[0,0,0,1,0,0,1,1,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0],
[0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0],
[1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,0,0,1,0,0,1,0,0,1],
[0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,0],
[0,0,1,0,0,1,1,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1]
], dtype=int 
)


# ------------------- Hsiao Generator matrices and Check matrices -------------------------

hsiao_G16=numpy.concatenate((numpy.eye(16,dtype=int),HsiaoName16.transpose()), axis = 1) 
hsiao_G32=numpy.concatenate((numpy.eye(32,dtype=int),HsiaoName32.transpose()), axis = 1) 
hsiao_G64=numpy.concatenate((numpy.eye(64,dtype=int),HsiaoName64.transpose()), axis = 1) 

hsiao_H16=numpy.concatenate(( HsiaoName16, numpy.eye(6, dtype=int)), axis = 1) 
hsiao_H32=numpy.concatenate(( HsiaoName32, numpy.eye(7, dtype=int)), axis = 1) 
hsiao_H64=numpy.concatenate(( HsiaoName64, numpy.eye(8, dtype=int)), axis = 1) 



























################### END OF HSIAO SEC-DED name matrix table for 16,32,64 ##########################







# import sys

#parity matrix is in G=[I,P] so H=[P',I] 
p16 = numpy.array(
[[1,0,1,0,0],
[0,1,0,1,0],
[0,0,1,0,1],
[1,0,1,1,0],
[0,1,0,1,1],
[1,0,0,0,1],
[1,1,1,0,0],
[0,1,1,1,0],
[0,0,1,1,1],
[1,0,1,1,1],
[1,1,1,1,1],
[1,1,0,1,1],
[1,1,0,0,1],
[1,1,0,0,0],
[0,1,1,0,0],
[0,0,1,1,0]], dtype=int 
)   # rxk 



p32 = numpy.array(
[[1,1,0,0,0,0],
[0,1,1,0,0,0],
[0,0,1,1,0,0],
[0,0,0,1,1,0],
[0,0,0,0,1,1],
[1,1,0,0,0,1],
[1,0,1,0,0,0],
[0,1,0,1,0,0],
[0,0,1,0,1,0],
[0,0,0,1,0,1],
[1,1,0,0,1,0],
[0,1,1,0,0,1],
[1,1,1,1,0,0],
[0,1,1,1,1,0],
[0,0,1,1,1,1],
[1,1,0,1,1,1],
[1,0,1,0,1,1],
[1,0,0,1,0,1],
[1,0,0,0,1,0],
[0,1,0,0,0,1],
[1,1,1,0,0,0],
[0,1,1,1,0,0],
[0,0,1,1,1,0],
[0,0,0,1,1,1],
[1,1,0,0,1,1],
[1,0,1,0,0,1],
[1,0,0,1,0,0],
[0,1,0,0,1,0],
[0,0,1,0,0,1],
[1,1,0,1,0,0],
[0,1,1,0,1,0],
[0,0,1,1,0,1]] , dtype=int) # Parity submatrix 32X6 for word size 32

p64=numpy.array(
[[1,0,0,1,0,0,0],
[0,1,0,0,1,0,0],
[0,0,1,0,0,1,0],
[0,0,0,1,0,0,1],
[1,0,0,1,1,0,0],
[0,1,0,0,1,1,0],
[0,0,1,0,0,1,1],
[1,0,0,0,0,0,1],
[1,1,0,1,0,0,0],
[0,1,1,0,1,0,0],
[0,0,1,1,0,1,0],
[0,0,0,1,1,0,1],
[1,0,0,1,1,1,0],
[0,1,0,0,1,1,1],
[1,0,1,1,0,1,1],
[1,1,0,0,1,0,1],
[1,1,1,1,0,1,0],
[0,1,1,1,1,0,1],
[1,0,1,0,1,1,0],
[0,1,0,1,0,1,1],
[1,0,1,1,1,0,1],
[1,1,0,0,1,1,0],
[0,1,1,0,0,1,1],
[1,0,1,0,0,0,1],
[1,1,0,0,0,0,0],
[0,1,1,0,0,0,0],
[0,0,1,1,0,0,0],
[0,0,0,1,1,0,0],
[0,0,0,0,1,1,0],
[0,0,0,0,0,1,1],
[1,0,0,1,0,0,1],
[1,1,0,1,1,0,0],
[0,1,1,0,1,1,0],
[0,0,1,1,0,1,1],
[1,0,0,0,1,0,1],
[1,1,0,1,0,1,0],
[0,1,1,0,1,0,1],
[1,0,1,0,0,1,0],
[0,1,0,1,0,0,1],
[1,0,1,1,1,0,0],
[0,1,0,1,1,1,0],
[0,0,1,0,1,1,1],
[1,0,0,0,0,1,1],
[1,1,0,1,0,0,1],
[1,1,1,1,1,0,0],
[0,1,1,1,1,1,0],
[0,0,1,1,1,1,1],
[1,0,0,0,1,1,1],
[1,1,0,1,0,1,1],
[1,1,1,1,1,0,1],
[1,1,1,0,1,1,0],
[0,1,1,1,0,1,1],
[1,0,1,0,1,0,1],
[1,1,0,0,0,1,0],
[0,1,1,0,0,0,1],
[1,0,1,0,0,0,0],
[0,1,0,1,0,0,0],
[0,0,1,0,1,0,0],
[0,0,0,1,0,1,0],
[0,0,0,0,1,0,1],
[1,0,0,1,0,1,0],
[0,1,0,0,1,0,1],
[1,0,1,1,0,1,0],
[0,1,0,1,1,0,1]], dtype = int ) 


p128 = numpy.array(
[[1,0,1,1,1,0,0,0],
[0,1,0,1,1,1,0,0],
[0,0,1,0,1,1,1,0],
[0,0,0,1,0,1,1,1],
[1,0,1,1,0,0,1,1],
[1,1,1,0,0,0,0,1],
[1,1,0,0,1,0,0,0],
[0,1,1,0,0,1,0,0],
[0,0,1,1,0,0,1,0],
[0,0,0,1,1,0,0,1],
[1,0,1,1,0,1,0,0],
[0,1,0,1,1,0,1,0],
[0,0,1,0,1,1,0,1],
[1,0,1,0,1,1,1,0],
[0,1,0,1,0,1,1,1],
[1,0,0,1,0,0,1,1],
[1,1,1,1,0,0,0,1],
[1,1,0,0,0,0,0,0],
[0,1,1,0,0,0,0,0],
[0,0,1,1,0,0,0,0],
[0,0,0,1,1,0,0,0],
[0,0,0,0,1,1,0,0],
[0,0,0,0,0,1,1,0],
[0,0,0,0,0,0,1,1],
[1,0,1,1,1,0,0,1],
[1,1,1,0,0,1,0,0],
[0,1,1,1,0,0,1,0],
[0,0,1,1,1,0,0,1],
[1,0,1,0,0,1,0,0],
[0,1,0,1,0,0,1,0],
[0,0,1,0,1,0,0,1],
[1,0,1,0,1,1,0,0],
[0,1,0,1,0,1,1,0],
[0,0,1,0,1,0,1,1],
[1,0,1,0,1,1,0,1],
[1,1,1,0,1,1,1,0],
[0,1,1,1,0,1,1,1],
[1,0,0,0,0,0,1,1],
[1,1,1,1,1,0,0,1],
[1,1,0,0,0,1,0,0],
[0,1,1,0,0,0,1,0],
[0,0,1,1,0,0,0,1],
[1,0,1,0,0,0,0,0],
[0,1,0,1,0,0,0,0],
[0,0,1,0,1,0,0,0],
[0,0,0,1,0,1,0,0],
[0,0,0,0,1,0,1,0],
[0,0,0,0,0,1,0,1],
[1,0,1,1,1,0,1,0],
[0,1,0,1,1,1,0,1],
[1,0,0,1,0,1,1,0],
[0,1,0,0,1,0,1,1],
[1,0,0,1,1,1,0,1],
[1,1,1,1,0,1,1,0],
[0,1,1,1,1,0,1,1],
[1,0,0,0,0,1,0,1],
[1,1,1,1,1,0,1,0],
[0,1,1,1,1,1,0,1],
[1,0,0,0,0,1,1,0],
[0,1,0,0,0,0,1,1],
[1,0,0,1,1,0,0,1],
[1,1,1,1,0,1,0,0],
[0,1,1,1,1,0,1,0],
[0,0,1,1,1,1,0,1],
[1,0,1,0,0,1,1,0],
[0,1,0,1,0,0,1,1],
[1,0,0,1,0,0,0,1],
[1,1,1,1,0,0,0,0],
[0,1,1,1,1,0,0,0],
[0,0,1,1,1,1,0,0],
[0,0,0,1,1,1,1,0],
[0,0,0,0,1,1,1,1],
[1,0,1,1,1,1,1,1],
[1,1,1,0,0,1,1,1],
[1,1,0,0,1,0,1,1],
[1,1,0,1,1,1,0,1],
[1,1,0,1,0,1,1,0],
[0,1,1,0,1,0,1,1],
[1,0,0,0,1,1,0,1],
[1,1,1,1,1,1,1,0],
[0,1,1,1,1,1,1,1],
[1,0,0,0,0,1,1,1],
[1,1,1,1,1,0,1,1],
[1,1,0,0,0,1,0,1],
[1,1,0,1,1,0,1,0],
[0,1,1,0,1,1,0,1],
[1,0,0,0,1,1,1,0],
[0,1,0,0,0,1,1,1],
[1,0,0,1,1,0,1,1],
[1,1,1,1,0,1,0,1],
[1,1,0,0,0,0,1,0],
[0,1,1,0,0,0,0,1],
[1,0,0,0,1,0,0,0],
[0,1,0,0,0,1,0,0],
[0,0,1,0,0,0,1,0],
[0,0,0,1,0,0,0,1],
[1,0,1,1,0,0,0,0],
[0,1,0,1,1,0,0,0],
[0,0,1,0,1,1,0,0],
[0,0,0,1,0,1,1,0],
[0,0,0,0,1,0,1,1],
[1,0,1,1,1,1,0,1],
[1,1,1,0,0,1,1,0],
[0,1,1,1,0,0,1,1],
[1,0,0,0,0,0,0,1],
[1,1,1,1,1,0,0,0],
[0,1,1,1,1,1,0,0],
[0,0,1,1,1,1,1,0],
[0,0,0,1,1,1,1,1],
[1,0,1,1,0,1,1,1],
[1,1,1,0,0,0,1,1],
[1,1,0,0,1,0,0,1],
[1,1,0,1,1,1,0,0],
[0,1,1,0,1,1,1,0],
[0,0,1,1,0,1,1,1],
[1,0,1,0,0,0,1,1],
[1,1,1,0,1,0,0,1],
[1,1,0,0,1,1,0,0],
[0,1,1,0,0,1,1,0],
[0,0,1,1,0,0,1,1],
[1,0,1,0,0,0,0,1],
[1,1,1,0,1,0,0,0],
[0,1,1,1,0,1,0,0],
[0,0,1,1,1,0,1,0],
[0,0,0,1,1,1,0,1],
[1,0,1,1,0,1,1,0],
[0,1,0,1,1,0,1,1],
[1,0,0,1,0,1,0,1]], dtype = int ) 

p256 = numpy.array(
[[1,0,0,0,1,0,0,0,0],
[0,1,0,0,0,1,0,0,0],
[0,0,1,0,0,0,1,0,0],
[0,0,0,1,0,0,0,1,0],
[0,0,0,0,1,0,0,0,1],
[1,0,0,0,1,1,0,0,0],
[0,1,0,0,0,1,1,0,0],
[0,0,1,0,0,0,1,1,0],
[0,0,0,1,0,0,0,1,1],
[1,0,0,0,0,0,0,0,1],
[1,1,0,0,1,0,0,0,0],
[0,1,1,0,0,1,0,0,0],
[0,0,1,1,0,0,1,0,0],
[0,0,0,1,1,0,0,1,0],
[0,0,0,0,1,1,0,0,1],
[1,0,0,0,1,1,1,0,0],
[0,1,0,0,0,1,1,1,0],
[0,0,1,0,0,0,1,1,1],
[1,0,0,1,1,0,0,1,1],
[1,1,0,0,0,1,0,0,1],
[1,1,1,0,1,0,1,0,0],
[0,1,1,1,0,1,0,1,0],
[0,0,1,1,1,0,1,0,1],
[1,0,0,1,0,1,0,1,0],
[0,1,0,0,1,0,1,0,1],
[1,0,1,0,1,1,0,1,0],
[0,1,0,1,0,1,1,0,1],
[1,0,1,0,0,0,1,1,0],
[0,1,0,1,0,0,0,1,1],
[1,0,1,0,0,0,0,0,1],
[1,1,0,1,1,0,0,0,0],
[0,1,1,0,1,1,0,0,0],
[0,0,1,1,0,1,1,0,0],
[0,0,0,1,1,0,1,1,0],
[0,0,0,0,1,1,0,1,1],
[1,0,0,0,1,1,1,0,1],
[1,1,0,0,1,1,1,1,0],
[0,1,1,0,0,1,1,1,1],
[1,0,1,1,1,0,1,1,1],
[1,1,0,1,0,1,0,1,1],
[1,1,1,0,0,0,1,0,1],
[1,1,1,1,1,0,0,1,0],
[0,1,1,1,1,1,0,0,1],
[1,0,1,1,0,1,1,0,0],
[0,1,0,1,1,0,1,1,0],
[0,0,1,0,1,1,0,1,1],
[1,0,0,1,1,1,1,0,1],
[1,1,0,0,0,1,1,1,0],
[0,1,1,0,0,0,1,1,1],
[1,0,1,1,1,0,0,1,1],
[1,1,0,1,0,1,0,0,1],
[1,1,1,0,0,0,1,0,0],
[0,1,1,1,0,0,0,1,0],
[0,0,1,1,1,0,0,0,1],
[1,0,0,1,0,1,0,0,0],
[0,1,0,0,1,0,1,0,0],
[0,0,1,0,0,1,0,1,0],
[0,0,0,1,0,0,1,0,1],
[1,0,0,0,0,0,0,1,0],
[0,1,0,0,0,0,0,0,1],
[1,0,1,0,1,0,0,0,0],
[0,1,0,1,0,1,0,0,0],
[0,0,1,0,1,0,1,0,0],
[0,0,0,1,0,1,0,1,0],
[0,0,0,0,1,0,1,0,1],
[1,0,0,0,1,1,0,1,0],
[0,1,0,0,0,1,1,0,1],
[1,0,1,0,1,0,1,1,0],
[0,1,0,1,0,1,0,1,1],
[1,0,1,0,0,0,1,0,1],
[1,1,0,1,1,0,0,1,0],
[0,1,1,0,1,1,0,0,1],
[1,0,1,1,1,1,1,0,0],
[0,1,0,1,1,1,1,1,0],
[0,0,1,0,1,1,1,1,1],
[1,0,0,1,1,1,1,1,1],
[1,1,0,0,0,1,1,1,1],
[1,1,1,0,1,0,1,1,1],
[1,1,1,1,1,1,0,1,1],
[1,1,1,1,0,1,1,0,1],
[1,1,1,1,0,0,1,1,0],
[0,1,1,1,1,0,0,1,1],
[1,0,1,1,0,1,0,0,1],
[1,1,0,1,0,0,1,0,0],
[0,1,1,0,1,0,0,1,0],
[0,0,1,1,0,1,0,0,1],
[1,0,0,1,0,0,1,0,0],
[0,1,0,0,1,0,0,1,0],
[0,0,1,0,0,1,0,0,1],
[1,0,0,1,1,0,1,0,0],
[0,1,0,0,1,1,0,1,0],
[0,0,1,0,0,1,1,0,1],
[1,0,0,1,1,0,1,1,0],
[0,1,0,0,1,1,0,1,1],
[1,0,1,0,1,1,1,0,1],
[1,1,0,1,1,1,1,1,0],
[0,1,1,0,1,1,1,1,1],
[1,0,1,1,1,1,1,1,1],
[1,1,0,1,0,1,1,1,1],
[1,1,1,0,0,0,1,1,1],
[1,1,1,1,1,0,0,1,1],
[1,1,1,1,0,1,0,0,1],
[1,1,1,1,0,0,1,0,0],
[0,1,1,1,1,0,0,1,0],
[0,0,1,1,1,1,0,0,1],
[1,0,0,1,0,1,1,0,0],
[0,1,0,0,1,0,1,1,0],
[0,0,1,0,0,1,0,1,1],
[1,0,0,1,1,0,1,0,1],
[1,1,0,0,0,1,0,1,0],
[0,1,1,0,0,0,1,0,1],
[1,0,1,1,1,0,0,1,0],
[0,1,0,1,1,1,0,0,1],
[1,0,1,0,0,1,1,0,0],
[0,1,0,1,0,0,1,1,0],
[0,0,1,0,1,0,0,1,1],
[1,0,0,1,1,1,0,0,1],
[1,1,0,0,0,1,1,0,0],
[0,1,1,0,0,0,1,1,0],
[0,0,1,1,0,0,0,1,1],
[1,0,0,1,0,0,0,0,1],
[1,1,0,0,0,0,0,0,0],
[0,1,1,0,0,0,0,0,0],
[0,0,1,1,0,0,0,0,0],
[0,0,0,1,1,0,0,0,0],
[0,0,0,0,1,1,0,0,0],
[0,0,0,0,0,1,1,0,0],
[0,0,0,0,0,0,1,1,0],
[0,0,0,0,0,0,0,1,1],
[1,0,0,0,1,0,0,0,1],
[1,1,0,0,1,1,0,0,0],
[0,1,1,0,0,1,1,0,0],
[0,0,1,1,0,0,1,1,0],
[0,0,0,1,1,0,0,1,1],
[1,0,0,0,0,1,0,0,1],
[1,1,0,0,1,0,1,0,0],
[0,1,1,0,0,1,0,1,0],
[0,0,1,1,0,0,1,0,1],
[1,0,0,1,0,0,0,1,0],
[0,1,0,0,1,0,0,0,1],
[1,0,1,0,1,1,0,0,0],
[0,1,0,1,0,1,1,0,0],
[0,0,1,0,1,0,1,1,0],
[0,0,0,1,0,1,0,1,1],
[1,0,0,0,0,0,1,0,1],
[1,1,0,0,1,0,0,1,0],
[0,1,1,0,0,1,0,0,1],
[1,0,1,1,1,0,1,0,0],
[0,1,0,1,1,1,0,1,0],
[0,0,1,0,1,1,1,0,1],
[1,0,0,1,1,1,1,1,0],
[0,1,0,0,1,1,1,1,1],
[1,0,1,0,1,1,1,1,1],
[1,1,0,1,1,1,1,1,1],
[1,1,1,0,0,1,1,1,1],
[1,1,1,1,1,0,1,1,1],
[1,1,1,1,0,1,0,1,1],
[1,1,1,1,0,0,1,0,1],
[1,1,1,1,0,0,0,1,0],
[0,1,1,1,1,0,0,0,1],
[1,0,1,1,0,1,0,0,0],
[0,1,0,1,1,0,1,0,0],
[0,0,1,0,1,1,0,1,0],
[0,0,0,1,0,1,1,0,1],
[1,0,0,0,0,0,1,1,0],
[0,1,0,0,0,0,0,1,1],
[1,0,1,0,1,0,0,0,1],
[1,1,0,1,1,1,0,0,0],
[0,1,1,0,1,1,1,0,0],
[0,0,1,1,0,1,1,1,0],
[0,0,0,1,1,0,1,1,1],
[1,0,0,0,0,1,0,1,1],
[1,1,0,0,1,0,1,0,1],
[1,1,1,0,1,1,0,1,0],
[0,1,1,1,0,1,1,0,1],
[1,0,1,1,0,0,1,1,0],
[0,1,0,1,1,0,0,1,1],
[1,0,1,0,0,1,0,0,1],
[1,1,0,1,1,0,1,0,0],
[0,1,1,0,1,1,0,1,0],
[0,0,1,1,0,1,1,0,1],
[1,0,0,1,0,0,1,1,0],
[0,1,0,0,1,0,0,1,1],
[1,0,1,0,1,1,0,0,1],
[1,1,0,1,1,1,1,0,0],
[0,1,1,0,1,1,1,1,0],
[0,0,1,1,0,1,1,1,1],
[1,0,0,1,0,0,1,1,1],
[1,1,0,0,0,0,0,1,1],
[1,1,1,0,1,0,0,0,1],
[1,1,1,1,1,1,0,0,0],
[0,1,1,1,1,1,1,0,0],
[0,0,1,1,1,1,1,1,0],
[0,0,0,1,1,1,1,1,1],
[1,0,0,0,0,1,1,1,1],
[1,1,0,0,1,0,1,1,1],
[1,1,1,0,1,1,0,1,1],
[1,1,1,1,1,1,1,0,1],
[1,1,1,1,0,1,1,1,0],
[0,1,1,1,1,0,1,1,1],
[1,0,1,1,0,1,0,1,1],
[1,1,0,1,0,0,1,0,1],
[1,1,1,0,0,0,0,1,0],
[0,1,1,1,0,0,0,0,1],
[1,0,1,1,0,0,0,0,0],
[0,1,0,1,1,0,0,0,0],
[0,0,1,0,1,1,0,0,0],
[0,0,0,1,0,1,1,0,0],
[0,0,0,0,1,0,1,1,0],
[0,0,0,0,0,1,0,1,1],
[1,0,0,0,1,0,1,0,1],
[1,1,0,0,1,1,0,1,0],
[0,1,1,0,0,1,1,0,1],
[1,0,1,1,1,0,1,1,0],
[0,1,0,1,1,1,0,1,1],
[1,0,1,0,0,1,1,0,1],
[1,1,0,1,1,0,1,1,0],
[0,1,1,0,1,1,0,1,1],
[1,0,1,1,1,1,1,0,1],
[1,1,0,1,0,1,1,1,0],
[0,1,1,0,1,0,1,1,1],
[1,0,1,1,1,1,0,1,1],
[1,1,0,1,0,1,1,0,1],
[1,1,1,0,0,0,1,1,0],
[0,1,1,1,0,0,0,1,1],
[1,0,1,1,0,0,0,0,1],
[1,1,0,1,0,0,0,0,0],
[0,1,1,0,1,0,0,0,0],
[0,0,1,1,0,1,0,0,0],
[0,0,0,1,1,0,1,0,0],
[0,0,0,0,1,1,0,1,0],
[0,0,0,0,0,1,1,0,1],
[1,0,0,0,1,0,1,1,0],
[0,1,0,0,0,1,0,1,1],
[1,0,1,0,1,0,1,0,1],
[1,1,0,1,1,1,0,1,0],
[0,1,1,0,1,1,1,0,1],
[1,0,1,1,1,1,1,1,0],
[0,1,0,1,1,1,1,1,1],
[1,0,1,0,0,1,1,1,1],
[1,1,0,1,1,0,1,1,1],
[1,1,1,0,0,1,0,1,1],
[1,1,1,1,1,0,1,0,1],
[1,1,1,1,0,1,0,1,0],
[0,1,1,1,1,0,1,0,1],
[1,0,1,1,0,1,0,1,0],
[0,1,0,1,1,0,1,0,1],
[1,0,1,0,0,1,0,1,0],
[0,1,0,1,0,0,1,0,1],
[1,0,1,0,0,0,0,1,0],
[0,1,0,1,0,0,0,0,1],
[1,0,1,0,0,0,0,0,0],
[0,1,0,1,0,0,0,0,0],
[0,0,1,0,1,0,0,0,0],
[0,0,0,1,0,1,0,0,0],
[0,0,0,0,1,0,1,0,0]], dtype = int) #P256 = 256X9 parity submatrix 

g16 = numpy.concatenate((numpy.eye(16,dtype=int),p16), axis = 1)  

h16 = numpy.concatenate((numpy.transpose(p16), numpy.eye(5, dtype=int)), axis = 1) 

g32 = numpy.concatenate((numpy.eye(32,dtype=int),p32), axis = 1)  

h32 = numpy.concatenate((numpy.transpose(p32), numpy.eye(6, dtype=int)), axis = 1) 

g64 = numpy.concatenate((numpy.eye(64,dtype=int),p64), axis = 1) 
h64 = numpy.concatenate((numpy.transpose(p64), numpy.eye(7, dtype=int)), axis = 1)  

g128 = numpy.concatenate((numpy.eye(128,dtype=int),p128), axis = 1) 
h128 = numpy.concatenate((numpy.transpose(p128), numpy.eye(8, dtype=int)), axis = 1) 

g256 = numpy.concatenate((numpy.eye(256,dtype=int), p256), axis = 1) 
h256 = numpy.concatenate((numpy.transpose(p256), numpy.eye(9, dtype=int)), axis = 1)   
#generator matrix and parity matrix lookup table 
gentable = {16:g16,32:g32, 64:g64, 128:g128, 256:g256} 
partable = {16:h16, 32:h32, 64:h64, 128:h128, 256:h256} 
 
def createMessage(length):
    """
    randomly create original information bits 
    input: information length 
    output: a numpy array vector 

     """
    msg = []
    for i in range(length):
        letter = random.choice([0,1])
        msg.append(letter)
    return numpy.array(msg, dtype = int)
 
def encode(msg, g): 
    "encoder by Generator matrix g.  m * G = c , works on SEC part ; Return a numpy array "
    enc = numpy.dot(msg, g)%2
    return enc
 
def syndrome(received, h):
    "syndrome calculation syn = r x H' or H x r' = syn' ,take np array,   return a numpy array"
    synd = numpy.dot(h, received)%2
    return synd
 
def noise(vin, ber, n_err):
    "ber is error rate, bit is total #corrupted bits,m is the input vector; insert noise in the message; out: a numpy array"
    noisy_msg = numpy.copy(vin)
    cont = 0
    for i in range(len(noisy_msg)):
        e = random.random() # return a random number in [0,1)
        if e < ber:
            if noisy_msg[i] == 0:
                noisy_msg[i] = 1
                cont +=1
            else:
                noisy_msg[i] = 0
                cont +=1
            if cont == n_err:  # bit is  #corrupted bits
                break
    return noisy_msg #return noise mask 
 
def findError(synd, H_matrix):
    # need to altered by Colin , return the location index of error, works on the SEC part  
    "error locator function. return the position of error"
    if all(synd==0):
        return -1 # no error , clean syndrome returns -1 
    block_length = int(H_matrix.shape[1]) # H is a rxn matrix, so n is the code length 
    e = numpy.zeros(block_length,int) 
    for i in xrange(0,block_length):
        e1      = numpy.copy(e)  #copy original zeros vector
        e1[i]   = 1
        compare = numpy.dot(e1,H_matrix.transpose())
        if numpy.array_equal(compare,synd):
            return i # locator index 
        else:
            continue 
    else:
        return 1000 # beyond correction capability   BUGGY !!! TO DEBUG      
 
def correct(noisy, i):
    "flip bits at n-th position. return : a numpy.array "
    # copy the received vector first 
    recv    = numpy.copy(noisy)
    recv[i] = int(not(recv[i]))  # flip the bit at location i
   
    return recv


##### SECDED for detection only NEW ON FEB 13 

def hsiaoDet(k,code):
    "SECDED HSIAO for error detection only based on syndrome. compare to CRC"
    hsiao_Htable={16:hsiao_H16, 32:hsiao_H32, 64:hsiao_H64}  

    h = hsiao_Htable[k] 

    synd = syndrome(code, h) 

    errdet = any(synd) 

    return errdet 





#### verify the Hsiao Decoder Robustness by exhausting SEC patterns 

def verifyHsiaoDec(k):

    assert k in (16,32,64)
    r = int(math.ceil(math.log(k, 2)) ) + 2 ; 
    n = k+r 
    Hmap = {16:hsiao_H16, 32:hsiao_H32, 64:hsiao_H64} 
    H = Hmap[k] 

    for i in xrange(k):  ## error in databits 
        e1 = np.zeros(n,dtype=int) 
        e1[i]=1 











def HsiaoSECDED(info_length, erate, maxerr, ITEARTION=5): #PENDING
     
    assert info_length in (16,32,64) 
    hsiao_Gtable={16:hsiao_G16, 32:hsiao_G32, 64:hsiao_G64} 
    hsiao_Htable={16:hsiao_H16, 32:hsiao_H32, 64:hsiao_H64} 
    g = hsiao_Gtable[info_length] 
    h = hsiao_Htable[info_length] 
    
    corr_cnt  = 0
    noerr_cnt = 0
    miss_cnt  = 0
    beyond    = 0
    tohex= lambda array: hex(int(''.join(map(str,array)),2)) 
    for i in range(ITEARTION): # n incoming received message repetitions 
        msg = createMessage(info_length) # generate a random information vector u(x)
        enc = encode(msg, g) 

        # ------- check parity right after encoder : parity before corruption ----------
          
        print "original message hex: ", tohex(msg)   
        print "encoded msg SECDED hex: ", tohex(enc) 

        # ------introduce corruption --------------
        noisy    = noise(enc, erate, maxerr)

        
      
        print 'received mesage: ', noisy
        print 'received code HEX: ', tohex(noisy)
        ep = [x^y for x,y in izip(noisy.tolist(),enc.tolist())] 
        print 'error pattern: ',  ep 
        print 'number of errors: ', sum(ep) 

        # -----compute syndrome , set the SEC flag ------------------------------
        syndromes = syndrome(noisy, h)
        print 'syndrome vector: ', syndromes # DEBUG 
         # -------- error pattern / error location returned if only 1 error bit, if clean, error_index = -1 ----
        error_index = findError(syndromes, h) 

        SEC_flag = int(error_index >= 0)  # SEC_flag 1 denotes error alert in SEC part if index = 1000, then beyond t=1 

        if SEC_flag ==0:
            print 'clean! no err ' 
            noerr_cnt += 1 

        elif SEC_flag and error_index != 1000:
            corrected_vector = correct(noisy, error_index)
            print 'corrected vector : ', corrected_vector
            if numpy.array_equal(corrected_vector, enc):
                print 'correction success!!!' 
                corr_cnt += 1 
            else:
                print 'mis-correction..'
                miss_cnt += 1 

        else:
            print '2 or more err detected!'
            beyond += 1  

        # print '---------------NEXT----------------'

    print "corr_cnt = ", corr_cnt
    print "noerr_cnt = ", noerr_cnt
    print "miss_cnt = ", miss_cnt 
    print "2+ error cnt = ",beyond
    print "total cnt = ", corr_cnt+noerr_cnt+miss_cnt+beyond

            
        
   

    





























def eHamming(info_length, erate, maxerr, ITEARTION=5):
    # g =  numpy.array([[1, 0, 0, 0, 0, 1, 1],[0, 1, 0, 0, 1, 0, 1],[0, 0, 1, 0, 1, 1, 0],[0, 0, 0, 1, 1, 1, 1]])
    # h = numpy.array([[0, 0, 0, 1, 1, 1, 1],[0, 1, 1, 0, 0, 1, 1],[1, 0, 1, 0, 1, 0, 1]]) # colin. remove a extra , comma
    assert info_length in (16,32,64,128,256) 
    g = gentable[info_length]
    h = partable[info_length] 
    # corrected = 0
    # uncorrected = 0
    corr_cnt  = 0
    noerr_cnt = 0
    fail_cnt  = 0
    beyond    = 0
    tohex= lambda array: hex(int(''.join(map(str,array)),2)) 
    for i in range(ITEARTION): # n incoming received message repetitions 
        msg = createMessage(info_length) # generate a random information vector u(x)
        enc = encode(msg, g) 

        # ------- check parity right after encoder : parity before corruption ----------
        op_before =  enc.tolist().count(1) % 2
        enc_op = numpy.append(enc,op_before)  
        print "original message hex: ", tohex(msg)   
        print "encoded msg SECDED hex: ", tohex(enc_op) 

        # ------introduce corruption --------------
        noisy    = noise(enc, erate, maxerr)

        #------check parity after corruption --------
        op_after = noisy.tolist().count(1) % 2
        # --------DED_flag denotes the status of DED part, 1 means detected parity mismatch -- --
        DED_flag = op_before ^ op_after
        print 'received mesage: ', noisy," parity(after pollution): ", op_after
        ep = [x^y for x,y in izip(noisy.tolist(),enc.tolist())] 
        print 'error pattern: ',  ep 
        print 'number of errors: ', sum(ep) 

        # -----compute syndrome , set the SEC flag ------------------------------
        syndromes = syndrome(noisy, h)
        print 'syndrome vector: ', syndromes
         # -------- error pattern / error location returned if only 1 error bit, if clean, error_index = -1 ----
        error_index = findError(syndromes, h) 

        SEC_flag = int(error_index >= 0)  # SEC_flag 1 denotes error alert in SEC part 

        # create a error status code , a tuple of SEC and DED flags 
        ERROR_STATUS_CODE = (SEC_flag,DED_flag)  

        #---------------CORRECTION ACTION AS PER THE STATUS OF (SEC_FLAG,DED_FLAG) ----------
        # ------------------------------------------------------------------------------------
        if ERROR_STATUS_CODE == (0,0):
            print 'Clean! No errors !'
            noerr_cnt += 1
        elif ERROR_STATUS_CODE == (1,1) and error_index != 1000:
            corrected_vector = correct(noisy, error_index)
            print 'corrected vector : ', corrected_vector
            if numpy.array_equal(corrected_vector, enc):
                print 'correction success!!!'
                corr_cnt += 1
            else:
                print 'mis-correction...'
                fail_cnt += 1 
        elif ERROR_STATUS_CODE == (1,1) and error_index == 1000:
            print 'odd number of errors, beyond capability! '
            beyond += 1
        elif ERROR_STATUS_CODE == (1,0):
            print "2 errors detected! Unable to correct! (or even number of errors >2) " 
        else:  # error code is (0,1) odd number of error, but syndrome is zero 
            print "The impossible occurs, something wrong! fatal " 
        print '-----------------------------'

    print '================= \Summary\ ========================='
    print 'word width = ', info_length, '; bit error rate = ',erate, '; max #error = ', maxerr 
    print 'Total number of iterations: ', ITEARTION 
    print 'Corrected : ', corr_cnt 
    print 'No-error count: ',noerr_cnt 
    print 'Mis-correction: ',fail_cnt 
    print 'beyond capability: ', beyond 
    if fail_cnt == 0 :
        print 'all codes are properly handled !'

    


        # if error_index >= 0 and error_index < 1000:
        #     corrected_vector = correct(noisy,error_index)
        #     print 'corrected vector is ',corrected_vector 
        # else: # if synd = 0 
        #     print 'no error detected!' 





        
        
if __name__ == '__main__':

    
        
    
    length = int(raw_input('word width [must be valid]: '))
    n_iter = int(raw_input('Repetitions: '))
    ber    = float(raw_input('bit error rate: '))
    nerr   = int(raw_input('maximum number of errors: '))
    # eHamming(length,ber, nerr,n_iter) 
    HsiaoSECDED(length,ber, nerr,n_iter) 











