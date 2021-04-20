# Initialization

from Adafruit_PWM_Servo_Driver import PWM
import time

pwm1 = PWM(0x40)
pwm2 = PWM(0x41)
pwm1.setPWMFreq(50)
pwm2.setPWMFreq(50)
channel = 3
start   = 120
mid     = 340
end     = 560
pwm = pwm1

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

tickmin	= 0
tickmax = 0

try:
	for tickmin in my_range(0,4096,4):
		pwm.setPWM(channel, 0, tickmin)
		time.sleep(0.2)
		print(tickmin)
except KeyboardInterrupt:
	pass




try:
	for tickmax in my_range(tickmin,4096,4):
		pwm.setPWM(channel, 0, tickmax)
		time.sleep(0.2)
		print(tickmax)
except KeyboardInterrupt:
	pass

print("FAF")
print("\n")
print(tickmin)
print(tickmax)

tickmid = (tickmin+tickmax)/2


pwm.setPWM(channel, 0, tickmin)
time.sleep(2)
pwm.setPWM(channel, 0, tickmid)
time.sleep(2)
pwm.setPWM(channel, 0, tickmax)
time.sleep(2)
pwm.setPWM(channel, 0, tickmid)


# angle to pulse
#min_angle   = 150
#slope       = 2.833





#for angle in my_range(1, 180, 0.5):
#    pulse = angle*slope + min_angle
#    pulse = int(pulse)
#    pwm.setPWM(channel, 0, pulse)
#    time.sleep(0.00001)

#time.sleep(0.25)
#pwm.setPWM(channel, 0, start)
