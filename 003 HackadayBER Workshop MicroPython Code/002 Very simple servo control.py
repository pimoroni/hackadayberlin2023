import time
from machine import Pin
from servo import Servo, servo2040

# Set up the servo the _1 dinotes the gpio pin 
my_servo1 = Servo(servo2040.SERVO_1)

# Set up the servo position the range is -80 to 80
max_position = -60

# Enable the servo (normally sets the servo to a start position)
my_servo1.enable()
time.sleep(2)
 
# Move the servo to the maximum position
my_servo1.value(max_position)

