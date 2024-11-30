import time
from unittest import mock

# Giả lập GPIO
GPIO = mock.MagicMock()

# Định nghĩa các hằng số GPIO
GPIO.BCM = 'BCM'
TRIG = 17
ECHO = 27
led = 22
m11 = 16
m12 = 12
m21 = 21
m22 = 20

# Hàm setup giả lập
def setup(pin, mode):
    GPIO.setup(pin, mode)

# Thay thế các phương thức GPIO thực tế bằng mock
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup = setup
GPIO.output = mock.MagicMock()
GPIO.input = mock.MagicMock(return_value=0)

# Giả lập các phương thức LED và động cơ
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

# Giả lập khoảng cách cho việc kiểm tra
def simulate_distance():
    # Giả lập khoảng cách ngẫu nhiên hoặc theo logic
    return 40  # Bạn có thể thay đổi giá trị này để thử nghiệm

def dist():
    time.sleep(0.1)  # Giả lập độ trễ trong việc đo khoảng cách
    distance = simulate_distance()  # Gọi hàm giả lập
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
