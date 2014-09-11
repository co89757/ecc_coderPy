
// ENCODER TESTBENCH OF crc8
module crc8_64_enc_tb;

//------ INPUT PORTS -----
reg clk_drv ;
reg rst_n ;
reg [0:63] DATA_IN; 
wire [0:71] CODE_OUT; 
wire VALID_OUT; 
reg EN ; 
reg active;

// ---- instantiate the UUT ----

crc8_64_enc u_crc8_64_enc(
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
# 10 DATA_IN = 64'hb4705b94; active = 1; // enc:5a382dca7a
# 10 DATA_IN = 64'hb35ae135; //enc: 59ad709afa 
# 10 DATA_IN = 64'hf4631f09;  // enc 7a318f84e9
# 10 DATA_IN = 64'h5f9254db; //enc 2fc92a6dfb

# 10 DATA_IN = 64'ha9056227; //enc 5482b113cc
# 10 DATA_IN = 64'h51d04972; // enc 28e824b907
# 10 DATA_IN = 64'h601f993b; active=0; //en 300fcc9dab

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

		 
