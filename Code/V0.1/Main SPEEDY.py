
import pygame, sys, time, os, math, threading
from pygame.locals import *
from pygame import event
from Adafruit_PWM_Servo_Driver import PWM	

pwm0 = PWM(0x40)
pwm1 = PWM(0x41)
pwm0.setPWMFreq(60)
pwm1.setPWMFreq(60)

foot_vectors = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
foot_coordinates = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

gait_array_0 = [[], [], [], [], [], [], [], [], [], [], [], []]
gait_array_1 = [[], [], [], [], [], [], [], [], [], [], [], []]
gait_array_2 = [[], [], [], [], [], [], [], [], [], [], [], []]
gait_array_3 = [[], [], [], [], [], [], [], [], [], [], [], []]
gait_selected = [[], [], [], [], [], [], [], [], [], [], [], []]

def read_in_gaits():
    import csv
    global gait_array_1
    global gait_array_2
    global gait_array_3
    global gait_array_0

    with open('gaits/gait_0.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = 0
        for row in csv_reader:
            col_count = 0
            gait_array_col = 0
            for col_entry in row:
                if (row_count != 0) and ((col_count%3 != 0)):
                    gait_array_0[gait_array_col].append(col_entry)
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
                    gait_array_1[gait_array_col].append(col_entry)
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
                    gait_array_2[gait_array_col].append(col_entry)
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
                    gait_array_3[gait_array_col].append(col_entry)
                    gait_array_col += 1
                col_count += 1  
            row_count += 1
        print('Processed %s rows.' % (row_count))

#Take in calucluated angles for a motor and moves it using PWM
def move_motor(leg, part, end_angle):
        #[[(claw),(Arm),(shoulder)],[]...]
        channel =   [[(0,0,130,2.167),(1,8,140,2.222),(1,0,140,2.111)],
                     [(0,1,130,2.000),(1,9,130,2.000),(1,1,125,3.056)],
                     [(0,2,150,2.500),(1,10,125,3.056),(1,2,135,2.611)],
                     [(0,3,130,-2.000),(1,11,120,-2.167),(1,3,135,2.389)],
                     [(0,4,145,-2.389),(1,12,130,-1.889),(1,4,160,1.778)],
                     [(0,5,130,-1.889),(1,13,140,-2.111),(1,5,165,1.667)]]

        min_pulse       = channel[leg][part][2]
        slope           = channel[leg][part][3]

        if channel[leg][part][3]<0:
            end_angle  = 180-end_angle
            slope = -slope
        
        pulse = end_angle * slope + min_pulse
        pulse = int(pulse)
        
        if channel[leg][part][0] == 0:
            pwm0.setPWM(channel[leg][part][1], 0, pulse)
        else:
            pwm1.setPWM(channel[leg][part][1], 0, pulse)
        #time.sleep(0.05)
        #print "motor moved to" + str(end_angle)
                
#Takes in the current angles and moves each leg with the "move_motor" function
def move_legs(end_angles):
        #print "MOVING LEGS"
        for leg in range(6):
            for part in range(3):
                move_motor(leg, part,end_angles[3*leg+part])
         

#Takes in the desired XYZ components for each leg and outputs the end angles
def calc_angles(foot_coordinates):
    l1 = 3
    l2 = 7.5
    p_magnitudes = [0,0,0,0,0,0]
    alphas_rads = [0,0,0,0,0,0]
    thetas_rads = [0,0,0,0,0,0]
    betas_rads = [0,0,0,0,0,0]
    foot_angles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(6):
        p_magnitudes[i] = (((foot_coordinates[i][0])**2) + ((foot_coordinates[i][1])**2) + ((foot_coordinates[i][2])**2))**(0.5)

        #fix div by 0 error
        if(p_magnitudes[i] == 0):
            p_magnitudes[i] = 0.00000000001
        
        alpha_acos_piece = (((l1**2)+(l2**2)-(p_magnitudes[i]**2))/(2 * l1 * l2))
        #fix acos domain error
        if (alpha_acos_piece<=-1):
            alpha_acos_piece = -1
        if (alpha_acos_piece>=1):
            alpha_acos_piece = 1
        alphas_rads[i] = math.acos(alpha_acos_piece)
        
        #fix div by 0 error
        if (foot_coordinates[i][0] == 0):
            foot_coordinates[i][0] = 0.00000000000001
        
        theta_acos_piece = (((l1**2)-(l2**2)+(p_magnitudes[i]**2))/(2*l1*p_magnitudes[i]))
        theta_atan_piece = ((foot_coordinates[i][2])/((((foot_coordinates[i][0])**2)+((foot_coordinates[i][1])**2))**(0.5)))
        
        #fix acos domain error
        if (theta_acos_piece<=-1):
            theta_acos_piece = -1
        if (theta_acos_piece>=1):
            theta_acos_piece = 1
           
        thetas_rads[i] = (math.pi/2) - math.acos(theta_acos_piece) - math.atan(theta_atan_piece)
        
        betas_rads[i] = (math.pi/2) - math.atan((foot_coordinates[i][1])/(foot_coordinates[i][0]))
        foot_angles[3*i] = round(alphas_rads[i]*(180/math.pi),0)
        #patch up the -90 issue
        if (thetas_rads[i] < 0):
            thetas_rads[i] = -thetas_rads[i]
        foot_angles[3*i+1] = round(thetas_rads[i]*(180/math.pi),0)
        foot_angles[3*i+2] = round(betas_rads[i]*(180/math.pi),0)
    return foot_angles

#Calculating Foot Vectors
def calc_foot_vectors(Qx,Qy,Qr):
        foot_vectors=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        
        global_datum = [[10.61,6.13],[0,12.25],[-10.61,6.13],[-10.61,-6.13],[0,-12.25],[10.61,-6.13]]
        
        Qxy_mag = (((global_datum[0][0])**2)+((global_datum[0][1])**2))**(0.5)
        #fix div by 0 error
        if (Qxy_mag == 0):
            Qxy_mag = 0.00000000000001

        body_rotation_val = (Qr)/(2*Qxy_mag)
        #fix acos domain error
        if (body_rotation_val<=-1):
            body_rotation_val = -1
        if (body_rotation_val>=1):
            body_rotation_val = 1
            
        body_rotation = 2*math.asin(body_rotation_val)
        for leg in range(6):
             foot_vectors[leg][0]= round(((Qx + global_datum[leg][0]*math.cos(body_rotation) - global_datum[leg][1]*math.sin(body_rotation))-global_datum[leg][0])/2,2)
             foot_vectors[leg][1]= round(((-Qy + global_datum[leg][0]*math.sin(body_rotation) + global_datum[leg][1]*math.cos(body_rotation))-global_datum[leg][1])/2,2)
             foot_vectors[leg][2]= round((((foot_vectors[leg][0]**2)+(foot_vectors[leg][1]**2))**(0.5)),2)
        return foot_vectors

def gait_main():
        global shutdown_sequence
        global standup_sequence
        global reset_sequence
        global ready_to_walk
        
        shutdown_complete = False
        while not shutdown_complete:
                
            #Special Sequences:
            if standup_sequence:
                #stand up code
                ready_to_walk = True
                standup_sequence = False
            if reset_sequence:
                #reset code
                ready_to_walk = True
                reset_sequence = False
            if shutdown_sequence:
                #shutdown code
                shutdown_complete = True
                shutdown_sequence = False
                break

            #Standard Continuous gait sequence
            x_datum = 3
            y_datum = 0
            z_datum = -7.5
            scale = 3
            
            #t0 = time.time()
            
            for i in range(len(gait_array_0[0])):
                if shutdown_sequence:
                    break
                for leg in range(6):
                    if shutdown_sequence:
                        break
                    #access z column of gait csv and multiply it by the magnitude of the foot vector for that leg
                    foot_coordinates[leg][2] = float(gait_array_0[leg*2][i])*foot_vectors[leg][2]*scale*(-3) + z_datum
                    #access the xy column of the gait csv and multiply it by the x component of the foot vector
                    foot_coordinates[leg][0] = float(gait_array_0[leg*2+1][i])*foot_vectors[leg][0]*scale + x_datum
                    #access the xy column of the gait csv and multiply it by the y component of the foot vector
                    foot_coordinates[leg][1] = float(gait_array_0[leg*2+1][i])*foot_vectors[leg][1]*scale + y_datum
                    #call calc angles

                    calculated_angles = calc_angles(foot_coordinates)
                #print foot_vectors
                move_legs(calculated_angles)
                #time.sleep(0.1)
                    
            #t1 = time.time()
            #run_time = t1 - t0
            #print run_time
            #time.sleep(0.1)
        
        print "Gait thread exited."

def controller_main():
        #Check if there are any controllers connected
        pygame.init()
        pygame.joystick.init()
        found = False
        while not found:
            print "Searching for controller..."
            contoller_count = 0
            contoller_count = pygame.joystick.get_count()
            print "Controller count is: " + str(contoller_count)
            if contoller_count > 0:
                for i in range(contoller_count):
                    controller = pygame.joystick.Joystick(i)
                    controller.init()
                    controller_name = controller.get_name()
                    print "Controller " + str(i) + " name: " + controller_name
                    print "Controller connection successful"
                found = True
            else:
                #If nothing was found try again after 5 seconds
                time.sleep(5)
                pygame.joystick.quit()
                pygame.joystick.init()

        #Define controller as the first one found
        contr = pygame.joystick.Joystick(0)
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.JOYAXISMOTION)
        pygame.event.set_allowed(pygame.JOYBUTTONDOWN)

        #Initialize variables:
        left_x = 0
        left_y = 0
        right_x = 0
        exit_program = False
        on_off_state = False
        global shutdown_sequence
        global standup_sequence
        global reset_sequence
        global ready_to_walk
        global foot_vectors
        ready_to_walk = True #marked true after reset and standup sequence
        shutdown_sequence = False #tucks in legs to body then de-engergizes motors.
        standup_sequence = False #move legs to datums from having been powered off.
        reset_sequence = False #moves legs to datums from having been walking.

        print "press START and SELECT buttons to Exit"
        print "press PS button to turn Hexapi On and Off"
        while not exit_program:
            t0 = time.time()
            for event in pygame.event.get():
                if event.type ==pygame.JOYBUTTONDOWN:
                    select_pressed = contr.get_button(0)

                    #Select and Start: Kill Program
                    if select_pressed and (contr.get_button(3) == 1):
                        print "Ending code: reset then shutdown. Exit code."
                        shutdown_sequence = True
                        exit_program = True
                        break
                
                    #Select and PS: On/Off function
                    if select_pressed and (contr.get_button(16) == 1):
                        if on_off_state:
                            print "turning off: reset then shutdown"
                            reset_sequence = True
                            shutdown_sequence = True
                            time.sleep(1)
                        else:
                            print "turning on: start stand up sequence"
                            standup_sequence = True
                            time.sleep(1)
                            gait_thread = threading.Thread(target=gait_main)
                            gait_thread.start()
                        on_off_state ^= True
                        
                    if select_pressed and (contr.get_button(13) == 1):
                        print "New gait chosen. Reset."
                    
                if (on_off_state) and (event.type == pygame.JOYAXISMOTION) and ((event.axis == 0) or (event.axis == 1) or (event.axis == 2)):
                    js_filter = 2
                    left_x_prev = left_x
                    left_y_prev = left_y 
                    right_x_prev = right_x
                    left_x = round(contr.get_axis(0),js_filter)
                    left_y = round(contr.get_axis(1),js_filter)
                    right_x = round(contr.get_axis(2),js_filter)
                    if (left_x != left_x_prev) or (left_y != left_y_prev) or(right_x != right_x_prev):
                        foot_vectors = calc_foot_vectors(left_x,left_y,right_x)
                        

                        
            #t1 = time.time()
            #run_time = t1 - t0
            #print run_time

            #Controller update rate:
            time.sleep(0.1)
        print "Code successfully terminated"


#Start program
read_in_gaits()
controller_main()





#                        pulse = int(300 + right_x*50)
#                        #print pulse
#                        for leg in range(6):
#                            for part in range(3):
#                                #time.sleep(0.1)
#                                if channel[leg][part][0] == 0:
#                                    pwm0.setPWM(channel[leg][part][1], 0, pulse)
#                                else:
#                                    pwm1.setPWM(channel[leg][part][1], 0, pulse)

end_angles = []
for i in range(18):
        if i%3==2:
            end_angles.append(90)
        else:
            end_angles.append(90)

#end_angles = [90,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60]
move_legs(end_angles)



