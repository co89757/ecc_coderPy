### scratchpad for simple scripts running in the current dir 

import os,sys; p=os.getcwd() ; sys.path.append(p) 

import bch2pad, bch3dpad,crcpad, tbcoder

# bch2pad.main(64) 

# bch3dpad.bch3dCodeGen(k=64)  

# crcpad.main(r=6,k=64)

# tbcoder.decodertb('bch',64,78)

# tbcoder.decodertb('bch3d',64, 79) 

# tbcoder.decodertb('crc',64,70) 

tbcoder.decodertb('secded2',128,137)

# tbcoder.decodertb('crc',128,134) 