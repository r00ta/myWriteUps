# kiss - DEFCON 2016

I solved this challenge after competition's end. During the competition i didn't found a "stack pivoting" gadget. Leak the libc used on server was (IMHO) impossible, so i decided to switch challenge. 

Today i found this write up of the challenge http://sibears.ru/labs/DEF-CON-CTF-Quals-2016-kiss/ , so they wrote the exploit using the standard linker of Ubuntu 14.04 and the exploit worked also on their server. So i wrote my exploit using the gadget that they used (unlucky me, i also had this version of the linker, but i decided to not spend no more time triyng a blind exploit on the linker)

```asm
	mov    rsp,rbx
	mov    rbx,QWORD PTR [rsp]
	add    rsp,0x30
	ret
```

The full exploit is available [here](exploit.py)!  