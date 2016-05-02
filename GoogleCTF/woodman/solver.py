from z3 import *
import sys

s1cor = int(sys.argv[1])
s2cor = int(sys.argv[2])
dimVector =35
x = BitVec('x', dimVector)
y = BitVec('y', dimVector)
p = BitVec('p',dimVector)
s1 = BitVec('s1',dimVector)
s2 = BitVec('s2',dimVector)
s = Solver()
s.add(p == 4646704883L)
s.add(s1 == s1cor)
s.add(s2== s2cor)
s.add( ( ( ( 2 * x + 3 ) % p ) ^ ( ( 3 * y + 9 ) % p ) )==s1)
s.add(( ( ( 2 * ( ( 2 * x + 3 ) % p )  + 3 ) % p ) ^ ( ( 3 * ( (  3 * y + 9 ) % p) + 9 ) % p ) )==s2)
while s.check() == sat:
	class SecurePrng(object):
		def __init__(self,x,y):
			self.p = 4646704883L
			self.x = x
			self.y = y
		def next(self):
			self.x = (2 * self.x + 3) % self.p
			self.y = (3 * self.y + 9) % self.p
			return (self.x ^ self.y)	
		def getX(self):
			return self.x
		def getY(self):
			return self.y
	m = s.model()
	pMy = 4646704883L
	myObj = SecurePrng(int(str(m[x]))%pMy,int(str(m[y]))%pMy)
	mySol1 = myObj.next()
	mySol2 = myObj.next()
	if mySol1 == s1cor and mySol2 == s2cor and int(str(m[x]))<= pMy and int(str(m[y])) <= pMy :
		print "x = " + str(m[x]) + " ; y = " + str(m[y]) 
	s.add(Or(x != s.model()[x], y != s.model()[y])) # prevent next model from using the same assignment as a previous model
