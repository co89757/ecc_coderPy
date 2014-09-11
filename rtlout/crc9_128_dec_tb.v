 
//---- TESTBENCH OF crc9_DEC ----// 


module crc9_128_dec_tb ;

//------ SIGNALS -----
reg clk_drv ;
reg rst_n ;
wire [0:127] DATA_OUT; 
reg [0:136] CODE_IN; 
wire VALID_OUT; 
reg EN ;  
wire HASERR;
reg active;

//------INSTANTIATE MODULE  -----
crc9_128_dec u_crc9_128_dec (
	.clk(clk_drv),
	.reset_n(rst_n),
	.enable(EN),
	.i_code(CODE_IN),
	.o_data(DATA_OUT),
	.o_valid(VALID_OUT),
	.o_haserr(HASERR) 


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
# 10 CODE_IN = 137'h1000; active=1; // 1 err 
# 10 CODE_IN = 137'h50000; // 2e 
# 10 CODE_IN = 137'h80000; // 1 err   
# 10 CODE_IN = 137'h1; // 1e, for appending bits, it is the parity err 
# 10 CODE_IN = 137'ha000; // 2e 
# 10 CODE_IN = 137'hb0000;  active=0;// 3err  

end 


//------- SYSTEM TASKS ----// 
initial 
$monitor($time, " data_out = %b ", DATA_OUT) ; 




initial 
# 14000 $finish ;  


endmodule 
// --- end of file ---

		
