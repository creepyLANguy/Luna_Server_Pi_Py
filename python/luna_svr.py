import socket
import struct
import threading

import queue

import board
import neopixel

import time

# LED strip configuration:
LED_COUNT      = 30     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
ORDER = neopixel.GRB
BOARD_PIN = board.D18

pixels = neopixel.NeoPixel(BOARD_PIN, LED_COUNT, auto_write=True, pixel_order=ORDER)

HOST = "192.168.8.154"
#HOST = "127.0.0.1"

PORT = 8886

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
print("Listening on UDP %s:%s" % (HOST, PORT))

q = queue.Queue(LED_COUNT)

def processQueue():
    runs = 0
    while True:        
        if q.empty() == False:
            item = q.get()
            pixels[item[0]] = (item[1],item[2],item[3])
#             runs = runs + 1
#             if runs == LED_COUNT:            
#                 pixels.show()
#                 runs = 0
#                 print("STRIP UPDATED!")
            pixels.show()
            print("-->\tOUT\t" + str(item[0]) + "\t|" + str(item[1]) + "\t|" + str(item[2]) + "\t|" + str(item[3]))

qprocessor = threading.Thread(target=processQueue)
qprocessor.start()

while True:
    (data, addr) = s.recvfrom(4)
    #(data, addr) = s.recvfrom(8)#64bit Windows hack
    #print(str(data))
   
    num = int.from_bytes(data, 'little')
    #print(num)
   
    sb = str("{0:b}".format(num)).zfill(32)#DO WE EVEN NEED TO ZFILL HERE??  
    #sb = sb[32:64]#64bit Windows hack
    #print(sb)
   
    ib = sb[0:8]
    i = int(ib, 2)
    #print("i : " + ib + " = " + str(i))
    
    rb = sb[8:16]
    r = int(rb, 2)
    #print("r : " + rb + " = " + str(r))
    
    gb = sb[16:24]
    g = int(gb, 2)
    #print("g : " + gb + " = " + str(g))
    
    bb= sb[24:32]
    b = int(bb, 2)
    #print("b : " + gb + " = " + str(b))
   
    #print(str(i) + " | " + str(r)  + " | " + str(g) + " | " + str(b))
    #print(str(i))
    
    #strip.setPixelColor(i, sb)
    #strip.show()

    if q.full() == True:
        print("!!!!!!FULLLLL!!!!!!")
        removedItem = q.get()
        print("Removed from q : " + removedItem[i])
            
    q.put((i,r,g,b))
    print("<--\tIN\t" + str(i) + "\t|" + str(r)  + "\t|" + str(g) + "\t|" + str(b))
    
    #print()
