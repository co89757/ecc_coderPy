 
	module crc7_32_enc(
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
	input [0:31] i_data;

	//----OUTPUT PORTS----
	output [0:38] o_code;
	output o_valid;

	//---INTERNAL SIGNALS --
	reg [0:31] datareg ; // OPTIONAL  input register 
	reg o_valid;
	reg [0:38] o_code;

	// reg enreg; 
	wire [0:6] par ;//parity (check bits) 
	
assign par[0] = datareg[0] ^ datareg[1] ^ datareg[2] ^ datareg[3] ^ datareg[4] ^ datareg[6] ^ datareg[7] ^ datareg[8] ^ datareg[9] ^ datareg[12] ^ datareg[13] ^ datareg[14] ^ datareg[16] ^ datareg[18] ^ datareg[19] ^ datareg[24] ^ datareg[26] ^ datareg[27] ^ datareg[28];
assign par[1] = datareg[1] ^ datareg[2] ^ datareg[3] ^ datareg[4] ^ datareg[5] ^ datareg[7] ^ datareg[8] ^ datareg[9] ^ datareg[10] ^ datareg[13] ^ datareg[14] ^ datareg[15] ^ datareg[17] ^ datareg[19] ^ datareg[20] ^ datareg[25] ^ datareg[27] ^ datareg[28] ^ datareg[29];
assign par[2] = datareg[0] ^ datareg[1] ^ datareg[5] ^ datareg[7] ^ datareg[10] ^ datareg[11] ^ datareg[12] ^ datareg[13] ^ datareg[15] ^ datareg[19] ^ datareg[20] ^ datareg[21] ^ datareg[24] ^ datareg[27] ^ datareg[29] ^ datareg[30];
assign par[3] = datareg[1] ^ datareg[2] ^ datareg[6] ^ datareg[8] ^ datareg[11] ^ datareg[12] ^ datareg[13] ^ datareg[14] ^ datareg[16] ^ datareg[20] ^ datareg[21] ^ datareg[22] ^ datareg[25] ^ datareg[28] ^ datareg[30] ^ datareg[31];
assign par[4] = datareg[2] ^ datareg[3] ^ datareg[7] ^ datareg[9] ^ datareg[12] ^ datareg[13] ^ datareg[14] ^ datareg[15] ^ datareg[17] ^ datareg[21] ^ datareg[22] ^ datareg[23] ^ datareg[26] ^ datareg[29] ^ datareg[31];
assign par[5] = datareg[3] ^ datareg[4] ^ datareg[8] ^ datareg[10] ^ datareg[13] ^ datareg[14] ^ datareg[15] ^ datareg[16] ^ datareg[18] ^ datareg[22] ^ datareg[23] ^ datareg[24] ^ datareg[27] ^ datareg[30];
assign par[6] = datareg[0] ^ datareg[1] ^ datareg[2] ^ datareg[3] ^ datareg[5] ^ datareg[6] ^ datareg[7] ^ datareg[8] ^ datareg[11] ^ datareg[12] ^ datareg[13] ^ datareg[15] ^ datareg[17] ^ datareg[18] ^ datareg[23] ^ datareg[25] ^ datareg[26] ^ datareg[27] ^ datareg[31];



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
	 
