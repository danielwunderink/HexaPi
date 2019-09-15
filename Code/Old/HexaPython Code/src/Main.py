import time
import math
                        
def calculate_angles(foot_vectors):
    l1 = 3
    l2 = 7.5
    p_magnitudes = [0,0,0,0,0,0]
    alphas_rads = [0,0,0,0,0,0]
    thetas_rads = [0,0,0,0,0,0]
    betas_rads = [0,0,0,0,0,0]
    foot_angles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(6):
        p_magnitudes[i] = (((foot_vectors[i][0])**2) + ((foot_vectors[i][1])**2) + ((foot_vectors[i][2])**2))**(0.5)
        alpha_acos_piece = (((l1**2)+(l2**2)-(p_magnitudes[i]**2))/(2 * l1 * l2))
        #fix acos domain error
        if (alpha_acos_piece<=-1):
            alpha_acos_piece = -1
        if (alpha_acos_piece>=1):
            alpha_acos_piece = 1
        alphas_rads[i] = math.acos(alpha_acos_piece)
        
        #fix div by 0 error
        if (foot_vectors[i][0] == 0):
            foot_vectors[i][0] = 0.00000000000001
        
        theta_acos_piece = (((l1**2)-(l2**2)+(p_magnitudes[i]**2))/(2*l1*p_magnitudes[i]))
        theta_atan_piece = ((foot_vectors[i][2])/((((foot_vectors[i][0])**2)+((foot_vectors[i][1])**2))**(0.5)))
        
        #fix acos domain error
        if (theta_acos_piece<=-1):
            theta_acos_piece = -1
        if (theta_acos_piece>=1):
            theta_acos_piece = 1
           
        thetas_rads[i] = (math.pi/2) - math.acos(theta_acos_piece) - math.atan(theta_atan_piece)
        
        betas_rads[i] = (math.pi/2) - math.atan((foot_vectors[i][1])/(foot_vectors[i][0]))
        foot_angles[3*i] = alphas_rads[i]*(180/math.pi)
        foot_angles[3*i+1] = thetas_rads[i]*(180/math.pi)
        foot_angles[3*i+2] = betas_rads[i]*(180/math.pi)
    return foot_angles

end_angles = []
for i in range(18):
        if i%3==2:
            end_angles.append(110)
        else:
            end_angles.append(90)

#end_angles = [75,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60]
#current_anlges = [80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80]
#movelegs(current_anlges, end_angles)

foot_vectors = [[3,0,-7.5],[3,0,-6],[2.12,2.12,-7.5],[0,10.5,0],[0,10.5,0],[0,10.5,0]]
print (calculate_angles(foot_vectors))

