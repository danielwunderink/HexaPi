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
    
        accuracy = 2
        
        a_left		=round(button_analog[11],accuracy)
        a_right	        =round(button_analog[9],accuracy)
        a_up		=round(button_analog[8],accuracy)
        a_down		=round(button_analog[10],accuracy)
        a_l1		=round(button_analog[14],accuracy)
        a_l2		=round(button_analog[12],accuracy)
        a_r1		=round(button_analog[15],accuracy)
        a_r2		=round(button_analog[13],accuracy)
        a_triangle	=round(button_analog[16],accuracy)
        a_circle	=round(button_analog[17],accuracy)
        a_square	=round(button_analog[19],accuracy)
        a_cross	        =round(button_analog[18],accuracy)
        a_js_left_x	=round(button_analog[0],accuracy)
        a_js_left_y	=round(button_analog[1],accuracy)
        a_js_right_x	=round(button_analog[2],accuracy)
        a_js_right_y	=round(button_analog[3],accuracy)
        acc_x		=round(button_analog[23],accuracy)
        acc_y		=round(button_analog[24],accuracy)
        acc_z		=round(button_analog[25],accuracy)
        
        #Read digital values
        for i in range(0,numbuttons):
                button_state[i]=self.get_button(i)
        
        b_select	=button_state[0]
        b_js_left	=button_state[1]
        b_js_right	=button_state[2]
        b_start	        =button_state[3]
        b_up		=button_state[4]
        b_right	        =button_state[5]
        b_down		=button_state[6]
        b_left		=button_state[7]
        b_l2		=button_state[8]
        b_r2		=button_state[9]
        b_l1		=button_state[10]
        b_r1		=button_state[11]
        b_triangle	=button_state[12]
        b_circle	=button_state[13]
        b_cross		=button_state[14]
        b_square	=button_state[15]
        b_ps		=button_state[16]
