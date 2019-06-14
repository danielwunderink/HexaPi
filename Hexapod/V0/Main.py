
import pygame, sys, time, os, math, threading
from pygame.locals import *
from pygame import event
from Adafruit_PWM_Servo_Driver import PWM	

pwm0 = PWM(0x40)
pwm1 = PWM(0x41)
pwm0.setPWMFreq(60)
pwm1.setPWMFreq(60)

foot_vectors = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
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
def move_motor(leg, part, current_anlge, end_angle):
        #[[(claw),(Arm),(shoulder)],[]...]
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
                
#Takes in the current angles and moves each leg with the "move_motor" function
def move_legs(current_angles, end_angles):
        print "MOVING LEGS"
        for leg in range(6):
                for part in range(3):
                        move_motor(leg, part,current_angles[3*leg+part],end_angles[3*leg+part])
                        print ("moved leg ",leg," part ",part)
        current_angles = end_angles

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
             foot_vectors[leg][2]= round(((foot_vectors[leg][0]**2)+(foot_vectors[leg][1]**2))**(0.5),2)
        return foot_vectors

#Update the button values
def update_inputs(self):
        numaxes=27
        numbuttons=19
        button_state=[0]*numbuttons
        button_analog=[0]*numaxes
        
        #Start suppressing the output on stdout from Pygame
        devnull = open('/dev/null', 'w')
        
        #Read analog values
        for i in range(0,numaxes):
                button_analog[i] = self.get_axis(i)
        
        #global a_left
        #global a_right
        #global a_up
        #global a_down
        #global a_l1
        #global a_l2
        #global a_r1
        #global a_r2
        #global a_triangle
        #global a_circle
        #global a_square
        #global a_cross
        global a_js_left_x
        global a_js_left_y
        global a_js_right_x
        global a_js_right_y
        #global acc_x
        #global acc_y
        #global acc_z
        
        accuracy = 2
        
        #a_left		=round(button_analog[11],accuracy)
        #a_right	=round(button_analog[9],accuracy)
        #a_up		=round(button_analog[8],accuracy)
        #a_down		=round(button_analog[10],accuracy)
        #a_l1		=round(button_analog[14],accuracy)
        #a_l2		=round(button_analog[12],accuracy)
        #a_r1		=round(button_analog[15],accuracy)
        #a_r2		=round(button_analog[13],accuracy)
        #a_triangle	=round(button_analog[16],accuracy)
        #a_circle	=round(button_analog[17],accuracy)
        #a_square	=round(button_analog[19],accuracy)
        #a_cross	=round(button_analog[18],accuracy)
        a_js_left_x	=round(button_analog[0],accuracy)
        a_js_left_y	=round(button_analog[1],accuracy)
        a_js_right_x	=round(button_analog[2],accuracy)
        a_js_right_y	=round(button_analog[3],accuracy)
        #acc_x		=round(button_analog[23],accuracy)
        #acc_y		=round(button_analog[24],accuracy)
        ##acc_z		=round(button_analog[25],accuracy)
        
        #Read digital values
        for i in range(0,numbuttons):
                button_state[i]=self.get_button(i)
        
        global b_select
        #global b_js_left
        #global b_js_right
        global b_start
        global b_up
        #global b_right
        #global b_down
        #global b_left
        #global b_l2
        #global b_r2
        #global b_l1
        #global b_r1
        global b_triangle
        global b_circle
        global b_cross
        global b_square
        global b_ps
        
        b_select	=button_state[0]
        #b_js_left	=button_state[1]
        #b_js_right	=button_state[2]
        b_start	        =button_state[3]
        b_up		=button_state[4]
        #b_right	=button_state[5]
        #b_down		=button_state[6]
        #b_left		=button_state[7]
        #b_l2		=button_state[8]
        #b_r2		=button_state[9]
        #b_l1		=button_state[10]
        #b_r1		=button_state[11]
        b_triangle	=button_state[12]
        b_circle	=button_state[13]
        b_cross		=button_state[14]
        b_square	=button_state[15]
        b_ps		=button_state[16]
        
        #refresh
        pygame.event.get()
        return button_analog

def gait_main():
        global shutdown_sequence
        global standup_sequence
        global reset_sequence
        global ready_to_walk
        
        shutdown_complete = False
        while not shutdown_complete:
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
            #if not doing any special sequence: do walking stuff
            #print foot_vectors
            current_angles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            foot_coordinates = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
            x_datum = 3
            y_datum = 0
            z_datum = -7.5
            for i in range(len(gait_array_0[0])):
                for leg in range(6):
                    #access z column of gait csv and multiply it by the magnitude of the foot vector for that leg
                    foot_coordinates[leg][2] = float(gait_array_0[leg*2][i])*foot_vectors[leg][2] + z_datum
                    #access the xy column of the gait csv and multiply it by the x component of the foot vector
                    foot_coordinates[leg][0] = float(gait_array_0[leg*2+1][i])*foot_vectors[leg][0] + x_datum
                    #access the xy column of the gait csv and multiply it by the y component of the foot vector
                    foot_coordinates[leg][1] = float(gait_array_0[leg*2+1][i])*foot_vectors[leg][1] + y_datum
                    #call calc angles
                    calculated_angles = calc_angles(foot_coordinates)
                    print calculated_angles
                    #move the robot
                    #move_legs(current_angles,calculated_angles)
                    current_angles = calculated_angles
        
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
        update_inputs(contr)
        exit_program = False
        on_off_state = False
        
        global shutdown_sequence
        global standup_sequence
        global reset_sequence
        global ready_to_walk
        
        ready_to_walk = False #marked true after reset and standup sequence
        shutdown_sequence = False #tucks in legs to body then de-engergizes motors.
        standup_sequence = False #move legs to datums from having been powered off.
        reset_sequence = False #moves legs to datums from having been walking.


        #gait_thread = threading.Thread(target=gait_main)
        print "press START and SELECT buttons to Exit"
        print "press PS button to turn Hexapi On and Off"
        while not exit_program:
            for event in pygame.event.get():
                #print pygame.event.EventType
                    
                if event.type == pygame.QUIT:
                    done=True
                if event.type ==pygame.JOYBUTTONDOWN:
                    #print "Button Pressed"
                    update_inputs(contr)
                    #Check which button was pressed
                    if b_ps == 1:
                        if on_off_state:
                            print "turning off: reset then shutdown"
                            reset_sequence = True
                            shutdown_sequence = True
                        else:
                            print "turning on: start stand up sequence"
                            #gait_thread = threading.Thread(target=gait_main)
                            #gait_thread.start()
                            standup_sequence = True
                        on_off_state ^= True
                        
                    if (b_start == 1) and (b_select == 1):
                        print "Ending code: reset then shutdown. Exit code."
                        reset_sequence = True
                        shutdown_sequence = True
                        exit_program = True
                    if ((b_square == 1) or (b_up == 1) or (b_circle == 1) or (b_cross == 1)) and b_select == 1:
                        print "New gait chosen. Reset."
                        if b_square == 1 and b_select == 1:
                            global gate_selected
                            gait_selected = gait_array_0
                            print "Gait pattern 0 chosen"
                            print len(gait_selected[0])
                            gait_thread = threading.Thread(target=gait_main)
                            gait_thread.start()
                        if b_up == 1 and b_select == 1:
                            gait_selected = gait_array_1
                            print "Gait pattern 1 chosen"
                            gait_thread = threading.Thread(target=gait_main)
                            gait_thread.start()
                        if b_circle == 1 and b_select == 1:
                            gait_selected = gait_array_2
                            print "Gait pattern 2 chosen"
                            gait_thread = threading.Thread(target=gait_main)
                            gait_thread.start()
                        if b_cross == 1 and b_select == 1:
                            gait_selected = gait_array_3
                            print "Gait pattern 3 chosen"
                            gait_thread = threading.Thread(target=gait_main)
                            gait_thread.start()
                        reset_sequence = True

                if on_off_state and ready_to_walk and event.type == pygame.JOYAXISMOTION:
                    #print "joystick moved. Recalculate foot vectors"
                    prev_a_js_left_x = a_js_left_x
                    prev_a_js_left_y = a_js_left_y 
                    prev_a_js_right_x = a_js_right_x
                    prev_a_js_right_y = a_js_right_y
                    update_inputs(contr)
                    if (a_js_left_x != prev_a_js_left_x) or (a_js_left_y != prev_a_js_left_y) or(a_js_right_x != prev_a_js_right_x):
                        global foot_vectors
                        foot_vectors = calc_foot_vectors(a_js_left_x,a_js_left_y,a_js_right_x)
                        #print foot_vectors
            #time.sleep(0.2)
        print "Code successfully terminated"


#Start program
read_in_gaits()
controller_main()








#end_angles = []
#for i in range(18):
#        if i%3==2:
#            end_angles.append(110)
#        else:
#            end_angles.append(90)

#end_angles = [75,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60]
#current_anlges = [80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80]
#movelegs(current_anlges, end_angles)

