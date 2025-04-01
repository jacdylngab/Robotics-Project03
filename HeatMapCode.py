import numpy as np
import matplotlib.pyplot as plt

# Define the grid size
width, height = 150, 150
heatmap = np.zeros((height, width))
goal = (140, 140)
for y in range(height):
    for x in range(width):
        heatmap[y, x] =0.01 * ((x-goal[0])**2 + (y-goal[1])**2)
def add_attractive_potential(grid, goal, strength=100):
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            dist = np.hypot(goal[0] - x, goal[1] - y)
            grid[y, x] -= strength / (dist + 1)  # Avoid division by zero
    return grid

# Define repulsive potential (obstacles)
obstacles = [(95,30),(90,33),(97,35),(90,37),(85,40),(87,45),(105,105),(108,106),(112,98)]
def add_repulsive_potentials(grid, obstacles, strength=200, radius=6):
    for oy, ox in obstacles:
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):
                dist = np.hypot(ox - x, oy - y)
                if dist < radius:
                    grid[y, x] += strength * (1 / (dist + 1))
    return grid

# Apply potentials
heatmap = add_attractive_potential(heatmap, goal)
heatmap = add_repulsive_potentials(heatmap, obstacles)

# Plot the heatmap
plt.figure(figsize=(8, 6))
plt.imshow(heatmap, origin='lower', cmap='hot', interpolation='nearest')
plt.colorbar(label='Potential')
plt.scatter(goal[0], goal[1], c='blue', label='Goal')
for ox, oy in obstacles:
    plt.scatter(oy, ox, c='black', label='Obstacle' if (ox, oy) == obstacles[0] else "")
plt.legend()
plt.title("Potential Field for Robot Navigation")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(False)
plot_path = "heatMap.png"
plt.savefig(plot_path)
print(f"Plot saved as {plot_path}")
plt.show()
