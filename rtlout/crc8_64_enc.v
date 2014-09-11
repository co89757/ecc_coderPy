 
	module crc8_64_enc(
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
	input [0:63] i_data;

	//----OUTPUT PORTS----
	output [0:71] o_code;
	output o_valid;

	//---INTERNAL SIGNALS --
	reg [0:63] datareg ; // OPTIONAL  input register 
	reg o_valid;
	reg [0:71] o_code;

	// reg enreg; 
	wire [0:7] par ;//parity (check bits) 
	
assign par[0] = datareg[0] ^ datareg[1] ^ datareg[2] ^ datareg[3] ^ datareg[7] ^ datareg[12] ^ datareg[13] ^ datareg[15] ^ datareg[18] ^ datareg[19] ^ datareg[21] ^ datareg[22] ^ datareg[24] ^ datareg[25] ^ datareg[26] ^ datareg[27] ^ datareg[28] ^ datareg[29] ^ datareg[31] ^ datareg[32] ^ datareg[33] ^ datareg[35] ^ datareg[36] ^ datareg[39] ^ datareg[40] ^ datareg[41] ^ datareg[43] ^ datareg[47] ^ datareg[49] ^ datareg[52] ^ datareg[55] ^ datareg[56] ^ datareg[57] ^ datareg[58] ^ datareg[59] ^ datareg[62] ^ datareg[63];
assign par[1] = datareg[0] ^ datareg[4] ^ datareg[7] ^ datareg[8] ^ datareg[12] ^ datareg[14] ^ datareg[15] ^ datareg[16] ^ datareg[18] ^ datareg[20] ^ datareg[21] ^ datareg[23] ^ datareg[24] ^ datareg[30] ^ datareg[31] ^ datareg[34] ^ datareg[35] ^ datareg[37] ^ datareg[39] ^ datareg[42] ^ datareg[43] ^ datareg[44] ^ datareg[47] ^ datareg[48] ^ datareg[49] ^ datareg[50] ^ datareg[52] ^ datareg[53] ^ datareg[55] ^ datareg[60] ^ datareg[62];
assign par[2] = datareg[1] ^ datareg[5] ^ datareg[8] ^ datareg[9] ^ datareg[13] ^ datareg[15] ^ datareg[16] ^ datareg[17] ^ datareg[19] ^ datareg[21] ^ datareg[22] ^ datareg[24] ^ datareg[25] ^ datareg[31] ^ datareg[32] ^ datareg[35] ^ datareg[36] ^ datareg[38] ^ datareg[40] ^ datareg[43] ^ datareg[44] ^ datareg[45] ^ datareg[48] ^ datareg[49] ^ datareg[50] ^ datareg[51] ^ datareg[53] ^ datareg[54] ^ datareg[56] ^ datareg[61] ^ datareg[63];
assign par[3] = datareg[0] ^ datareg[1] ^ datareg[3] ^ datareg[6] ^ datareg[7] ^ datareg[9] ^ datareg[10] ^ datareg[12] ^ datareg[13] ^ datareg[14] ^ datareg[15] ^ datareg[16] ^ datareg[17] ^ datareg[19] ^ datareg[20] ^ datareg[21] ^ datareg[23] ^ datareg[24] ^ datareg[27] ^ datareg[28] ^ datareg[29] ^ datareg[31] ^ datareg[35] ^ datareg[37] ^ datareg[40] ^ datareg[43] ^ datareg[44] ^ datareg[45] ^ datareg[46] ^ datareg[47] ^ datareg[50] ^ datareg[51] ^ datareg[54] ^ datareg[56] ^ datareg[58] ^ datareg[59] ^ datareg[63];
assign par[4] = datareg[0] ^ datareg[3] ^ datareg[4] ^ datareg[8] ^ datareg[10] ^ datareg[11] ^ datareg[12] ^ datareg[14] ^ datareg[16] ^ datareg[17] ^ datareg[19] ^ datareg[20] ^ datareg[26] ^ datareg[27] ^ datareg[30] ^ datareg[31] ^ datareg[33] ^ datareg[35] ^ datareg[38] ^ datareg[39] ^ datareg[40] ^ datareg[43] ^ datareg[44] ^ datareg[45] ^ datareg[46] ^ datareg[48] ^ datareg[49] ^ datareg[51] ^ datareg[56] ^ datareg[58] ^ datareg[60] ^ datareg[62] ^ datareg[63];
assign par[5] = datareg[1] ^ datareg[4] ^ datareg[5] ^ datareg[9] ^ datareg[11] ^ datareg[12] ^ datareg[13] ^ datareg[15] ^ datareg[17] ^ datareg[18] ^ datareg[20] ^ datareg[21] ^ datareg[27] ^ datareg[28] ^ datareg[31] ^ datareg[32] ^ datareg[34] ^ datareg[36] ^ datareg[39] ^ datareg[40] ^ datareg[41] ^ datareg[44] ^ datareg[45] ^ datareg[46] ^ datareg[47] ^ datareg[49] ^ datareg[50] ^ datareg[52] ^ datareg[57] ^ datareg[59] ^ datareg[61] ^ datareg[63];
assign par[6] = datareg[2] ^ datareg[5] ^ datareg[6] ^ datareg[10] ^ datareg[12] ^ datareg[13] ^ datareg[14] ^ datareg[16] ^ datareg[18] ^ datareg[19] ^ datareg[21] ^ datareg[22] ^ datareg[28] ^ datareg[29] ^ datareg[32] ^ datareg[33] ^ datareg[35] ^ datareg[37] ^ datareg[40] ^ datareg[41] ^ datareg[42] ^ datareg[45] ^ datareg[46] ^ datareg[47] ^ datareg[48] ^ datareg[50] ^ datareg[51] ^ datareg[53] ^ datareg[58] ^ datareg[60] ^ datareg[62];
assign par[7] = datareg[0] ^ datareg[1] ^ datareg[2] ^ datareg[6] ^ datareg[11] ^ datareg[12] ^ datareg[14] ^ datareg[17] ^ datareg[18] ^ datareg[20] ^ datareg[21] ^ datareg[23] ^ datareg[24] ^ datareg[25] ^ datareg[26] ^ datareg[27] ^ datareg[28] ^ datareg[30] ^ datareg[31] ^ datareg[32] ^ datareg[34] ^ datareg[35] ^ datareg[38] ^ datareg[39] ^ datareg[40] ^ datareg[42] ^ datareg[46] ^ datareg[48] ^ datareg[51] ^ datareg[54] ^ datareg[55] ^ datareg[56] ^ datareg[57] ^ datareg[58] ^ datareg[61] ^ datareg[62];



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
	 
