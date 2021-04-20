# Initialization

from Adafruit_PWM_Servo_Driver import PWM
import time

pwm1 = PWM(0x40)
pwm2 = PWM(0x41)
pwm1.setPWMFreq(50)
pwm2.setPWMFreq(50)
channel = 5
start   = 120
mid     = 340
end     = 560
pwm = pwm1


def my_range(start, end, step):
    while start <= end:
        yield start
        start += step


pwm.setPWM(channel, 0, start)
time.sleep(2)
pwm.setPWM(channel, 0, mid)
time.sleep(2)
pwm.setPWM(channel, 0, end)
time.sleep(2)
pwm.setPWM(channel, 0, start)
time.sleep(2)

# angle to pulse
min_angle   = start
slope       = 2.444





for angle in my_range(1, 180, 0.5):
    pulse = angle*slope + min_angle
    pulse = int(pulse)
    pwm.setPWM(channel, 0, pulse)
    time.sleep(0.01)

time.sleep(0.25)
pwm.setPWM(channel, 0, mid)

for chan in range(0,5):
	pwm1.setPWM(chan, 0, mid)

for chan in range(0,5):
	pwm2.setPWM(chan, 0, mid)

for chan in range(8,13):
	pwm2.setPWM(chan, 0, mid)
