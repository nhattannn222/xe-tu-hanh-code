import cv2   
import numpy as np
import RPi.GPIO as GPIO                    # Import GPIO library
import time

# Import time library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                    # Programming the GPIO by BCM pin numbers

TRIG = 17
ECHO = 27
led = 22

m11 = 16
m12 = 12
m21 = 21
m22 = 20

GPIO.setup(TRIG, GPIO.OUT)                  # Initialize GPIO Pin as outputs
GPIO.setup(ECHO, GPIO.IN)                   # Initialize GPIO Pin as input
GPIO.setup(led, GPIO.OUT)                  

GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)

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

# Capturing video through webcam
cap = cv2.VideoCapture(0)

forward()
while cap.isOpened():
    _, img1 = cap.read()
    img = img1[30:2000, 500:700]  # For leftmost ROI
    
    # Converting frame (img i.e BGR) to HSV (hue-saturation-value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Defining the range of red color
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    # Defining the range of green color
    green_lower = np.array([66, 122, 129], np.uint8)
    green_upper = np.array([86, 255, 255], np.uint8)

    # Finding the range of red and green color in the image
    red = cv2.inRange(hsv, red_lower, red_upper)
    green = cv2.inRange(hsv, green_lower, green_upper)

    # Morphological transformation, Dilation
    kernel = np.ones((5, 5), "uint8")

    red = cv2.dilate(red, kernel)
    res = cv2.bitwise_and(img, img, mask=red)
    
    green = cv2.dilate(green, kernel)
    res2 = cv2.bitwise_and(img, img, mask=green)    

    # Tracking the Red Color
    (contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)	
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(img, "RED color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))	
            print('Red')
            stop()

    # Tracking the Green Color
    (contours, hierarchy) = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)	
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "Green color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))  
            print('Green')
            forward()
           
    # Display the images (uncomment if you want to see the output)
    # cv2.imshow("Red Color Tracking", red)
    # cv2.imshow("Green Color Tracking", green)
    # cv2.imshow("Tracking", img)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break 

GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()
