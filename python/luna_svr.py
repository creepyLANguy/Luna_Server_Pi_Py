import socket
import struct

#HOST = "192.168.8.120"
HOST = "127.0.0.1"

PORT = 8886

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
print("Listening on UDP %s:%s" % (HOST, PORT))

while True:
    (data, addr) = s.recvfrom(4)
    #print(str(data))
   
    num = int.from_bytes(data, 'little')
    #print(num)
   
    sb = str("{0:b}".format(num)).zfill(32)    
    print(sb)
   
    ib = sb[0:8]
    i = int(ib, 2)
    print("i : " + ib + " = " + str(i))
   
    rb = sb[8:16]
    r = int(rb, 2)
    print("r : " + rb + " = " + str(r))
   
    gb = sb[16:24]
    g = int(gb, 2)
    print("g : " + gb + " = " + str(g))
   
    bb= sb[24:32]
    b = int(bb, 2)
    print("b : " + gb + " = " + str(b))
   
    #print(str(i) + " | " + str(r)  + " | "  + " | " + str(g) + " | " + str(b))
    #print(str(i))
    print()