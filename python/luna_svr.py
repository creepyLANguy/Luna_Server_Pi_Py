#!/usr/bin/sudo python3

import sys
import os

import socket
import struct
import threading

import queue

import board
import neopixel
import time

MAX_INDEX = 249
CONFIG_INDEX = 250
SHUTDOWN_PI_INDEX = 251
RESTART_PI_INDEX = 252
FILL_INDEX = 255

# LED strip configuration:
LED_COUNT      = 28      # Number of LED pixels.
LED_BRIGHTNESS = 0.5     # [0.0, 1.0]
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
ORDER = neopixel.GRB
BOARD_PIN = board.D18
AUTO_WRITE = False


if len(sys.argv) > 1:
    LED_BRIGHTNESS = float(int(sys.argv[1])/100)
    LED_COUNT = int(sys.argv[2])

print("Initialising strip with brightness : " + str(LED_BRIGHTNESS) + ", count : " + str(LED_COUNT))

pixels = neopixel.NeoPixel(BOARD_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=AUTO_WRITE, pixel_order=ORDER)


HOST = "192.168.0.174" # Update to hosts's IP
PORT = 8886

print("Sleeping for 10 seconds in case this is running on boot...")
time.sleep(10)

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
            pixels.show()
            print("-->\tOUT\t" + str(item[0]) + "\t|" + str(item[1]) + "\t|" + str(item[2]) + "\t|" + str(item[3]))

qprocessor = threading.Thread(target=processQueue)
qprocessor.start()

while True:
    (data, addr) = s.recvfrom(4)
    #(data, addr) = s.recvfrom(8)#64bit Windows hack

    num = int.from_bytes(data, 'little')

    sb = str("{0:b}".format(num)).zfill(32)#DO WE EVEN NEED TO ZFILL HERE?!
    #sb = sb[32:64]#64bit Windows hack

    ib = sb[0:8]
    i = int(ib, 2)

    rb = sb[8:16]
    r = int(rb, 2)
    if r == 0:
        r = 1

    gb = sb[16:24]
    g = int(gb, 2)
    if g == 0:
        g = 1

    bb= sb[24:32]
    b = int(bb, 2)
    if b == 0:
        b = 1

    if q.full() == True:
        q.get()

    if i > MAX_INDEX:
        if i == FILL_INDEX:
            pixels.fill((r,g,b))
            pixels.show()
            print("<-->\t[ALL]\t" + str(r) + "\t|" + str(g) + "\t|" + str(b))
            q.queue.clear()
        elif i == CONFIG_INDEX:
            print("Configuration packet received.\nRestarting with : " + str(g) + "|" + str(b))
            os.execv(sys.executable, ['python3'] + [sys.argv[0]] + [str(g),str(b)])
        elif i == SHUTDOWN_PI_INDEX:
            print("Shutdown packet recieved. Shutting down entire system immediately.")
            os.system("shutdown now -h")
        elif i == RESTART_PI_INDEX:
            print("Restart packet recieved. Restarting entire system immediately.")
            os.system("shutdown now -r")
        else:
            print("UNIMPLEMENTED PACKET TYPE")
    else:
        q.put((i,r,g,b))
        print("<--\tIN\t" + str(i) + "\t|" + str(r)  + "\t|" + str(g) + "\t|" + str(b))
