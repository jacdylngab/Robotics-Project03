from gpiozero import Motor, PWMOutputDevice
from time import sleep
import math

# Define the pins connected to L293D for motor 1 (right) and 2 (left)
motor1 = Motor(forward=27, backward=17)
motor2 = Motor(forward=23, backward=18)

enable1 = PWMOutputDevice(24, frequency=1000)
enable2 = PWMOutputDevice(22, frequency=1000)

radius = 3
d = 15
#angle = math.pi / 2


def setup():
    global p1, p2
    p1 = enable1
    p2 = enable2

def get_rotation_direction(current_angle, target_angle):
    # Normalize both angles to [0, 360]
    current = current_angle % (2 * math.pi)
    target = target_angle % (2 * math.pi)

    # Find the smallest angle difference
    delta = (target - current) % (2 * math.pi)

    # Decide turn direction
    if delta == 0:
        return 0 # No turn needed
    elif delta <= math.pi: 
        return -1 # Turn left
    else:
        return 1 # Turn right

def get_turn_amount(current_angle, target_angle):
    delta = (target_angle - current_angle) % (2 * math.pi)
    return delta if delta <= math.pi else (2 * math.pi) - delta

def turn(duty_cycle_left, duty_cycle_right, direction):
    motor1.forward()
    motor2.forward()
    p1.value = duty_cycle_left
    p2.value = duty_cycle_right

    dt = (direction * d) / (4 * math.pi * radius * (p2.value - p1.value))

    sleep(dt)
    p1.off()
    p2.off()

# This function identifies whether to turn left or right based on the angle
def smart_turn(current_angle, target_angle):
    direction = get_rotation_direction(current_angle, target_angle)
    angle_to_turn = get_turn_amount(current_angle, target_angle)
    print(f"direction: {direction}")

    if direction == 0:
        print("Already facing the target angle.")
        return

    # Set duty cycles based on direction
    if direction == 1: # Turn right
        print("Turning right...")
        turn(duty_cycle_left=0.5, duty_cycle_right=0, direction=-angle_to_turn-0.9)
    else: # turn left
        print("Turning left...")
        turn(duty_cycle_left=0, duty_cycle_right=0.5, direction=angle_to_turn+1.4)


def motor(speed):
    motor1.forward()
    motor2.forward()
    p1.value = speed / 100  # Convert Speed (0-100) to 0-1 range
    p2.value = (speed / 100)

    sleep(3)
    p1.off()
    p2.off()

    '''
    motor1.backward()
    motor2.backward()
    p1.value = (speed / 100) - 0.012  # Convert Speed (0-100) to 0-1 range
    p2.value = speed / 100 

    sleep(3)
    p1.off()
    p2.off()
    '''


def destroy():
    p1.off()
    p2.off()
    motor1.stop()
    motor2.stop()
'''
if __name__ == "__main__":
    setup()
    #motor(50)
    #motor(100)
    #print("Left tank turn 45 degrees")
    #turn(duty_cycle_left=0, duty_cycle_right=0.5, direction=(math.pi/2)+1)
    #print("Right tank turn 45 degrees")
    #turn(duty_cycle_left=0.5, duty_cycle_right=0, direction=-(math.pi/4)-0.9)
    smart_turn(math.pi/3, math.pi/4)
    
    destroy()
'''
