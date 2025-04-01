import matplotlib.pyplot as plt
import math 

def polar_to_cartesian(angle, distance):
    radians = math.radians(angle) 
    x = distance * math.cos(radians)
    y = distance * math.sin(radians)
    return x, y

def plot_scan(data):
    x_values, y_values = [], []

    for angle, distance in data:
        x, y = polar_to_cartesian(angle, distance)
        x_values.append(x)
        y_values.append(y)

    plt.figure(figsize=(6, 6))
    plt.scatter(x_values, y_values, c='r', label="Scanned Points")
    plt.axhline(0, color='k', linewidth=1)
    plt.axvline(0, color='k', linewidth=1)
    plt.xlim(-100, 100)
    plt.ylim(0, 100)

    # Set ticks every 1 unit
    plt.xticks(range(-100, 101, 10))
    plt.yticks(range(0, 101, 10))

    plt.xlabel("X (cm)")
    plt.ylabel("Y (cm)")
    plt.title("Ultrasonic Range Sensor Mapping")
    plt.legend()
    plt.grid(True)

    plot_path = "scan_plot.png"
    plt.savefig(plot_path)
    print(f"Plot saved as {plot_path}")

    plt.show()