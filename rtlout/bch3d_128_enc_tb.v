
		// ENCODER TESTBENCH OF bch3d
		module bch3d_128_enc_tb;

		//------ INPUT PORTS -----
		reg clk_drv ;
		reg rst_n ;
		reg [0:127] DATA_IN; 
		wire [0:144] CODE_OUT; 
		wire VALID_OUT; 
		reg EN ; 

		// ---- instantiate the UUT ----

		bch3d_128_enc UUT(
			.clk(clk_drv),
			.reset_n(rst_n),
			.enable(EN),
			.i_data(DATA_IN),
			.o_code(CODE_OUT),
			.o_valid(VALID_OUT)
			);
		 
		 
		initial 
			clk_drv = 1'b0; // set drive clock to 0 

		always 
			#5 clk_drv = ~clk_drv;  //clock period = 10ns

		initial begin  //provide DATA_IN 
		DATA_IN = 0  ; 
		# 10 DATA_IN = 128'hb4705b94; // enc:5a382dca7a
		# 10 DATA_IN = 128'hb35ae135; //enc: 59ad709afa 
		# 10 DATA_IN = 128'hf4631f09;  // enc 7a318f84e9
		# 10 DATA_IN = 128'h5f9254db; //enc 2fc92a6dfb

		# 10 DATA_IN = 128'ha9056227; //enc 5482b113cc
		# 10 DATA_IN = 128'h51d04972; // enc 28e824b907
		# 10 DATA_IN = 128'h601f993b; //en 300fcc9dab

		end 

		initial begin  // ENABLE control 
		EN = 1'b1 ;
		# 110 EN = ~EN ;  
		end 

		initial begin 
		rst_n = 0 ; 

		# 5 rst_n = 1 ; 

		end 

		initial 
		# 120 $finish ;  

		initial 
		$monitor($time, " code_out = %b", CODE_OUT) ;

		endmodule 

		 
