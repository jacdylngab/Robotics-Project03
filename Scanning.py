from time import sleep
import statistics
from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from gpiozero import DistanceSensor

trigPin = 26  # GPIO 26
echoPin = 19  # GPIO 19

sensor = DistanceSensor(echo=echoPin, trigger=trigPin, max_distance=2.2)

i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)

pca.frequency = 50  # the 20 ms width required by the servos
servo0 = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2400)  # SG90

def get_distance(samples):
    readings = []

    for _ in range(samples):
        distance = sensor.distance * 100
        readings.append(distance)
        sleep(0.05)

    return statistics.mean(readings)  # Return mean value

def real_data(scan_data):
    distances = [dist[1] for dist in scan_data]
    
    mean = statistics.mean(distances)
    print(f"mean: {mean}")
    standard_deviation = statistics.stdev(distances)
    print(f"standard_deviation: {standard_deviation}")

    threshold = 1 # This helps identify the severity of what is considered an outlier
    lower_bound = mean - (threshold * standard_deviation)
    upper_bound = mean + (threshold * standard_deviation)

    outliers = [x for x in distances if x < lower_bound or x > upper_bound]
    print(f"outliers: {outliers}")
    
    real_data = [data for data in scan_data if data[1] not in outliers]
    print(f"real_data: {real_data}")

    return real_data


def scan():
    scan_data = [] # Store scanned points
    start_angle = 90

    anticlockwise_angles = [i for i in range(start_angle + 5, 181, 5)]
    clockwise_angles = [i for i in range(start_angle, -1, -5)]
    first_pass = True

    try:
        while first_pass:
            # Start at current position
            servo0.angle = start_angle
            distance = get_distance(10)
            if distance < 40: #Range limit
                scan_data.append((start_angle, distance))
            print(f"{start_angle} degrees: {distance:.2f} cm")
            sleep(0.1) # Small delay for stability

            for angle_list in [anticlockwise_angles, reversed(anticlockwise_angles[:-1]), clockwise_angles, reversed(clockwise_angles[:-1])]:
                for angle in angle_list:
                    servo0.angle = angle
                    distance = get_distance(10)
                    if distance < 40: # Range limit
                        scan_data.append((angle, distance))
                    print(f"{angle} degrees: {distance:.2f} cm")
                    sleep(0.1) # Small delay for stability

            first_pass = False
            print(f"scan_data: {scan_data}")
            filtered_real_data = real_data(scan_data)
            return filtered_real_data
            
    except KeyboardInterrupt:  # Press ctrl-c to end the program
        print("Ending program")
        servo0.angle = None
        pca.deinit()
        sensor.close()
        filtered_real_data = real_data(scan_data)
        return filtered_real_data
        