### CRC code combinational logic algorithm. Similar to BCH comb. 


from gfield import poly_div 
from itertools import  izip, combinations 
import numpy as np 
from bch import  CreateMessage , noise
from bch2 import bin2code 
# from mail import send_mail 
# from toyhamm import hsiaoFixable 
import math,collections,functools 

################ Math Helpers ##################
class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)


@memoized
def factorial(n):
  "factorial n!"
  if n <= 1:
    return 1 
  else:
    return n*factorial(n-1) 


def nCr(n,r):
  "compute nCr" 
  z = factorial(n)/(factorial(r)*factorial(n-r)) 

  return z 


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







# =============== CRC helpers ============================
# ------------------------------------------------------

#CRC generator polynomial table as per genpoly degree CRC-r 
#crcGeneratorMap = {3:11, 4:19, 5:41, 6:67} # choices for CRC-5: 41(odd),53(even),37(odd) 
# crcGeneratorMap = {3:11, 4:19, 5:41, 6:111} # choices for CRC-5: 41(odd),53(even),37(odd) 
crcGeneratorMap = {3:9, 4:29, 5:53, 6:111, 7:197, 8:411,9:807} # CRC-r table , all optimized to g(x)=p(x)(1+x) form 

def crcGenMatrix(r,k):
  	"produce G matrix of CRC-r code , Generator degree = r; able to detect r-1 burst errors" 
  	genpoly = crcGeneratorMap[r]  
  	b = [] 
	for i in xrange(k):
		b.append(bin2code( poly_div(2**(r+i), genpoly), r ) )


	b_array = np.array(b) # convert it to np array for matrix operation 
	G_array = np.hstack((b_array, np.eye(k,dtype=int)))
	return G_array 

def crcCheckMatrix(r,k):
	"produce corresponding H matrix for CRC-r and information length k" 
	# if genpoly == 0:
	genpoly = crcGeneratorMap[r]  
  	b = [] 
	for i in xrange(k):
		b.append(bin2code( poly_div(2**(r+i), genpoly), r ) )


	b_array = np.array(b) # convert it to np array for matrix operation 
	name_array = b_array.transpose() # [rxk]
	H_array = np.hstack( (np.eye(r, dtype=int), name_array  ) ) 

	return H_array 



# ================= CRC Encoder ========================

def crcEncoder(r,k,data,parityonly=False):
	"CRC-r encoder for k info bits "

	assert isinstance(data, list) and len(data) == k 
 	# assert k % 8 == 0 
 	G_array = crcGenMatrix(r, k) # get G matrix for wordsize k 
	data_array = np.array(data) 
	# matrix mult to generate code 
	enc_array = np.dot(data_array, G_array) % 2 
	enc_array = enc_array.astype('int') 
	enc = enc_array.tolist() 
	out = enc if not parityonly else enc[:r]
	return out 


# ============= CRC-r Decoder ====================
def crcDecoder(r,k,code):
	"CRC-r decoder for k info bits. return a flag indicating error  "
	assert isinstance(code, list)
	H_array = crcCheckMatrix(r,k)
	c_array = np.array(code) 
	s_array = np.dot(H_array,c_array) % 2 # S = Hxr 
	s_array = s_array.astype('int')   # syndrome vector as a np array 

	# print 'syndrome: ', ''.join(map(str,s_array)) # DEBUG 

	return True if any(s_array) else False 

### ============ Composite CRC (CRC-5 + simple parity) Decoder ====

def compCRC6Decoder(k,code):
	"composite CRC6=CRC-5 + CRC-1 Decoder r=6" 
	assert isinstance(code, list) and len(code)==k+6
	n = k + 6
	crc5_err = crcDecoder(5,k,code[:(n-1)]) # use CRC-5 to check up to but the last bit 
	odd_err = reduce(lambda x,y:x^y, code) # overall parity check 

	has_err = crc5_err or odd_err 

	return has_err 




# ============ MAIN TESTBENCH ==============
def main(r, k, ber, nerr, ITERATION=10):
	"testbench of CRC-r " 

	 
	
	detect_fail = 0
	
	# -----------------------------END OF INIT --------------------------

	for i in range(ITERATION):
		# ----------ENCODER PART --------------------

		info = CreateMessage(k) 
		vec2hex = lambda v:hex(int(''.join(map(str,v)),2)) 
		enc = crcEncoder(r, k, info)  
		print 'data_in:  ', info 
		print 'in_data HEX : ', vec2hex(info) 
		print 'encoded codeword: ',enc, 'parity: ', enc[:r]
		print 'encoded HEX: ', vec2hex(enc) 
		
		# ------------NOISE/POLLUTION -------------------

		received = noise( enc, ber, nerr ) 
		err_vector = [x^y for x,y in izip(received, enc)] 
		err_location = np.nonzero(np.array(err_vector))[0].astype('int')  
		print 'received code: ', received
		print 'received code HEX: ', vec2hex(received) 
		# print 'error pattern: ', err_vector  
		print 'number of errors = ', sum(err_vector), '; err_locator: ', err_location 


		# -------------- DECODER PART --------------------
		has_error = crcDecoder(r,k, received) # a boolean flag indicating error 
		if (sum(err_vector) and not has_error) or ( not sum(err_vector) and has_error ) :
			print 'fail to detect errors'
			detect_fail += 1  
		else:
			print 'success!!!' 


		

		
		print '-------------------- NEXT -----------------'

	print " detection failures = ", detect_fail 


# ================== Reliability Test of different CRC generator polys ==================

### exhaustive error-pattern test for CRC-r 

### polynomial display helper 


def showpoly(f,deg):
	"string representation of a input polynomial"
	 
	s = ''

	if f==0:
		return '0'
	for i in range(deg,0,-1):
		if (1<<i) & f:
			s = s + (' x^'+ repr(i))
	if 1 & f:
		s = s + ' 1'
	return s.strip().replace(' ','+') 

def robustTest(r,k):
	"Exhaustive error testing for CRC-r of generator polynomial crcgen"

	g = crcGeneratorMap[r] 
	n = k+r 
	fails = 0 
	#####1e
	# for i in xrange(n):
	# 	e = [0]*(n) 
	# 	e[i] = 1 
	# 	has_err = crcDecoder( r,k, e) 
	# 	if not has_err:
	# 		fails += 1 
	# 		# print 'miss error: ', ''.join(map(str,e)) 

	# ##2e

	# for i1,i2 in combinations(xrange(n),2):
	# 	e = [0]*(n) 
	# 	e[i1]=e[i2]=1 
	# 	has_err = crcDecoder(r,k,e) 
	# 	if not has_err:
	# 		fails += 1
	# 		# print 'miss error: ', ''.join(map(str,e)) 


	##3e
	# for i1,i2,i3 in combinations(xrange(n),3):
	# 	e = [0]*(n) 
	# 	e[i1]=e[i2]=e[i3]=1 
	# 	has_err = crcDecoder(r,k,e) 
	# 	if not has_err:
	# 		fails += 1
	# 		# print 'miss error: ', ''.join(map(str,e)) 

	###4e 

	for i1,i2,i3,i4 in combinations(xrange(n),4):
		e = [0]*(n) 
		e[i1]=e[i2]=e[i3]=e[i4]=1 
		has_err = crcDecoder(r,k,e) 
		if not has_err:
			fails += 1
			# print 'miss error: ', '4.join(map(str,e)) 

	##5e
	# for i1,i2,i3,i4,i5 in combinations(xrange(n),5):
	# 	e = [0]*(n) 
	# 	e[i1]=e[i2]=e[i3]=e[i4]=e[i5]=1 
	# 	has_err = crcDecoder(r,k,e) 
	# 	if not has_err:
	# 		fails += 1
	# 		# print 'miss error: ', ''.join(map(str,e)) 
	outs = '--------------SUMMARY----------------\n'
	outs += 'CRC generator:{0} ; datasize k = {1} \n'.format(showpoly(g,r), k)  
	outs += 'total 4err fails: {0} \n'.format(fails)   
	outs +=  'total 4e cases: {0}, fail rate = {1:.3f}% \n'.format(nCr(n,4),100*fails/float(nCr(n,4)) )  

	print outs 
	#send_mail( 'Colin', ['hcolinlin@gmail.com'], 'CRCrepr2', outs) #OPTIONAL 


def robustTestComp(r,k):
	"Exhaustive error testing for CRC-r of generator polynomial crcgen"

	# g = crcGeneratorMap[r] 

	fails = 0 
	# 1e
	for i in xrange(k+r):
		e = [0]*(k+r) 
		e[i] = 1 
		has_err = compCRC6Decoder(k, e)
		if not has_err:
			fails += 1 
			# print 'miss error: ', ''.join(map(str,e)) 

	##2e

	for i1,i2 in combinations(xrange(k+r),2):
		e = [0]*(k+r) 
		e[i1]=e[i2]=1 
		has_err = compCRC6Decoder(k, e)
		if not has_err:
			fails += 1
			# print 'miss error: ', ''.join(map(str,e)) 


	#3e
	for i1,i2,i3 in combinations(xrange(k+r),3):
		e = [0]*(k+r) 
		e[i1]=e[i2]=e[i3]=1 
		has_err = compCRC6Decoder(k, e)
		if not has_err:
			fails += 1
			# print 'miss error: ', ''.join(map(str,e)) 

	#4e 

	for i1,i2,i3,i4 in combinations(xrange(k+r),4):
		e = [0]*(k+r) 
		e[i1]=e[i2]=e[i3]=e[i4]=1 
		has_err = compCRC6Decoder(k, e)
		if not has_err:
			fails += 1
			# print 'miss error: ', ''.join(map(str,e)) 

	##5e
	for i1,i2,i3,i4,i5 in combinations(xrange(k+r),5):
		e = [0]*(k+r) 
		e[i1]=e[i2]=e[i3]=e[i4]=e[i5]=1 
		has_err = compCRC6Decoder(k, e)
		if not has_err:
			fails += 1
			# print 'miss error: ', ''.join(map(str,e)) 
	outs = '--------------SUMMARY----------------\n'
	outs += 'Composite CRC-5+1 generator \n'   
	outs += 'total 5err fails: {0} \n'.format(fails)   
	outs +=  'total 5e cases: {0}, fail rate = {1:.3f}% \n'.format(584934,fails/584934.0)   

	print outs 
	# send_mail( 'Colin', ['hcolinlin@gmail.com'], 'CRCrepr3', outs) #OPTIONAL 


#### Compare CRC-r and SECDED in light of detection capacity ###############
 
# def robustTestHsiao(k):
# 	"Exhaustive error testing for Hsiao detection capacity "

	
# 	r = int(math.ceil(math.log(k,2)) ) + 2 
# 	fails = 0 
# 	#####1e
# 	# for i in xrange(k+r):
# 	# 	e = [0]*(k+r) 
# 	# 	e[i] = 1 
# 	# 	fixable = hsiaoFixable(k,e)
# 	# 	if not fixable:
# 	# 		fails += 1 
# 	# 		# print 'miss error: ', ''.join(map(str,e)) 

# 	# ##2e

# 	for i1,i2 in combinations(xrange(k+r),2):
# 		e = [0]*(k+r) 
# 		e[i1]=e[i2]=1 
# 		evenerr = hsiaoFixable(k,e) 
# 		if not evenerr:
# 			fails += 1
# 			# print 'miss error: ', ''.join(map(str,e)) 


# 	#3e
# 	# for i1,i2,i3 in combinations(xrange(k+r),3):
# 	# 	e = [0]*(k+r) 
# 	# 	e[i1]=e[i2]=e[i3]=1 
# 	# 	fixable = hsiaoFixable(k,e) 
# 	# 	if  fixable:
# 	# 		fails += 1
# 	# 		# print 'miss error: ', ''.join(map(str,e)) 

# 	###4e 

# 	# for i1,i2,i3,i4 in combinations(xrange(k+r),4):
# 	# 	e = [0]*(k+r) 
# 	# 	e[i1]=e[i2]=e[i3]=e[i4]=1 
# 	# 	evenerr = hsiaoFixable(k,e) 
# 	# 	if  not evenerr:
# 	# 		fails += 1
# 	# 		# print 'miss error: ', ''.join(map(str,e)) 

# 	##5e
# 	# for i1,i2,i3,i4,i5 in combinations(xrange(k+r),5):
# 	# 	e = [0]*(k+r) 
# 	# 	e[i1]=e[i2]=e[i3]=e[i4]=e[i5]=1 
# 	# 	fixable = hsiaoFixable(k,e) 
# 	# 	if fixable:
# 	# 		fails += 1
# 	# 		# print 'miss error: ', ''.join(map(str,e)) 
# 	outs = '--------------SUMMARY----------------\n'
# 	outs += 'Hsiao {0} \n'.format(k)  
# 	outs += 'total 2,4 err-detection fails: {0} \n'.format(fails)   
# 	# outs +=  'total 5e cases: {0}, fail rate = {1:.3f}% \n'.format(575757, 100*fails/575757.0)  

# 	print outs 



#### encoder testbench 

def crcEncTest(inlist,k):
	"given a inlist of hex form data, puts encoded words "

	for data in inlist:
		data_ls = hex2list(data,k)
		o_code = crcEncoder(7,k,data_ls)
		hex_code = list2hex(o_code)
		print 'encoded: ', hex_code 





if __name__ == '__main__':
	k = int(raw_input('data word size k = ')) 
	errate = float(raw_input('bit error rate = ')) 
	maxerr = int(raw_input('max error occurences = '))
	r = int(raw_input('CRC-r r = ')) 
	reads = int(raw_input(' iterations = ')) 
	main(r, k , errate, maxerr, reads)

	# k=32
	# r=4
	# robustTest(r,k) 
	# for r in range(4,10):
	# 	robustTest(r,k)
	# robustTestHsiao(k) 
	#robustTestComp(r,k)
