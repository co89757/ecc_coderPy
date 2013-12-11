# Pure Combinational Logic BCH enc/dec 
# Author:Colin 
# Date created: Dec 10 2013 
# BCH enc-dec based on matrix operations using pure Combinational logic
# STIPULATION: Function return values should all be converted to *list type* 
			 # Use *prepending* parity to create systematic encoding. 
			 # all polynomials are presented in *ascending degree* form . for example:
			 # (c0,c1,c2,...c5) = c0 + c1x + c2*x^2 + ... c5*x^5 
# =================== ENCODER ====================

from gfield import * 
from itertools import combinations, izip 
import numpy as np 
import math 
from bch import minpol 

# -------/ Helper functions /------------

def bin2code(number,width=None):
	"convert a binary number or integer to its ascending polynomial vector form as list type. e.g. 0b110--> 0110"

	b = bin(number)[2:] # convert to a str repr of binary number 
	b_reverse = b[::-1] # reverse a stirng 
	if width and width > len(b):
		appendix = '0'*(width - len(b) )  
		result_s = b_reverse + appendix 
		return map(int, result_s) 
	else:
		return map(int, b_reverse) 

wd2mTable = {8:4, 16:5, 32:6, 64:7, 128:8, 256:9} 



def genMatrix(k):
	"return generator matrix of BCH(k,t=2) code. k : word width; return a numpy array G " 
	# m = wd2mTable[k] 
 	m = int(math.ceil(math.log(k, 2)) ) + 1 # DEBUG 
 	minipol_1 = minpol[m][1] 
	minipol_3 = minpol[m][3] 

	r = 2*m  # redundancy n-k = t*m = 2m 

	genpoly = poly_mul(minipol_1, minipol_3) # generator polynomial = LCM{m1,m3} 
	b = [] 
	for i in xrange(k):
		b.append(bin2code( poly_div(2**(r+i), genpoly), r ) )


	b_array = np.array(b) # convert it to np array for matrix operation 
	G_array = np.hstack((b_array, np.eye(k,dtype=int)))
	return G_array 





# ==================== ENCODER ================
def encoder(data,k):
 	" use combinational logic to generate encoded data. k is word width "
 	assert isinstance(data, list) and len(data) == k 
 	# assert k % 8 == 0 
 	G_array = genMatrix(k) # get G matrix for wordsize k 
	data_array = np.array(data) 
	# matrix mult to generate code 
	enc_array = np.dot(data_array, G_array) % 2 
	enc_array = enc_array.astype('int') 
	enc = enc_array.tolist() 

	return enc 

# ============== DECODER ============== 

def parMatrix(k, transpose=False):
	"return H matrix of BCH code for k wordsize. ref: Jorge P131/102" 
	# m = wd2mTable[k] 	
 	m = int(math.ceil(math.log(k, 2)) ) + 1 # DEBUG 
 	elem_order = 2**m - 1 # element order that a^elem_order = 1 in GF(2^m)  
 	n = k + 2*m 
 	a = FiniteField(m)
 	h = [] 
 	for i in xrange(n):
 		newrow = bin2code(a.gf_exp[i], m) + bin2code(a.gf_exp[(3*i % elem_order)], m ) 
 		h.append(newrow) 
 	HT_array = np.array(h,dtype=int) 

 	H_array = np.transpose( HT_array) 

 	z = H_array if not transpose else HT_array 
 	return z 



def decoder(code,k):
	"take prepended code as a list and decode it , return the corrected codeword as list. report err status"
	assert isinstance(code, list)
	m = int(math.ceil(math.log(k, 2)) ) + 1 # DEBUG 
	r = m*2  
	HT_array = parMatrix(k, True) 
	c_array = np.array(code) 
	s_array = np.dot(c_array,HT_array) % 2 
	s_array = s_array.astype('int')   # syndrome vector as a np array 
	if not any(s_array):
		print 'no error'
		return code  
	# s_list = s_array.tolist() 


	# iterate over 1-error flip pattern
	e=[0]*(k+r)  
	e_array = np.array(e)
	for i in xrange(k+r):
		e1 = np.copy(e_array) 
		e1[i] = 1

		prod = np.dot(e1, HT_array) 
		if np.array_equal( prod, s_array):
			code_out = [x^y for x,y in izip(e1,code)] 
			print '1 err at {0}-th position'.format(i)  
			return code_out 
	# 2-error pattern
	for i,j in combinations(range(k+r),2):
		e2 = np.copy(e_array)
		e2[i] = 1 
		e2[j] = 1 
		product = np.dot(e2, HT_array)
		if np.array_equal(product,s_array):
		 	code_out = [x^y for x,y in izip(e2,code)] 
		 	print '2 error, postion at ({0},{1}).'.format(i,j) 
		 	return code_out 

	# no name-match 
	print 'beyond error correctability'
	return code  


def errbit2synd(k):
	"return a dictionary. d[i] returns a list of syndromes corresponding to cases where flip[i]=1"
	m = int(math.ceil(math.log(k, 2)) ) + 1 # DEBUG 
	r = m*2  
	HT_array = parMatrix(k, True) 
	n = k+r 
	dic = {}

	# 1-error i indicate i-th databit error 
	for i in xrange(k):
		dic[i] = [] 
		e1_array = np.array([0]*n)  
		e1_array[i+r] = 1 

		s1_array = np.dot(e1_array,HT_array) % 2 

		s1_list = s1_array.tolist()

		dic[i].append(s1_list)  
		 

	for i,j in combinations(range(k),2):
		e2_array = np.array([0]*n) 
		e2_array[i+r] = 1
		e2_array[j+r] = 1 

		s2_array = np.dot(e2_array, HT_array) % 2 

		s2_list = s2_array.tolist() 

		dic[i].append(s2_list) 
		dic[j].append(s2_list) 

	return dic 




		




		


		 


		





	







	

		
			
