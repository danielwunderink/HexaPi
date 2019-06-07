# Initialization
from Adafruit_PWM_Servo_Driver import PWM
from First_try import moveto
import time

pwm = PWM(0x40)
pwm.setPWMFreq(60)

channel = 5
slope = 2.833
min_pulse = 150
angle_i = 0
pulse_i = angle_i * slope + min_pulse
pwm.setPWM(channel, 0, int(pulse_i))
leave = 0
speed = 50

while leave == 0:

    #Test Code

    angle_f = input('enter value between 0 and 180: ')
    
    def my_range(start, end, step):
        while start <= end:
            yield start
            start += step

    for angle in my_range(angle_i, angle_f, speed):
        pulse = angle * slope + min_pulse
        pwm.setPWM(channel, 0, int(pulse))
        print angle
        print pulse

           
    angle_i = angle_f
    leave = input('Exit the program? (y:1 or n:0) ')

pwm.setPWM(channel, 0, int(pulse_i))
