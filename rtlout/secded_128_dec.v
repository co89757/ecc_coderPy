 
	module secded_128_dec (
	clk,
	reset_n,
	enable,
	i_code,
	o_data,
	o_valid,
	o_err_corr,
	o_err_detec,
	o_err_fatal

	);

	//------ INPUT PORTS -----
	input clk ;
	input reset_n;
	input enable;
	input [0:136] i_code;


	//------OUTPUT PORTS -----
	output [0:127] o_data;
	output o_valid;
	output o_err_corr;
	output o_err_detec;
	output o_err_fatal;

	//---- INTERNAL VARIABLES ---

	reg [0:136] codereg ;
	reg o_err_fatal;
	reg o_err_detec;
	reg o_err_corr;
	reg o_valid;
	wire noerr; 
	wire synpar;
	wire [0:127] corr_word; 


	wire [0:8] synd ; 
	wire [0:127] flip ; // databits error mask 
	reg [0:127] o_data; 
	wire[0:8] chk = codereg[128:136]; //extract the checkbits 

	wire [0:127] data = codereg[0:127] ; //extract databits

	//---STATEMENTS 
	 
	

	
//--------- Syndrome Generation -------//
assign synd[0] = chk[0] ^ data[0] ^ data[4] ^ data[5] ^ data[6] ^ data[10] ^ data[13] ^ data[15] ^ data[16] ^ data[17] ^ data[24] ^ data[25] ^ data[28] ^ data[31] ^ data[34] ^ data[35] ^ data[37] ^ data[38] ^ data[39] ^ data[42] ^ data[48] ^ data[50] ^ data[52] ^ data[53] ^ data[55] ^ data[56] ^ data[58] ^ data[60] ^ data[61] ^ data[64] ^ data[66] ^ data[67] ^ data[72] ^ data[73] ^ data[74] ^ data[75] ^ data[76] ^ data[78] ^ data[79] ^ data[81] ^ data[82] ^ data[83] ^ data[84] ^ data[86] ^ data[88] ^ data[89] ^ data[90] ^ data[92] ^ data[96] ^ data[101] ^ data[102] ^ data[104] ^ data[105] ^ data[109] ^ data[110] ^ data[111] ^ data[112] ^ data[115] ^ data[116] ^ data[117] ^ data[120] ^ data[121] ^ data[125] ^ data[127];
assign synd[1] = chk[1] ^ data[1] ^ data[5] ^ data[6] ^ data[7] ^ data[11] ^ data[14] ^ data[16] ^ data[17] ^ data[18] ^ data[25] ^ data[26] ^ data[29] ^ data[32] ^ data[35] ^ data[36] ^ data[38] ^ data[39] ^ data[40] ^ data[43] ^ data[49] ^ data[51] ^ data[53] ^ data[54] ^ data[56] ^ data[57] ^ data[59] ^ data[61] ^ data[62] ^ data[65] ^ data[67] ^ data[68] ^ data[73] ^ data[74] ^ data[75] ^ data[76] ^ data[77] ^ data[79] ^ data[80] ^ data[82] ^ data[83] ^ data[84] ^ data[85] ^ data[87] ^ data[89] ^ data[90] ^ data[91] ^ data[93] ^ data[97] ^ data[102] ^ data[103] ^ data[105] ^ data[106] ^ data[110] ^ data[111] ^ data[112] ^ data[113] ^ data[116] ^ data[117] ^ data[118] ^ data[121] ^ data[122] ^ data[126];
assign synd[2] = chk[2] ^ data[0] ^ data[2] ^ data[4] ^ data[5] ^ data[7] ^ data[8] ^ data[10] ^ data[12] ^ data[13] ^ data[16] ^ data[18] ^ data[19] ^ data[24] ^ data[25] ^ data[26] ^ data[27] ^ data[28] ^ data[30] ^ data[31] ^ data[33] ^ data[34] ^ data[35] ^ data[36] ^ data[38] ^ data[40] ^ data[41] ^ data[42] ^ data[44] ^ data[48] ^ data[53] ^ data[54] ^ data[56] ^ data[57] ^ data[61] ^ data[62] ^ data[63] ^ data[64] ^ data[67] ^ data[68] ^ data[69] ^ data[72] ^ data[73] ^ data[77] ^ data[79] ^ data[80] ^ data[82] ^ data[85] ^ data[89] ^ data[91] ^ data[94] ^ data[96] ^ data[98] ^ data[101] ^ data[102] ^ data[103] ^ data[105] ^ data[106] ^ data[107] ^ data[109] ^ data[110] ^ data[113] ^ data[114] ^ data[115] ^ data[116] ^ data[118] ^ data[119] ^ data[120] ^ data[121] ^ data[122] ^ data[123] ^ data[125];
assign synd[3] = chk[3] ^ data[0] ^ data[1] ^ data[3] ^ data[4] ^ data[8] ^ data[9] ^ data[10] ^ data[11] ^ data[14] ^ data[15] ^ data[16] ^ data[19] ^ data[20] ^ data[24] ^ data[26] ^ data[27] ^ data[29] ^ data[32] ^ data[36] ^ data[38] ^ data[41] ^ data[43] ^ data[45] ^ data[48] ^ data[49] ^ data[50] ^ data[52] ^ data[53] ^ data[54] ^ data[56] ^ data[57] ^ data[60] ^ data[61] ^ data[62] ^ data[63] ^ data[65] ^ data[66] ^ data[67] ^ data[68] ^ data[69] ^ data[70] ^ data[72] ^ data[75] ^ data[76] ^ data[79] ^ data[80] ^ data[82] ^ data[84] ^ data[88] ^ data[89] ^ data[95] ^ data[96] ^ data[97] ^ data[99] ^ data[101] ^ data[103] ^ data[105] ^ data[106] ^ data[107] ^ data[108] ^ data[109] ^ data[112] ^ data[114] ^ data[119] ^ data[122] ^ data[123] ^ data[124] ^ data[125] ^ data[126] ^ data[127];
assign synd[4] = chk[4] ^ data[0] ^ data[1] ^ data[2] ^ data[6] ^ data[9] ^ data[11] ^ data[12] ^ data[13] ^ data[20] ^ data[21] ^ data[24] ^ data[27] ^ data[30] ^ data[31] ^ data[33] ^ data[34] ^ data[35] ^ data[38] ^ data[44] ^ data[46] ^ data[48] ^ data[49] ^ data[51] ^ data[52] ^ data[54] ^ data[56] ^ data[57] ^ data[60] ^ data[62] ^ data[63] ^ data[68] ^ data[69] ^ data[70] ^ data[71] ^ data[72] ^ data[74] ^ data[75] ^ data[77] ^ data[78] ^ data[79] ^ data[80] ^ data[82] ^ data[84] ^ data[85] ^ data[86] ^ data[88] ^ data[92] ^ data[97] ^ data[98] ^ data[100] ^ data[101] ^ data[105] ^ data[106] ^ data[107] ^ data[108] ^ data[111] ^ data[112] ^ data[113] ^ data[116] ^ data[117] ^ data[121] ^ data[123] ^ data[124] ^ data[126];
assign synd[5] = chk[5] ^ data[1] ^ data[2] ^ data[3] ^ data[7] ^ data[10] ^ data[12] ^ data[13] ^ data[14] ^ data[21] ^ data[22] ^ data[25] ^ data[28] ^ data[31] ^ data[32] ^ data[34] ^ data[35] ^ data[36] ^ data[39] ^ data[45] ^ data[47] ^ data[49] ^ data[50] ^ data[52] ^ data[53] ^ data[55] ^ data[57] ^ data[58] ^ data[61] ^ data[63] ^ data[64] ^ data[69] ^ data[70] ^ data[71] ^ data[72] ^ data[73] ^ data[75] ^ data[76] ^ data[78] ^ data[79] ^ data[80] ^ data[81] ^ data[83] ^ data[85] ^ data[86] ^ data[87] ^ data[89] ^ data[93] ^ data[98] ^ data[99] ^ data[101] ^ data[102] ^ data[106] ^ data[107] ^ data[108] ^ data[109] ^ data[112] ^ data[113] ^ data[114] ^ data[117] ^ data[118] ^ data[122] ^ data[124] ^ data[125] ^ data[127];
assign synd[6] = chk[6] ^ data[2] ^ data[3] ^ data[4] ^ data[8] ^ data[11] ^ data[13] ^ data[14] ^ data[15] ^ data[22] ^ data[23] ^ data[26] ^ data[29] ^ data[32] ^ data[33] ^ data[35] ^ data[36] ^ data[37] ^ data[40] ^ data[46] ^ data[48] ^ data[50] ^ data[51] ^ data[53] ^ data[54] ^ data[56] ^ data[58] ^ data[59] ^ data[62] ^ data[64] ^ data[65] ^ data[70] ^ data[71] ^ data[72] ^ data[73] ^ data[74] ^ data[76] ^ data[77] ^ data[79] ^ data[80] ^ data[81] ^ data[82] ^ data[84] ^ data[86] ^ data[87] ^ data[88] ^ data[90] ^ data[94] ^ data[99] ^ data[100] ^ data[102] ^ data[103] ^ data[107] ^ data[108] ^ data[109] ^ data[110] ^ data[113] ^ data[114] ^ data[115] ^ data[118] ^ data[119] ^ data[123] ^ data[125] ^ data[126];
assign synd[7] = chk[7] ^ data[3] ^ data[4] ^ data[5] ^ data[9] ^ data[12] ^ data[14] ^ data[15] ^ data[16] ^ data[23] ^ data[24] ^ data[27] ^ data[30] ^ data[33] ^ data[34] ^ data[36] ^ data[37] ^ data[38] ^ data[41] ^ data[47] ^ data[49] ^ data[51] ^ data[52] ^ data[54] ^ data[55] ^ data[57] ^ data[59] ^ data[60] ^ data[63] ^ data[65] ^ data[66] ^ data[71] ^ data[72] ^ data[73] ^ data[74] ^ data[75] ^ data[77] ^ data[78] ^ data[80] ^ data[81] ^ data[82] ^ data[83] ^ data[85] ^ data[87] ^ data[88] ^ data[89] ^ data[91] ^ data[95] ^ data[100] ^ data[101] ^ data[103] ^ data[104] ^ data[108] ^ data[109] ^ data[110] ^ data[111] ^ data[114] ^ data[115] ^ data[116] ^ data[119] ^ data[120] ^ data[124] ^ data[126] ^ data[127];
assign synd[8] = chk[8] ^ data[0] ^ data[1] ^ data[2] ^ data[3] ^ data[5] ^ data[10] ^ data[11] ^ data[12] ^ data[15] ^ data[17] ^ data[18] ^ data[19] ^ data[20] ^ data[21] ^ data[22] ^ data[23] ^ data[25] ^ data[26] ^ data[27] ^ data[31] ^ data[32] ^ data[33] ^ data[35] ^ data[36] ^ data[38] ^ data[42] ^ data[43] ^ data[44] ^ data[45] ^ data[46] ^ data[47] ^ data[50] ^ data[51] ^ data[53] ^ data[54] ^ data[56] ^ data[57] ^ data[60] ^ data[64] ^ data[65] ^ data[67] ^ data[68] ^ data[69] ^ data[70] ^ data[71] ^ data[73] ^ data[75] ^ data[78] ^ data[81] ^ data[83] ^ data[86] ^ data[87] ^ data[89] ^ data[92] ^ data[93] ^ data[94] ^ data[95] ^ data[101] ^ data[104] ^ data[109] ^ data[111] ^ data[115] ^ data[117] ^ data[118] ^ data[119] ^ data[121] ^ data[122] ^ data[123] ^ data[124] ^ data[127];

//--------- Syndrome Decoding ----------//
assign noerr = ~synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & ~synd[8];
assign flip[0] = synd[0] & ~synd[1] & synd[2] & synd[3] & synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[1] = ~synd[0] & synd[1] & ~synd[2] & synd[3] & synd[4] & synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[2] = ~synd[0] & ~synd[1] & synd[2] & ~synd[3] & synd[4] & synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[3] = ~synd[0] & ~synd[1] & ~synd[2] & synd[3] & ~synd[4] & synd[5] & synd[6] & synd[7] & synd[8];
assign flip[4] = synd[0] & ~synd[1] & synd[2] & synd[3] & ~synd[4] & ~synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[5] = synd[0] & synd[1] & synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[6] = synd[0] & synd[1] & ~synd[2] & ~synd[3] & synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & ~synd[8];
assign flip[7] = ~synd[0] & synd[1] & synd[2] & ~synd[3] & ~synd[4] & synd[5] & ~synd[6] & ~synd[7] & ~synd[8];
assign flip[8] = ~synd[0] & ~synd[1] & synd[2] & synd[3] & ~synd[4] & ~synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[9] = ~synd[0] & ~synd[1] & ~synd[2] & synd[3] & synd[4] & ~synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[10] = synd[0] & ~synd[1] & synd[2] & synd[3] & ~synd[4] & synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[11] = ~synd[0] & synd[1] & ~synd[2] & synd[3] & synd[4] & ~synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[12] = ~synd[0] & ~synd[1] & synd[2] & ~synd[3] & synd[4] & synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[13] = synd[0] & ~synd[1] & synd[2] & ~synd[3] & synd[4] & synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[14] = ~synd[0] & synd[1] & ~synd[2] & synd[3] & ~synd[4] & synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[15] = synd[0] & ~synd[1] & ~synd[2] & synd[3] & ~synd[4] & ~synd[5] & synd[6] & synd[7] & synd[8];
assign flip[16] = synd[0] & synd[1] & synd[2] & synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[17] = synd[0] & synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[18] = ~synd[0] & synd[1] & synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[19] = ~synd[0] & ~synd[1] & synd[2] & synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[20] = ~synd[0] & ~synd[1] & ~synd[2] & synd[3] & synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[21] = ~synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & synd[4] & synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[22] = ~synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[23] = ~synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & synd[6] & synd[7] & synd[8];
assign flip[24] = synd[0] & ~synd[1] & synd[2] & synd[3] & synd[4] & ~synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[25] = synd[0] & synd[1] & synd[2] & ~synd[3] & ~synd[4] & synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[26] = ~synd[0] & synd[1] & synd[2] & synd[3] & ~synd[4] & ~synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[27] = ~synd[0] & ~synd[1] & synd[2] & synd[3] & synd[4] & ~synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[28] = synd[0] & ~synd[1] & synd[2] & ~synd[3] & ~synd[4] & synd[5] & ~synd[6] & ~synd[7] & ~synd[8];
assign flip[29] = ~synd[0] & synd[1] & ~synd[2] & synd[3] & ~synd[4] & ~synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[30] = ~synd[0] & ~synd[1] & synd[2] & ~synd[3] & synd[4] & ~synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[31] = synd[0] & ~synd[1] & synd[2] & ~synd[3] & synd[4] & synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[32] = ~synd[0] & synd[1] & ~synd[2] & synd[3] & ~synd[4] & synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[33] = ~synd[0] & ~synd[1] & synd[2] & ~synd[3] & synd[4] & ~synd[5] & synd[6] & synd[7] & synd[8];
assign flip[34] = synd[0] & ~synd[1] & synd[2] & ~synd[3] & synd[4] & synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[35] = synd[0] & synd[1] & synd[2] & ~synd[3] & synd[4] & synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[36] = ~synd[0] & synd[1] & synd[2] & synd[3] & ~synd[4] & synd[5] & synd[6] & synd[7] & synd[8];
assign flip[37] = synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[38] = synd[0] & synd[1] & synd[2] & synd[3] & synd[4] & ~synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[39] = synd[0] & synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & synd[5] & ~synd[6] & ~synd[7] & ~synd[8];
assign flip[40] = ~synd[0] & synd[1] & synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[41] = ~synd[0] & ~synd[1] & synd[2] & synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[42] = synd[0] & ~synd[1] & synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[43] = ~synd[0] & synd[1] & ~synd[2] & synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[44] = ~synd[0] & ~synd[1] & synd[2] & ~synd[3] & synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[45] = ~synd[0] & ~synd[1] & ~synd[2] & synd[3] & ~synd[4] & synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[46] = ~synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & synd[4] & ~synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[47] = ~synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[48] = synd[0] & ~synd[1] & synd[2] & synd[3] & synd[4] & ~synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[49] = ~synd[0] & synd[1] & ~synd[2] & synd[3] & synd[4] & synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[50] = synd[0] & ~synd[1] & ~synd[2] & synd[3] & ~synd[4] & synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[51] = ~synd[0] & synd[1] & ~synd[2] & ~synd[3] & synd[4] & ~synd[5] & synd[6] & synd[7] & synd[8];
assign flip[52] = synd[0] & ~synd[1] & ~synd[2] & synd[3] & synd[4] & synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[53] = synd[0] & synd[1] & synd[2] & synd[3] & ~synd[4] & synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[54] = ~synd[0] & synd[1] & synd[2] & synd[3] & synd[4] & ~synd[5] & synd[6] & synd[7] & synd[8];
assign flip[55] = synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[56] = synd[0] & synd[1] & synd[2] & synd[3] & synd[4] & ~synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[57] = ~synd[0] & synd[1] & synd[2] & synd[3] & synd[4] & synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[58] = synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[59] = ~synd[0] & synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[60] = synd[0] & ~synd[1] & ~synd[2] & synd[3] & synd[4] & ~synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[61] = synd[0] & synd[1] & synd[2] & synd[3] & ~synd[4] & synd[5] & ~synd[6] & ~synd[7] & ~synd[8];
assign flip[62] = ~synd[0] & synd[1] & synd[2] & synd[3] & synd[4] & ~synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[63] = ~synd[0] & ~synd[1] & synd[2] & synd[3] & synd[4] & synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[64] = synd[0] & ~synd[1] & synd[2] & ~synd[3] & ~synd[4] & synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[65] = ~synd[0] & synd[1] & ~synd[2] & synd[3] & ~synd[4] & ~synd[5] & synd[6] & synd[7] & synd[8];
assign flip[66] = synd[0] & ~synd[1] & ~synd[2] & synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[67] = synd[0] & synd[1] & synd[2] & synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[68] = ~synd[0] & synd[1] & synd[2] & synd[3] & synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[69] = ~synd[0] & ~synd[1] & synd[2] & synd[3] & synd[4] & synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[70] = ~synd[0] & ~synd[1] & ~synd[2] & synd[3] & synd[4] & synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[71] = ~synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & synd[4] & synd[5] & synd[6] & synd[7] & synd[8];
assign flip[72] = synd[0] & ~synd[1] & synd[2] & synd[3] & synd[4] & synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[73] = synd[0] & synd[1] & synd[2] & ~synd[3] & ~synd[4] & synd[5] & synd[6] & synd[7] & synd[8];
assign flip[74] = synd[0] & synd[1] & ~synd[2] & ~synd[3] & synd[4] & ~synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[75] = synd[0] & synd[1] & ~synd[2] & synd[3] & synd[4] & synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[76] = synd[0] & synd[1] & ~synd[2] & synd[3] & ~synd[4] & synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[77] = ~synd[0] & synd[1] & synd[2] & ~synd[3] & synd[4] & ~synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[78] = synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & synd[4] & synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[79] = synd[0] & synd[1] & synd[2] & synd[3] & synd[4] & synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[80] = ~synd[0] & synd[1] & synd[2] & synd[3] & synd[4] & synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[81] = synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & synd[5] & synd[6] & synd[7] & synd[8];
assign flip[82] = synd[0] & synd[1] & synd[2] & synd[3] & synd[4] & ~synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[83] = synd[0] & synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[84] = synd[0] & synd[1] & ~synd[2] & synd[3] & synd[4] & ~synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[85] = ~synd[0] & synd[1] & synd[2] & ~synd[3] & synd[4] & synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[86] = synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & synd[4] & synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[87] = ~synd[0] & synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & synd[5] & synd[6] & synd[7] & synd[8];
assign flip[88] = synd[0] & ~synd[1] & ~synd[2] & synd[3] & synd[4] & ~synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[89] = synd[0] & synd[1] & synd[2] & synd[3] & ~synd[4] & synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[90] = synd[0] & synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[91] = ~synd[0] & synd[1] & synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[92] = synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[93] = ~synd[0] & synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[94] = ~synd[0] & ~synd[1] & synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[95] = ~synd[0] & ~synd[1] & ~synd[2] & synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[96] = synd[0] & ~synd[1] & synd[2] & synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & ~synd[8];
assign flip[97] = ~synd[0] & synd[1] & ~synd[2] & synd[3] & synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & ~synd[8];
assign flip[98] = ~synd[0] & ~synd[1] & synd[2] & ~synd[3] & synd[4] & synd[5] & ~synd[6] & ~synd[7] & ~synd[8];
assign flip[99] = ~synd[0] & ~synd[1] & ~synd[2] & synd[3] & ~synd[4] & synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[100] = ~synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & synd[4] & ~synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[101] = synd[0] & ~synd[1] & synd[2] & synd[3] & synd[4] & synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[102] = synd[0] & synd[1] & synd[2] & ~synd[3] & ~synd[4] & synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[103] = ~synd[0] & synd[1] & synd[2] & synd[3] & ~synd[4] & ~synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[104] = synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[105] = synd[0] & synd[1] & synd[2] & synd[3] & synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & ~synd[8];
assign flip[106] = ~synd[0] & synd[1] & synd[2] & synd[3] & synd[4] & synd[5] & ~synd[6] & ~synd[7] & ~synd[8];
assign flip[107] = ~synd[0] & ~synd[1] & synd[2] & synd[3] & synd[4] & synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[108] = ~synd[0] & ~synd[1] & ~synd[2] & synd[3] & synd[4] & synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[109] = synd[0] & ~synd[1] & synd[2] & synd[3] & ~synd[4] & synd[5] & synd[6] & synd[7] & synd[8];
assign flip[110] = synd[0] & synd[1] & synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[111] = synd[0] & synd[1] & ~synd[2] & ~synd[3] & synd[4] & ~synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[112] = synd[0] & synd[1] & ~synd[2] & synd[3] & synd[4] & synd[5] & ~synd[6] & ~synd[7] & ~synd[8];
assign flip[113] = ~synd[0] & synd[1] & synd[2] & ~synd[3] & synd[4] & synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[114] = ~synd[0] & ~synd[1] & synd[2] & synd[3] & ~synd[4] & synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[115] = synd[0] & ~synd[1] & synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & synd[6] & synd[7] & synd[8];
assign flip[116] = synd[0] & synd[1] & synd[2] & ~synd[3] & synd[4] & ~synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[117] = synd[0] & synd[1] & ~synd[2] & ~synd[3] & synd[4] & synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[118] = ~synd[0] & synd[1] & synd[2] & ~synd[3] & ~synd[4] & synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[119] = ~synd[0] & ~synd[1] & synd[2] & synd[3] & ~synd[4] & ~synd[5] & synd[6] & synd[7] & synd[8];
assign flip[120] = synd[0] & ~synd[1] & synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & synd[7] & ~synd[8];
assign flip[121] = synd[0] & synd[1] & synd[2] & ~synd[3] & synd[4] & ~synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[122] = ~synd[0] & synd[1] & synd[2] & synd[3] & ~synd[4] & synd[5] & ~synd[6] & ~synd[7] & synd[8];
assign flip[123] = ~synd[0] & ~synd[1] & synd[2] & synd[3] & synd[4] & ~synd[5] & synd[6] & ~synd[7] & synd[8];
assign flip[124] = ~synd[0] & ~synd[1] & ~synd[2] & synd[3] & synd[4] & synd[5] & ~synd[6] & synd[7] & synd[8];
assign flip[125] = synd[0] & ~synd[1] & synd[2] & synd[3] & ~synd[4] & synd[5] & synd[6] & ~synd[7] & ~synd[8];
assign flip[126] = ~synd[0] & synd[1] & ~synd[2] & synd[3] & synd[4] & ~synd[5] & synd[6] & synd[7] & ~synd[8];
assign flip[127] = synd[0] & ~synd[1] & ~synd[2] & synd[3] & ~synd[4] & synd[5] & ~synd[6] & synd[7] & synd[8];


	assign synpar = ^synd[0:8];  // syndrome's parity 

	assign corr_word = data  ^ flip ; 


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
			o_err_detec <=0;
			o_err_corr <= 0;
			o_err_fatal <= 0;
		end
		else if (enable) begin

			o_data <= corr_word ;
			o_err_detec <= ~noerr ;
			o_err_corr <= | flip ; // found one name match 
			o_err_fatal <= ~synpar & ~noerr ; // has error AND syndrome has even parity. 2 err or more 
			o_valid <= 1 ; 
			
		end
	end



	endmodule 
	//--------- end of file ------//

	 
