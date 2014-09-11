 
	module secded_128_enc(
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
	input [0:127] i_data;

	//----OUTPUT PORTS----
	output [0:136] o_code;
	output o_valid;

	//---INTERNAL SIGNALS --
	reg [0:127] datareg ; // OPTIONAL  input register 
	reg o_valid;
	reg [0:136] o_code;

	// reg enreg; 
	wire [0:8] par ;//parity (check bits) 
	
assign par[0] = datareg[0] ^ datareg[4] ^ datareg[5] ^ datareg[6] ^ datareg[10] ^ datareg[13] ^ datareg[15] ^ datareg[16] ^ datareg[17] ^ datareg[24] ^ datareg[25] ^ datareg[28] ^ datareg[31] ^ datareg[34] ^ datareg[35] ^ datareg[37] ^ datareg[38] ^ datareg[39] ^ datareg[42] ^ datareg[48] ^ datareg[50] ^ datareg[52] ^ datareg[53] ^ datareg[55] ^ datareg[56] ^ datareg[58] ^ datareg[60] ^ datareg[61] ^ datareg[64] ^ datareg[66] ^ datareg[67] ^ datareg[72] ^ datareg[73] ^ datareg[74] ^ datareg[75] ^ datareg[76] ^ datareg[78] ^ datareg[79] ^ datareg[81] ^ datareg[82] ^ datareg[83] ^ datareg[84] ^ datareg[86] ^ datareg[88] ^ datareg[89] ^ datareg[90] ^ datareg[92] ^ datareg[96] ^ datareg[101] ^ datareg[102] ^ datareg[104] ^ datareg[105] ^ datareg[109] ^ datareg[110] ^ datareg[111] ^ datareg[112] ^ datareg[115] ^ datareg[116] ^ datareg[117] ^ datareg[120] ^ datareg[121] ^ datareg[125] ^ datareg[127];
assign par[1] = datareg[1] ^ datareg[5] ^ datareg[6] ^ datareg[7] ^ datareg[11] ^ datareg[14] ^ datareg[16] ^ datareg[17] ^ datareg[18] ^ datareg[25] ^ datareg[26] ^ datareg[29] ^ datareg[32] ^ datareg[35] ^ datareg[36] ^ datareg[38] ^ datareg[39] ^ datareg[40] ^ datareg[43] ^ datareg[49] ^ datareg[51] ^ datareg[53] ^ datareg[54] ^ datareg[56] ^ datareg[57] ^ datareg[59] ^ datareg[61] ^ datareg[62] ^ datareg[65] ^ datareg[67] ^ datareg[68] ^ datareg[73] ^ datareg[74] ^ datareg[75] ^ datareg[76] ^ datareg[77] ^ datareg[79] ^ datareg[80] ^ datareg[82] ^ datareg[83] ^ datareg[84] ^ datareg[85] ^ datareg[87] ^ datareg[89] ^ datareg[90] ^ datareg[91] ^ datareg[93] ^ datareg[97] ^ datareg[102] ^ datareg[103] ^ datareg[105] ^ datareg[106] ^ datareg[110] ^ datareg[111] ^ datareg[112] ^ datareg[113] ^ datareg[116] ^ datareg[117] ^ datareg[118] ^ datareg[121] ^ datareg[122] ^ datareg[126];
assign par[2] = datareg[0] ^ datareg[2] ^ datareg[4] ^ datareg[5] ^ datareg[7] ^ datareg[8] ^ datareg[10] ^ datareg[12] ^ datareg[13] ^ datareg[16] ^ datareg[18] ^ datareg[19] ^ datareg[24] ^ datareg[25] ^ datareg[26] ^ datareg[27] ^ datareg[28] ^ datareg[30] ^ datareg[31] ^ datareg[33] ^ datareg[34] ^ datareg[35] ^ datareg[36] ^ datareg[38] ^ datareg[40] ^ datareg[41] ^ datareg[42] ^ datareg[44] ^ datareg[48] ^ datareg[53] ^ datareg[54] ^ datareg[56] ^ datareg[57] ^ datareg[61] ^ datareg[62] ^ datareg[63] ^ datareg[64] ^ datareg[67] ^ datareg[68] ^ datareg[69] ^ datareg[72] ^ datareg[73] ^ datareg[77] ^ datareg[79] ^ datareg[80] ^ datareg[82] ^ datareg[85] ^ datareg[89] ^ datareg[91] ^ datareg[94] ^ datareg[96] ^ datareg[98] ^ datareg[101] ^ datareg[102] ^ datareg[103] ^ datareg[105] ^ datareg[106] ^ datareg[107] ^ datareg[109] ^ datareg[110] ^ datareg[113] ^ datareg[114] ^ datareg[115] ^ datareg[116] ^ datareg[118] ^ datareg[119] ^ datareg[120] ^ datareg[121] ^ datareg[122] ^ datareg[123] ^ datareg[125];
assign par[3] = datareg[0] ^ datareg[1] ^ datareg[3] ^ datareg[4] ^ datareg[8] ^ datareg[9] ^ datareg[10] ^ datareg[11] ^ datareg[14] ^ datareg[15] ^ datareg[16] ^ datareg[19] ^ datareg[20] ^ datareg[24] ^ datareg[26] ^ datareg[27] ^ datareg[29] ^ datareg[32] ^ datareg[36] ^ datareg[38] ^ datareg[41] ^ datareg[43] ^ datareg[45] ^ datareg[48] ^ datareg[49] ^ datareg[50] ^ datareg[52] ^ datareg[53] ^ datareg[54] ^ datareg[56] ^ datareg[57] ^ datareg[60] ^ datareg[61] ^ datareg[62] ^ datareg[63] ^ datareg[65] ^ datareg[66] ^ datareg[67] ^ datareg[68] ^ datareg[69] ^ datareg[70] ^ datareg[72] ^ datareg[75] ^ datareg[76] ^ datareg[79] ^ datareg[80] ^ datareg[82] ^ datareg[84] ^ datareg[88] ^ datareg[89] ^ datareg[95] ^ datareg[96] ^ datareg[97] ^ datareg[99] ^ datareg[101] ^ datareg[103] ^ datareg[105] ^ datareg[106] ^ datareg[107] ^ datareg[108] ^ datareg[109] ^ datareg[112] ^ datareg[114] ^ datareg[119] ^ datareg[122] ^ datareg[123] ^ datareg[124] ^ datareg[125] ^ datareg[126] ^ datareg[127];
assign par[4] = datareg[0] ^ datareg[1] ^ datareg[2] ^ datareg[6] ^ datareg[9] ^ datareg[11] ^ datareg[12] ^ datareg[13] ^ datareg[20] ^ datareg[21] ^ datareg[24] ^ datareg[27] ^ datareg[30] ^ datareg[31] ^ datareg[33] ^ datareg[34] ^ datareg[35] ^ datareg[38] ^ datareg[44] ^ datareg[46] ^ datareg[48] ^ datareg[49] ^ datareg[51] ^ datareg[52] ^ datareg[54] ^ datareg[56] ^ datareg[57] ^ datareg[60] ^ datareg[62] ^ datareg[63] ^ datareg[68] ^ datareg[69] ^ datareg[70] ^ datareg[71] ^ datareg[72] ^ datareg[74] ^ datareg[75] ^ datareg[77] ^ datareg[78] ^ datareg[79] ^ datareg[80] ^ datareg[82] ^ datareg[84] ^ datareg[85] ^ datareg[86] ^ datareg[88] ^ datareg[92] ^ datareg[97] ^ datareg[98] ^ datareg[100] ^ datareg[101] ^ datareg[105] ^ datareg[106] ^ datareg[107] ^ datareg[108] ^ datareg[111] ^ datareg[112] ^ datareg[113] ^ datareg[116] ^ datareg[117] ^ datareg[121] ^ datareg[123] ^ datareg[124] ^ datareg[126];
assign par[5] = datareg[1] ^ datareg[2] ^ datareg[3] ^ datareg[7] ^ datareg[10] ^ datareg[12] ^ datareg[13] ^ datareg[14] ^ datareg[21] ^ datareg[22] ^ datareg[25] ^ datareg[28] ^ datareg[31] ^ datareg[32] ^ datareg[34] ^ datareg[35] ^ datareg[36] ^ datareg[39] ^ datareg[45] ^ datareg[47] ^ datareg[49] ^ datareg[50] ^ datareg[52] ^ datareg[53] ^ datareg[55] ^ datareg[57] ^ datareg[58] ^ datareg[61] ^ datareg[63] ^ datareg[64] ^ datareg[69] ^ datareg[70] ^ datareg[71] ^ datareg[72] ^ datareg[73] ^ datareg[75] ^ datareg[76] ^ datareg[78] ^ datareg[79] ^ datareg[80] ^ datareg[81] ^ datareg[83] ^ datareg[85] ^ datareg[86] ^ datareg[87] ^ datareg[89] ^ datareg[93] ^ datareg[98] ^ datareg[99] ^ datareg[101] ^ datareg[102] ^ datareg[106] ^ datareg[107] ^ datareg[108] ^ datareg[109] ^ datareg[112] ^ datareg[113] ^ datareg[114] ^ datareg[117] ^ datareg[118] ^ datareg[122] ^ datareg[124] ^ datareg[125] ^ datareg[127];
assign par[6] = datareg[2] ^ datareg[3] ^ datareg[4] ^ datareg[8] ^ datareg[11] ^ datareg[13] ^ datareg[14] ^ datareg[15] ^ datareg[22] ^ datareg[23] ^ datareg[26] ^ datareg[29] ^ datareg[32] ^ datareg[33] ^ datareg[35] ^ datareg[36] ^ datareg[37] ^ datareg[40] ^ datareg[46] ^ datareg[48] ^ datareg[50] ^ datareg[51] ^ datareg[53] ^ datareg[54] ^ datareg[56] ^ datareg[58] ^ datareg[59] ^ datareg[62] ^ datareg[64] ^ datareg[65] ^ datareg[70] ^ datareg[71] ^ datareg[72] ^ datareg[73] ^ datareg[74] ^ datareg[76] ^ datareg[77] ^ datareg[79] ^ datareg[80] ^ datareg[81] ^ datareg[82] ^ datareg[84] ^ datareg[86] ^ datareg[87] ^ datareg[88] ^ datareg[90] ^ datareg[94] ^ datareg[99] ^ datareg[100] ^ datareg[102] ^ datareg[103] ^ datareg[107] ^ datareg[108] ^ datareg[109] ^ datareg[110] ^ datareg[113] ^ datareg[114] ^ datareg[115] ^ datareg[118] ^ datareg[119] ^ datareg[123] ^ datareg[125] ^ datareg[126];
assign par[7] = datareg[3] ^ datareg[4] ^ datareg[5] ^ datareg[9] ^ datareg[12] ^ datareg[14] ^ datareg[15] ^ datareg[16] ^ datareg[23] ^ datareg[24] ^ datareg[27] ^ datareg[30] ^ datareg[33] ^ datareg[34] ^ datareg[36] ^ datareg[37] ^ datareg[38] ^ datareg[41] ^ datareg[47] ^ datareg[49] ^ datareg[51] ^ datareg[52] ^ datareg[54] ^ datareg[55] ^ datareg[57] ^ datareg[59] ^ datareg[60] ^ datareg[63] ^ datareg[65] ^ datareg[66] ^ datareg[71] ^ datareg[72] ^ datareg[73] ^ datareg[74] ^ datareg[75] ^ datareg[77] ^ datareg[78] ^ datareg[80] ^ datareg[81] ^ datareg[82] ^ datareg[83] ^ datareg[85] ^ datareg[87] ^ datareg[88] ^ datareg[89] ^ datareg[91] ^ datareg[95] ^ datareg[100] ^ datareg[101] ^ datareg[103] ^ datareg[104] ^ datareg[108] ^ datareg[109] ^ datareg[110] ^ datareg[111] ^ datareg[114] ^ datareg[115] ^ datareg[116] ^ datareg[119] ^ datareg[120] ^ datareg[124] ^ datareg[126] ^ datareg[127];
assign par[8] = datareg[0] ^ datareg[1] ^ datareg[2] ^ datareg[3] ^ datareg[5] ^ datareg[10] ^ datareg[11] ^ datareg[12] ^ datareg[15] ^ datareg[17] ^ datareg[18] ^ datareg[19] ^ datareg[20] ^ datareg[21] ^ datareg[22] ^ datareg[23] ^ datareg[25] ^ datareg[26] ^ datareg[27] ^ datareg[31] ^ datareg[32] ^ datareg[33] ^ datareg[35] ^ datareg[36] ^ datareg[38] ^ datareg[42] ^ datareg[43] ^ datareg[44] ^ datareg[45] ^ datareg[46] ^ datareg[47] ^ datareg[50] ^ datareg[51] ^ datareg[53] ^ datareg[54] ^ datareg[56] ^ datareg[57] ^ datareg[60] ^ datareg[64] ^ datareg[65] ^ datareg[67] ^ datareg[68] ^ datareg[69] ^ datareg[70] ^ datareg[71] ^ datareg[73] ^ datareg[75] ^ datareg[78] ^ datareg[81] ^ datareg[83] ^ datareg[86] ^ datareg[87] ^ datareg[89] ^ datareg[92] ^ datareg[93] ^ datareg[94] ^ datareg[95] ^ datareg[101] ^ datareg[104] ^ datareg[109] ^ datareg[111] ^ datareg[115] ^ datareg[117] ^ datareg[118] ^ datareg[119] ^ datareg[121] ^ datareg[122] ^ datareg[123] ^ datareg[124] ^ datareg[127];



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
	 
