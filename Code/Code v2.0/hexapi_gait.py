
import sys, time, os, math, threading, csv
from Adafruit_PWM_Servo_Driver import PWM

pwm0 = PWM(0x40)
pwm1 = PWM(0x41)
pwm0.setPWMFreq(50)
pwm1.setPWMFreq(50)

#globals imported from controller inputs (in hexapi_main.py)



def read_in_servo_config():
        print "import servo config"
        global servo_config
                       #[[(shoulder), (arm), (claw)],[]...]
        servo_config =  [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        
        with open('servo_config.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                row_count = 0
                for row in csv_reader:
                    col_count = 0
                    array_col = 0
                    for col_entry in row:
                        servo_config[array_col].append(col_entry)
                        array_col += 1
                        col_count += 1  
                    row_count += 1
                print "servo config import complete"
                print('Processed %s columns.' % (col_count))
                print('Processed %s rows.' % (row_count))

def read_in_gaits():
        print "import gaits"
        global gait_array

        #                leg1    leg2    leg3    leg4    leg5    leg6
        #               tz,txy  tz,txy  tz,txy  tz,txy  tz,txy  tz,txy 
        gait_array =  [[[], [], [], [], [], [], [], [], [], [], [], []], #gait option 0
                       [[], [], [], [], [], [], [], [], [], [], [], []], #gait option 1
                       [[], [], [], [], [], [], [], [], [], [], [], []], #gait option 2
                       [[], [], [], [], [], [], [], [], [], [], [], []]] #gait option 3


        with open('gaits/gait_0.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                row_count = 0
                for row in csv_reader:
                    col_count = 0
                    gait_array_col = 0
                    for col_entry in row:
                        if (row_count != 0) and ((col_count%3 != 0)):
                            gait_array[0][gait_array_col].append(col_entry)
                            gait_array_col += 1
                        col_count += 1  
                    row_count += 1
                print('Processed %s rows.' % (row_count))

        with open('gaits/gait_1.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                row_count = 0
                for row in csv_reader:
                    col_count = 0
                    gait_array_col = 0
                    for col_entry in row:
                        if (row_count != 0) and ((col_count%3 != 0)):
                            gait_array[1][gait_array_col].append(col_entry)
                            gait_array_col += 1
                        col_count += 1  
                    row_count += 1
                print('Processed %s rows.' % (row_count))

        with open('gaits/gait_2.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                row_count = 0
                for row in csv_reader:
                    col_count = 0
                    gait_array_col = 0
                    for col_entry in row:
                        if (row_count != 0) and ((col_count%3 != 0)):
                            gait_array[2][gait_array_col].append(col_entry)
                            gait_array_col += 1
                        col_count += 1  
                    row_count += 1
                print('Processed %s rows.' % (row_count))

        with open('gaits/gait_3.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                row_count = 0
                for row in csv_reader:
                    col_count = 0
                    gait_array_col = 0
                    for col_entry in row:
                        if (row_count != 0) and ((col_count%3 != 0)):
                            gait_array[3][gait_array_col].append(col_entry)
                            gait_array_col += 1
                        col_count += 1  
                    row_count += 1
                print('Processed %s rows.' % (row_count))

#Take in calucluated angles for a motor and moves it using PWM
def move_motor(leg, part, servo_angle):
        use_col = 3*leg + part
        use_i2c = int(servo_config[use_col][183])
        use_channel = int(servo_config[use_col][184])
        use_angle = int(servo_angle)

        use_pwm = int(servo_config[use_col][use_angle])

        
        if use_i2c == 0:
                pwm0.setPWM(use_channel, 0, use_pwm)
        else:
                pwm1.setPWM(use_channel, 0, use_pwm)
                
#Takes in the current angles and moves each leg with the "move_motor" function
def move_legs(servo_angles):
    for leg in range(6):
        for part in range(3):
            move_motor(leg, part, servo_angles[leg][part])
            
#Takes in the desired XYZ components for each leg and outputs the end angles
def calc_angles(foot_coordinates):
        l1 = 7.75
        l2 = 14.5
        l3 = 5.75
        
        #                leg1      2       3       4       5       6
        #           [beta,theta,alpha] ie shoulder,arm,claw
        servo_angles = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]


        for leg in range(6):
                x = foot_coordinates[leg][0]
                y = foot_coordinates[leg][1]
                z = foot_coordinates[leg][2]
                xy = ((x**2)+(y**2))**(0.5)
                c = (((xy-l3)**2)+(z**2))**(0.5)

                #Calculate alpha
                #fix acos domain error
                alpha_acos_piece = ((l1**2)+(l2**2)-(c**2))/(2*l1*l2)

                if (alpha_acos_piece<=-1):
                        alpha_acos_piece = -1
                if (alpha_acos_piece>=1):
                        alpha_acos_piece = 1

                alpha = math.acos(alpha_acos_piece) - (math.pi/2)
                        
                #Calculate theta
                #fix acos domain error
                theta_acos_piece = ((l1**2)+(c**2)-(l2**2))/(2*l1*c)
                if (theta_acos_piece<=-1):
                        theta_acos_piece = -1
                if (theta_acos_piece>=1):
                        theta_acos_piece = 1
                
                theta_acos_piece1 = z/c
                if (theta_acos_piece1<=-1):
                        theta_acos_piece1 = -1
                if (theta_acos_piece1>=1):
                        theta_acos_piece1 = 1
                
                if(c == 0):
                        c = 0.00000000001

                if(xy<=l3):
                        theta_piece1 = - math.acos(theta_acos_piece1)
                else:
                        theta_piece1 = math.acos(theta_acos_piece1)
                        
                theta = theta_piece1 - math.acos(theta_acos_piece)

                #Calculate beta
                beta_acos_piece = x/xy
                if (beta_acos_piece<=-1):
                        beta_acos_piece = -1
                if (beta_acos_piece>=1):
                        beta_acos_piece = 1
                if(x == 0):
                        x = 0.00000000001
                beta = math.pi - math.acos(beta_acos_piece)
                
                if (beta > math.pi):
                        beta = math.pi
                if (alpha > math.pi):
                        alpha = math.pi
                if (theta > math.pi):
                        theta = math.pi
                
                if (beta < 0):
                        beta = 0
                if (alpha < 0):
                        alpha = 0
                if (theta < 0):
                        theta = 00

                servo_angles[leg] = [beta*(180/math.pi),theta*(180/math.pi),alpha*(180/math.pi)]
                
        return servo_angles


def calc_foot_xyz(i):
        x_datum = 0
        y_datum = 13
        z_datum = -17
        scale = 6
        #                      leg1     2       3       4       5       6
        #                    [x,y,z] [x,y,z] [x,y,z] [x,y,z] [x,y,z] [x,y,z]
        foot_coordinates  = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        
        for leg in range(6):
                #access z column of gait csv and multiply it by the magnitude of the foot vector for that leg
                foot_coordinates[leg][2] = float(gait_array[gait_selected][leg*2][i])*foot_vectors[leg][2]*scale + z_datum
                
                #access the xy column of the gait csv and multiply it by the x component of the foot vector
                foot_coordinates[leg][0] = float(gait_array[gait_selected][leg*2+1][i])*foot_vectors[leg][0]*scale + x_datum
                
                #access the xy column of the gait csv and multiply it by the y component of the foot vector
                foot_coordinates[leg][1] = float(gait_array[gait_selected][leg*2+1][i])*foot_vectors[leg][1]*scale + y_datum
        
        return foot_coordinates

#Main gait
def gait_main(foot_vectors_from_main, hexapi_sequence_from_main, gait_selected_from_main):
        read_in_servo_config()
        read_in_gaits()
        
                         #[shutdown, standup, reset]
        hexapi_sequence = hexapi_sequence_from_main
        global gait_selected
        gait_selected = gait_selected_from_main
        global foot_vectors
        foot_vectors = foot_vectors_from_main
        
        global foot_coordinates
        
        #                      leg1     2       3       4       5       6
        #                    [x,y,z] [x,y,z] [x,y,z] [x,y,z] [x,y,z] [x,y,z]
        foot_coordinates  = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        
        #                     leg1      2       3       4       5       6
        #               [beta,theta,alpha] ie shoulder,arm,claw        
        calculated_angles = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        
        while not hexapi_sequence[0]:
                start_time = time.time()
                for i in range(len(gait_array[gait_selected][0])):                                
                        foot_coordinates = calc_foot_xyz(i)
                        calculated_angles = calc_angles(foot_coordinates)
                        move_legs(calculated_angles)
                #print("--- %s ---" % (time.time() - start_time))
                #print hexapi_sequence[0]
                #print foot_coordinates
        
        print "Gait Thread terminated successfully"


#Start program

#gait_main()


