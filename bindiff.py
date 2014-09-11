



from bitarray import bitarray

def bindiff(bfile1,bfile2):
	""" 
	compare 2 binary files and show all differing bit locations/indices, one index per line 
	in: binary file 1, binary file 2 for bit-wise comparison. 
	out: Optionally store the flipped-bit index [one index location per line] in a output file 'ebitlog'

	"""

	f1 = open(bfile1,'rb')
	f2 = open(bfile2, 'rb') 

	a1 = bitarray() 
	a2 = bitarray() 

	a1.fromfile(f1) 
	a2.fromfile(f2) 

	f1.close()
	f2.close() 

	assert a1.length() == a2.length() 

	n_bits = a1.length() 

	# if FileOut:
	# 	outf= open('ebitlog','w') 

	for i in xrange(n_bits):
		if a1[i] != a2[i]:
			print 'bit mismatch at index: ',i 
			# if FileOut:
			# 	print >>outf, 'bit mismatch at index: ',i
		else:
			continue  




if __name__ == '__main__':
	f1 = str(raw_input('binary file 1 [full/relative path]: \n')) 
	f2 = str(raw_input('binary file 2: \n'))
	bindiff(f1,f2) 




