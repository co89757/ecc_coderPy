# File-based testbench of BCH and SEC-DED. Stream-data from binary files IO 
# Author: Colin
# Date created: Nov 26 2013 Encoder testbench . write to a file_out (binary) 
# My idea: write a generator/coroutine to achieve enc/dec pipeline for input binary data stream
# EN/DECODER **APPEND** parity bits in all ECCs used here  

import os,sys

p=os.getcwd() ; sys.path.append(p) 

import bch 

import toyhamm as hamm 
from array import array
from bitarray import bitarray # use bitarray rather than array 
import copy 
import numpy 
import random 

# ========== HELPERS ===========
# /-----------------------------/
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

	


 
# wordsize to corresponding m in GF(2^m) mapping table 
wd2mTable = {16:5, 32:6, 64:7, 128:8, 256:9} 

# CLEAR
# ================== TERMINAL SIDE HELPERS FILE R/W================== 
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
			assert len(a_list)==wdsize  	 
			next_coroutine.send(a_list) 
		next_coroutine.close()
		 
	except EOFError:
		pass  
	except AssertionError:
		print 'a_vec length=',len(a_list)

	finally: 
		f.close() 
	# print li # debug 

@coroutine
def Writer(ofile):
	try:
		#Check if ofile exists, if so, remove it first NEWLY ADDED 
		if os.path.isfile(ofile):
			os.remove(ofile) 
		f = open(ofile,'ab') 
		while True: 
			idata = (yield)
			assert isinstance(idata, list) # type check. consumes a list 
			assert len(idata) % 8 == 0 # optional: ensure byte-alignment 
			# print 'PRINTOUT: \n',idata #debug 
			
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
	
# ============== deal with non-alignment reading, i.e. the read bits are not multiple of 8 bit =====

def NA_Reader(file, chunksize, next_coroutine):
	""" 
	read non-aligned codewords into a huge list and send one code each time as list down the piple  
	in: chunksize: the #bits read at a time. may not be 8x 
	out: send the read codeword list to next coroutine 
	
	"""
	f = open(file,'rb') 
	a = bitarray() 
	a.fromfile(f)
	f.close() 
	ptr = 0
	ptr_end = a.length() 
	while ptr < ptr_end and ptr + chunksize <= ptr_end: # prevent boundary overflow below 
		 
		code_list = map(int, a[ptr:ptr+chunksize].to01() )
		print 'code chunk: ', code_list #debug  
		next_coroutine.send(code_list) 
		ptr += chunksize
	if ptr < ptr_end: 
		#send the last bit of odd end down the pipe, padding zeros 
		oddend_list = map(int, a[ptr:].to01()) + [0]*(chunksize - ptr_end + ptr) # filling trailing 0s
		next_coroutine.send(oddend_list)

@coroutine
def NA_Writer(ofile):
	"similiar to NA_Reader; consumes non-aligned codeword and aggregate to a huge list then write file"
	try:
		if os.path.isfile(ofile):  # NEWLY ADDED: check if file exist
			os.remove(ofile)
		f = open(ofile,'ab')
		a = bitarray()
		while True:
			chunk = (yield) 
			assert isinstance(chunk, list) 
			a.extend(chunk) 
		
	except GeneratorExit:
		a.tofile(f) # write the huge bitarray to file with zero padding at the rear end 
		f.close() 
		print '=== FILE WRITTEN ===' 
		

#****   RE-INTERLEAVE THE RED. AND DATA. FILE INTO A ENCODED FILE ***  NEWLY ADDED 
#PENDING 
def Interleave(dfile,rfile,k,r,outname='encfile'):
	""" 
	re-interleave the data and red. file into a normal interleaved encoded file 
	in: dfile(datafile),rfile(redundancy bits file),k(wordsize),r(number of parity)
	out: a interleaved join of data and redundancy-bits file. a encoded file 
	"""
	assert isinstance(dfile,str) and isinstance(rfile,str) 
	# initialize bitarray to store data file and redundancy file 
	data_bita = bitarray()   
	red_bita = bitarray()
	# read from file , store content in a big bitarray  
 	df = open(dfile,'rb') 
 	data_bita.fromfile(df)
 	# print 'show df content' #DEBUG
 	# print data_bita.to01() #DEBUG

 	data_list = map(int, data_bita.to01() )  
 	df.close() 

 	rf = open(rfile,'rb') 
 	red_bita.fromfile(rf)
 	# print 'show rf content' #DEBUG
 	# print red_bita.to01() #DEBUG 
 	red_list = map(int, red_bita.to01()) 
 	rf.close() 
 	# out list 
 	out_list=[]
 	#iterator of data bitarray
 	pd = 0 
 	pd_end = data_bita.length() 
 	pr = 0 
 	assert data_bita.length() % k ==0  # check data alignment 
 	#iterator of red. bitarray
 	while pd<pd_end:
 		codeword_list = data_list[pd:pd+k] + red_list[pr:pr+r] # each time extract k,r bits from data and red and join 
 		out_list += codeword_list 
 		pd += k 
 		pr += r 

 	out_bita = bitarray(out_list) 
 	print 'show out_list content \n', out_bita.to01()  #DEBUG 
 	outf = open(outname,'wb') # overwrite encfile 
 	out_bita.tofile(outf)
 	outf.close() 















# =============================== END OF NON-ALIGNMENT TERMINAL SIDE HELPERS =====================
# ////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
		



# ///////////////////// ENCODERS ////////////////////////////////////
# //////////////////////////////////////////////////////////////////


#CLEAR 
@coroutine
def HamEncoder(wdsize, next_coroutine,redonly=False):
	""" 
	Hamming encoder 
	in: wdsize and take a list
	out: a encoded vector (list)
	redonly: store redundancy bits in a separate file and only output the redundancy file. 
	"""
	r = wd2mTable[wdsize] + 1 # number of parity incl. overall parity. SECDED 
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
		 	# send a np array to next, added a redonly option; NEW MODIFICATION 
		 	if redonly:  
		 		next_coroutine.send(enc_list[-r:]) 
		 	else:
		 		next_coroutine.send(enc_list)  
	 	# enc = list(enc)  #  for writing bin files. 
	except GeneratorExit:
		next_coroutine.close() 
	# except AssertionError:
	# 	print 'ASSERTION ERROR! msg length=',len(msg)
# =========================================BCH ENCODER =======================
@coroutine
def BCHencoder(wdsize, next_coroutine,redonly=False):
	""" 
	in: wdsize, take (yield) as a list 
	out: a encoded list of bits 
	redonly: optional redundancy only file output 
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
			if redonly:
				next_coroutine.send(enc_list[-2*m:])  # only send the redundancy bits, 2m of them 
			else: 
				next_coroutine.send(enc_list) 
	except GeneratorExit:
		next_coroutine.close()
	# except AssertionError:
	# 	print 'ASSERTION ERROR! msg length =',len(msg)  




		






# ========================================// DECODER //===========================================
# Tentative clear : 3-err detection nemesis
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

		

# CLEAR 
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
 				next_coroutine.send(corr_vec[:wdsize]) 
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





# -----------ENCODER ALL-IN-ONE WRAPPER --------------
# ----------------------------------------------------

def mainENC(ifile,ofile,ecctype,wdsize):
	"encoder wrapper all-in-one testbench"
	enc_dict = {'bch':BCHencoder, 'ham': HamEncoder}
	assert isinstance(ecctype, str) and ecctype in enc_dict.keys() 

	Reader(ifile, wdsize, enc_dict[ecctype](wdsize, NA_Writer(ofile)) )



## *****  Only output redundancy-bits file **** 
def mainENC2(ifile,ofile,ecctype,wdsize):
	"encoder wrapper , using separate data and red. storage files" 
	enc_dict = {'bch':BCHencoder, 'ham': HamEncoder}
	assert isinstance(ecctype, str) and ecctype in enc_dict.keys() 

	Reader(ifile, wdsize, enc_dict[ecctype](wdsize, NA_Writer(ofile),True) )

# ----------------- DECODER ALL-IN-ONE WRAPPER ---------
# ------------------------------------------------------

def mainDEC(ifile,ofile,ecctype,wdsize):
 	"decoder all-in-one wrapper testbench" 

 	dec_dict = {'bch':BCHdecoder, 'ham':HamDecoder} 
 	assert ecctype in dec_dict.keys() 
 	m = wd2mTable[wdsize] 
 	overhead_dict = {'bch':2*m, 'ham':m+1}  

 	blocklen = wdsize + overhead_dict[ecctype] # get codeword length 

 	NA_Reader( ifile, blocklen, dec_dict[ecctype](wdsize, Writer(ofile) ) ) 




def mainDEC2(dfile,rfile,ofile,ecctype,wdsize):
	"decoder wrapper alternative. using separate data and red. files and re-interleave the two "
	dec_dict = {'bch':BCHdecoder, 'ham':HamDecoder} 
 	assert ecctype in dec_dict.keys() 
 	m = wd2mTable[wdsize] 
 	overhead_dict = {'bch':2*m, 'ham':m+1}  
 	r= overhead_dict[ecctype]

 	blocklen = wdsize + r # get codeword length 

 	Interleave(dfile,rfile,wdsize,r) # re-interleave data and red. file 

 	NA_Reader( 'encfile', blocklen, dec_dict[ecctype](wdsize, Writer(ofile) ) )

















# TO BE REFINED  
import getopt 
 
def main():
	""" 
	-----------------Testbench User Guide----------------------
	This is a testbench for BCH/SECDED enc/dec test via command-line options/args 
	3 modes of test: 
	------------------------
	'whole' [default mode] : 
		all-in-one test. binary file Reader-->Encoder(BCH/HAM) --> ErrorGen(Vdd) --> Decoder(BCH/Ham) -->Writer(outfile)
		under 'whole', vdd is default to 0.8V. please specify by -v0.7 for example 

	'enc': encoder mode. provide the option -e/--enc. Reader-->Encode-->NA_Writer must provide I/O filename and wordsize 
	'dec': decoder mode. provide the option -d/--dec  NA_Reader --> Decode --> Writer 
	---------------------
	OPTIONS 
	--------------------
	-s : separate mode. encoder only output parity file. decoder takes 2 files, data and parity file and re-interleave 
	-p: in separate mode [-s], followed by parity file that feeds into the decoder along with data file . ONLY WORKS WITH -s turned on 
	-i/--ifile : Input filename. eg. -ifoo (reads file 'foo') set to 'bin' by default 
	-o/--ofile : Output filename . similiar to ifile in usage set to 'printout' by default 
	-h/-b: ECCtype BCH/SECDED(Hamming) set to 'h' [hamming] by default 
	-w/--wdsize: word width. choose among (16,32,64,128,256) ; set to 16 by default 
	-e/-d | --enc/--dec : mode select [dec/enc] . 'whole' by default if not specified 

	**WARNING**
	when -s and -d are both ON, decoder needs both data file (ifile) and parity file (-p:) provided by -p option. SO -p MUST BE ON ALSO!!
	-----------------------
	Example Use: 
	-----------------------
	./testbench -ibin -oausgang -w32 -v0.7 -b  
	whole pipeline test under vdd=0.7, wordwidth=32, file-to-read = 'bin', file-to-write='ausgang' , ECCtype = BCH 
	./testbench -ibin -oausgang -w64 -b -e (encoder mode ) 
	
	"""








	encmap = {'bch': BCHencoder, 'ham': HamEncoder}
	decmap = {'bch': BCHdecoder, 'ham': HamDecoder}
	
	# ============PARSE command line arguments ============================
	try:
		# opts, remainder = getopt.getopt(sys.argv[1:],"i:o:bhw:edv:",['infile=','outfile=','bch', 'ham','wdsize=','enc','dec']) 
		opts, remainder = getopt.getopt(sys.argv[1:],"i:p:so:bhw:edv:",['infile=','outfile=','bch', 'ham','wdsize=','enc','dec']) #NEWLY ADDED
	except getopt.GetoptError as err:
		print str(err) 
		print "provide arguments : -i(--infile) -o(--ofile) -s(separate mode) -p(parity file input) \
		\n -h/-b [choose ecc hamming/bch] -w(--wdsize) wordwidth -e/-d [enc/dec] whole-test by default" 
		print main.__doc__

		sys.exit(2) 
	# set defaults 
	ofile = 'out_default'
	ifile = 'bin' 
	ecctype = 'ham' 
	wdsize = 16 
	mode = 'whole'
	alternate_mode = False 
	vdd = 0.8 
	parity_f = 'out_default'
	print opts # debug 
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
		elif option in ('-e','--enc'):
			mode = 'enc' 
		elif option in ('-d','--dec'):
			mode = 'dec' 
		elif option in ('-v',):
			vdd = float(arg)
		elif option in ('-s',):
			alternate_mode = True 
		elif option in ('-p',):
			parity_f = arg 


		else:
			assert False, 'unhandled option' 
	# ==============================================END OF Arg parser ===================
	try:

		if mode == 'whole':
			Reader(ifile, wdsize, encmap[ecctype](wdsize, ErrorGen(vdd, decmap[ecctype](wdsize,Writer(ofile)) ))) 
		elif mode == 'enc':
			if alternate_mode: # alternate mode ON 
				mainENC2(ifile,ofile,ecctype,wdsize)
			else: # alternate mode OFF 
				mainENC( ifile, ofile, ecctype, wdsize) 
		elif mode == 'dec':
			if alternate_mode:
				mainDEC2(ifile,parity_f,ofile,ecctype,wdsize)
			else:
				mainDEC( ifile, ofile, ecctype, wdsize) 
		else:
			raise ValueError
	except ValueError:
		print 'mode must be enc/dec or whole' 




if __name__ == '__main__':
	main() 
	


		





	





		


