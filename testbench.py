# File-based testbench of BCH and SEC-DED. Stream-data from binary files IO 
# Author: Colin
# Date created: Nov 26 2013 Encoder testbench . write to a file_out (binary) 
# My idea: write a generator/coroutine to achieve enc/dec pipeline for input binary data stream 

import os,sys

p=os.getcwd() ; sys.path.append(p) 

import bch 

import toyhamm as hamm 
from array import array
from bitarray import bitarray # use bitarray rather than array 
import copy 
import numpy 
import random 


def coroutine(func):
	def start(*args,**keyargs):
		g = func(*args,**keyargs)
		g.next()
		return g 
	return start 

def bytearray2vec(a):
	" convert a byte array to a list. a is a bytearray [a1,a2,...] all elements in 0-255 (byte size)"
	assert isinstance(a, array)  
	aa = copy.copy(a)
	aa = aa.tolist()  
	aa = map(lambda x:bin(x)[2:].zfill(8),aa ) 
	aa = map(int, ''.join(aa) ) 
	return aa  

	

# ========================== SECDED =======================================

 

wd2mTable = {16:5, 32:6, 64:7, 128:8, 256:9} 
# CLEAR 
def Reader(file,wdsize, next_coroutine):
# def Reader(file,wdsize): #debug 
	""" input: file to read (file), word size (wdsize) , next_coroutine 
	output: frames of data as lists/vector """
	n_bytes = wdsize/8 
	f = open(file,'rb')
	# li = []  #debug 
	try:
		while True:
			
			a = bitarray() 
			a.fromfile(f,n_bytes) 
			a_list = map(int, a.to01() ) 
			# a = array('B')	 
			# a.fromfile(f, n_bytes) # grab a word each time 
			# a_list = bytearray2vec(a) 
			assert len(a_list)==wdsize  
			# li.extend(a_list) #debug 
			next_coroutine.send(a_list) 
		next_coroutine.close()
		# print li
	except EOFError:
		pass  
	except AssertionError:
		print 'a_vec length=',len(a_list)

	finally: 
		f.close() 
	# print li # debug 
	


#CLEAR 
@coroutine
def HamEncoder(wdsize, next_coroutine):
	""" 
	Hamming encoder 
	in: wdsize and take a list
	out: a encoded vector (list)
	"""

	# print '----- SECDED Encoding -------'
	try:
		while True:
			msg = (yield)
			assert len(msg) == wdsize and isinstance(msg, list) # type check and length match  
			msg_np = numpy.array(msg, dtype = int) # convert to np array 
		 	g = hamm.gentable[wdsize]
		 	enc_np = numpy.dot(msg_np, g) % 2
		 	enc_list = enc_np.tolist() 
		 	op = enc_list.count(1) % 2 # compute overall parity bit 
		 	enc_list.append(op) # append overall parity bits
		 	# send a np array to next 
		 	next_coroutine.send(enc_list)  
	 	# enc = list(enc)  #  for writing bin files. 
	except GeneratorExit:
		next_coroutine.close() 
	except AssertionError:
		print 'msg length=',len(msg)
# =========================================BCH ENCODER =======================
@coroutine
def BCHencoder(wdsize, next_coroutine):
	""" 
	in: wdsize, take (yield) as a list 
	out: a encoded list of bits 
	""" 

	# print ' ----- BCH Encoding ------------'
	try:
		while True:	
			m = wd2mTable[wdsize] 
			msg = (yield)
			assert len(msg)==wdsize 
			assert isinstance(msg, list) # type check : consumes list
			enc_list = bch.encode( m, msg)
			# print enc_list #debug 
			next_coroutine.send(enc_list) 
	except GeneratorExit:
		next_coroutine.close()
	except AssertionError:
		print 'msg length =',len(msg)  


@coroutine
def Printer(ofile):
	try:
		while True: 
			idata = (yield)
			assert isinstance(idata, list) # type check. consumes a list 
			# print 'PRINTOUT: \n',idata #debug 
			f = open(ofile,'ab') 
			# f = open(ofile,'a') #debug 
			# s = ''.join(map(str,idata)) #debug 
			# f.write(s+'\n') #debug 
			a = bitarray(idata) # convert the in_data to a bitarray for writing 
			a.tofile(f) # write bytes  with padding  

	except GeneratorExit:
		f.close()
		print ' ====DONE===='
	finally:
		if not f.closed:
			f.close() 
		else:
			pass 

		






# ========================================// DECODER //===========================================
#BUGGY 
@coroutine
def BCHdecoder(wdsize,next_coroutine):
	""" 
	in: wdsize (word width)
	out: corrected word , if fail ,then hands-off and return original data 
	"""
	# noerr_count = 0 
	corr_count = 0 
	fail_count = 0
	err_detected = 0 
	m = wd2mTable[wdsize] 
	n = 2*m + wdsize # code block length 
	try:
		while True:
			recv = (yield)
			assert isinstance(recv, list) and len(recv) == n 
			(s1,s3) = bch.syndrome(m, recv) 
			if s1==0:
				next_coroutine.send(recv[:wdsize]) # return original data for printing/writing 
				# noerr_count += 1
				continue
			else:
				err_detected += 1  # syndrome non-zero --> error detected! 
				(A1,A2) = bch.errorLocator(m,s1,s3) 
				errpol = bch.errorPoly( m, A1, A2) 
				if errpol < 0:
					# -------------decoding failure, return original data -------  
					fail_count += 1  
					next_coroutine.send(recv[:wdsize])
					continue 
				corr_vec = bch.correct(recv, errpol)
				corr_count += 1  
				assert isinstance(corr_vec, list) 
				next_coroutine.send(corr_vec[:wdsize]) 



	except GeneratorExit:
		next_coroutine.close()
		# ---- write stat into log file ---- TODO 
		with open('bchlog.txt','w') as f:
			print >>f, '========= STATS ========='
			print >>f, '# corrupted codewords: ', err_detected
			print >>f, '# corrected codewords: ', corr_count 
			print >>f, '# decoding failures :', fail_count 

		


@coroutine
def HamDecoder(wdsize, next_coroutine):
 	""" 
 	 in: wdsize(wordsize) and a list input for decoding 
 	 out: decoded word and error log write 
 	 """ 
 	r = wd2mTable[wdsize] + 1 # number of parity bits 
 	H = hamm.partable[wdsize] 
 	corrupted = 0 
 	twoerr = 0
 	corrected = 0
 	fatal = 0
 	try:
 		while True:
 			recv = (yield)
 			assert isinstance(recv, list) and len(recv) == r+wdsize  # received code validation
 			DED_flag = reduce(lambda x,y: x^y, recv )  # parity check 
 			recv_np = numpy.array(recv, dtype = int )  
 			error_index = hamm.findError( hamm.syndrome(recv_np[:-1], H), H)  # if return 1000, it's beyond capability !!
 			SEC_flag = int(error_index >= 0)  # set SEC  flag. 
 			ERROR_STATUS_CODE = (SEC_flag, DED_flag) 
 			if ERROR_STATUS_CODE==(0,0):
 			 	next_coroutine.send(recv[:wdsize]) 
 			elif ERROR_STATUS_CODE == (1,1) and error_index != 1000:   # MAKE SURE IT'S 1 ERROR 
 				corrupted += 1 # detected a corrupt word , also corrects 
 				corr_np = hamm.correct(recv[:-1], error_index)
 				corr_vec = corr_np.tolist() 
 				corrected += 1 
 				next_coroutine.send(corr_vec) 
 			elif ERROR_STATUS_CODE == (1,0):
 				corrupted += 1  # detected a corrupt word , unable to correct 
 				twoerr += 1
 				next_coroutine.send(recv[:wdsize]) # detected 2 err, not correctable. send original data(list)  
 			else:  # 0,1 or error_index = 1000 && (1,1) [odd number of errors, beyond ]  #err >=3 
 				next_coroutine.send(recv[:wdsize])  # fatal error 
 				fatal += 1 


 	except GeneratorExit:
 		next_coroutine.close() 
 		# -----write stat log TODO ---
 		with open('SECDEDlog.txt','w') as f:
 			print >>f, '========= STATS ========='
			print >>f, '# detected corrupted codewords: ', corrupted 
			print >>f, '# attampted corrected codewords: ', corrected
			print >>f, '# detected two-error detected/or even number of errors :', twoerr
			print >>f, '# fatal-error codewords: ',fatal    
	




# ======================/ END OF DECODER /=========================


# =============== ARTIFICAL CODE ERROR GENERATOR =========================

@coroutine
def ErrorGen(vdd, next_coroutine):
	""" 
	in: vdd : supply voltage. adopt the BER model as a function of VDD. BER = f(Vdd)= A(Vo-Vdd)^k 
	out: corrupted vector ; in list out list 
	"""
	ber = 0 if vdd > 0.85 else 6*(0.85-vdd)**6.14 
	# flip = lambda x: x if random.random() < ber else int(not(x)) 
	try:
		while True:
			vin = (yield)
			assert isinstance(vin, list)
			vin2 = copy.copy(vin)  
			# vin2 = map(flip, vin2) 
			for i in xrange(len(vin2)):
				if random.random() < ber:	
					vin2[i] = int( not(vin2[i]) ) # flip bits 

			next_coroutine.send(vin2) 

			
	except GeneratorExit:
		next_coroutine.close()  




 
import getopt 
 
def main():
	encoder_sel = {'bch': BCHencoder, 'ham': HamEncoder}
	# ============PARSE command line arguments ============================
	try:
		opts, remainder = getopt.getopt(sys.argv[1:],"i:o:bhw:",['infile=','outfile=','bch', 'ham','wdsize=']) 
	except getopt.GetoptError as err:
		print "provide arguments : -i infile -o ofile -h(hamming) or -b(bch) -w(--wdsize) wordwidth" 
		print str(err) 
		sys.exit(2) 
	ofile = 'printout'
	ifile = 'bin' 
	print opts 
	for option,arg in opts:
		if option in ('-i','--infile'):
			ifile = arg 
		elif option in ('-o','--outfile'):
			ofile = arg 
		elif option in ('-b','--bch'):
			ecctype = 'bch' 
		elif option in ('-h','--ham'):
			ecctype = 'ham' 
		elif option in ('-w','--wdsize'):
			wdsize = int(arg ) 

		else:
			assert False, 'unhandled option' 
	# ==============================================END OF Arg parser ===================
	Reader( ifile, wdsize, encoder_sel[ecctype](wdsize, Printer(ofile) ) ) 

if __name__ == '__main__':
	main() 
	


		





	





		


