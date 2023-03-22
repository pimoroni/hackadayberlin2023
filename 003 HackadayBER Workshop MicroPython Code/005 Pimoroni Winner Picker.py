from machine import Pin
from servo import Servo, servo2040
import time, math, random

# Create a servo on pin 0
my_servo = Servo(servo2040.SERVO_1)

# Set up the servo position variables
idle_position = 0
left_position = -80
right_position = 79
step_size = 10

# Enable the servo (this puts it at the middle)
my_servo.enable()
time.sleep(2)

# Go to min
my_servo.to_min()
time.sleep(2)

left_button = Pin(15, Pin.IN, Pin.PULL_DOWN)
right_button = Pin(14, Pin.IN, Pin.PULL_DOWN)
prev_left_button_state = 1
prev_right_button_state = 1

def gitter():
    position = [10, 50, -30, -60, -10, 30]
    for _ in range(20):
        my_servo.value(random.choice(position))
        time.sleep(0.2)
        
while True:
    left_button_state = not left_button.value()
    if left_button_state and not prev_left_button_state:
        # Button has been released, trigger action
        print("Left Picked")
        gitter()
        my_servo.value(left_position)
        time.sleep(5)
    prev_left_button_state = left_button_state
    
    right_button_state = not right_button.value()
    if right_button_state and not prev_right_button_state:
        # Button has been released, trigger action
        print("Right Picked")
        gitter()
        my_servo.value(right_position)
        time.sleep(5)
    prev_right_button_state = right_button_state    
    
    
    time.sleep(0.02)
    my_servo.value(idle_position)    
    
