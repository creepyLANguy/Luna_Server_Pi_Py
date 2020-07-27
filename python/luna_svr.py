import socket
import struct

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


#HOST = "192.168.8.120"
HOST = "127.0.0.1"

PORT = 8886

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
print("Listening on UDP %s:%s" % (HOST, PORT))

# Create NeoPixel object with appropriate configuration.
#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
#strip.begin()


while True:
    #(data, addr) = s.recvfrom(4)
    (data, addr) = s.recvfrom(8)#64bit Windows hack
    #print(str(data))
   
    num = int.from_bytes(data, 'little')
    #print(num)
   
    sb = str("{0:b}".format(num)).zfill(32)    
    sb = sb[32:64]#64bit Windows hack
    print(sb)
   
    ib = sb[0:8]
    i = int(ib, 2)
    print("i : " + ib + " = " + str(i))
    
    #rb = sb[8:16]
    #r = int(rb, 2)
    #print("r : " + rb + " = " + str(r))
    #
    #gb = sb[16:24]
    #g = int(gb, 2)
    #print("g : " + gb + " = " + str(g))
    #
    #bb= sb[24:32]
    #b = int(bb, 2)
    #print("b : " + gb + " = " + str(b))
   
    print(str(i) + " | " + str(r)  + " | " + str(g) + " | " + str(b))
    #print(str(i))
    print()
    
    #strip.setPixelColor(i, sb)
    #strip.show()
    
