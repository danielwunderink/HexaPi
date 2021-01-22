'''
Created on Jun 4, 2019

@author: Daniel.Wunderink
'''

import csv

leg_1_z = []
leg_1_xy = []
leg_2_z = []
leg_2_xy = []
leg_3_z = []
leg_3_xy = []
leg_4_z = []
leg_4_xy = []
leg_5_z = []
leg_5_xy = []
leg_6_z = []
leg_6_xy = []

gait_array = [leg_1_z, leg_1_xy, leg_2_z, leg_2_xy, leg_3_z, leg_3_xy, leg_4_z, leg_4_xy, leg_5_z, leg_5_xy, leg_6_z, leg_6_xy]

with open('3 step gait.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    row_count = 0
    for row in csv_reader:
        col_count = 0
        gait_array_col = 0
        for col_entry in row:
            if (row_count != 0) and ((col_count%3 != 0)):
                gait_array[gait_array_col].append(col_entry)
                gait_array_col += 1
            col_count += 1  
        row_count += 1
    print('Processed %s rows.' % (row_count))

for i in range(5):
    for leg in range(6):
        print gait_array[leg*2][i]
        print gait_array[leg*2+1][i]

