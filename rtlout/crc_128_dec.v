 
	// Composite CRC-r decoder 
	module crc_128_dec (
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
	input [0:133] i_code;


	//------OUTPUT PORTS -----
	output [0:127] o_data;
	output o_valid;
	output o_haserr;

	//---- INTERNAL VARIABLES ---

	reg [0:133] codereg ;
	reg o_haserr;
	reg o_valid;
	 
	 


	wire [0:5] synd ; 
	 
	reg [0:127] o_data; 
	wire [0:127] data = codereg[6:133] ; //extract databits 
	

	//---STATEMENTS 
	 


	
//----------Syndrome Generation-------------//
assign synd[0] = codereg[0] ^ codereg[6] ^ codereg[7] ^ codereg[10] ^ codereg[12] ^ codereg[13] ^ codereg[15] ^ codereg[16] ^ codereg[17] ^ codereg[18] ^ codereg[20] ^ codereg[22] ^ codereg[26] ^ codereg[29] ^ codereg[30] ^ codereg[31] ^ codereg[37] ^ codereg[38] ^ codereg[41] ^ codereg[43] ^ codereg[44] ^ codereg[46] ^ codereg[47] ^ codereg[48] ^ codereg[49] ^ codereg[51] ^ codereg[53] ^ codereg[57] ^ codereg[60] ^ codereg[61] ^ codereg[62] ^ codereg[68] ^ codereg[69] ^ codereg[72] ^ codereg[74] ^ codereg[75] ^ codereg[77] ^ codereg[78] ^ codereg[79] ^ codereg[80] ^ codereg[82] ^ codereg[84] ^ codereg[88] ^ codereg[91] ^ codereg[92] ^ codereg[93] ^ codereg[99] ^ codereg[100] ^ codereg[103] ^ codereg[105] ^ codereg[106] ^ codereg[108] ^ codereg[109] ^ codereg[110] ^ codereg[111] ^ codereg[113] ^ codereg[115] ^ codereg[119] ^ codereg[122] ^ codereg[123] ^ codereg[124] ^ codereg[130] ^ codereg[131];
assign synd[1] = codereg[1] ^ codereg[6] ^ codereg[8] ^ codereg[10] ^ codereg[11] ^ codereg[12] ^ codereg[14] ^ codereg[15] ^ codereg[19] ^ codereg[20] ^ codereg[21] ^ codereg[22] ^ codereg[23] ^ codereg[26] ^ codereg[27] ^ codereg[29] ^ codereg[32] ^ codereg[37] ^ codereg[39] ^ codereg[41] ^ codereg[42] ^ codereg[43] ^ codereg[45] ^ codereg[46] ^ codereg[50] ^ codereg[51] ^ codereg[52] ^ codereg[53] ^ codereg[54] ^ codereg[57] ^ codereg[58] ^ codereg[60] ^ codereg[63] ^ codereg[68] ^ codereg[70] ^ codereg[72] ^ codereg[73] ^ codereg[74] ^ codereg[76] ^ codereg[77] ^ codereg[81] ^ codereg[82] ^ codereg[83] ^ codereg[84] ^ codereg[85] ^ codereg[88] ^ codereg[89] ^ codereg[91] ^ codereg[94] ^ codereg[99] ^ codereg[101] ^ codereg[103] ^ codereg[104] ^ codereg[105] ^ codereg[107] ^ codereg[108] ^ codereg[112] ^ codereg[113] ^ codereg[114] ^ codereg[115] ^ codereg[116] ^ codereg[119] ^ codereg[120] ^ codereg[122] ^ codereg[125] ^ codereg[130] ^ codereg[132];
assign synd[2] = codereg[2] ^ codereg[7] ^ codereg[9] ^ codereg[11] ^ codereg[12] ^ codereg[13] ^ codereg[15] ^ codereg[16] ^ codereg[20] ^ codereg[21] ^ codereg[22] ^ codereg[23] ^ codereg[24] ^ codereg[27] ^ codereg[28] ^ codereg[30] ^ codereg[33] ^ codereg[38] ^ codereg[40] ^ codereg[42] ^ codereg[43] ^ codereg[44] ^ codereg[46] ^ codereg[47] ^ codereg[51] ^ codereg[52] ^ codereg[53] ^ codereg[54] ^ codereg[55] ^ codereg[58] ^ codereg[59] ^ codereg[61] ^ codereg[64] ^ codereg[69] ^ codereg[71] ^ codereg[73] ^ codereg[74] ^ codereg[75] ^ codereg[77] ^ codereg[78] ^ codereg[82] ^ codereg[83] ^ codereg[84] ^ codereg[85] ^ codereg[86] ^ codereg[89] ^ codereg[90] ^ codereg[92] ^ codereg[95] ^ codereg[100] ^ codereg[102] ^ codereg[104] ^ codereg[105] ^ codereg[106] ^ codereg[108] ^ codereg[109] ^ codereg[113] ^ codereg[114] ^ codereg[115] ^ codereg[116] ^ codereg[117] ^ codereg[120] ^ codereg[121] ^ codereg[123] ^ codereg[126] ^ codereg[131] ^ codereg[133];
assign synd[3] = codereg[3] ^ codereg[8] ^ codereg[10] ^ codereg[12] ^ codereg[13] ^ codereg[14] ^ codereg[16] ^ codereg[17] ^ codereg[21] ^ codereg[22] ^ codereg[23] ^ codereg[24] ^ codereg[25] ^ codereg[28] ^ codereg[29] ^ codereg[31] ^ codereg[34] ^ codereg[39] ^ codereg[41] ^ codereg[43] ^ codereg[44] ^ codereg[45] ^ codereg[47] ^ codereg[48] ^ codereg[52] ^ codereg[53] ^ codereg[54] ^ codereg[55] ^ codereg[56] ^ codereg[59] ^ codereg[60] ^ codereg[62] ^ codereg[65] ^ codereg[70] ^ codereg[72] ^ codereg[74] ^ codereg[75] ^ codereg[76] ^ codereg[78] ^ codereg[79] ^ codereg[83] ^ codereg[84] ^ codereg[85] ^ codereg[86] ^ codereg[87] ^ codereg[90] ^ codereg[91] ^ codereg[93] ^ codereg[96] ^ codereg[101] ^ codereg[103] ^ codereg[105] ^ codereg[106] ^ codereg[107] ^ codereg[109] ^ codereg[110] ^ codereg[114] ^ codereg[115] ^ codereg[116] ^ codereg[117] ^ codereg[118] ^ codereg[121] ^ codereg[122] ^ codereg[124] ^ codereg[127] ^ codereg[132];
assign synd[4] = codereg[4] ^ codereg[6] ^ codereg[8] ^ codereg[9] ^ codereg[10] ^ codereg[12] ^ codereg[13] ^ codereg[17] ^ codereg[18] ^ codereg[19] ^ codereg[20] ^ codereg[21] ^ codereg[24] ^ codereg[25] ^ codereg[27] ^ codereg[30] ^ codereg[35] ^ codereg[37] ^ codereg[39] ^ codereg[40] ^ codereg[41] ^ codereg[43] ^ codereg[44] ^ codereg[48] ^ codereg[49] ^ codereg[50] ^ codereg[51] ^ codereg[52] ^ codereg[55] ^ codereg[56] ^ codereg[58] ^ codereg[61] ^ codereg[66] ^ codereg[68] ^ codereg[70] ^ codereg[71] ^ codereg[72] ^ codereg[74] ^ codereg[75] ^ codereg[79] ^ codereg[80] ^ codereg[81] ^ codereg[82] ^ codereg[83] ^ codereg[86] ^ codereg[87] ^ codereg[89] ^ codereg[92] ^ codereg[97] ^ codereg[99] ^ codereg[101] ^ codereg[102] ^ codereg[103] ^ codereg[105] ^ codereg[106] ^ codereg[110] ^ codereg[111] ^ codereg[112] ^ codereg[113] ^ codereg[114] ^ codereg[117] ^ codereg[118] ^ codereg[120] ^ codereg[123] ^ codereg[128] ^ codereg[130] ^ codereg[132] ^ codereg[133];
assign synd[5] = codereg[5] ^ codereg[7] ^ codereg[9] ^ codereg[10] ^ codereg[11] ^ codereg[13] ^ codereg[14] ^ codereg[18] ^ codereg[19] ^ codereg[20] ^ codereg[21] ^ codereg[22] ^ codereg[25] ^ codereg[26] ^ codereg[28] ^ codereg[31] ^ codereg[36] ^ codereg[38] ^ codereg[40] ^ codereg[41] ^ codereg[42] ^ codereg[44] ^ codereg[45] ^ codereg[49] ^ codereg[50] ^ codereg[51] ^ codereg[52] ^ codereg[53] ^ codereg[56] ^ codereg[57] ^ codereg[59] ^ codereg[62] ^ codereg[67] ^ codereg[69] ^ codereg[71] ^ codereg[72] ^ codereg[73] ^ codereg[75] ^ codereg[76] ^ codereg[80] ^ codereg[81] ^ codereg[82] ^ codereg[83] ^ codereg[84] ^ codereg[87] ^ codereg[88] ^ codereg[90] ^ codereg[93] ^ codereg[98] ^ codereg[100] ^ codereg[102] ^ codereg[103] ^ codereg[104] ^ codereg[106] ^ codereg[107] ^ codereg[111] ^ codereg[112] ^ codereg[113] ^ codereg[114] ^ codereg[115] ^ codereg[118] ^ codereg[119] ^ codereg[121] ^ codereg[124] ^ codereg[129] ^ codereg[131] ^ codereg[133];



	
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

	
