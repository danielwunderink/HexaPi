# Initialization

from Adafruit_PWM_Servo_Driver import PWM
import time

pwm1 = PWM(0x40)
pwm2 = PWM(0x41)
pwm1.setPWMFreq(50)
pwm2.setPWMFreq(50)
channel = 4
start   = 120
mid     = 342
end     = 570
pwm = pwm1


def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

pwm.setPWM(channel, 0, start)
time.sleep(1)
pwm.setPWM(channel, 0, mid)
time.sleep(4)
pwm.setPWM(channel, 0, start)
time.sleep(4)
pwm.setPWM(channel, 0, end)
time.sleep(4)
pwm.setPWM(channel, 0, mid)
