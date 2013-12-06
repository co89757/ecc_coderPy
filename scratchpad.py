




def enc(inword):
	assert isinstance(inword, list) and len(inword)==8
	p = [0]*5 
	inword_r = inword[::-1] # reverse so it becomes [7:0] inword_r 
	p[0] = inword_r[6] ^ inword_r[4] ^ inword_r[3] ^ inword_r[1] ^ inword_r[0] 
	p[1] = inword_r[6] ^ inword_r[5] ^ inword_r[3] ^ inword_r[2] ^ inword_r[0]
	p[2]= inword_r[7] ^ inword_r[3] ^ inword_r[2] ^ inword_r[1] 
	p[3]= inword_r[7] ^ inword_r[6] ^ inword_r[5] ^ inword_r[4] 
	p[4]= inword_r[7] ^ inword_r[5] ^ inword_r[4] ^ inword_r[2] ^ inword_r[1] ^ inword_r[0] 

	return (inword + p ) 


def main():
	word_array = [[0,1,1,0,0,1,1,1],[0,0,0,1,0,1,1,0],[0,0,0,0,1,1,1,1],[1,0,1,1,1,0,0,0],[0,1,1,1,0,0,0,0],
	[1,1,1,1,0,1,1,1],[0,0,1,1,0,1,1,1]] 
	for word in word_array:
		print 'in_word: ', word 
		cw = enc(word)
		cw_str = ''.join(map(str,cw))  
		print 'databits: ', cw_str[:8], 'checkbits: ', cw_str[8:] 
		print '--------' 





# ============================ Verilog Code Generator ================================

import sys,os
p=os.getcwd() ; sys.path.append(p) 

from toyhamm import p16,p32,p64,p128,p256 



import numpy as np

op = lambda p: np.array( [int(not(sum(row) % 2)) for row in p] ) 

P16 = np.column_stack( (p16,op(p16)) ) 
P32 = np.column_stack( (p32,op(p32)) ) 
P64 = np.column_stack( (p64,op(p64)) ) 
P128 = np.column_stack( (p128,op(p128)) ) 
P256 = np.column_stack( (p256,op(p256)) )  

N16 = np.transpose(P16) 
N32 = np.transpose(P32) 
N64 = np.transpose(P64) 
N128 = np.transpose(P128) 
N256 = np.transpose(P256) # name matrices. rxn 

# [0:k-1] data_in , [0:r-1] par 

wd2N = {16:N16, 32:N32, 64:N64, 128:N128, 256:N256}

def paritygen(wdsize):
	"code Generator for parity generation" 
	NameMat = wd2N[wdsize]  # get name matrix (rxn)
	# f = open('paritygen_code.txt','w') # file IO 
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



	# f.close() #file IO 


def hamenc_codegen(wdsize):
	"Verilog code Generator for SECDED encoder" 
	k2rmap={16:6,32:7,64:8,128:9,256:10}
	r = k2rmap[wdsize] # number of checkbits 
	n = r + wdsize # block length 
	f = open('henc_code.txt','w') 
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
	input [0:{dLSBid}] i_data;

	//----OUTPUT PORTS----
	output [0:{codeLSBid}] o_code;
	output o_valid;

	//---INTERNAL SIGNALS --
	reg [0:{dLSBid}] datareg ; // OPTIONAL  input register 
	reg o_valid;
	reg [0:{codeLSBid}] o_code;

	// reg enreg; 
	wire [0:{ckLSBid}] par ;//parity (check bits) 
	""".format(wdwidth=wdsize, dLSBid=wdsize-1, codeLSBid=n-1, ckLSBid=r-1) 

	print >>f, header 

	paritygen_text = paritygen(wdsize)

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
			o_code <= {datareg,par}; 
			o_valid <= 1 ;
		end
	//
	//	else 
	//		o_valid <= 0 ;  // disable and not reset --> output invalid , o_code remains unchanged 
				
		
	end




	endmodule 
	//---- end of file -----//  
	 """ 

	print >>f, tail 

	f.close() 


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

k2pmap= {16:P16, 32:P32, 64:P64, 128:P128, 256:P256}

def syndsolve(wdsize):
	"syndrome decoding code generation"
	k2rmap={16:6,32:7,64:8,128:9,256:10} 
	# NameMat = wd2N[wdsize]
	

	P = k2pmap[wdsize] # get the full parity matrix <kxr>   
	r = k2rmap[wdsize] 
	finals = '' 
	s1='assign noerr = '
	for i in xrange(r):
		ss = '~synd[{0}] & '.format(i) if i !=r-1 else '~synd[{0}];'.format(i) 
		s1 += ss 

	s1 += '\n' 

	finals += s1 

	neg = lambda x: '~' if x==0 else '' 

	s2 = ''

	for idx, name in enumerate(P):
		flip_s = 'assign flip[{0}] = '.format(idx) 
		for i, n in enumerate(name):
			subs = '{sign}synd[{index}] & '.format(sign= neg(n), index = i) if i != r-1 else '{sign}synd[{index}];'.format(sign=neg(n), index=i) 
			flip_s += subs 
		s2 = s2 + flip_s + '\n' 


	finals += s2 

	return finals 		

def hamdec_codegen(wdsize):
	k2rmap={16:6,32:7,64:8,128:9,256:10}
	r = k2rmap[wdsize] # number of checkbits 
	n = r + wdsize # block length 
	f = open('hdec_code.txt','w')

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
			o_err_fatal <= ~synpar & ~noerr; // has error AND syndrome has even parity. 2 err or more 
			o_valid <= 1 ; 
			
		end
	end



	endmodule 
	//--------- end of file ------//

	 """.format(Wtopid=wdsize-1, Ptopid=r-1) 

	print >>f, tail 

	f.close() 





if __name__ == '__main__':
	main() 