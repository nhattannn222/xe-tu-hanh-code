#!/usr/bin/env python3.4
# OpenCV 3.1.0
import math
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

def slope(vx1, vx2, vy1, vy2):         # Parameters to calculate slope
    m = float(vy2 - vy1) / float(vx2 - vx1)  # Slope equation
    theta1 = math.atan(m)                  # Calculate the slope angle
    return theta1 * (180 / np.pi)          # Calculated angle in degrees

cap = cv2.VideoCapture(0)

# Variables for tracking turns
a = b = c = 1

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break
    img = cv2.resize(img, (600, 600))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(gray)
    blur = cv2.GaussianBlur(equ, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY)

    # Find Contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Draw Contours
    cv2.drawContours(thresh, contours, -1, (255, 0, 0), 3)
    
    drawing = np.zeros(img.shape, np.uint8)

    # Detect lines using Hough Transform
    lines = cv2.HoughLinesP(thresh, 1, np.pi / 180, 25, minLineLength=10, maxLineGap=40)

    l = r = 0
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                if (x2 - x1) != 0:
                    arctan = slope(x1, x2, y1, y2)

                    if 250 < y1 < 600 and 250 < y2 < 600:
                        if -80 <= arctan <= -30:
                            r += 1
                            l = 0
                            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
                        elif 30 <= arctan <= 80:
                            l += 1
                            r = 0
                            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2, cv2.LINE_AA)

    # Determine the direction
    if l >= 10 and a == 1:
        print('left')
        a, b, c = 0, 1, 1
    elif r >= 10 and b == 1:
        print('right')
        a, b, c = 1, 0, 1
    elif l < 10 and r < 10 and c == 1:
        print('straight')
        a, b, c = 1, 1, 0

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Processed Video')
    plt.show()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
