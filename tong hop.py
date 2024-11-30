# Import libraries
import time
import math
import cv2
import numpy as np
try:
    import RPi.GPIO as GPIO  # Dùng RPi.GPIO trên Raspberry Pi
except ImportError:
    import Mock.GPIO as GPIO  # Dùng Mock.GPIO trên máy tính để mô phỏng

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define pins
TRIG = 17
ECHO = 27
led = 22
m11, m12, m21, m22 = 16, 12, 21, 20

# Initialize GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)

def stop():
    print('Stop')
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
    print('Back')

def left():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print('Left')

def right():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print('Right')

def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.1)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

def color_tracking():
    cap = cv2.VideoCapture(0)
    forward()
    while cap.isOpened():
        _, img1 = cap.read()
        img = img1[30:2000, 500:700]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        red_lower, red_upper = np.array([136, 87, 111], np.uint8), np.array([180, 255, 255], np.uint8)
        green_lower, green_upper = np.array([66, 122, 129], np.uint8), np.array([86, 255, 255], np.uint8)
        red, green = cv2.inRange(hsv, red_lower, red_upper), cv2.inRange(hsv, green_lower, green_upper)
        kernel = np.ones((5, 5), "uint8")
        red, green = cv2.dilate(red, kernel), cv2.dilate(green, kernel)

        contours, _ = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 300:
                stop()
                print('Red')
                break

        contours, _ = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 300:
                forward()
                print('Green')
                break

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def line_detection():
    cap = cv2.VideoCapture(0)
    a = b = c = 1
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        img = cv2.resize(img, (600, 600))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(cv2.equalizeHist(gray), (5, 5), 0)
        _, thresh = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY)
        lines = cv2.HoughLinesP(thresh, 1, np.pi / 180, 25, minLineLength=10, maxLineGap=40)
        l = r = 0

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if x2 - x1 != 0:
                    angle = math.atan2(y2 - y1, x2 - x1) * (180 / np.pi)
                    if -80 <= angle <= -30:
                        r += 1
                    elif 30 <= angle <= 80:
                        l += 1

        if l >= 10 and a == 1:
            print("Left")
            a, b, c = 0, 1, 1
        elif r >= 10 and b == 1:
            print("Right")
            a, b, c = 1, 0, 1
        elif l < 10 and r < 10 and c == 1:
            print("Straight")
            a, b, c = 1, 1, 0

        cv2.imshow('Thresh', thresh)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def main():
    try:
        GPIO.output(led, 1)
        print("Measuring distance and checking movement...")
        if measure_distance() < 30:
            print("Obstacle detected, stopping.")
            stop()
            time.sleep(1)
            back()
            time.sleep(1.5)
            right() if measure_distance() % 3 == 1 else left()
            time.sleep(1.5)
            stop()
        else:
            forward()
        
        print("Starting color tracking...")
        color_tracking()
        
        print("Starting line detection...")
        line_detection()

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        GPIO.cleanup()
        print("Cleanup done.")

if __name__ == "__main__":
    main()
