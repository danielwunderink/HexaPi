from Adafruit_PWM_Servo_Driver import PWM
import time

pwm0 = PWM(0x40)
pwm1 = PWM(0x41)
pwm0.setPWMFreq(60)
pwm1.setPWMFreq(60)

def moveto(leg, part, current_anlge, end_angle):
        channel =   [[(0,0,130,2.167),(1,8,140,2.222),(1,0,140,2.111)],
                     [(0,1,130,2.000),(1,9,130,2.000),(1,1,125,3.056)],
                     [(0,2,150,2.500),(1,10,125,3.056),(1,2,135,2.611)],
                     [(0,3,130,-2.000),(1,11,120,-2.167),(1,3,135,2.389)],
                     [(0,4,145,-2.389),(1,12,130,-1.889),(1,4,160,1.778)],
                     [(0,5,130,-1.889),(1,13,140,-2.111),(1,5,165,1.667)]]

        min_pulse       = channel[leg][part][2]
        slope           = channel[leg][part][3]
        
        def my_range(start1, end1, step1):
            if start1 >= end1:
                while end1 <= start1:
                    yield start1
                    start1 -= step1
            else:
                while start1 <= end1:
                    yield start1
                    start1 += step1

        for work_anlge in my_range(current_anlge, end_angle, 0.5):
            if channel[leg][part][3]<0:
                work_anlge  = 180-work_anlge
                slope = -slope
            pulse = work_anlge * slope + min_pulse
            pulse = int(pulse)
            if channel[leg][part][0] == 0:
                pwm0.setPWM(channel[leg][part][1], 0, pulse)
            else:
                pwm1.setPWM(channel[leg][part][1], 0, pulse)

def movelegs(current_angles, end_anges):
        for leg in range(6):
                for part in range(3):
                        moveto(leg, part,current_angles[3*leg+part],end_angles[3*leg+part])
                        print ("moved leg ",leg," part ",part)
                        

end_angles = []
for i in range(18):
        if i%3==2:
            end_angles.append(110)
        else:
            end_angles.append(90)

#end_angles = [75,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60]
current_anlges = [80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80]
movelegs(current_anlges, end_angles)

