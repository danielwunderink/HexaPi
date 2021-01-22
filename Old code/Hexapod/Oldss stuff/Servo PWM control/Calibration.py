# Initialization

from Adafruit_PWM_Servo_Driver import PWM
import time

pwm1 = PWM(0x40)
pwm2 = PWM(0x41)
pwm1.setPWMFreq(60)
pwm2.setPWMFreq(60)
channel = 4
start   = 160
mid     = 360
end     = 595

pwm2.setPWM(channel, 0, start)
time.sleep(2)
pwm2.setPWM(channel, 0, mid)
time.sleep(2)
pwm2.setPWM(channel, 0, end)
time.sleep(2)
pwm2.setPWM(channel, 0, mid)


# angle to pulse
#min_angle   = 150
#slope       = 2.833

#def my_range(start, end, step):
#    while start <= end:
#        yield start
#        start += step



#for angle in my_range(1, 180, 0.5):
#    pulse = angle*slope + min_angle
#    pulse = int(pulse)
#    pwm.setPWM(channel, 0, pulse)
#    time.sleep(0.00001)

#time.sleep(0.25)
#pwm.setPWM(channel, 0, start)
