#### some shared utilities 
import random,copy,math 

list2hex = lambda v:hex(int(''.join(map(str,v)),2))[2:] 





### ............ generate encoder test cases ........ 

def encTestCases(k,iter):
	"generate encoder databits vector in hex and store it to file  "
	assert k%4==0
	f = open('encTestVec{0}.csv'.format(k),'w')
	charset = '0123456789abcdef'
	for x in xrange(iter):
		prefix = "0x".format(_k=k) 
		# data = "{_k}'h".format(_k=k) 
		digits = ''.join([random.choice(charset) for i in xrange(k/4)  ]   )
		# for i in xrange(k/4):
		# 	c = random.choice(charset)
		# 	data += c 
		line = ''.join([prefix, digits]) 
		print >>f , line 

	f.close()

  # noisy_msg = numpy.copy(vin)
  #   cont = 0
  #   for i in range(len(noisy_msg)):
  #       e = random.random() # return a random number in [0,1)
  #       if e < ber:
  #           if noisy_msg[i] == 0:
  #               noisy_msg[i] = 1
  #               cont +=1
  #           else:
  #               noisy_msg[i] = 0
  #               cont +=1
  #           if cont == n_err:  # bit is  #corrupted bits
  #               break
  #   return noisy_msg #return noise mask 

def decTestCases(n,ber,maxn,iter):
	"generate iter randome vectors of length n with BER and error upperbound = maxn"
	width = int(math.ceil(n/4.0) )
	
	f = open("decTestVec{0}.csv".format(n),'w')
	for x in xrange(iter):
		errvec = [0]*n 
		count = 0 
		for i in xrange(len(errvec)):
			p = random.random()
			# print "random p = ",p ### DEBUG 
			if p < ber: ### flip bits 
				errvec[i] = 1 ## flip 
				# print "fliped location i=",i ### DEBUG 
				count += 1
				if count == maxn:
				 	break 

			else:
				continue 
		
		if not any(errvec):
			continue  ## not print out clean vectors 
		hexvec = list2hex(errvec).zfill(width) 
		if hexvec[-1]=='L':
			hexvec = hexvec[:-1] 
		### text output  
		# vector = "{_n}'h{hexnumber}".format(_n = n, hexnumber=hexvec)
		# line = "# 10 CODE_IN = " + vector + ';' 
		vector = "0x{0}".format(hexvec)
		print >>f , vector  

	f.close()




				
		
if __name__ == '__main__':

	
		decTestCases(137,.03,3,1000)
		# decTestCases(144,.03,2,1000)
		# decTestCases(145,.03,3,1000)
		
		
