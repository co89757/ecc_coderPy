# code generator for Hsiao SECDED code 
# Parity matrix = NameMatrix.transpose() 

import sys,os
p=os.getcwd() ; sys.path.append(p) 

from toyhamm import HsiaoName16,HsiaoName32,HsiaoName64 
import math 
import numpy as np 
# ------------------------------------------------------------------------
# ----------------------- Modular Helper Functions ------------------------
# -------------------------------------------------------------------------

wd2N = {16:HsiaoName16, 32:HsiaoName32, 64:HsiaoName64} # wordsize to name matrix table 

# Parity bits generation for Hsiao 
def paritygen(wdsize):
    "check bits Generator for Hsiao" 
    assert wdsize in (16,32,64) 
    NameMat = wd2N[wdsize]  # get name matrix (rxn)
    # f = open('paritygen_code.txt','w') # file IO 
    result_s = ''  #string return 
    for rowid,row in enumerate(NameMat):
        s = 'assign par[{0}] = '.format(rowid) 
        incl_d_index = np.nonzero(row) 
        incl_d_index = incl_d_index[0].astype('int') # get a array of included databit indices 
        for i in incl_d_index:
            ss = 'datareg[{0}] ^ '.format(i) if i != incl_d_index[-1] else 'datareg[{0}];'.format(i) 
            s += ss 
        # print >>f, s  #file IO
        s += '\n' # string return

        result_s += s #string return 

    return result_s #string return 

    # f.close() 
# -----------------------------------------------------
#syndrome bits generation of Hsiao code 
def syndgen(wdsize):
    NameMat = wd2N[wdsize] 
    result_s = ''  #string return 
    for rowid,row in enumerate(NameMat):
        s = 'assign synd[{0}] = chk[{0}] ^ '.format(rowid) 
        incl_d_index = np.nonzero(row) 
        incl_d_index = incl_d_index[0].astype('int') # get a array of included databit indices 
        for i in incl_d_index:
            ss = 'data[{0}] ^ '.format(i) if i != incl_d_index[-1] else 'data[{0}];'.format(i) 
            s += ss 
        # print >>f, s  #file IO
        s += '\n' # string return

        result_s += s #string return 

    return result_s #string return 


#wordsize to parity matrix[kxr] mapping 
k2pmap= {16:HsiaoName16.transpose(), 32:HsiaoName32.transpose(), 64:HsiaoName64.transpose()} 


# -----------------------------------------------------
# Hsiao syndrome solver 
def syndsolve(wdsize):
    "syndrome decoding code generation"
    # NameMat = wd2N[wdsize]
    r = int(math.ceil(math.log(wdsize, 2)) ) + 2 

    P = k2pmap[wdsize] # get the full parity matrix <kxr>   
    # r = k2rmap[wdsize] 
    finals = '' 
    s1='assign noerr = '
    for i in xrange(r):
        ss = '~synd[{0}] & '.format(i) if i !=r-1 else '~synd[{0}];'.format(i) 
        s1 += ss 

    s1 += '\n' 

    finals += s1 

    neg = lambda x: '~' if x==0 else '' 

    s2 = ''

    for idx, name in enumerate(P):
        flip_s = 'assign flip[{0}] = '.format(idx) 
        for i, n in enumerate(name):
            subs = '{sign}synd[{index}] & '.format(sign= neg(n), index = i) if i != r-1 else '{sign}synd[{index}];'.format(sign=neg(n), index=i) 
            flip_s += subs 
        s2 = s2 + flip_s + '\n' 


    finals += s2 

    return finals   


# NEW :OPTIMIZED syndrome decoding. ONLY and the set bits of a syndrome to locate error 
def syndSolveLazy(wdsize): # PENDING to debug
    """Lazy syndrome decoding. 
    only AND set bits in a correctible syndrome pattern to locate error
    given Parity Matrix P[kxr] a numpy array """
    # NameMat = wd2N[wdsize]
    r = int(math.ceil(math.log(wdsize, 2)) ) + 2 
     
    P = k2pmap[wdsize] # get the full parity matrix <kxr>   
    assert P.shape[0]==wdsize and P.shape[1]==r 
    finals = '' 
    s1='assign noerr = '
    for i in xrange(r):
        ss = '~synd[{0}] & '.format(i) if i !=r-1 else '~synd[{0}];'.format(i) 
        s1 += ss 

    s1 += '\n' 

    finals += s1 

    # neg = lambda x: '~' if x==0 else '' 

    s2 = ''

    for idx, name in enumerate(P):
        flip_s = 'assign flip[{0}] = '.format(idx)
        setbit_ind_array = np.nonzero(name)[0].astype('int')  
        for i in setbit_ind_array: # set bit index
            subs = 'synd[{index}] & '.format(index = i) if i != setbit_ind_array[-1] else \
            'synd[{index}];'.format( index=i) 
            flip_s += subs 
        s2 = s2 + flip_s + '\n' 


    finals += s2 

    return finals 






# Hsiao ignore signal generation (if 1 err in parity bits, then ignore) synd[0:r-1] 
# if only 1 set bit in synd[] , then it's an err in parity-bits. Ignore it . 


def ignore(r):
    "generate flag for ignore parity err "
    reduced_sum_width = int(math.floor(math.log(r,2)) ) + 1 
    line1="wire [{topid}:0] sbitsum = ".format(topid=reduced_sum_width-1)  
    for i in xrange(r):
        item = "synd[{0}] + ".format(i) if i < r-1 else 'synd[{0}];\n'.format(i) 
        line1 += item 

    line2 = "wire ignore = (sbitsum==1)? 1:0; \n" 

    return (line1+line2) 



# //////////////////////// END OF HELPERS /////////////////////////////////



#-------------------- Verilog Code Generator for Hsiao SECDED  [APPENDING CHECK BITS ]-------------------------

# Hsiao encoder .v file generator 
def hsiaoEncGen(wdsize): # PENDING 
    "Verilog code Generator for SECDED encoder" 
    r = int(math.ceil(math.log(wdsize, 2)) ) + 2 
    n = r + wdsize # block length 
    f = open("hsiao_{0}_enc.v".format(wdsize),'w') 
    header = """ 
    module hsiao_{wdwidth}_enc(
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
    input [0:{dLSBid}] i_data;

    //----OUTPUT PORTS----
    output [0:{codeLSBid}] o_code;
    output o_valid;

    //---INTERNAL SIGNALS --
    reg [0:{dLSBid}] datareg ; // OPTIONAL  input register 
    reg o_valid;
    reg [0:{codeLSBid}] o_code;

    // reg enreg; 
    wire [0:{ckLSBid}] par ;//parity (check bits) 
    """.format(wdwidth=wdsize, dLSBid=wdsize-1, codeLSBid=n-1, ckLSBid=r-1) 

    print >>f, header 

    paritygen_text = paritygen(wdsize)

    print >>f, paritygen_text   

    tail = """

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
            // appending parity bits 
            o_valid <= 1 ;
        end
      
                
        
    end




    endmodule 
    //---- end of file -----//  
     """ 

    print >>f, tail 

    f.close() 


# ------------ Hsiao Decoder ----------
def HsiaoDecGen(wdsize):
    r = int(math.ceil(math.log(wdsize, 2)) ) + 2  
    n = r + wdsize # block length 
    f = open("hsiao_{0}_dec.v".format(wdsize),'w') 

    head = """ 
    module hsiao_{Wsize}_dec (
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
    input [0:{Ctopid}] i_code;


    //------OUTPUT PORTS -----
    output [0:{Wtopid}] o_data;
    output o_valid;
    output o_err_corr;
    output o_err_detec;
    output o_err_fatal;

    //---- INTERNAL VARIABLES ---

    reg [0:{Ctopid}] codereg ;
    reg o_err_fatal;
    reg o_err_detec;
    reg o_err_corr;
    reg o_valid;
    wire noerr; 
    
    wire [0:{Wtopid}] corr_word; 


    wire [0:{Ptopid}] synd ; 
    wire [0:{Wtopid}] flip ; // databits error mask 
    reg [0:{Wtopid}] o_data; 
    wire[0:{Ptopid}] chk = codereg[{Pstartid}:{Pstopid}]; //extract the checkbits 

    wire [0:{Wtopid}] data = codereg[0:{Wtopid}] ; //extract databits

    //---STATEMENTS 
     
    

    """.format(Wsize=wdsize, Ctopid=n-1, Wtopid=wdsize-1, Ptopid=r-1, Pstartid=wdsize, Pstopid=n-1) 




    print >>f, head 
    print >>f, ignore(r) # incl. ignore flag to ignore err in parity part 

    print >>f, "//--------- Syndrome Generation -------//"

    print >>f, syndgen(wdsize) 

    print >>f, "//--------- Syndrome Decoding ----------//"

    print >>f, syndsolve(wdsize) 

    tail = """
    

    assign corr_word = data[0:{Wtopid}] ^ flip[0:{Wtopid}]; 


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
            o_err_fatal <= ~(| flip) & ~noerr & ~ignore; // has error AND no column-match. 2+ errors  
            o_valid <= 1 ; 
            
        end
    end



    endmodule 
    //--------- end of file ------//

     """.format(Wtopid=wdsize-1, Ptopid=r-1) 

    print >>f, tail 

    f.close() 


#### ------ Optimized Hisao Decoder using Lazy Syndrome Decoding ---- 

def Hsiao2DecGen(wdsize):
    r = int(math.ceil(math.log(wdsize, 2)) ) + 2  
    n = r + wdsize # block length 
    f = open("hsiao2_{0}_dec.v".format(wdsize),'w') 

    head = """ 
    module hsiao2_{Wsize}_dec (
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
    input [0:{Ctopid}] i_code;


    //------OUTPUT PORTS -----
    output [0:{Wtopid}] o_data;
    output o_valid;
    output o_err_corr;
    output o_err_detec;
    output o_err_fatal;

    //---- INTERNAL VARIABLES ---

    reg [0:{Ctopid}] codereg ;
    reg o_err_fatal;
    reg o_err_detec;
    reg o_err_corr;
    reg o_valid;
    wire noerr; 
    
    wire [0:{Wtopid}] corr_word; 


    wire [0:{Ptopid}] synd ; 
    wire [0:{Wtopid}] flip ; // databits error mask 
    reg [0:{Wtopid}] o_data; 
    wire[0:{Ptopid}] chk = codereg[{Pstartid}:{Pstopid}]; //extract the checkbits 

    wire [0:{Wtopid}] data = codereg[0:{Wtopid}] ; //extract databits

    wire correctible = ^synd & ~noerr; // correctible (1err) 
    wire fall_thru = noerr | ~correctible; // fall-through when fatal or clean 
    reg [0:{Wtopid}] sel_dout; //selected data output, either corrected data or fall through bits 

    //---STATEMENTS 
     
    

    """.format(Wsize=wdsize, Ctopid=n-1, Wtopid=wdsize-1, Ptopid=r-1, Pstartid=wdsize, Pstopid=n-1) 




    print >>f, head 

    print >>f, "//--------- Syndrome Generation -------//"

    print >>f, syndgen(wdsize) 

    print >>f, "//--------- Syndrome Decoding ----------//"

    print >>f, syndSolveLazy(wdsize) ## using lazy syndrome decoding 

    tail = """
    

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

     """.format(Wtopid=wdsize-1, Ptopid=r-1) 

    print >>f, tail 

    f.close() 
































def main(k):
    "generate both enc/dec file , a wrapper routine"

    hsiaoEncGen(k)
    HsiaoDecGen(k)