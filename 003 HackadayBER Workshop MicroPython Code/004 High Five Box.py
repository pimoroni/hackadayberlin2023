import time
from machine import Pin
from servo import Servo, servo2040


# Set up the servo the _1 dinotes the gpio pin
my_servo = Servo(servo2040.SERVO_1)

# Set up the button and LED
button = Pin(14, Pin.IN, Pin.PULL_DOWN)
led = Pin(15, Pin.OUT)
led.on()


# Set up the servo position variables and button state
max_position = 80
current_position = 80
target_position = -20
step_size = 10
prev_button_state = 0


# Enable the servo (normally sets the servo to a start position)
my_servo.enable()
time.sleep(2)

# Move the servo to the maximum position
my_servo.value(max_position)

while True:
    # Loop until the user moves the servo to the minimum position
    while current_position >= target_position:
        # Check button state and do stuff when released
        button_state = not button.value()
        if button_state and not prev_button_state:
            # Button has been released, trigger action
            print("Button released")
            # Move the servo back 10 degrees
            current_position -= step_size
        if current_position < max_position:
            current_position += 1
    
        # Reset button state
        prev_button_state = button_state

        my_servo.value(current_position)
        print(current_position)
        # Change the time to reset the difficulty 
        time.sleep(0.02)

    my_servo.value(max_position)
    time.sleep(2)
    current_position = 80
    print("success")

my_servo.disable()
