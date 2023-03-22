#This code is based on https://projects.raspberrypi.org/en/projects/get-started-pico-w/0 

import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
from servo import Servo, servo2040

ssid = 'NAME OF YOUR WIFI NETWORK'
password = 'YOUR SECRET PASSWORD'

# Set up the servo the _1 dinotes the gpio pin 
my_servo1 = Servo(servo2040.SERVO_1)

# Enable the servo (normally sets the servo to a start position)
my_servo1.enable()
sleep(2)

# Move the servo to a default position
my_servo1.value(0)

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection
    
def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            <p>Servo control:</p>
            <form action="./-60">
            <input type="submit" value="-60" />
            </form>
            <form action="./0">
            <input type="submit" value="0" />
            </form>
            <form action="./60">
            <input type="submit" value="60" />
            </form>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
        elif request =='/-60?':
            my_servo1.value(-60)
            sleep(1)
        elif request =='/0?':
            my_servo1.value(0)
            sleep(1)
        elif request =='/60?':
            my_servo1.value(60)
            sleep(1)
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()