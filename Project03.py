from HeatMapCode import generate_heatmap
from Motor import *
import math

# Function to change the coordinates from robot frame to lab frame
def robot_to_lab(data):
    coordinates, angle = data
    y, x = coordinates
    theta = math.radians(angle)

    x2 = x*math.cos(theta) + y*math.sin(theta)
    y2 = -x*math.sin(theta) + y*math.cos(theta)

    return (y2, x2)

def navigation():
    # Step 1: Have the robot pointing in the postive x-axis 
    # in the lab frame so that the robot frame is the same.
    # Then the robot will scan in its range for objects.
    obstacles_data = generate_heatmap()

    # If you did not find any obstacles move forward freely
    if not obstacles_data:
        setup()
        motor(50)
        destroy()
    else:
        obstacles_lab_coordinates = [robot_to_lab(data) for data in obstacles_data]
        print(f"Obstacles_lab_coordinates: {obstacles_lab_coordinates}")
    

