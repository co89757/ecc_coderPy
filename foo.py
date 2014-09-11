import collections
import functools

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)


@memoized
def factorial(n):
  "factorial n!"
  if n <= 1:
    return 1 
  else:
    return n*factorial(n-1) 


def nCr(n,r):
  "compute nCr" 
  if r == 0:
    return 1 
  z = factorial(n)/(factorial(r)*factorial(n-r)) 

  return z 

def dbinom(n,k,p):
  "binomial distribution density at (n,k) with probability p "
  d = nCr(n,k)*(p**k)*((1-p)**(n-k))
  return d 


def Pfail(n,p2,p4,perr):
  pfail = p2*dbinom(n,2,perr) + p4*dbinom(n,4,perr) ## only even number errors cause detection fails 
  return pfail 


####### write csv file Pfail as a function of perr for varying CRC-? 
def crcFailRec(r,k,p2,p4):
  "CRC-r's Pfail vs perr data in csv "

  n = k+r 
  perr = 1e-3   
  outs = ''
  while(dbinom(n,4,perr)/dbinom(n,6,perr) > 15): #### assumption for ignoring >= 6 errors 
    pfail = Pfail(n,p2,p4,perr)   
    outs += "CRC{order},{berpercent},{failpercent:.5f},{wd} \n".format(order=r, berpercent=perr*100, failpercent=pfail*100,wd=k )
    perr += 0.001 

  return outs 


def csvWrite(k):

  #### fail rate for P2e and P4e respectively for CRC-r on 32/64bits. 
  pf_32 = {3:(.314,.247), 4:(.119, .124), 5:(.0435, .064), 6:(.01, .033), 7:(0, .01633)} 
  pf_64 = {4:(.13038, .12432), 5:(.05371, .06271), 6:(.01946, .03169), 7:(.00322, .0161),8:(0, 0.00797) }

  pf_select = {32:pf_32, 64:pf_64} 


  f = open('crcpfail.csv','a') 
  # print >>f, 'ECC,Perr,Pfail,Wordsize' 
  pf = pf_select[k] 

  for r in pf:
    p2 = pf[r][0] 
    p4 = pf[r][1] 
    f.write(crcFailRec(r, k, p2, p4) ) 


  f.close() 











def nerrCases(r,k,maxn):
  "return the number of error locations when #err max up to maxn, and C(k,r)"
  tot = 0
  n = k+r 
  for nerr in xrange(maxn+1):
    tot += nCr(n,nerr) 

  return tot 





def main():
   # k=64 
   # for r in xrange(4,9):
   #   for i in xrange(1,6):
   #     z = nerrCases(r,k,i)
   #     print 'for (k,r) = ({0},{1}), number of error combinations up to {2} is {3}'.format(k,r, i, z) 
   # n = 38 
   # p = 1e-4
   # print "p(4err) = ", dbinom(n,4,p) 
   # print 'p(6err) = ', dbinom(n,6,p) 
   # print dbinom(n,4,p)/dbinom(n,6,p) 

   # csvWrite(32)
   csvWrite(64) 


if __name__ == '__main__':
  main()