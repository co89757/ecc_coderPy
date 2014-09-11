 
    module hsiao2_64_dec (
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
    input [0:71] i_code;


    //------OUTPUT PORTS -----
    output [0:63] o_data;
    output o_valid;
    output o_err_corr;
    output o_err_detec;
    output o_err_fatal;

    //---- INTERNAL VARIABLES ---

    reg [0:71] codereg ;
    reg o_err_fatal;
    reg o_err_detec;
    reg o_err_corr;
    reg o_valid;
    wire noerr; 
    
    wire [0:63] corr_word; 


    wire [0:7] synd ; 
    wire [0:63] flip ; // databits error mask 
    reg [0:63] o_data; 
    wire[0:7] chk = codereg[64:71]; //extract the checkbits 

    wire [0:63] data = codereg[0:63] ; //extract databits

    wire correctible = ^synd & ~noerr; // correctible (1err) 
    wire fall_thru = noerr | ~correctible; // fall-through when fatal or clean 
    reg [0:63] sel_dout; //selected data output, either corrected data or fall through bits 

    //---STATEMENTS 
     
    

    
//--------- Syndrome Generation -------//
assign synd[0] = chk[0] ^ data[0] ^ data[1] ^ data[2] ^ data[3] ^ data[4] ^ data[5] ^ data[6] ^ data[7] ^ data[10] ^ data[13] ^ data[14] ^ data[17] ^ data[20] ^ data[23] ^ data[24] ^ data[27] ^ data[35] ^ data[43] ^ data[46] ^ data[47] ^ data[51] ^ data[52] ^ data[53] ^ data[56] ^ data[57] ^ data[58];
assign synd[1] = chk[1] ^ data[0] ^ data[1] ^ data[2] ^ data[8] ^ data[9] ^ data[10] ^ data[11] ^ data[12] ^ data[13] ^ data[14] ^ data[15] ^ data[18] ^ data[21] ^ data[22] ^ data[25] ^ data[28] ^ data[31] ^ data[32] ^ data[35] ^ data[43] ^ data[51] ^ data[54] ^ data[55] ^ data[59] ^ data[60] ^ data[61];
assign synd[2] = chk[2] ^ data[3] ^ data[4] ^ data[5] ^ data[8] ^ data[9] ^ data[10] ^ data[16] ^ data[17] ^ data[18] ^ data[19] ^ data[20] ^ data[21] ^ data[22] ^ data[23] ^ data[26] ^ data[29] ^ data[30] ^ data[33] ^ data[36] ^ data[39] ^ data[40] ^ data[43] ^ data[51] ^ data[59] ^ data[62] ^ data[63];
assign synd[3] = chk[3] ^ data[3] ^ data[6] ^ data[7] ^ data[11] ^ data[12] ^ data[13] ^ data[16] ^ data[17] ^ data[18] ^ data[24] ^ data[25] ^ data[26] ^ data[27] ^ data[28] ^ data[29] ^ data[30] ^ data[31] ^ data[34] ^ data[37] ^ data[38] ^ data[41] ^ data[44] ^ data[47] ^ data[48] ^ data[51] ^ data[59];
assign synd[4] = chk[4] ^ data[3] ^ data[11] ^ data[14] ^ data[15] ^ data[19] ^ data[20] ^ data[21] ^ data[24] ^ data[25] ^ data[26] ^ data[32] ^ data[33] ^ data[34] ^ data[35] ^ data[36] ^ data[37] ^ data[38] ^ data[39] ^ data[42] ^ data[45] ^ data[46] ^ data[49] ^ data[52] ^ data[55] ^ data[56] ^ data[59];
assign synd[5] = chk[5] ^ data[0] ^ data[3] ^ data[11] ^ data[19] ^ data[22] ^ data[23] ^ data[27] ^ data[28] ^ data[29] ^ data[32] ^ data[33] ^ data[34] ^ data[40] ^ data[41] ^ data[42] ^ data[43] ^ data[44] ^ data[45] ^ data[46] ^ data[47] ^ data[50] ^ data[53] ^ data[54] ^ data[57] ^ data[60] ^ data[63];
assign synd[6] = chk[6] ^ data[1] ^ data[4] ^ data[7] ^ data[8] ^ data[11] ^ data[19] ^ data[27] ^ data[30] ^ data[31] ^ data[35] ^ data[36] ^ data[37] ^ data[40] ^ data[41] ^ data[42] ^ data[48] ^ data[49] ^ data[50] ^ data[51] ^ data[52] ^ data[53] ^ data[54] ^ data[55] ^ data[58] ^ data[61] ^ data[62];
assign synd[7] = chk[7] ^ data[2] ^ data[5] ^ data[6] ^ data[9] ^ data[12] ^ data[15] ^ data[16] ^ data[19] ^ data[27] ^ data[35] ^ data[38] ^ data[39] ^ data[43] ^ data[44] ^ data[45] ^ data[48] ^ data[49] ^ data[50] ^ data[56] ^ data[57] ^ data[58] ^ data[59] ^ data[60] ^ data[61] ^ data[62] ^ data[63];

//--------- Syndrome Decoding ----------//
assign noerr = ~synd[0] & ~synd[1] & ~synd[2] & ~synd[3] & ~synd[4] & ~synd[5] & ~synd[6] & ~synd[7];
assign flip[0] = synd[0] & synd[1] & synd[5];
assign flip[1] = synd[0] & synd[1] & synd[6];
assign flip[2] = synd[0] & synd[1] & synd[7];
assign flip[3] = synd[0] & synd[2] & synd[3] & synd[4] & synd[5];
assign flip[4] = synd[0] & synd[2] & synd[6];
assign flip[5] = synd[0] & synd[2] & synd[7];
assign flip[6] = synd[0] & synd[3] & synd[7];
assign flip[7] = synd[0] & synd[3] & synd[6];
assign flip[8] = synd[1] & synd[2] & synd[6];
assign flip[9] = synd[1] & synd[2] & synd[7];
assign flip[10] = synd[0] & synd[1] & synd[2];
assign flip[11] = synd[1] & synd[3] & synd[4] & synd[5] & synd[6];
assign flip[12] = synd[1] & synd[3] & synd[7];
assign flip[13] = synd[0] & synd[1] & synd[3];
assign flip[14] = synd[0] & synd[1] & synd[4];
assign flip[15] = synd[1] & synd[4] & synd[7];
assign flip[16] = synd[2] & synd[3] & synd[7];
assign flip[17] = synd[0] & synd[2] & synd[3];
assign flip[18] = synd[1] & synd[2] & synd[3];
assign flip[19] = synd[2] & synd[4] & synd[5] & synd[6] & synd[7];
assign flip[20] = synd[0] & synd[2] & synd[4];
assign flip[21] = synd[1] & synd[2] & synd[4];
assign flip[22] = synd[1] & synd[2] & synd[5];
assign flip[23] = synd[0] & synd[2] & synd[5];
assign flip[24] = synd[0] & synd[3] & synd[4];
assign flip[25] = synd[1] & synd[3] & synd[4];
assign flip[26] = synd[2] & synd[3] & synd[4];
assign flip[27] = synd[0] & synd[3] & synd[5] & synd[6] & synd[7];
assign flip[28] = synd[1] & synd[3] & synd[5];
assign flip[29] = synd[2] & synd[3] & synd[5];
assign flip[30] = synd[2] & synd[3] & synd[6];
assign flip[31] = synd[1] & synd[3] & synd[6];
assign flip[32] = synd[1] & synd[4] & synd[5];
assign flip[33] = synd[2] & synd[4] & synd[5];
assign flip[34] = synd[3] & synd[4] & synd[5];
assign flip[35] = synd[0] & synd[1] & synd[4] & synd[6] & synd[7];
assign flip[36] = synd[2] & synd[4] & synd[6];
assign flip[37] = synd[3] & synd[4] & synd[6];
assign flip[38] = synd[3] & synd[4] & synd[7];
assign flip[39] = synd[2] & synd[4] & synd[7];
assign flip[40] = synd[2] & synd[5] & synd[6];
assign flip[41] = synd[3] & synd[5] & synd[6];
assign flip[42] = synd[4] & synd[5] & synd[6];
assign flip[43] = synd[0] & synd[1] & synd[2] & synd[5] & synd[7];
assign flip[44] = synd[3] & synd[5] & synd[7];
assign flip[45] = synd[4] & synd[5] & synd[7];
assign flip[46] = synd[0] & synd[4] & synd[5];
assign flip[47] = synd[0] & synd[3] & synd[5];
assign flip[48] = synd[3] & synd[6] & synd[7];
assign flip[49] = synd[4] & synd[6] & synd[7];
assign flip[50] = synd[5] & synd[6] & synd[7];
assign flip[51] = synd[0] & synd[1] & synd[2] & synd[3] & synd[6];
assign flip[52] = synd[0] & synd[4] & synd[6];
assign flip[53] = synd[0] & synd[5] & synd[6];
assign flip[54] = synd[1] & synd[5] & synd[6];
assign flip[55] = synd[1] & synd[4] & synd[6];
assign flip[56] = synd[0] & synd[4] & synd[7];
assign flip[57] = synd[0] & synd[5] & synd[7];
assign flip[58] = synd[0] & synd[6] & synd[7];
assign flip[59] = synd[1] & synd[2] & synd[3] & synd[4] & synd[7];
assign flip[60] = synd[1] & synd[5] & synd[7];
assign flip[61] = synd[1] & synd[6] & synd[7];
assign flip[62] = synd[2] & synd[6] & synd[7];
assign flip[63] = synd[2] & synd[5] & synd[7];


    

    assign corr_word = data ^ flip ; 


    ////////// REGISTER INPUT CODEWORD ////////////////

    always @(posedge clk or negedge reset_n) begin
        if (!reset_n) 
            // reset
            codereg <= 0 ;
        
        else if (enable)  
            codereg <= i_code; 
         
    end

    ////////// MUX OUTPUT THAT FEEDS THE OUTPUT REGISTER //////////
    always @(corr_word or data or fall_thru) begin 

        case (fall_thru)
            1'b1: sel_dout = data ; 
            1'b0: sel_dout = corr_word ; 
        endcase 
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
            o_err_fatal <= ~correctible ; // has error AND no column-match. 2+ errors  
            o_valid <= 1 ; 
            
        end
    end



    endmodule 
    //--------- end of file ------//

    
