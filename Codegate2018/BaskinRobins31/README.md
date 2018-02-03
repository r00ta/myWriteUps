# BaskinRobins31 pwnable -CODEGATE 2018

Just 2 hours of pwning this weekend :( But anyway, i did this exploit! The idea is quite simple and
i have to say "classic". Just leak the libc address and call again the
vulnerable function with the first payload, then send the ropchain built on the libc with a second
payload. See `exploit.py` :) Enjoy!
