from HeatMapCode import generate_heatmap, polar_to_cartesian
from Motor import *
import math
import heapq

# Function to change the coordinates from robot frame to lab frame
def robot_to_lab(point, angle):
    y_local, x_local = point
    theta = math.radians(angle)

    # Rotate to the local point
    x2 = x_local*math.cos(theta) + y_local*math.sin(theta)
    y2 = -x_local*math.sin(theta) + y_local*math.cos(theta)

    return (x2, y2)

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
            # Can't divide by zero. You're right on the obstacle - spike potential high
            total += 1e6

    gradient = (K * attraction) - (C / attraction) + (D * total)

    return gradient

# Function to compute the robot heading. Like the angle it needs to turn to to reach the goal
def compute_heading(robot_pos, goal):
    x_r, y_r = robot_pos
    x_g, y_g = goal
    dx = x_g - x_r
    dy = y_g - y_r

    return math.atan2(dy, dx)

# Function to update the robot's current position
def update_robot_curr_pos(robot_pos, robot_curr_angle, robot_heading):
    dy, dx = polar_to_cartesian(distance=45, angle=robot_heading)

    x, y = robot_pos
    robot_pos = (x + dx, y + dy)

    robot_curr_angle = robot_heading

    return robot_pos, robot_curr_angle

# Function to choose which point neighbor to go to based on the one with the lowest potential
# from the gradient descent.
def get_next_pos_from_gradient(obstacles_data, obstacles_lab_coordinates, goal):
    start_angle = 0
    angles = [i for i in range(start_angle + 5, 181, 5)]

    # Remove obstacles
    for obstacle in obstacles_data:
        while obstacle[1] in angles:
            angles.remove(obstacle[1])
    
    queue = [] # Priority queue to effieciently get the item with the lowest potential

    # Move to the position with the angle/neighbor with the lowest potential
    for angle in angles:
        y, x = polar_to_cartesian(distance=45, angle=angle)
        gradient_num = gradient(K=1, C=200, D=500, robot_pos=(x, y), goal=goal, obstacles=obstacles_lab_coordinates)
        heapq.heappush(queue, (gradient_num, angle))

    print(f"Priority queue: {queue}")
    lowest = heapq.heappop(queue)

    return lowest

def navigation():
    goal = (140, 140)
    x_g, y_g = goal
    robot_pos = (0, 0) # Robot starting position
    robot_curr_angle = math.pi / 2
    while robot_pos < (x_g - 15, y_g - 15):
        robot_heading = compute_heading(robot_pos, goal)
        print(f"Robot_pos: {robot_pos}")
        print(f"Robot_curr_angle: {math.degrees(robot_curr_angle)}")
        print(f"Robot_heading: {math.degrees(robot_heading)}")
        obstacles_data = generate_heatmap()
        print(f"obstacles_data: {obstacles_data}")

        # If you did not find any obstacles move forward freely
        if not obstacles_data:
            print("Moving.....")
            setup()
            smart_turn(current_angle=robot_curr_angle, target_angle=robot_heading)
            motor(45)
            
            # Update robot curr position
            robot_pos, robot_curr_angle = update_robot_curr_pos(
            robot_pos=robot_pos, 
            robot_curr_angle=robot_curr_angle, 
            robot_heading=robot_heading
            )

            destroy()
        else:
            obstacles_lab_coordinates = [robot_to_lab(point=data[0], angle=data[1]) for data in obstacles_data]
            print(f"Obstacles_lab_coordinates: {obstacles_lab_coordinates}")
            print(f"Lowest potential: {get_next_pos_from_gradient(obstacles_data=obstacles_data, obstacles_lab_coordinates=obstacles_lab_coordinates, goal=goal)}")
            lowest = get_next_pos_from_gradient(obstacles_data=obstacles_data, obstacles_lab_coordinates=obstacles_lab_coordinates, goal=goal)
            robot_heading = lowest[1]
            print("Moving away from obstacle.....")
            setup()
            smart_turn(current_angle=robot_curr_angle, target_angle=robot_heading)
            motor(45)
            
            # Update robot curr position
            robot_pos, robot_curr_angle = update_robot_curr_pos(
            robot_pos=robot_pos, 
            robot_curr_angle=robot_curr_angle, 
            robot_heading=robot_heading
            )

            destroy()
    

