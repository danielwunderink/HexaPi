#If button is pressed then do something
from PS3 import *
P = ps3()
P.update()
print "press Select to exit."
channel_0x40 = 0
channel_0x41 = 0

while not P.select:
    P.update()
    if P.start:
        print "Start"
    if P.triangle:
        print "Tiangle"
        import Spread
    if P.circle:
        print "Circle"
    if P.square:
        print "Square"
    if P.cross:
        print "Cross"
    if P.left:
        if not channel_0x40 == 0:
            time.sleep(0.2)
            channel_0x40 -= 1
        time.sleep(0.1)
        print "0x40: {}".format(channel_0x40)
    if P.right:
        if not channel_0x40 == 16:
            time.sleep(0.2)
            channel_0x40 += 1
        time.sleep(0.1)
        print "0x40: {}".format(channel_0x40)
    if P.up:
        if not channel_0x41 == 16:
            time.sleep(0.2)
            channel_0x41 += 1
        time.sleep(0.1)
        print "0x41: {}".format(channel_0x41)
    if P.down:
        if not channel_0x41 == 0:
            time.sleep(0.2)
            channel_0x41 -= 1
        time.sleep(0.1)
        print "0x41: {}".format(channel_0x41)
    if P.l1:
        print "L1"
    if P.l2:
        print "L2"    
    if P.r1:
        print "R1"
    if P.r2:
        print "R2"
    if P.ps:
        print "PS button"
    time.sleep(0.005)
