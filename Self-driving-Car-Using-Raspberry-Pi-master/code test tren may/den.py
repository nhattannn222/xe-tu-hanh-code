import cv2
import numpy as np

# Mock GPIO khi chạy trên máy tính
class MockGPIO:
    OUT = 'out'
    IN = 'in'
    BCM = 'BCM'  # Thêm giá trị BCM giả lập
    
    @staticmethod
    def setwarnings(warnings):
        pass  # Giả lập phương thức setwarnings, không làm gì cả
    
    @staticmethod
    def setmode(mode):
        pass
    
    @staticmethod
    def setup(pin, mode):
        pass
    
    @staticmethod
    def output(pin, state):
        pass
    
    @staticmethod
    def cleanup():
        pass

GPIO = MockGPIO()  # Thay thế RPi.GPIO bằng MockGPIO khi thử nghiệm trên máy tính


# Constants (các chân GPIO giả lập)
TRIG = 17
ECHO = 27
led = 22

m11 = 16
m12 = 12
m21 = 21
m22 = 20

# GPIO setup (không sử dụng thật, nên có thể bỏ qua)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def stop():
    print('stop')
    # GPIO.output(m11, 0)
    # GPIO.output(m12, 0)
    # GPIO.output(m21, 0)
    # GPIO.output(m22, 0)

def forward():
    print('Forward')
    # GPIO.output(m11, 0)
    # GPIO.output(m12, 1)
    # GPIO.output(m21, 1)
    # GPIO.output(m22, 0)

# Capturing video through webcam
cap = cv2.VideoCapture(0)

forward()
while cap.isOpened():
    _, img1 = cap.read()
    img = img1[30:2000, 500:700]  # Chọn vùng ROI (để kiểm tra phần bên trái)

    # Chuyển ảnh từ BGR (OpenCV mặc định) sang HSV (Màu sắc)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Định nghĩa phạm vi màu đỏ trong không gian HSV
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    # Định nghĩa phạm vi màu xanh lá cây trong không gian HSV
    green_lower = np.array([66, 122, 129], np.uint8)
    green_upper = np.array([86, 255, 255], np.uint8)

    # Tìm kiếm màu đỏ và xanh lá cây trong ảnh
    red = cv2.inRange(hsv, red_lower, red_upper)
    green = cv2.inRange(hsv, green_lower, green_upper)

    # Biến đổi hình học, Dilation (phóng đại)
    kernel = np.ones((5, 5), "uint8")
    red = cv2.dilate(red, kernel)
    res = cv2.bitwise_and(img, img, mask=red)
    
    green = cv2.dilate(green, kernel)
    res2 = cv2.bitwise_and(img, img, mask=green)

    # Theo dõi màu đỏ
    (contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)    
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(img, "RED color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))    
            print('Red')
            stop()

    # Theo dõi màu xanh lá cây
    (contours, hierarchy) = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)    
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "Green color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))  
            print('Green')
            forward()
           
    # Hiển thị hình ảnh (bạn có thể mở lại nếu muốn xem kết quả)
    # cv2.imshow("Red Color Tracking", red)
    # cv2.imshow("Green Color Tracking", green)
    cv2.imshow("Tracking", img)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break 

# GPIO.cleanup()  # Gọi khi sử dụng trên Raspberry Pi
cap.release()
cv2.destroyAllWindows()
