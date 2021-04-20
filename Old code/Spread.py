from Adafruit_PWM_Servo_Driver import PWM
import time

pwm1 = PWM(0x40)
pwm2 = PWM(0x41)
pwm1.setPWMFreq(50)
pwm2.setPWMFreq(50)

mid = 337
#end = 590

for channel in range(0, 6):
    pwm2.setPWM(channel, 0, mid)
    time.sleep(0.2)
    
for channel in range(8, 14):
    pwm2.setPWM(channel, 0, mid)
    time.sleep(0.2)
    
for channel in range(0, 6):
    pwm1.setPWM(channel, 0, mid)
    time.sleep(0.2)
