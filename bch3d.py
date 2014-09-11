# Pure Combinational Logic DECTED BCH enc/dec 
# Author:Colin 
# Date created: Dec 10 2013 
# BCH enc-dec based on matrix operations using pure Combinational logic , adding one overall parity for TED 
# STIPULATION: Function return values should all be converted to *list type* 
			 # Use *prepending* parity to create systematic encoding. 
			 # all polynomials are presented in *ascending degree* form . for example:
			 # (c0,c1,c2,...c5) = c0 + c1x + c2*x^2 + ... c5*x^5 

# =================== ENCODER ====================

from gfield import * 
from itertools import combinations, izip 
import numpy as np 
import math 
from bch import minpol, CreateMessage , noise
import copy   

# -------/ Helper functions /------------

def bin2code(number,width=None):
	"convert a binary number or integer to its ascending polynomial vector form as list type. e.g. 0b11001--> [10011]"

	b = bin(number)[2:] # convert to a str repr of binary number 
	b_reverse = b[::-1] # reverse a stirng 
	if width and width > len(b):
		appendix = '0'*(width - len(b) )  
		result_s = b_reverse + appendix 
		return map(int, result_s) 
	else:
		return map(int, b_reverse) 

wd2mTable = {8:4, 16:5, 32:6, 64:7, 128:8, 256:9} 

def hex2list(hex,n):
	"convert a hex number to 011001 form (a binary list of length n)"

	binx = bin(hex) 
	binx = binx[2:] ## a string ,like '1001101' 
	assert len(binx) <= n 

	binx = binx.zfill(n) 

	outlist = map(int, binx) 
	return outlist 

### turn a list to hex form 

list2hex = lambda v:hex(int(''.join(map(str,v)),2))   


def bch3dEncTest(ifile,k,ofile=None):
	"given a inlist of hex form data, puts encoded words "

	if ofile:
		of = open(ofile,'w')
		with open(ifile,'r') as inf:
			for data_str in inf:
				data_ls = hex2list(int(data_str, 16 ) ,k)
				o_code = encoder(data_ls,k)
				hex_code = list2hex(o_code)
				# print 'encoded: ', hex_code 
				print >>of, hex_code 
		of.close()
	else:
		print "-----codewords--------"
		for data in inlist:
			data_ls = hex2list(data,k)
			o_code = encoder(data_ls,k)
			hex_code = list2hex(o_code)
			print  hex_code






### -------------------------- END OF HELPERS -------------------- 

def genMatrix(k):
	"return generator matrix of BCH_3D(k,t=2) code. k : word width; return a numpy array G " 
	# m = wd2mTable[k] 
 	m = int(math.ceil(math.log(k, 2)) ) + 1 # DEBUG 
 	minipol_1 = minpol[m][1] 
	minipol_3 = minpol[m][3] 

	r = 2*m  # redundancy n-k = t*m = 2m 

	genpoly = poly_mul(minipol_1, minipol_3) # generator polynomial = LCM{m1,m3} 
	b = [] 
	for i in xrange(k):
		b.append(bin2code( poly_div(2**(r+i), genpoly), r ) )


	b_array = np.array(b) # parity matrix G= [P,I] 
	# p is initial parity matrix, op_column is the overall parity column as an numpy array
	op_column = lambda p: np.array( [int(not(sum(row) % 2)) for row in p] ) 
	b_array = np.column_stack((b_array,op_column(b_array)))
	G_array = np.hstack((b_array, np.eye(k,dtype=int)))
	return G_array 





# ==================== BCH_3D( 3e detection) ENCODER ================
def encoder(data,k,parityonly=False):
 	" use combinational logic to generate encoded data. k is word width "
 	assert isinstance(data, list) and len(data) == k 
 	# assert k % 8 == 0 
 	r = 2*(int(math.ceil(math.log(k, 2)) ) + 1) # #checkbits for DEC BCH 
 	G_array = genMatrix(k) # get G matrix for wordsize k 
	data_array = np.array(data) 
	# matrix mult to generate code 
	enc_array = np.dot(data_array, G_array) % 2 
	enc_array = enc_array.astype('int') 
	enc = enc_array.tolist()
	# op = reduce(lambda x,y:x^y, enc)
	# initial_checkbits = enc[:r]  
	out = enc if not parityonly else enc[:(r+1)] 
	return out 

# ============== DECODER ============== 

def checkMatrix(k, transpose=False):  
	"""return H matrix of BCH_3D code for k wordsize. 
	ref: Jorge P131/102 H[rxn] = [1 alpha alpha^2 .... alpha^n-1 ; 1 alpha^3 ...]
	to add TED , H is expanded by a inserting a all-0 column at the r-th col. and then an all-1 row at the bottom. 
	finally H for TED is H[(r+1)x(n+1)] 
	""" 
		
 	m = int(math.ceil(math.log(k, 2)) ) + 1  
 	elem_order = 2**m - 1 # element order that a^elem_order = 1 in GF(2^m)  
 	n = k + 2*m 
 	a = FiniteField(m)
 	h = [] 
 	for i in xrange(n):
 		newrow = bin2code(a.gf_exp[i], m) + bin2code(a.gf_exp[(3*i % elem_order)], m ) 
 		h.append(newrow) 
 	HT_array = np.array(h,dtype=int) # old HT 

 	H_array = np.transpose( HT_array) 
 	H_array = np.insert(H_array, 2*m, 0, axis=1 ) # add all-0 column to r-th col 

 	H_array_new = np.vstack((H_array, np.ones(n+1,dtype=int)) ) # add all-1 row to bottom, thus new H matrix 
 	HT_array_new = H_array_new.transpose() # new HT
 	z = H_array_new if not transpose else HT_array_new  
 	return z 



def decoder(code,k):
	"""take prepended code as a list and decode it , return the corrected codeword as list. report err status too
	return a tuple (decode_word, status_code)
	status_code: 0: no err 1: 1-2 errors 3: 2+ error 


	"""

	m = int(math.ceil(math.log(k, 2)) ) + 1  
	r = m*2 + 1 # DECTED , one additional check bit 
	assert isinstance(code, list)
	assert len(code) == r+k 
	
	HT_array = checkMatrix(k, True) 
	c_array = np.array(code) 
	s_array = np.dot(c_array,HT_array) % 2 # S = rHT 
	s_array = s_array.astype('int')   # syndrome vector as a np array 
	print 'syndrome: ', s_array # DEBUG 
	# print 'HT matrix: \n', HT_array # DEBUG 
	if not any(s_array):
		print 'no error'
		return (code,0)  
	# s_list = s_array.tolist() 


	# iterate over 1-error flip pattern
	e=[0]*(k+r)  
	e_array = np.array(e)
	for i in xrange(k+r):
		e1 = np.copy(e_array) 
		e1[i] = 1

		prod = np.dot(e1, HT_array) % 2 # check eq. S == eHT ? 
		if np.array_equal( prod, s_array):
			code_out = [x^y for x,y in izip(e1,code)] 
			print '1 err at {0}-th position'.format(i), '\n -------------------' 
			return (code_out,1) 
		else:
			continue  
	# 2-error pattern
	for i,j in combinations(range(k+r),2):
		e2 = np.zeros(k+r, dtype = int ) 
		e2[i] = 1 
		e2[j] = 1 
		product = np.dot(e2, HT_array) % 2 
		if np.array_equal(product,s_array):
		 	code_out = [x^y for x,y in izip(e2,code)] 
		 	print '2 error, postion at ({0},{1}).'.format(i,j) , '\n ------------------' 
		 	return (code_out,1) 
		else:
			continue 

	# no name-match 
	print 'detected 3+ errors \n -----------------'
	return (code,2)   



##################################### DEC-TED BCH with 1 extra overall parity at the end #################

 



def main(k, ber, nerr, ITERATION=10):
	"testbench of combinational DECTED BCH" 

	# m = int(math.ceil(math.log(k, 2)) ) + 1 # DEBUG 
	# r = m*2 
	
	miscorr = 0 
	
	# -----------------------------END OF INIT --------------------------

	for i in range(ITERATION):
		# ----------ENCODER PART --------------------

		info = CreateMessage(k) 
		vec2hex = lambda v:hex(int(''.join(map(str,v)),2)) 
		enc = encoder(info, k)  #use TED BCH 
		print 'data_in:  ', info 
		print 'in_data HEX : ', vec2hex(info) 
		print 'encoded codeword: ',enc, 'length: ', len(enc) 
		print 'encoded HEX: ', vec2hex(enc) 
		
		# ------------NOISE/POLLUTION -------------------

		received = noise( enc, ber, nerr ) 
		err_vector = [x^y for x,y in izip(received, enc)] 
		err_location = np.nonzero(np.array(err_vector))[0].astype('int')  
		print 'received code: ', received
		print 'received code HEX: ', vec2hex(received) 
		print 'error pattern: ', err_vector  
		print 'number of errors = ', sum(err_vector), '; err_locator: ', err_location 


		# -------------- DECODER PART --------------------
		out_code,status = decoder( received, k)  


		if out_code[-k:] == info:
			print 'clean readout !!!'
		elif out_code[-k:] != info and status == 1: 
			miscorr += 1 
			print 'mis-correction!' 
		else:
			print 'detected 3+ errors, ' 
		
		print '-------------------- NEXT -----------------'

	print 'Total miscorrections = ', miscorr 




# ------------------------------- END OF DEC-TED BCH SECTION ------------------------------------
# ///////////////////////////////////////////////////////////////////////////////////////////////


# ================= Syndrome pattern to error bit mapping function (for code generator) ====
def err2SyndMapping(k): # !!!  PENDING: ignore cases where 1-2 errs in parity.  
	"return a dictionary. for DECTED BCH d[i] returns a list of syndromes corresponding to cases where databitflip[i]=1"
	m = int(math.ceil(math.log(k, 2)) ) + 1 # DEBUG 
	r = m*2 + 1 # r(3D) = r(DEC) + 1 
	HT_array = checkMatrix(k, True) 
	n = k+r 
	# dic = {}.fromkeys(range(k),[]) # initialize dictionary with keys 0->(k-1) and empty list  
	dic = {}.fromkeys(xrange(k)) 

	# 1-databit-error i indicate i-th databit error: either 1e in databits OR 1e in data plus 1e in parity 
	for i in xrange(k):
		dic[i] = [] 
		#case1: 1e in databits 
		e1_array = np.array([0]*n)  
		e1_array[i+r] = 1 # offset by r, need to pass the parity bits 
		s1_array = np.dot(e1_array,HT_array) % 2 
		s1_list = s1_array.tolist()
		dic[i].append(s1_list)
	
	# mixed case: 1e in data 1e in parity
	for i in xrange(k):
		
		for p in xrange(r):
			e12_array = np.array([0]*n)
			e12_array[i+r] = 1 
			e12_array[p] = 1 
			s12_array = np.dot(e12_array,HT_array) % 2 
			s12_list = s12_array.tolist() 
			dic[i].append(s12_list)

	# 2-databit-error case 
	for i,j in combinations(range(k),2):
		e2_array = np.array([0]*n) 
		e2_array[i+r] = 1
		e2_array[j+r] = 1 

		s2_array = np.dot(e2_array, HT_array) % 2 

		s2_list = s2_array.tolist() 

		dic[i].append(s2_list) 
		dic[j].append(s2_list) 


	# print 'number of syndrome match for each databit = ', len(dic[0]) #DEBUG 
	return dic 

def BCH3dignore(k):
	"return the ignored syndrome pattern list indicating correctible err in parity only. "
	m = int(math.ceil(math.log(k, 2)) ) + 1 # DEBUG 
	r = m*2 + 1 # r(3D) = r(DEC) + 1 
	HT_array = checkMatrix(k, True) 
	n = k+r 

	ignorelist = []

	# Single-parity-error syndrome patterns 
	for p in xrange(r):
		e1_a = np.zeros(n,dtype=int) 
		e1_a[p] = 1 
		s1_a = np.dot(e1_a,HT_array) % 2 
		s1_ls = s1_a.tolist() 
		ignorelist.append(s1_ls ) 

	# double-parity error syndrome patterns 
	for i,j in combinations(range(r),2):
		e2_a = np.zeros(n,dtype=int) 
		e2_a[i] = e2_a[j] = 1 
		s2_a = np.dot(e2_a, HT_array) % 2 
		s2_ls = s2_a.tolist() 
		ignorelist.append(s2_ls) 


	return ignorelist 















# ================================ TESTING MODULE =========================


def testDecoder(k,n,nerr):
	"exhaustive testing for #err = nerr for BCH3D(n,k)" 

	### TED test 
	e = [0]*n 
	for i,j,k in combinations(xrange(n),3):
		etest = copy.copy(e) 
		etest[i]=etest[j] = etest[k] = 1 
		_ , status = decoder(etest, k) 
		if status != 2:
			print "3D failure!! " 
	print '==DONE==' 














if __name__ == '__main__':
	datasize = int(raw_input('data word size = ')) 
	errate = float(raw_input('bit error rate = ')) 
	maxerr = int(raw_input('max error occurences = ')) 
	reads = int(raw_input(' iterations = ')) 

	main(datasize, errate, maxerr, reads) 
	
	# TEST NOTE: still prone to 3-err miscorrection. a 3-error syndrome could equal a 2-error syndrome 
		 


		




		


		 


		





	







	

		
			
