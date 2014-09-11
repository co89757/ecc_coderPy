#### CRC-5+1   HW module code writer ####
### Encoded word :  (op,p1,p2,..p5,c0,c1,..c32) op: overall parity. CRC-5 prepends 5 bits , and then CRC-1 prepends an additional bit

import sys,os 
p=os.getcwd() ; sys.path.append(p) 

import crc 
import numpy as np 



# ##=========================== CRC Encoder Section ====================================

def CRCParGen(r,k):
	"k = word width, of generation parity equations "

	
	nameMatx = crc.crcGenMatrix(r,k)
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




# =================== CRC Decoder Helper ===================

# syndrome computation BCH DECTED
def CRCSyndGen(r,k):
	" generate code for syndrome bit generation using s=rxHT " 
	H = crc.crcCheckMatrix(r,k) 
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



# ##====================================================================================
# ##===============================   CRC Encoder Writer ===================

def CRCEncoderGen(r,k):
	"Composite CRC-r encoder verilog code generator for word width = k "
	n = k+r 
	f = open('crc{0}_{1}_enc.v'.format(r,k),'w') 
	header = """ 
	module crc{_r}_{Wsize}_enc(
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
	""".format(Wsize=k, Wtopid=k-1, Ctopid=n-1,chkTopid=r-1, _r = r)  

	print >>f, header 

	paritygen_text =  CRCParGen(r,k) 

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
			// prepending check bits 
			o_valid <= 1 ;
		end
	 
				
		
	end




	endmodule 
	//---- end of file -----//  
	 """ 

	print >>f, tail 

	f.close() 




### =================== Composite CRC Decoder writer ===============

def CRCDecoderGen(r,k):
	

	fname = 'crc{0}_{1}_dec.v'.format(r,k)  
	f = open(fname,'w')
	n = r + k 
	head = """ 
	//  CRC decoder 
	module crc{Nparity}_{Wsize}_dec (
	clk,
	reset_n,
	enable,
	i_code,
	o_data,
	o_valid,
	o_haserr

	);

	//------ INPUT PORTS -----
	input clk ;
	input reset_n;
	input enable;
	input [0:{Ctopid}] i_code;


	//------OUTPUT PORTS -----
	output [0:{Wtopid}] o_data;
	output o_valid;
	output o_haserr;

	//---- INTERNAL VARIABLES ---

	reg [0:{Ctopid}] codereg ;
	reg o_haserr;
	reg o_valid;
	 
	 


	wire [0:{Ptopid}] synd ; 
	 
	reg [0:{Wtopid}] o_data; 
	wire [0:{Wtopid}] data = codereg[{Nparity}:{Ctopid}] ; //extract databits 
	

	//---STATEMENTS 
	 


	""".format(Wsize=k,Ctopid=n-1,Wtopid=k-1,Ptopid=r-1, Nparity=r)  

	print >>f, head 

	print >>f, "//----------Syndrome Generation-------------//"

	print >>f, CRCSyndGen(r,k)

	tail = """

	
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
			o_haserr <= 0; 
		end
		else if (enable) begin

			o_data <= data ;
			o_haserr <= | synd ; // non-zero syndrome sets the error alarm 
			 
			o_valid <= 1 ; 
			
		end
	end



	endmodule 
	//--------- end of file ------//

	""" 

	print >>f, tail 
	f.close() 


def main(r,k):
	CRCEncoderGen(r,k) 
	CRCDecoderGen(r,k) 


if __name__ == '__main__':
	# r = 7 ; k = 32 
	# main(r,k)
	r=8; k = 64 
	main(r,k)
	r2=9; k2=128 
	main(r2,k2) 