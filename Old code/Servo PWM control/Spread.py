from Adafruit_PWM_Servo_Driver import PWM

pwm1 = PWM(0x40)
pwm2 = PWM(0x41)
pwm1.setPWMFreq(60)
pwm2.setPWMFreq(60)

for channel in range(0, 5):
    pwm2.setPWM(channel, 0, mid)
for channel in range(8, 13):
    pwm2.setPWM(channel, 0, mid)
for channel in range(0, 5):
    pwm2.setPWM(channel, 0, end)
                     
time.sleep(1)
setAllPWM(off)
        
