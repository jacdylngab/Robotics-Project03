from HeatMapCode import generate_heatmap
from Motor import *
import math


# Function to change the coordinates from robot frame to lab frame
def robot_to_lab(point, angle):
    x_local, y_local = point
    theta = math.radians(angle)

    # Rotate to the local point
    x2 = x_local*math.cos(theta) + y_local*math.sin(theta)
    y2 = -x_local*math.sin(theta) + y_local*math.cos(theta)

    return (x2, y2)

# Function to update the robot internal state after moving forward
def update_robot_state():
    theta = math.radians(robot_heading)
    dx = distance * math.cos(theta)
    dy = distance * math.sin(theta)

    x, y = robot_pos
    robot_pos = (x + dx, y + dy)

    robot_curr_angle = robot_heading

# Function to find the gradient
def gradient(K, C, D, robot_pos, goal, obstacles):
    x, y = robot_pos
    x_goal, y_goal = goal
    total = 0

    attract = (x - x_goal)**2 + (y - y_goal)**2

    if attract != 0:
        attraction = attract
    else:
        # Can't divide by zero
        attraction = 1e-6

    for x_i, y_i in obstacles:
        dist_squared = (x - x_i)**2 + (y - y_i)**2

        if dist_squared != 0:
            total += 1 / dist_squared
        else: 
            # You're right on the obstacle - spike potential high
            total += 1e6

    gradient = (K * attraction) - (C / attraction) + (D * total)

    return gradient


def navigation():
    goal = (140, 140)
    robot_pos = (0, 0) # Robot starting position
    robot_heading = 0 # degrees
    robot_curr_angle = 90
    while robot_pos != goal:
        print(f"Robot_pos: {robot_pos}")
        print(f"Robot_curr_angle: {robot_curr_angle}")
        print(f"Robot_heading: {robot_heading}")
        obstacles_data = generate_heatmap()
        print(f"obstacles_data: {obstacles_data}")

        # If you did not find any obstacles move forward freely
        if not obstacles_data:
            print("Moving.....")
            setup()
            motor(45)
            #update_robot_state()
            destroy()
        else:
            obstacles_lab_coordinates = [robot_to_lab(point=data[0], angle=data[1]) for data in obstacles_data]
            print(f"Obstacles_lab_coordinates: {obstacles_lab_coordinates}")
            gradient_num = gradient(K=1, C=1, D=1, robot_pos=robot_pos, goal=goal, obstacles=obstacles_lab_coordinates)
            print(f"gradient: {gradient_num}")
            #smart_turn(current_angle=math.radians(robot_curr_angle), target_angle=math.radians(robot_heading))
    

