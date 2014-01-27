#Description: code generator for normal SECDED (extented Hamming) 

# ========= HEADER =======
import sys,os,math 
p=os.getcwd() ; sys.path.append(p) 

from toyhamm import p16,p32,p64,p128,p256 
import numpy as np 




# ===== HELPER VARIABLE =====
op = lambda p: np.array( [int(not(sum(row) % 2)) for row in p] ) # overall parity column generator 

P16 = np.column_stack( (p16,op(p16)) ) 
P32 = np.column_stack( (p32,op(p32)) ) 
P64 = np.column_stack( (p64,op(p64)) ) 
P128 = np.column_stack( (p128,op(p128)) ) 
P256 = np.column_stack( (p256,op(p256)) )  # parity matrix, kxr G=[I,P], N = P' 

N16 = np.transpose(P16) 
N32 = np.transpose(P32) 
N64 = np.transpose(P64) 
N128 = np.transpose(P128) 
N256 = np.transpose(P256) # name matrices. rxk H=[N,I] 

wd2N = {16:N16, 32:N32, 64:N64, 128:N128, 256:N256} # wordsize to name-matrix mapping 


# ================== ENCODER HELPER FUNCTIONS =====================
# Parity generation 
def HamParityGen(wdsize):
	"code Generator for parity generation" 
	NameMat = wd2N[wdsize]  # get name matrix (rxn)
	# f = open('HamParityGen_code.txt','w') # file IO 
	result_s = ''  #string return 
	for rowid,row in enumerate(NameMat):
		s = 'assign par[{0}] = '.format(rowid) 
		incl_d_index = np.nonzero(row) 
		incl_d_index = incl_d_index[0].astype('int') # get a array of included databit indices 
		for i in incl_d_index:
			ss = 'datareg[{0}] ^ '.format(i) if i != incl_d_index[-1] else 'datareg[{0}];'.format(i) 
			s += ss 
		# print >>f, s  #file IO
		s += '\n' # string return

		result_s += s #string return 

	return result_s #string return 


# IGNORE PARITY ERRORS Hamming-------------------------
def ignore(r):
    "generate flag for ignore parity err "
    reduced_sum_width = int(math.floor(math.log(r,2)) ) + 1 
    line1="wire [{topid}:0] sbitsum = ".format(topid=reduced_sum_width-1)  
    for i in xrange(r):
        item = "synd[{0}] + ".format(i) if i < r-1 else 'synd[{0}];\n'.format(i) 
        line1 += item 

    line2 = "wire ignore = (sbitsum==1)? 1:0; \n" 

    return (line1+line2)




# ===================== ENCODER GENERATOR ==================================
# ==========================================================================

def HamEncoderGen(wdsize):
	"Verilog code Generator for normal SECDED encoder, APPENDING paritybits" 
	m = int(math.ceil(math.log(wdsize, 2)) ) + 1 # DEBUG  
	r = m+1 
	n = r + wdsize # block length 
	f = open('secded_{0}_enc.v'.format(wdsize),'w') 
	header = """ 
	module secded_{wdwidth}_enc(
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
	wire [0:{Ptopid}] par ;//parity (check bits) 
	""".format(wdwidth=wdsize, Wtopid=wdsize-1, Ctopid=n-1, Ptopid=r-1) 

	print >>f, header 

	HamParityGen_text = HamParityGen(wdsize)

	print >>f, HamParityGen_text   

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
			o_code <= {datareg,par}; 
			//Appending parity 
			o_valid <= 1 ;
		end 
				
		
	end




	endmodule 
	//---- end of file -----//  
	 """ 

	print >>f, tail 

	f.close() 





# =================== HAMMING SECDED DECODER HELPER FUNCTIONS ========================


#Hamming Code Syndrome generator 
def syndgen(wdsize):
	NameMat = wd2N[wdsize] 
	result_s = ''  #string return 
	for rowid,row in enumerate(NameMat):
		s = 'assign synd[{0}] = chk[{0}] ^ '.format(rowid) 
		incl_d_index = np.nonzero(row) 
		incl_d_index = incl_d_index[0].astype('int') # get a array of included databit indices 
		for i in incl_d_index:
			ss = 'data[{0}] ^ '.format(i) if i != incl_d_index[-1] else 'data[{0}];'.format(i) 
			s += ss 
		# print >>f, s  #file IO
		s += '\n' # string return

		result_s += s #string return 

	return result_s #string return 

#Word_width to Parity matrix LUT 
k2pmap= {16:P16, 32:P32, 64:P64, 128:P128, 256:P256}



#Hamming Code Syndrome Solver
def syndsolve(wdsize):
	"SECDED Hamming syndrome decoding code generation"
	m = int(math.ceil(math.log(wdsize, 2)) ) + 1 # DEBUG  
	r = m+1 
	P = k2pmap[wdsize] # get the full parity matrix <kxr>   
	 
	finals = '' 
	s1='assign noerr = '
	for i in xrange(r):
		ss = '~synd[{0}] & '.format(i) if i !=r-1 else '~synd[{0}];'.format(i) 
		s1 += ss 

	s1 += '\n' 

	finals += s1 

	neg = lambda x: '~' if x==0 else '' # sign assignment 

	s2 = ''

	for idx, name in enumerate(P):
		flip_s = 'assign flip[{0}] = '.format(idx) 
		for i, n in enumerate(name):
			subs = '{sign}synd[{index}] & '.format(sign= neg(n), index = i) if \
			i != r-1 else '{sign}synd[{index}];'.format(sign=neg(n), index=i) 
			flip_s += subs 
		s2 = s2 + flip_s + '\n' 


	finals += s2 

	return finals 	





# ================ HAMMING SECDED DECODER GENERATOR ============================
# ==============================================================================

def HamDecoderGen(wdsize):
	m = int(math.ceil(math.log(wdsize, 2)) ) + 1 # DEBUG  
	r = m+1
	n = r + wdsize # block length 
	f = open('secded_{0}_dec.v'.format(wdsize),'w')

	head = """ 
	module secded_{Wsize}_dec (
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
	wire synpar;
	wire [0:{Wtopid}] corr_word; 


	wire [0:{Ptopid}] synd ; 
	wire [0:{Wtopid}] flip ; // databits error mask 
	reg [0:{Wtopid}] o_data; 
	wire[0:{Ptopid}] chk = codereg[{Pstartid}:{Pstopid}]; //extract the checkbits 

	wire [0:{Wtopid}] data = codereg[0:{Wtopid}] ; //extract databits

	//---STATEMENTS 
	 
	

	""".format(Wsize=wdsize, Ctopid=n-1, Wtopid=wdsize-1, Ptopid=r-1, Pstartid=wdsize, Pstopid=n-1) 


	print >>f, head 
	

	print >>f, "//--------- Syndrome Generation -------//"

	print >>f, syndgen(wdsize) 

	print >>f, "//--------- Syndrome Decoding ----------//"

	print >>f, syndsolve(wdsize) 

	tail = """
	assign synpar = ^synd[0:{Ptopid}];  // syndrome's parity 

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
			o_err_fatal <= ~synpar & ~noerr ; // has error AND syndrome has even parity. 2 err or more 
			o_valid <= 1 ; 
			
		end
	end



	endmodule 
	//--------- end of file ------//

	 """.format(Wtopid=wdsize-1, Ptopid=r-1) # DOES CONVENTIONAL SECDED NEED IGNORE FLAG?? does even parity syndrome 

	print >>f, tail 

	f.close() 














# ================ MAIN FUNCTION =============================

def SECDEDcode(k):
	HamEncoderGen(k)
	HamDecoderGen(k) 

if __name__ == '__main__':
	k = int(raw_input("word size = ")) 
	SECDEDcode(k)