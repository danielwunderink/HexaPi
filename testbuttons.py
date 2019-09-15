import threading, subprocess
import RPi.GPIO as GPIO
import time

while 1:
    time.sleep(0.25)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if GPIO.input(7)!=True:
        print('High')
