#!/usr/bin/env python2
 
import sys, socket, telnetlib
from struct import *
import os
import time
 
from subprocess import check_output
 
def get_pid(name):
    try:
        return check_output(["pidof",name])
    except:
        return ""
 
def recvuntil(t):
    data = ''
    while not data.endswith(t):
        tmp = s.recv(1)
        if not tmp: break
        data += tmp
 
    return data
 
def recv_all(decode = True):
    if decode:
        os.system("(minimodem --rx 1200 -8 -R 48000 -q > /tmp/data_in_decoded) & ")
    data = ''
    f = open("/tmp/data_in.dat", "wb")
    i = 0
    recv_size = 8196
    aplay_started = 0
    while i != -1:
        i += recv_size
        if (i == recv_size*150):
            aplay_started = 1
            if decode:
                os.system("aplay -r 48000 -f FLOAT_LE /tmp/data_in.dat &")
        if (aplay_started == 1 and decode):
            if get_pid("aplay") == '':
                f.close()
                return
        try:
            if (i >= recv_size * 500 and recv_size < 8192 * 8):
                print "increasing" + str(recv_size)
                recv_size *= 2
            data = s.recv(recv_size)
            f.write(data)
            f.flush()
        except Exception as e:
            print e
            return data
    return data
 
def interactive():
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()
 
def recv_data(decode = True):
    print "receiving"
    recv_all(decode)
    print "finished"
   
    os.system("pkill minimodem")
    os.system("pkill aplay")
 
    f = open("/tmp/data_in_decoded", "r")
    data = f.read()
    return data
 
def send_data(message):
    os.system("(arecord -r 48000 -f FLOAT_LE > /tmp/data_out.dat) &")
    open("/tmp/data_out.txt", "w").write(message)
    os.system("cat /tmp/data_out.txt | minimodem --tx 1200 -8 -R 48000 -q")
 
    time.sleep(1)
 
    os.system("pkill minimodem")
    os.system("pkill arecord")
 
    data = open("/tmp/data_out.dat", 'rb').read()
    s.send(data)
 
def p32(x): return pack('<I', x)
def u32(x): return unpack('<I', x)[0]
def p64(x): return pack('<Q', x)
def u64(x): return unpack('<Q', x)[0]
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))
# s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
 
data = recv_data()
print data
 
send_data("Jacopo\n")
 
data = recv_data()
print data
 
send_data("F\n")
 
data = recv_data()
print data
 
send_data("2\n")
 
data = recv_data(False)
print data
 
# interactive()
 
s.close()
