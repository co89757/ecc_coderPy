 
	//  CRC decoder 
	module crc8_64_dec (
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
	input [0:71] i_code;


	//------OUTPUT PORTS -----
	output [0:63] o_data;
	output o_valid;
	output o_haserr;

	//---- INTERNAL VARIABLES ---

	reg [0:71] codereg ;
	reg o_haserr;
	reg o_valid;
	 
	 


	wire [0:7] synd ; 
	 
	reg [0:63] o_data; 
	wire [0:63] data = codereg[8:71] ; //extract databits 
	

	//---STATEMENTS 
	 


	
//----------Syndrome Generation-------------//
assign synd[0] = codereg[0] ^ codereg[8] ^ codereg[9] ^ codereg[10] ^ codereg[11] ^ codereg[15] ^ codereg[20] ^ codereg[21] ^ codereg[23] ^ codereg[26] ^ codereg[27] ^ codereg[29] ^ codereg[30] ^ codereg[32] ^ codereg[33] ^ codereg[34] ^ codereg[35] ^ codereg[36] ^ codereg[37] ^ codereg[39] ^ codereg[40] ^ codereg[41] ^ codereg[43] ^ codereg[44] ^ codereg[47] ^ codereg[48] ^ codereg[49] ^ codereg[51] ^ codereg[55] ^ codereg[57] ^ codereg[60] ^ codereg[63] ^ codereg[64] ^ codereg[65] ^ codereg[66] ^ codereg[67] ^ codereg[70] ^ codereg[71];
assign synd[1] = codereg[1] ^ codereg[8] ^ codereg[12] ^ codereg[15] ^ codereg[16] ^ codereg[20] ^ codereg[22] ^ codereg[23] ^ codereg[24] ^ codereg[26] ^ codereg[28] ^ codereg[29] ^ codereg[31] ^ codereg[32] ^ codereg[38] ^ codereg[39] ^ codereg[42] ^ codereg[43] ^ codereg[45] ^ codereg[47] ^ codereg[50] ^ codereg[51] ^ codereg[52] ^ codereg[55] ^ codereg[56] ^ codereg[57] ^ codereg[58] ^ codereg[60] ^ codereg[61] ^ codereg[63] ^ codereg[68] ^ codereg[70];
assign synd[2] = codereg[2] ^ codereg[9] ^ codereg[13] ^ codereg[16] ^ codereg[17] ^ codereg[21] ^ codereg[23] ^ codereg[24] ^ codereg[25] ^ codereg[27] ^ codereg[29] ^ codereg[30] ^ codereg[32] ^ codereg[33] ^ codereg[39] ^ codereg[40] ^ codereg[43] ^ codereg[44] ^ codereg[46] ^ codereg[48] ^ codereg[51] ^ codereg[52] ^ codereg[53] ^ codereg[56] ^ codereg[57] ^ codereg[58] ^ codereg[59] ^ codereg[61] ^ codereg[62] ^ codereg[64] ^ codereg[69] ^ codereg[71];
assign synd[3] = codereg[3] ^ codereg[8] ^ codereg[9] ^ codereg[11] ^ codereg[14] ^ codereg[15] ^ codereg[17] ^ codereg[18] ^ codereg[20] ^ codereg[21] ^ codereg[22] ^ codereg[23] ^ codereg[24] ^ codereg[25] ^ codereg[27] ^ codereg[28] ^ codereg[29] ^ codereg[31] ^ codereg[32] ^ codereg[35] ^ codereg[36] ^ codereg[37] ^ codereg[39] ^ codereg[43] ^ codereg[45] ^ codereg[48] ^ codereg[51] ^ codereg[52] ^ codereg[53] ^ codereg[54] ^ codereg[55] ^ codereg[58] ^ codereg[59] ^ codereg[62] ^ codereg[64] ^ codereg[66] ^ codereg[67] ^ codereg[71];
assign synd[4] = codereg[4] ^ codereg[8] ^ codereg[11] ^ codereg[12] ^ codereg[16] ^ codereg[18] ^ codereg[19] ^ codereg[20] ^ codereg[22] ^ codereg[24] ^ codereg[25] ^ codereg[27] ^ codereg[28] ^ codereg[34] ^ codereg[35] ^ codereg[38] ^ codereg[39] ^ codereg[41] ^ codereg[43] ^ codereg[46] ^ codereg[47] ^ codereg[48] ^ codereg[51] ^ codereg[52] ^ codereg[53] ^ codereg[54] ^ codereg[56] ^ codereg[57] ^ codereg[59] ^ codereg[64] ^ codereg[66] ^ codereg[68] ^ codereg[70] ^ codereg[71];
assign synd[5] = codereg[5] ^ codereg[9] ^ codereg[12] ^ codereg[13] ^ codereg[17] ^ codereg[19] ^ codereg[20] ^ codereg[21] ^ codereg[23] ^ codereg[25] ^ codereg[26] ^ codereg[28] ^ codereg[29] ^ codereg[35] ^ codereg[36] ^ codereg[39] ^ codereg[40] ^ codereg[42] ^ codereg[44] ^ codereg[47] ^ codereg[48] ^ codereg[49] ^ codereg[52] ^ codereg[53] ^ codereg[54] ^ codereg[55] ^ codereg[57] ^ codereg[58] ^ codereg[60] ^ codereg[65] ^ codereg[67] ^ codereg[69] ^ codereg[71];
assign synd[6] = codereg[6] ^ codereg[10] ^ codereg[13] ^ codereg[14] ^ codereg[18] ^ codereg[20] ^ codereg[21] ^ codereg[22] ^ codereg[24] ^ codereg[26] ^ codereg[27] ^ codereg[29] ^ codereg[30] ^ codereg[36] ^ codereg[37] ^ codereg[40] ^ codereg[41] ^ codereg[43] ^ codereg[45] ^ codereg[48] ^ codereg[49] ^ codereg[50] ^ codereg[53] ^ codereg[54] ^ codereg[55] ^ codereg[56] ^ codereg[58] ^ codereg[59] ^ codereg[61] ^ codereg[66] ^ codereg[68] ^ codereg[70];
assign synd[7] = codereg[7] ^ codereg[8] ^ codereg[9] ^ codereg[10] ^ codereg[14] ^ codereg[19] ^ codereg[20] ^ codereg[22] ^ codereg[25] ^ codereg[26] ^ codereg[28] ^ codereg[29] ^ codereg[31] ^ codereg[32] ^ codereg[33] ^ codereg[34] ^ codereg[35] ^ codereg[36] ^ codereg[38] ^ codereg[39] ^ codereg[40] ^ codereg[42] ^ codereg[43] ^ codereg[46] ^ codereg[47] ^ codereg[48] ^ codereg[50] ^ codereg[54] ^ codereg[56] ^ codereg[59] ^ codereg[62] ^ codereg[63] ^ codereg[64] ^ codereg[65] ^ codereg[66] ^ codereg[69] ^ codereg[70];



	
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

	
