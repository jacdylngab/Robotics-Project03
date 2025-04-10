from HeatMapCode import generate_heatmap
from Motor import *
import math
### MAY BE ADD THIS OPTIMIZATION LATER! ####
#robot_pos = (0, 0) # Robot starting position
#robot_heading = 0 # degrees
############################################

# Function to move the robot forward
def move_forward(distance, robot_heading):
    # turning left
    turn(duty_cycle_left=0, duty_cycle_right=0.5, direction=robot_heading+1.4)
    # turning right
    turn(duty_cycle_left=0.5, duty_cycle_right=0, direction=-robot_heading-0.9)
    # moving forward
    motor(distance)

# Function to change the coordinates from robot frame to lab frame
def robot_to_lab(point, angle):
    x_local, y_local = point
    theta = math.radians(angle)

    # Rotate to the local point
    x2 = x_local*math.cos(theta) + y_local*math.sin(theta)
    y2 = -x_local*math.sin(theta) + y_local*math.cos(theta)

    return (x2, y2)

def navigation():
    # Step 1: Have the robot pointing in the postive x-axis 
    # in the lab frame so that the robot frame is the same.
    # Then the robot will scan in its range for objects.
    obstacles_data = generate_heatmap()

    # If you did not find any obstacles move forward freely
    if not obstacles_data:
        print("Moving.....")
        #setup()
        #motor(50)
        #destroy()
    else:
        obstacles_lab_coordinates = [robot_to_lab(data) for data in obstacles_data]
        print(f"Obstacles_lab_coordinates: {obstacles_lab_coordinates}")
    

