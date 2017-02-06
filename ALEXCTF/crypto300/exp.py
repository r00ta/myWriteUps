#!/usr/bin/env python2

import sys, socket, telnetlib
from struct import *
import random
import time
import binascii
import time
def recvuntil(t):
    data = ''
    while not data.endswith(t):
        tmp = s.recv(1)
        if not tmp: break
        data += tmp

    return data

def interactive():
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()

def p32(x): return pack('<I', x)
def u32(x): return unpack('<I', x)[0]
def p64(x): return pack('<Q', x)
def u64(x): return unpack('<Q', x)[0]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))


f = open("file1.txt","wb")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))
i = 0
mySet = set()
while 1:
	print "i : " + str(i)
	i += 1
	recvuntil("2: Give me the next number\n")
	s.send("2\n")
	number = recvuntil("\n")
	mySet.add(int(number[:-1],10))
	f.write(str(i) + " " + number[:-1] + "\n")
	if(i != len(mySet)):
		f.close()
		print "GOT IT!!!"
		print i
		interactive()
