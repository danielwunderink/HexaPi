from Adafruit_PWM_Servo_Driver import PWM
import time

pwm = PWM(0x40)
pwm.setPWMFreq(60)

def moveto(channel, current, angle, speed):

        min_pulse_list  = [170,170,170,170,
                           170,150,170,170,
                           170,170,170,170,
                           170,170,170,170
        ]
        
        slope_list      = [2.800,2.800,2.800,2.800,
                           2.800,2.833,2.800,2.800,
                           2.800,2.800,2.800,2.800,
                           2.800,2.800,2.800,2.800
        ]

        min_pulse       = min_pulse_list[channel]
        slope           = slope_list[channel]

        print slope
        print min_angle
        
        def my_range(start1, end1, step1):
            while start1 <= end1:
                yield start1
                start1 += step1
                
        for work_angle in my_range(current, angle, 0.5):
            pulse = work_angle * slope + min_angle
            pulse = int(pulse)
            pwm.setPWM(channel, 0, pulse)
            wait_time = 0.001/speed
            time.sleep(wait_time)
            print pulse
            print work_angle

moveto(5, 390, 300, 10)

current = 300
angle = 340

slope = 2.833
min_angle = 150



                
for work_angle in my_range(current, angle, 0.5):
    pulse = work_angle * slope + min_angle
    pulse = int(pulse)
    pwm.setPWM(channel, 0, pulse)
    wait_time = 0.001/speed
    time.sleep(wait_time)
    print work_angle
    print pulse
