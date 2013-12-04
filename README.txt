this project is Colin's MS thesis on memory ECC for SCMs.
code include python implementation for a variety of ECC codes like BCH and SEC-DED and TPC 

Nov 21 2013

-) Finished BCH(15,7) enc/dec . debugged success for (15,7) 
-) Fixed some border case bugs in gfield.py and bch.py 
TODO:
*) check-through. scrutiny on border cases 
*) consider how to detect 3 errors in BCH 
*) Larger G,H for eHamming code. test BCH(31,21) etc. 

Nov 22 

-) corrected minimum polynomial table. passed Mem Wd size 16,32,64,128,256. Needs further optimization and tests. Attention to border cases!!! 

-) funny test case: BCH(15,7) 
	original info: in=[1,1,0,0,0,0,1] 
	enc: 110000101001101 
	recv:[1,1,0,0,0,1,1,0,1,0,1,1,1,0,1]
	ep:  000001000010000
	
	assertion error: s3=a.substitute (fin, ...) fin = 0 , that is r(X) mod m3(X) = 0 -->s3=0 
	
	DEBUG RESULT: fixed. fin can be 0 in substitute method. 
-) passed all tests for varying wd size. 
*) add TED detectability. consider CRC code 

Nov 25

-) tested eHamming for all word width range
*) check out CRC and 3-detection in BCH 

Nov 26 
-) devising means to read binary files for testing. use array module in Python. 
use array('B') [read a byte each time] and array.fromfile(f,n) to form a list 

*) how to write a list into binary file
*) numpy/Scipy r/w files. numpy.tofile() check out numpy cookbook


Nov 27 
-) wrote pipeline (coroutines) encoder testbench with command line arguments 
*) finish decoder testbench 

Nov 28 

-) tested testbench.py on jpg file. passed tests. added log files
*) how to enable 3-error detection without mis-correct on BCH ?? 
-) for SEC-DED . if 3 errors, it's possible that syndrome == 0 !!! so SEC,DED will be 0,1 .  
-----------for example -------------
original message:  [1 1 1 0 1 1 0 1 1 1 0 1 1 0 1 0]  parity:  1
encoded msg:  [1 1 1 0 1 1 0 1 1 1 0 1 1 0 1 0 1 0 0 0 1]
received mesage:  [1 1 0 0 1 1 1 1 1 1 0 1 0 0 1 0 1 0 0 0 1]  parity(after pollution):  0
error pattern:  [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
number of errors:  3
syndrome vector:  [0 0 0 0 0]
The impossible occurs, something wrong! fatal 
----------------------------------------



Dec 2 
*) to write a adaptor : long list --> binary file for encoder printout 
*) draft SECDED RTL design 
