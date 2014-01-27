# DECTED BCH Verilog Code Generator based on additional parity 
# Authro:Colin 
# Built on Jan 24, 2014
# Description:
# 	-> Use **Prepending** encoding , based on combinational BCH TED 
# 	-> Code (c0,c1,c2,...c_n-1) = c0 + c1x + c2x^2 + ... 
# 	-> based on DEC BCH. but add additional all-0 column and all-1 row to H matrix to make a new extended H matrix
# 	-> The bulk of the code is based on bch2 code Generator 










# headers 


import sys,os,math 
p=os.getcwd() ; sys.path.append(p) 
import bch3d as bch3 
import numpy as np

#============================== Helper Modules ===================================================


# =================== ENCODER HELPERS =================================
# BCH DECTED check bits generation [Encoder Component]
def BCH3dParGen(k):
	"k = word width, BCH 3D check bits generation parity equations "
	m = int(math.ceil(math.log(k, 2)) ) + 1 # GF(2^m) 
	r = 2*m+1 # number of checkbits 
	nameMatx = bch3.genMatrix(k) 
	nameMatx = nameMatx[:,:r].transpose()  # a numpy array
	result_s = '' 
	for rowid,row in enumerate(nameMatx):
		s = 'assign par[{0}] = '.format(rowid) 
		incl_d_index = np.nonzero(row) 
		incl_d_index = incl_d_index[0].astype('int') # get a array of included databit indices 
		for i in incl_d_index:
			ss = 'datareg[{0}] ^ '.format(i) if i != incl_d_index[-1] else 'datareg[{0}];'.format(i) 
			s += ss 
		# print >>f, s  #file IO
		s += '\n' # string return

		result_s += s #string return 

	# with open('bch3d_enc.txt','w') as f:
	# 	print >>f , result_s 



	return result_s #string return 


# =================== DECODER HELPERS ==========
# syndrome computation BCH DECTED
def BCH3dSyndGen(k):
	" generate code for syndrome bit generation using s=rxHT " 
	H = bch3.checkMatrix(k) 
	result_s = '' 
	for rowid,row in enumerate(H):
		s = 'assign synd[{0}] = '.format(rowid) 
		one_bit_index = np.nonzero(row)[0].astype('int') # a array of set-bit indices of each H row 
		for i in one_bit_index:
			ss = 'codereg[{0}] ^ '.format(i) if i != one_bit_index[-1] else 'codereg[{0}];'.format(i) 
			s += ss 
		s += '\n' 

		result_s += s 

	# with open('bch3d_syndgen.txt','w') as f:
	# 	print >>f, result_s 
	return result_s  

# mapping from syndrome pattern to error bits BCH TED 
def BCH3dSynd2Err(k):
	"syndrome to flip pattern mapping code generator for 3D BCH " 
	maptable = bch3.err2SyndMapping(k) 
	m = int(math.ceil(math.log(k, 2)) ) + 1 # GF(2^m) 
	r = 2*m + 1 # number of checkbits for DECTED  
	neg = lambda x: '~' if x == 0 else ''
	result_s  = '' 
	noerr_line='assign noerr = '
	for i in xrange(r):
		ss = '~synd[{0}] & '.format(i) if i !=r-1 else '~synd[{0}];'.format(i) 
		noerr_line += ss 

	noerr_line += '\n' 
	result_s += noerr_line 
	for i in xrange(k): # iterate across all dataflip bits INDEX PROBLEM!! DATABIS starts at (r)-th position !!  
		line = 'assign flip[{0}] = '.format(i) 
		syndpatlist = maptable[i] # syndrome pattern mapped to flip[i] 
		for subpatid, subpat in enumerate(syndpatlist): # iterate across subpatterns that comprise synpat 
			ss = '' # for a synd pattern-match 
			for bitind, synbit in enumerate(subpat):
				# sss for individual syndrome bits 
				sss = '{sign}synd[{index}] & '.format(sign = neg(synbit), index = bitind) if \
				bitind != r-1 else '{sign}synd[{index}]'.format(sign = neg(synbit), index = bitind)
				ss += sss 
			ss = '(' + ss + ')|' if subpatid != len(syndpatlist)-1 else '(' + ss+ ');' # a synd-pattern match (S_vec) 

			line += ss 
		line += '\n' 
		result_s += line 


	# with open('bch3d_syndsolve.txt','w') as f:
	# 	print >>f, result_s 

	return result_s #return text generated 



# IGNORE errors in parity =============

def BCHignoreFlag(k):
	"generate ignore flag as ignore = ... (pattern list)" 
	m = int(math.ceil(math.log(k, 2)) ) + 1 # GF(2^m) 
	r = 2*m + 1 # number of checkbits for DECTED 
	sign = lambda x: '~' if x == 0 else ''  # sign indicator 

	result_s = 'wire ignore = '

	ignorelist = bch3.BCH3dignore(k) # ignore-syndrome list [[..],[..],..] 

	for patid,pat in enumerate(ignorelist):
		ss = ''
		for bitid,synbit in enumerate(pat):
			sss = '{sign}synd[{index}] & '.format(sign = sign(synbit), index = bitid) if \
				bitid != r-1 else '{sign}synd[{index}]'.format(sign = sign(synbit), index = bitid)
			ss += sss 
		ss = '(' + ss + ')|' if patid != len(ignorelist)-1 else '(' + ss+ ');' # a synd-pattern match (S_vec)

		result_s += ss 
	result_s += '\n' 

	return result_s 













# =================== OK, WRAPPING UP IN A ENCODER GENERATOR FOR BCH 3D ===============

def BCH3dEncoderGen(k):
	"BCH3D encoder verilog code generator for word width = k "
	m = int(math.ceil(math.log(k, 2)) ) + 1 # GF(2^m) 
	r = 2*m + 1 # number of checkbits for DECTED   
	n = k+r 
	f = open('bch3d_{0}_enc.v'.format(k),'w') 
	header = """ 
	module bch3d_{Wsize}_enc(
	clk,
	reset_n,
	enable,
	i_data,
	o_code,
	o_valid
	);

	//--- INPUT PORTS ---
	input clk;
	input reset_n;
	input enable;
	input [0:{Wtopid}] i_data;

	//----OUTPUT PORTS----
	output [0:{Ctopid}] o_code;
	output o_valid;

	//---INTERNAL SIGNALS --
	reg [0:{Wtopid}] datareg ; // OPTIONAL  input register 
	reg o_valid;
	reg [0:{Ctopid}] o_code;

	// reg enreg; 
	wire [0:{chkTopid}] par ;//parity (check bits) 
	""".format(Wsize=k, Wtopid=k-1, Ctopid=n-1,chkTopid=r-1)  

	print >>f, header 

	paritygen_text = BCH3dParGen(k) 

	print >>f, paritygen_text   

	tail = """

		//------ GET INPUT ----
	//---------------------------

	always @(posedge clk or negedge reset_n) begin
		if (~reset_n) 
			datareg <= 0 ;

		else if (enable) 
			datareg <= i_data;
		
	end

	//--------Code is generated 1 cycle after input is registered 
	//----------------------------------------------

	always @(posedge clk or negedge reset_n) begin
		if (~reset_n) begin
			o_code  <= 0;
			o_valid <= 0;
		end	
		else if (enable) begin 
			o_code <= {par,datareg}; 
			o_valid <= 1 ;
		end
	 
				
		
	end




	endmodule 
	//---- end of file -----//  
	 """ 

	print >>f, tail 

	f.close() 


# =================== BCH 3D DECODER CODE GENERATOR =====================
def BCH3dDecoderGen(k):
	"BCH DECTED Decoder code generator for wsize=k"
	m = int(math.ceil(math.log(k, 2)) ) + 1 # GF(2^m) 
	r = 2*m + 1 # number of checkbits 
	fname = 'bch3d_{0}_dec.v'.format(k)  
	f = open(fname,'w')
	n = r + k 
	head = """ 
	module bch3d_{Wsize}_dec (
	clk,
	reset_n,
	enable,
	i_code,
	o_data,
	o_valid,
	o_err_corr,
	o_err_detec,
	o_err_fatal

	);

	//------ INPUT PORTS -----
	input clk ;
	input reset_n;
	input enable;
	input [0:{Ctopid}] i_code;


	//------OUTPUT PORTS -----
	output [0:{Wtopid}] o_data;
	output o_valid;
	output o_err_corr;
	output o_err_detec;
	output o_err_fatal;

	//---- INTERNAL VARIABLES ---

	reg [0:{Ctopid}] codereg ;
	reg o_err_fatal;
	reg o_err_detec;
	reg o_err_corr;
	reg o_valid;
	wire noerr; 
	wire [0:{Wtopid}] corr_word; 


	wire [0:{Ptopid}] synd ; 
	wire [0:{Wtopid}] flip ; // databits error mask 
	reg [0:{Wtopid}] o_data; 
	wire [0:{Wtopid}] data = codereg[{Nparity}:{Ctopid}] ; //extract databits 
	

	//---STATEMENTS 
	 


	""".format(Wsize=k,Ctopid=n-1,Wtopid=k-1,Ptopid=r-1, Nparity=r)  

	print >>f, head 

	print >>f, "//----------Syndrome Generation-------------//"

	print >>f, BCH3dSyndGen(k) 

	print >>f, "//----------Syndrome Decoding----------------//"

	print >>f, BCH3dSynd2Err(k) 
	print >>f, BCHignoreFlag(k) # NEW: add IGNORE flag to ignore error-in-parity 

	tail = """

	

	assign corr_word = data[0:{Wtopid}] ^ flip[0:{Wtopid}]; 


	////////// REGISTER INPUT CODEWORD ////////////////

	always @(posedge clk or negedge reset_n) begin
		if (!reset_n) 
			// reset
			codereg <= 0 ;
		
		else if (enable)  
			codereg <= i_code; 
		 
	end

	//////////// GET OUTPUT ////////////////////////
	always @(posedge clk or negedge reset_n) begin
		if (!reset_n) begin
			// reset
			o_data <= 0;
			o_valid <= 0; 
			o_err_detec <=0;
			o_err_corr <= 0;
			o_err_fatal <= 0;
		end
		else if (enable) begin

			o_data <= corr_word ;
			o_err_detec <= ~noerr ;
			o_err_corr <= | flip[0:{Wtopid}] ; // found one name match 
			o_err_fatal <= ~(|flip) & ~noerr & ~ignore; // has error AND syndrome has even parity. 2 err or more 
			o_valid <= 1 ; 
			
		end
	end



	endmodule 
	//--------- end of file ------//



	 """.format(Wtopid=k-1)

	print >>f, tail 

	f.close() 







# ================ MAIN FUNCTION ===============================================
def bch3dCodeGen(k):
	"one-stop encoder-decoder verilog file generation for BCH 3D"
	BCH3dEncoderGen(k)
	BCH3dDecoderGen(k) 



if __name__ == '__main__':

	k = int(raw_input("BCH DECTED ECC code for word width k= "))
	bch3dCodeGen(k)
