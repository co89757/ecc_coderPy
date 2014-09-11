 
		//---- TESTBENCH OF bch3d_DEC ----// 


		module bch3d_64_dec_tb ;

		//------ SIGNALS -----
		reg clk_drv ;
		reg rst_n ;
		wire [0:63] DATA_OUT; 
		reg [0:78] CODE_IN; 
		wire VALID_OUT; 
		reg EN ;  
		wire ERR_DET;
		wire ERR_CORR;
		wire ERR_FATAL;


		//------INSTANTIATE MODULE  -----
		bch3d_64_dec UUT(
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
		initial 
			clk_drv = 1'b0; // set drive clock to 0 

		always 
			#5 clk_drv = ~clk_drv;  //clock period = 2x5=10ns


		initial begin  // ENABLE control 
		EN = 1'b1 ;
		# 110 EN = ~EN ;  
		end 

		initial begin 
		rst_n = 0 ; 

		# 5 rst_n = 1 ; 

		end 

		//--- DATA DRIVER ------//

		initial begin

		CODE_IN = 0; // no err 
		# 10 CODE_IN = 79'h1000; // 1 err 
		# 10 CODE_IN = 79'h50000; // 2e 
		# 10 CODE_IN = 79'h80000; // 1 err   
		# 10 CODE_IN = 79'h1; // 1e, for appending bits, it is the parity err 
		# 10 CODE_IN = 79'ha000; // 2e 
		# 10 CODE_IN = 79'hb0000;  // 3err  

		end 


		//------- SYSTEM TASKS ----// 
		initial 
		$monitor($time, " data_out = %b ", DATA_OUT) ; 




		initial 
		# 120 $finish ;  


		endmodule 
	    // --- end of file ---

		
