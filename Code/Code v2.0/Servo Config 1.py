# Initialization

from Adafruit_PWM_Servo_Driver import PWM
import time

pwm0 = PWM(0x40)
pwm1 = PWM(0x41)
pwm0.setPWMFreq(50)
pwm1.setPWMFreq(50)
channel = 12
start   = 250
mid     = 350
end     = 400
pwm = pwm1


def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

for chan in range(0,6):
	pwm0.setPWM(chan, 0, start)
	time.sleep(0.1)
	pwm0.setPWM(chan, 0, end)
	time.sleep(0.1)
	pwm0.setPWM(chan, 0, mid)

for chan in range(0,6):
	pwm1.setPWM(chan, 0, start)
	time.sleep(0.1)
	pwm1.setPWM(chan, 0, end)
	time.sleep(0.1)
	pwm1.setPWM(chan, 0, mid)

for chan in range(8,14):
	pwm1.setPWM(chan, 0, start)
	time.sleep(0.1)
	pwm1.setPWM(chan, 0, end)
	time.sleep(0.1)
	pwm1.setPWM(chan, 0, mid)
