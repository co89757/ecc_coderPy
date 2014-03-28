# Description: generic testbench verilog code generator 

def encodertb(ecc,k,n):
	"encoder testbench template . ecc: ECC type, k: in_data width "

	fname = '{ecctype}_{wsize}_enc_tb.v'.format(ecctype=ecc,wsize=k) 
	with open(fname,'w') as f:

		text = """
// ENCODER TESTBENCH OF {ecctype}
module {ecctype}_{wsize}_enc_tb;

//------ INPUT PORTS -----
reg clk_drv ;
reg rst_n ;
reg [0:{wtopid}] DATA_IN; 
wire [0:{ctopid}] CODE_OUT; 
wire VALID_OUT; 
reg EN ; 
reg active;

// ---- instantiate the UUT ----

{ecctype}_{wsize}_enc u_{ecctype}_{wsize}_enc(
	.clk(clk_drv),
	.reset_n(rst_n),
	.enable(EN),
	.i_data(DATA_IN),
	.o_code(CODE_OUT),
	.o_valid(VALID_OUT)
	);
 
 
initial begin
	clk_drv = 1'b0; // set drive clock to 0 
	active=0; // init active signal 
end 
always 
	#5 clk_drv = ~clk_drv;  //clock period = 10ns

initial begin  //provide DATA_IN 
DATA_IN = 0  ; 
# 10 DATA_IN = {wsize}'hb4705b94; active = 1; // enc:5a382dca7a
# 10 DATA_IN = {wsize}'hb35ae135; //enc: 59ad709afa 
# 10 DATA_IN = {wsize}'hf4631f09;  // enc 7a318f84e9
# 10 DATA_IN = {wsize}'h5f9254db; //enc 2fc92a6dfb

# 10 DATA_IN = {wsize}'ha9056227; //enc 5482b113cc
# 10 DATA_IN = {wsize}'h51d04972; // enc 28e824b907
# 10 DATA_IN = {wsize}'h601f993b; active=0; //en 300fcc9dab

end 

initial begin  // ENABLE control 
EN = 1'b1 ;
//# 110 EN = ~EN ;  
end 

initial begin 
rst_n = 0 ; 

# 7 rst_n = 1 ; 

end 

initial 
# 14000 $finish ;  

initial 
$monitor($time, " code_out = %b", CODE_OUT) ;

endmodule 

		 """.format(ecctype=ecc,wsize=k,wtopid=k-1, ctopid=n-1)

		print >>f, text 

	# return text 




def decodertb(ecctype,k,n):
	"generic decoder testbench template for word-width k and code length n "

	fname = '{0}_{1}_dec_tb.v'.format(ecctype,k) 
	with open(fname,'w') as f:
		text = """ 
//---- TESTBENCH OF {ECC}_DEC ----// 


module {ECC}_{wsize}_dec_tb ;

//------ SIGNALS -----
reg clk_drv ;
reg rst_n ;
wire [0:{wtopid}] DATA_OUT; 
reg [0:{ctopid}] CODE_IN; 
wire VALID_OUT; 
reg EN ;  
wire ERR_DET;
wire ERR_CORR;
wire ERR_FATAL;
reg active;

//------INSTANTIATE MODULE  -----
{ECC}_{wsize}_dec u_{ECC}_{wsize}_dec (
	.clk(clk_drv),
	.reset_n(rst_n),
	.enable(EN),
	.i_code(CODE_IN),
	.o_data(DATA_OUT),
	.o_valid(VALID_OUT),
	.o_err_corr(ERR_CORR),
	.o_err_detec(ERR_DET),
	.o_err_fatal(ERR_FATAL) 


	);

//-------- CLOCKING SETUP -----// 
initial begin
	clk_drv = 1'b0; // set drive clock to 0 
	active = 0; // init active signal 
end 

always 
	#5 clk_drv = ~clk_drv;  //clock period = 2x5=10ns


initial begin  // ENABLE control 
EN = 1'b1 ;
//# 110 EN = ~EN ;  
end 

initial begin 
rst_n = 0 ; 

# 7 rst_n = 1 ; 

end 

//--- DATA DRIVER ------//

initial begin

CODE_IN = 0; // no err 
# 10 CODE_IN = {codelen}'h1000; active=1; // 1 err 
# 10 CODE_IN = {codelen}'h50000; // 2e 
# 10 CODE_IN = {codelen}'h80000; // 1 err   
# 10 CODE_IN = {codelen}'h1; // 1e, for appending bits, it is the parity err 
# 10 CODE_IN = {codelen}'ha000; // 2e 
# 10 CODE_IN = {codelen}'hb0000;  active=0;// 3err  

end 


//------- SYSTEM TASKS ----// 
initial 
$monitor($time, " data_out = %b ", DATA_OUT) ; 




initial 
# 14000 $finish ;  


endmodule 
// --- end of file ---

		""".format(ECC=ecctype, wsize=k, wtopid=k-1, ctopid=n-1, codelen=n ) 
		print >>f , text 

	# return text 




if __name__ == '__main__':
	encodertb('crc8',64,72)
	encodertb('crc9',128,137)

	decodertb('crc8',64,72)
	decodertb('crc9',128,137)











































 