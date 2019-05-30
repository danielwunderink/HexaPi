Testing Git hub edits

from PS3 import *
import pygame, sys, time, os
from pygame.locals import *
pygame.init()
pygame.joystick.init()

#Check if there are any controllers connected
print "Initialize"
print "Searching for controller..."
found = False

while not found:
    joysticks = 0
    joysticks = pygame.joystick.get_count()
    if joysticks:
        print str(joysticks) + " Controller detected"
        for i in range(joysticks):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            joystick_name = joystick.get_name()
            print "Joystick " + str(1) + " name: " + joystick_name
        found = True
    else:
        break

P = ps3()
P.update() 
print "press Start to begin"
print "press Select to exit"
while not P.select:
    P.update() 
    if P.start:
        print "Reading Controller inputs"
        import Controls_Inputs
    time.sleep(.01)
print "Code Terminated"
            
        
        
        
