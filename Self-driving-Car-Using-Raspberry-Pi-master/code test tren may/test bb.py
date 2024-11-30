import cv2
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import time

# Sử dụng Mock GPIO khi không có RPi.GPIO
try:
    import RPi.GPIO as GPIO
    print("Sử dụng thư viện RPi.GPIO trên Raspberry Pi")
except ModuleNotFoundError:
    class MockGPIO:
        OUT = 'out'
        IN = 'in'
        BCM = 'BCM'
        LOW = 0
        HIGH = 1

        @staticmethod
        def setwarnings(flag):
            print(f"MockGPIO: setwarnings({flag})")

        @staticmethod
        def setmode(mode):
            if mode == MockGPIO.BCM:
                print("MockGPIO: Mode set to BCM")
            else:
                print(f"MockGPIO: Unsupported mode {mode}")

        @staticmethod
        def setup(pin, mode):
            print(f"MockGPIO: Pin {pin} set as {mode}")

        @staticmethod
        def output(pin, state):
            state_str = 'HIGH' if state == MockGPIO.HIGH else 'LOW'
            print(f"MockGPIO: Pin {pin} set to {state_str}")

        @staticmethod
        def cleanup():
            print("MockGPIO: Cleaning up GPIO")

    GPIO = MockGPIO()
    print("Sử dụng Mock GPIO trên máy tính")


# Đường dẫn đến model và class.csv
model_path = "C:\\AI\\do an nganh\\Self-driving-Car-Using-Raspberry-Pi-master\\Self-driving-Car-Using-Raspberry-Pi-master\\code test tren may\\Dataset_trafficsignsVN\\CNN_SignTrafficVN_new.h5"
class_file_path = "C:\\AI\\do an nganh\\Self-driving-Car-Using-Raspberry-Pi-master\\Self-driving-Car-Using-Raspberry-Pi-master\\code test tren may\\Dataset_trafficsignsVN-20241102T083235Z-001\\Dataset_trafficsignsVN\\class.csv"

# Khởi tạo GPIO (thay bằng Mock.GPIO nếu thử nghiệm)
GPIO.setmode(GPIO.BCM)
# Gán chân GPIO cho động cơ (giả sử)
motor_pins = {"forward": 17, "backward": 18, "left": 22, "right": 23, "stop": 24}
for pin in motor_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Load model và file class
model = load_model(model_path)
class_names = pd.read_csv(class_file_path, header=None)
class_labels = class_names[0].values

# Hàm điều khiển động cơ
def control_motor(command):
    for pin in motor_pins.values():
        GPIO.output(pin, GPIO.LOW)  # Tắt tất cả trước
    if command in motor_pins:
        GPIO.output(motor_pins[command], GPIO.HIGH)  # Bật lệnh cần thiết

def predict_traffic_sign(image):
    image = cv2.resize(image, (30, 30))
    image = image.astype('float32') / 255.0
    image = np.expand_dims(image, axis=0)
    predictions = model.predict(image)
    predicted_class = np.argmax(predictions)

    if predicted_class >= len(class_labels):
        print(f"Warning: predicted class {predicted_class} out of bounds!")
        predicted_class = 0  # Chọn một lớp mặc định trong trường hợp này
        
    return class_labels[predicted_class]


# Map lệnh từ biển báo sang điều khiển
sign_to_command = {
    "Đi Thẳng": "forward",
    "Rẽ Trái": "left",
    "Rẽ Phải": "right",
    "Dừng Lại": "stop",
}

# Khởi tạo camera
cap = cv2.VideoCapture(0)  # Thay 0 bằng id camera nếu cần

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không nhận được hình ảnh từ camera")
            break
        
        # Dự đoán biển báo
        predicted_sign = predict_traffic_sign(frame)
        print(f"Biển báo nhận diện: {predicted_sign}")

        # Điều khiển động cơ
        command = sign_to_command.get(predicted_sign, "stop")  # Mặc định dừng nếu không nhận diện
        control_motor(command)
        print(f"Lệnh động cơ: {command}")
        
        time.sleep(0.5)  # Chờ một chút trước khi xử lý tiếp

except KeyboardInterrupt:
    print("Kết thúc chương trình")

finally:
    cap.release()
    GPIO.cleanup()
    print("Dọn dẹp và thoát")
