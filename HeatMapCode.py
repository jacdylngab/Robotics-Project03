import numpy as np
import matplotlib.pyplot as plt
import math
from Scanning import scan

def polar_to_cartesian(angle, distance):
    radians = math.radians(angle)
    '''
    # Shifting negative numbers 
    x = distance * math.cos(radians) + width // 2
    y = distance * math.sin(radians) + height // 2'
    '''
    x = distance * math.cos(radians)
    y = distance * math.sin(radians)
    return y, x

def scanned_points(scanned_data, goal, width, height):
    obstacles = []
    
    for angle, distance in scanned_data:
        y, x = polar_to_cartesian(angle, distance)
        coordinates = (y, x)
        if coordinates != goal and (0 <= y < width and 0 <= x < height):
            obstacles.append(coordinates)

    return obstacles 

def add_attractive_potential(grid, goal, strength=100):
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            dist = np.hypot(goal[0] - x, goal[1] - y)
            grid[y, x] -= strength / (dist + 1)  # Avoid division by zero
    return grid

def add_repulsive_potentials(grid, obstacles, strength=200, radius=6):
    for oy, ox in obstacles:
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                dist = np.hypot(ox - x, oy - y)
                if dist < radius:
                    grid[y, x] += strength * (1 / (dist + 1))
    return grid

def generate_heatmap():
    # Define the grid size
    width, height = 150, 150
    heatmap = np.zeros((height, width))
    goal = (140, 140)
    
    # Compute initial potential field
    for y in range(height):
        for x in range(width):
            heatmap[y, x] =0.01 * ((x-goal[0])**2 + (y-goal[1])**2)

    # Scan for obstacles
    data = scan()
    obstacles = scanned_points(data, goal, width, height)
    if not obstacles:
        print("No obstacles found")
        return

    # Apply potentials
    heatmap = add_attractive_potential(heatmap, goal)
    heatmap = add_repulsive_potentials(heatmap, obstacles)

    # Plot the heatmap
    plt.figure(figsize=(8, 6))
    plt.imshow(heatmap, origin='lower', cmap='hot', interpolation='nearest')
    plt.colorbar(label='Potential')
    plt.scatter(goal[0], goal[1], c='blue', label='Goal')
    for oy, ox in obstacles:
        plt.scatter(ox, oy, c='black', label='Obstacle' if (oy, ox) == obstacles[0] else "")
    plt.legend()
    plt.title("Potential Field for Robot Navigation")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(False)
    plot_path = "heatMap.png"
    plt.savefig(plot_path)
    print(f"Plot saved as {plot_path}")
    plt.show()
