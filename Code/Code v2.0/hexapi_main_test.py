
import pygame, time, math, threading
from pygame.locals import *
from pygame import event
from hexapi_gait import *

#Calculating Foot Vectors
def calc_foot_vectors(Qx,Qy,Qr):
        print "in here"
        gfv=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        xlation_angle=[5.2360,0,1.0472,0.2122,3.1416,4.1888]
        #foot_vectors=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        
        g_datum = [[-20.14,11.63],[0,23.25],[20.14,11.63],[20.14,-11.63],[0,-23.25],[-20.14,-11.63]]
        Qxy_mag = (((g_datum[0][0])**2)+((g_datum[0][1])**2))**(0.5)
        
        body_rotation_val = (Qr)/(2*Qxy_mag)
        #fix acos domain error
        if (body_rotation_val<=-1):
                body_rotation_val = -0.999999
        if (body_rotation_val>=1):
                body_rotation_val = 0.999999
            
        body_rotation = 2*math.asin(body_rotation_val)
         
        for leg in range(6):
                
                Qrx = g_datum[leg][0]*math.cos(body_rotation) - g_datum[leg][1]*math.sin(body_rotation)
                Qry = g_datum[leg][0]*math.sin(body_rotation) + g_datum[leg][1]*math.cos(body_rotation)

                gfv[leg][0]= (Qx + Qrx)
                gfv[leg][1]= (Qy + Qry)
                
                foot_vectors[leg][0] = round((gfv[leg][0]-g_datum[leg][0])*math.cos(xlation_angle[leg]) - (gfv[leg][1]-g_datum[leg][1])*math.sin(xlation_angle[leg]),2)
                foot_vectors[leg][1] = round((gfv[leg][0]-g_datum[leg][0])*math.sin(xlation_angle[leg]) + (gfv[leg][1]-g_datum[leg][1])*math.cos(xlation_angle[leg]),2)
                foot_vectors[leg][2] = round(((foot_vectors[leg][0]**2)+(foot_vectors[leg][1]**2))**(0.5),2)
        
        return foot_vectors

def controller_thread(contr):
	while True:
		contr.update_joysticks()
		contr.update_buttons()
		time.sleep(0.001)

class PS2Controller():
	#An instance of a PS2Controller will inherit the methods and properties from the pygame.joystick.Joystick object
	def __init__(self, controller):
		self.controller = controller
		self.num_axes = 6
		self.num_buttons = 17
		self.analog_accuracy = 2
		self.b_select
		self.b_start
		self.b_ps
		self.b_triangle
		self.b_circle
		self.b_cross
		self.b_square

	#Update joystick variables
	def update_joysticks(self):
			#Start suppressing the output on stdout from Pygame
			devnull = open('/dev/null', 'w')

			num_ax = 6
			button_analog=[0]*num_ax
			accuracy = 2
			
			#Read analog values
			for i in range(0,num_ax):
					button_analog[i] = self.get_axis(i)
			
			self.a_js_left_x	    =round(button_analog[0],accuracy)
			self.a_js_left_y	    =round(button_analog[1],accuracy) * (-1)
			self.a_js_right_x	    =round(button_analog[3],accuracy)
        
	#Update button variables
	def update_buttons(self):
			#Start suppressing the output on stdout from Pygame
			devnull = open('/dev/null', 'w')
			
			num_bt = 17
			button_state=[0]*num_bt
			
			#Read digital values
			for i in range(0,num_bt):
					button_state[i]=self.get_button(i)
			
			self.b_cross	=button_state[0]
			self.b_circle	=button_state[1]
			self.b_triangle	=button_state[2]
			self.b_square	=button_state[3]
			
			self.b_select	=button_state[8]
			self.b_start	=button_state[9]
			self.b_ps		=button_state[10]


def hexapi_main():
               
        #Check if there are any controllers connected
        global contr_found
        contr_found = False
        
        while not contr_found:
            pygame.init()
            pygame.joystick.init()
            print "Searching for controller..."
            contoller_count = 0
            contoller_count = pygame.joystick.get_count()
            print "Controller count is: " + str(contoller_count)
            if contoller_count > 0:
                for i in range(contoller_count):
                    contr = PS2Controller(i)
                    contr.init()
                    controller_name = contr.get_name()
                    print "Controller " + str(i) + " name: " + controller_name
                    print "Controller connection successful"
                contr_found = True
                print "press START and SELECT buttons to Exit"
                print "press PS button to turn Hexapi On and Off"
                print "press SELECT and shape to select a different gait"
            else:
                #If nothing was found try again after 5 seconds
                pygame.joystick.quit()
                time.sleep(5)
				
		contr_thread = threading.Thread(target=controller_thread,args=(contr, ))
		contr_thread.setDaemon(True)
        contr_thread.start()

        #global variables
        global shutdown_sequence
        global standup_sequence
        global reset_sequence
        global gate_selected
        global foot_vectors
        
        shutdown_sequence =  False      #tucks in legs to body then de-engergizes motors.
        standup_sequence =  False       #move legs to datums from having been powered off.
        reset_sequence =  False         #moves legs to datums from having been walking.
        gait_selected = 0
        foot_vectors=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        
        #local variables
        exit_program = False
        ready_to_walk = True
        on_state = False
        prev_a_js_left_x = 0
        prev_a_js_left_y = 0 
        prev_a_js_right_x = 0
		
		move robot (contr.joystick_axes())
		
        while not exit_program:
            #Buttons
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    update_buttons(contr)
                    if b_ps == 1:
                        if on_state:
                            print "turning off: reset then shutdown"
                            reset_sequence = True
                            shutdown_sequence = True
                        else:
                            print "turning on: start stand up sequence"
                            standup_sequence = True
                        on_state ^= True
                        
                        gait_thread = threading.Thread(target=gait_main,args=(foot_vectors, [shutdown_sequence, standup_sequence, reset_sequence], gait_selected, ))
                        gait_thread.start()
                        
                    if (b_start == 1) and (b_select == 1):
                        print "Ending code: reset then shutdown. Exit code."
                        reset_sequence = True
                        shutdown_sequence = True
                        time.sleep(2) #wait for gait thread to terminate
                        exit_program = True
                        
                    if ((b_square == 1) or (b_triangle == 1) or (b_circle == 1) or (b_cross == 1)) and b_select == 1:
                        print "New gait chosen. Reset."
                        reset_sequence = True
                        if b_square == 1 and b_select == 1:
                            gait_selected = 0
                            print "Gait pattern 0 chosen"
                        if b_triangle == 1 and b_select == 1:
                            gait_selected = 1
                            print "Gait pattern 1 chosen"
                        if b_circle == 1 and b_select == 1:
                            gait_selected = 2
                            print "Gait pattern 2 chosen"
                        if b_cross == 1 and b_select == 1:
                            gait_selected = 3
                            print "Gait pattern 3 chosen"

                #Joysticks
                if event.type == pygame.JOYAXISMOTION:
                    if on_state and ready_to_walk:
                        update_joysticks(contr)
                        if (a_js_left_x != prev_a_js_left_x) or (a_js_left_y != prev_a_js_left_y) or(a_js_right_x != prev_a_js_right_x):
                        
                            foot_vectors = calc_foot_vectors(a_js_left_x,a_js_left_y,a_js_right_x)
                            print foot_vectors
                            time.sleep(0.1)
                            
                        prev_a_js_left_x = a_js_left_x
                        prev_a_js_left_y = a_js_left_y 
                        prev_a_js_right_x = a_js_right_x

        
        print "Code successfully terminated"

                
#Start program
hexapi_main()









