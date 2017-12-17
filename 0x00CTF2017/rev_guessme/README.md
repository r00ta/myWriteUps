#guessme - 0x00CTF 2017

First at all execute `file` command on the binary
```bash
$ file guessme
guessme: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=92b1d84ee22b7c92dc80fac971bdc7f6cd0e3672, stripped
```

The challenge is a standard crackme: we have to insert the correct key to get the flag.

```bash
$ ./guessme
Enter a key: hello
FAIL
```

After a little bit of debugging i realized that the program checks first of all that the lenght of the input key is 14, and then starts checking every char starting from the first one. Easy! I used my [pintool](https://github.com/r00ta/pintool). And playing a little bit with the parameters i got the key ;)

```bash
$ python pintool.py -a 64 ../reverse/00x0CTF/guessme -l 14 -c 6 -d '=> 49'
a_____________ = 2075437 difference 49 instructions
ab____________ = 2075486 difference 49 instructions
abb___________ = 2075535 difference 49 instructions
abbc__________ = 2075584 difference 49 instructions
abbcd_________ = 2075633 difference 49 instructions
abbcdf________ = 2075682 difference 49 instructions
abbcdfi_______ = 2075731 difference 49 instructions
abbcdfin______ = 2075780 difference 49 instructions
abbcdfinv_____ = 2075829 difference 49 instructions
abbcdfinvi____ = 2075878 difference 49 instructions
abbcdfinvid___ = 2075927 difference 49 instructions
abbcdfinvidl__ = 2075976 difference 49 instructions
abbcdfinvidlo_ = 2076025 difference 49 instructions
abbcdfinvidloz = 2078469 difference 2444 instructions
Password:  abbcdfinvidloz
```

and the flag ;)

```bash
$ ./guessme
Enter a key: abbcdfinvidloz
Good key!
The flag is: 0x00CTF{abbcdfinvidloz}
```

Find the binary [here](guessme)! 
