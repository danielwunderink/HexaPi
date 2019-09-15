from Adafruit_PWM_Servo_Driver import PWM
import time

pwm1 = PWM(0x40)
pwm2 = PWM(0x41)
pwm1.setPWMFreq(50)
pwm2.setPWMFreq(50)

mid = 400
#end = 590

#****************************************************************************************

print "Finding Lower Limit Starting at 210"
starting_point = 210

stop = ""
user_input = 0
print "Write 'stop' after the first time the servo shakes"
pwm2.setPWM(0,0,300)
for i in range(0,200,10):
    pwm2.setPWM(0,0,starting_point-i)
    print(starting_point-i)
    time.sleep(0.6)
    stop = raw_input()
    if stop == 'stop':
        user_input = starting_point-i+10
        stop = ""
        break

print user_input
print "Write 'stop' after the first time the servo shakes"
pwm2.setPWM(0,0,300)
for i in range(0,20):
    pwm2.setPWM(0,0,user_input-i)
    print(user_input-i)
    time.sleep(0.6)
    stop = raw_input()
    if stop == 'stop':
        lower_limit = user_input-i+1
        stop = ""
        break

time.sleep(1)
pwm2.setPWM(0,0,lower_limit)
time.sleep(0.9)
pwm2.setPWM(0,0,400)
time.sleep(0.9)
pwm2.setPWM(0,0,lower_limit)
time.sleep(0.9)
pwm2.setPWM(0,0,400)

print "The lower limit is: "+str(lower_limit)

#****************************************************************************************


print "Finding Upper Limit Starting at 450"
starting_point = 450

stop = ""
user_input = 0
print "Write 'stop' after the first time the servo shakes"
pwm2.setPWM(0,0,300)
for i in range(0,200,10):
    pwm2.setPWM(0,0,starting_point+i)
    print(starting_point+i)
    time.sleep(0.6)
    stop = raw_input()
    if stop == 'stop':
        user_input = starting_point+i-20
        stop = ""
        break

print user_input
print "Write 'stop' after the first time the servo shakes"
pwm2.setPWM(0,0,300)
for i in range(0,30,2):
    pwm2.setPWM(0,0,user_input+i)
    print(user_input+i)
    time.sleep(0.6)
    stop = raw_input()
    if stop == 'stop':
        upper_limit = user_input+i-4
        stop = ""
        break

time.sleep(1)
pwm2.setPWM(0,0,upper_limit)
time.sleep(0.9)
pwm2.setPWM(0,0,400)
time.sleep(0.9)
pwm2.setPWM(0,0,upper_limit)
time.sleep(0.9)
pwm2.setPWM(0,0,400)

print "The upper limit is: "+str(upper_limit)


#****************************************************************************************

##lower_limit = 115
##upper_limit = 520
middle_point  = lower_limit + (upper_limit-lower_limit)/2
print middle_point

time_input = 1
while True:
    time_input = raw_input("Enter the time in sec: ")
    time_input = float(time_input)
    time.sleep(time_input)
    pwm2.setPWM(0,0,lower_limit)
    time.sleep(time_input)
    pwm2.setPWM(0,0,middle_point)
    time.sleep(time_input)
    pwm2.setPWM(0,0,upper_limit)
    time.sleep(time_input)
    







