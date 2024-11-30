import RPi.GPIO as GPIO  # Import GPIO library
import time

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Programming the GPIO by BCM pin numbers

# Define GPIO pins
TRIG = 17
ECHO = 27
led = 22
m11 = 16
m12 = 12
m21 = 21
m22 = 20

# Setup GPIO pins
GPIO.setup(TRIG, GPIO.OUT)  # Initialize TRIG as output
GPIO.setup(ECHO, GPIO.IN)   # Initialize ECHO as input
GPIO.setup(led, GPIO.OUT)    # Initialize LED as output

GPIO.setup(m11, GPIO.OUT)    # Motor control pins
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)

# Turn on LED for 5 seconds
GPIO.output(led, 1)
time.sleep(5)

def stop():
    print('stop')
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)

def forward():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print('Forward')

def back():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print('back')

def left():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print('left')

def right():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print("right")

def dist():
    GPIO.output(TRIG, False)  # Set TRIG as LOW
    time.sleep(0.1)  # Delay

    GPIO.output(TRIG, True)  # Set TRIG as HIGH
    time.sleep(0.00001)  # Delay of 0.00001 seconds
    GPIO.output(TRIG, False)  # Set TRIG as LOW

    # Measure pulse duration
    while GPIO.input(ECHO) == 0:
        GPIO.output(led, False)
    pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        GPIO.output(led, False)
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start  # Time to get back the pulse to sensor
    distance = pulse_duration * 17150  # Multiply pulse duration by 17150 (34300/2) to get distance
    distance = round(distance, 2)  # Round to two decimal points
    return distance

p = 0

forward()
while True:
    if p == 1:
        stop()

    # Move left for 1.2 seconds
    now = time.time()
    while time.time() <= now + 1.2:
        left()
    stop()

    # Move back for 0.7 seconds
    now = time.time()
    while time.time() <= now + 0.7:
        back()
    print('park')
    stop()
    break

# Measure distance
distance = dist()
if distance > 30:
    now = time.time()
    while time.time() <= now + 0.3:
        distance = dist()
        print(distance)
        if distance < 30:
            p = 0
            break
        p = 1

# Cleanup GPIO settings
GPIO.cleanup()
