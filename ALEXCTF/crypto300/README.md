# Bring weakness (crypto300) - ALEX CTF

That was a funny challenge. We have to connect to a server and guess 10 numbers randomly generated consecutively in order to get the flag. The 
usage is very simple

```bash
$ nc 195.154.53.62 7412
Guessed 0/10
1: Guess the next number
2: Give me the next number
2
2882282195
Guessed 0/10
1: Guess the next number
2: Give me the next number
2
3616041256
Guessed 0/10
1: Guess the next number
2: Give me the next number
..
..
..
```

A (very) little theory.. A good random number generator should have high entropy. Infact if the random generator returns a number that i saw 
few time ago, i can guess the next generated number easily (it generates the next number depending from the previous one!). My first idea was to always ask the next random numer, save it and see if I've encountered it in the past. It always happens sooner (if the generator is weak) or later (if the generator is well made). So even if the genator is well made it happens, but we should wait so long that we would all be dead :D

So that's my very simple POC exploit.. but hey.. we know that it is weak :D  Let's see!

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
```

i know that it looks like shit, but it works! After 32768 iterations i got a repeated number: i looked at the file saved and 
interactively send the correct numbers and i got the flag 

```bash
..
..
..
i : 32761
i : 32762
i : 32763
i : 32764
i : 32765
i : 32766
i : 32767
i : 32768
GOT IT!!!
32769
Guessed 0/10
1: Guess the next number
2: Give me the next number
1
Next number (in decimal) is
1198007487
Guessed 1/10
1: Guess the next number
2: Give me the next number
1
Next number (in decimal) is
1196723700
Guessed 2/10
1: Guess the next number
2: Give me the next number
1
Next number (in decimal) is
3223035981
Guessed 3/10
1: Guess the next number
2: Give me the next number
1
Next number (in decimal) is
3629331723
Guessed 4/10
1: Guess the next number
2: Give me the next number
1
Next number (in decimal) is
216206427
Guessed 5/10
1: Guess the next number
2: Give me the next number
1
Next number (in decimal) is
1252512825
Guessed 6/10
1: Guess the next number
2: Give me the next number
1
Next number (in decimal) is
3100277946
Guessed 7/10
1: Guess the next number
2: Give me the next number
1
Next number (in decimal) is
3166866393
Guessed 8/10
1: Guess the next number
2: Give me the next number
1
Next number (in decimal) is
3024820857
Guessed 9/10
1: Guess the next number
2: Give me the next number
1
Next number (in decimal) is
645079395
flag is ALEXCTF{f0cfad89693ec6787a75fa4e53d8bdb5}
```

The script is [here](exploit.py), and the file saved [here](file.txt). I know that saving all the numbers was unnecessary, but i wrote this very quickly and i didn't have time to reorganize the script: i apologize for that :D