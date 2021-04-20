import sys, time, os, math, threading
from Adafruit_PWM_Servo_Driver import PWM

pwm0 = PWM(0x40)
pwm1 = PWM(0x41)
pwm0.setPWMFreq(50)
pwm1.setPWMFreq(50)

start_time = time.time()
pwm0.setPWM(0, 0, 300)	
print("--- %s ---" % (time.time() - start_time))
