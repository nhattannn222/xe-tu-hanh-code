import time
from unittest import mock

# Giả lập GPIO
GPIO = mock.MagicMock()

# Định nghĩa một số hằng số
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
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print('back')

def left():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print('left')

def right():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print("right")

# Giả lập khoảng cách cho việc kiểm tra
def simulate_distance():
    # Giả lập khoảng cách ngẫu nhiên
    return 30  # Đặt khoảng cách này theo ý muốn để thử nghiệm

count = 0
while True:
    avgDistance = 0
    for _ in range(5):
        # Giả lập quá trình đo khoảng cách
        distance = simulate_distance()  # Thay thế đo khoảng cách thực tế
        avgDistance += distance

    avgDistance /= 5
    print(avgDistance)
    flag = 0

    if avgDistance < 25:
        count += 1
        stop()
        time.sleep(1)
        time.sleep(1.5)

        if (count % 3 == 1) and (flag == 0):
            right()
            flag = 1
        else:
            left()
            flag = 0

        time.sleep(1.5)
        stop()
        time.sleep(1)
    else:
        forward()
        flag = 0

    # Thêm một điều kiện để thoát khỏi vòng lặp
    if count >= 10:  # Thay thế điều kiện này để dừng chương trình khi cần
        break
