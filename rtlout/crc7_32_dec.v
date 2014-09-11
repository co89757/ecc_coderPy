 
	//  CRC decoder 
	module crc7_32_dec (
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
	input [0:38] i_code;


	//------OUTPUT PORTS -----
	output [0:31] o_data;
	output o_valid;
	output o_haserr;

	//---- INTERNAL VARIABLES ---

	reg [0:38] codereg ;
	reg o_haserr;
	reg o_valid;
	 
	 


	wire [0:6] synd ; 
	 
	reg [0:31] o_data; 
	wire [0:31] data = codereg[7:38] ; //extract databits 
	

	//---STATEMENTS 
	 


	
//----------Syndrome Generation-------------//
assign synd[0] = codereg[0] ^ codereg[7] ^ codereg[8] ^ codereg[9] ^ codereg[10] ^ codereg[11] ^ codereg[13] ^ codereg[14] ^ codereg[15] ^ codereg[16] ^ codereg[19] ^ codereg[20] ^ codereg[21] ^ codereg[23] ^ codereg[25] ^ codereg[26] ^ codereg[31] ^ codereg[33] ^ codereg[34] ^ codereg[35];
assign synd[1] = codereg[1] ^ codereg[8] ^ codereg[9] ^ codereg[10] ^ codereg[11] ^ codereg[12] ^ codereg[14] ^ codereg[15] ^ codereg[16] ^ codereg[17] ^ codereg[20] ^ codereg[21] ^ codereg[22] ^ codereg[24] ^ codereg[26] ^ codereg[27] ^ codereg[32] ^ codereg[34] ^ codereg[35] ^ codereg[36];
assign synd[2] = codereg[2] ^ codereg[7] ^ codereg[8] ^ codereg[12] ^ codereg[14] ^ codereg[17] ^ codereg[18] ^ codereg[19] ^ codereg[20] ^ codereg[22] ^ codereg[26] ^ codereg[27] ^ codereg[28] ^ codereg[31] ^ codereg[34] ^ codereg[36] ^ codereg[37];
assign synd[3] = codereg[3] ^ codereg[8] ^ codereg[9] ^ codereg[13] ^ codereg[15] ^ codereg[18] ^ codereg[19] ^ codereg[20] ^ codereg[21] ^ codereg[23] ^ codereg[27] ^ codereg[28] ^ codereg[29] ^ codereg[32] ^ codereg[35] ^ codereg[37] ^ codereg[38];
assign synd[4] = codereg[4] ^ codereg[9] ^ codereg[10] ^ codereg[14] ^ codereg[16] ^ codereg[19] ^ codereg[20] ^ codereg[21] ^ codereg[22] ^ codereg[24] ^ codereg[28] ^ codereg[29] ^ codereg[30] ^ codereg[33] ^ codereg[36] ^ codereg[38];
assign synd[5] = codereg[5] ^ codereg[10] ^ codereg[11] ^ codereg[15] ^ codereg[17] ^ codereg[20] ^ codereg[21] ^ codereg[22] ^ codereg[23] ^ codereg[25] ^ codereg[29] ^ codereg[30] ^ codereg[31] ^ codereg[34] ^ codereg[37];
assign synd[6] = codereg[6] ^ codereg[7] ^ codereg[8] ^ codereg[9] ^ codereg[10] ^ codereg[12] ^ codereg[13] ^ codereg[14] ^ codereg[15] ^ codereg[18] ^ codereg[19] ^ codereg[20] ^ codereg[22] ^ codereg[24] ^ codereg[25] ^ codereg[30] ^ codereg[32] ^ codereg[33] ^ codereg[34] ^ codereg[38];



	
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

	
