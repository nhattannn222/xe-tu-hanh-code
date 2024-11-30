import cv2
import numpy as np
from tensorflow.keras.models import load_model
import pandas as pd
import playsound  # Cần cài đặt thư viện playsound để phát âm thanh: pip install playsound==1.2.2

# Đường dẫn đến model đã train và file class
model_path = "C:\\AI\\do an nganh\\Self-driving-Car-Using-Raspberry-Pi-master\\Self-driving-Car-Using-Raspberry-Pi-master\\code test tren may\\Dataset_trafficsignsVN\\CNN_SignTrafficVN_new.h5"
class_file_path = "C:\\AI\\do an nganh\\Self-driving-Car-Using-Raspberry-Pi-master\\Self-driving-Car-Using-Raspberry-Pi-master\\code test tren may\\Dataset_trafficsignsVN-20241102T083235Z-001\\Dataset_trafficsignsVN\\class.csv"

# Load model và tên lớp
model = load_model(model_path)
class_names = pd.read_csv(class_file_path, header=None)
class_labels = class_names[0].values
print(f"Số lượng lớp trong class_labels: {len(class_labels)}")  # Kiểm tra số lớp trong class_labels

# Định nghĩa cảnh báo cho từng loại biển báo
warnings = {
    "Turn Left": "alert_turn_left.mp3",     # Đường dẫn đến file âm thanh cảnh báo rẽ trái
    "Turn Right": "alert_turn_right.mp3",   # Đường dẫn đến file âm thanh cảnh báo rẽ phải
    "U-Turn": "alert_u_turn.mp3",           # Đường dẫn đến file âm thanh cảnh báo quay lại
    "Go Straight": "alert_go_straight.mp3", # Đường dẫn đến file âm thanh cảnh báo đi thẳng
    "Stop": "alert_stop.mp3"                # Đường dẫn đến file âm thanh cảnh báo dừng
}

# Hàm phát âm thanh cảnh báo
def play_warning_sound(warning_label):
    if warning_label in warnings:
        try:
            playsound.playsound(warnings[warning_label], block=False)
            print(f"Phát cảnh báo: {warning_label}")
        except Exception as e:
            print(f"Không thể phát âm thanh cho cảnh báo '{warning_label}': {e}")

# Hàm phát hiện biển báo từ một khung hình
def detect_and_display_signs(frame):
    # Resize và chuẩn hóa hình ảnh
    image = cv2.resize(frame, (30, 30))
    image = image.astype('float32') / 255.0
    image = np.expand_dims(image, axis=0)

    # Dự đoán biển báo
    predictions = model.predict(image)
    predicted_class = np.argmax(predictions)

    # Kiểm tra nếu predicted_class vượt ngoài phạm vi của class_labels
    if 0 <= predicted_class < len(class_labels):
        sign_label = class_labels[predicted_class]
    else:
        print(f"Predicted class {predicted_class} is out of bounds!")
        sign_label = "Unknown"

    # Hiển thị tên biển báo lên khung hình
    print(f"Detected sign: {sign_label}")  # In tên biển báo ra console để kiểm tra
    cv2.putText(frame, f"Sign: {sign_label}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Phát cảnh báo nếu là biển báo đặc biệt
    play_warning_sound(sign_label)

    return frame

# Mở video và phát hiện biển báo
video_path = "C:\\AI\\do an nganh\\Self-driving-Car-Using-Raspberry-Pi-master\\Một số biển báo hiệu giao thông đường bộ thường gặp - YouTube - Google Chrome 2024-11-10 21-27-45.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Phát hiện biển báo và hiển thị
    output_frame = detect_and_display_signs(frame)
    cv2.imshow("Traffic Sign Detection", output_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
