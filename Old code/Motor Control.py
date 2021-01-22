#------------------------------------------------#
# Initialise the PWM device
from Adafruit_PWM_Servo_Driver import PWM
pwm1 = PWM(0x40, debug=False)
pwm2 = PWM(0x41, debug=False)
pwm1.setPWMFreq(60) # Set PWM frequency to 60Hz
pwm2.setPWMFreq(60)

#------------------------------------------------#
# Define the servo degree max and mins and other working parameters
# Min pulse length out of 4096
# [Claw,..
#  Arm,...
#  Shoulder,...
#  ]
pulseMin = [130, 130, 150, 130, 135, 130,
			140, 130, 125, 120, 140, 140,
			140, 125, 135, 135, 160, 165
			]

# Max pulse length out of 4096
pulseMax = [595, 560, 660, 595, 605, 575,
			600, 610, 580, 565, 670, 605,
			620, 570, 590, 600, 595, 675
			]

#Total working range of servo in degrees
totalDegree = 180

#Slope of Pulse per degree
Slope = (pulseMax - pulseMin) / totalDegree

# Min working angle
degreeMin = [15, 15, 15, 15, 15, 15,
			15, 15, 15, 15, 15, 15,
			15, 15, 15, 15, 15, 15
			]

# Max working angle
degreeMax = [160, 160, 160, 160, 160, 160,
			160, 160, 160, 160, 160, 160,
			160, 160, 160, 160, 160, 160
			]
			
# Servo Defualt startup angles
degreeDefault = [60, 60, 60, 60, 60, 60,
				60, 60, 60, 60, 60, 60,
				60, 60, 60, 60, 60, 60
				]

# Number of degrees to increase/decrease each run throught the loop
degreeRate = 2

#------------------------------------------------#
#The inputs to the motor command function is:
#	1) Servo channel:			"channel"
#	2) Position in degrees:		"d"

def setDegree(channel, d):
    degreePulse = servoMin(channel) + Slope(channel) * d
    pwm.setPWM(channel, 0, degreePulse)

#------------------------------------------------#
#Basic Forward/Back/Left/Right Function
def FBLR(direction, Channel)
	if  direction == F:
	#very simplified now. Needs to include walking loop
		degree += degreeRate
		if  d > maxDegree:
			d = maxDegree
			
	#very simplified now. Needs to include walking loop
	elif direction == B
		d -= degreeRate
		if  d < minDegree:
			d = minDegree	
			
	elif direction == L
		#do some shit
		
	elif direction == R
		#do some shit
		
	setDegree(Channel, d)

#------------------------------------------------#
#The inputs to the motor command function is:



#------------------------------------------------#


#Set all servos in default position:
for c in cRange(0, 15):		#only include one servo hat atm
	setDegree(c, 90)

#------------------------------------------------#
#Controls
#Initiallize the libraries and wait for an input
import curses



#Working with only one motor at a time for now
Channel = 1
##########

# While 'q' is not pressed run the following loop:
key = ''
while key != ord('q'):
    key = scr.getch()
    if key == curses.KEY_UP:
		direction = F
	elif key == curses.KEY_DOWN:
		direction = B
	elif key == curses.KEY_LEFT:
		direction = L
	elif key == curses.KEY_RIGHT:
		direction = R
	FBLR(direction, Channel)
curses.endwin()

#------------------------------------------------#
