import cv2
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

# Đường dẫn đến model đã train
model_path = "C:\\AI\\do an nganh\\Self-driving-Car-Using-Raspberry-Pi-master\\Self-driving-Car-Using-Raspberry-Pi-master\\code test tren may\\Dataset_trafficsignsVN\\CNN_SignTrafficVN_new.h5"

# Đường dẫn đến file class.csv
class_file_path = "C:\\AI\\do an nganh\\Self-driving-Car-Using-Raspberry-Pi-master\\Self-driving-Car-Using-Raspberry-Pi-master\\code test tren may\\Dataset_trafficsignsVN-20241102T083235Z-001\\Dataset_trafficsignsVN\\class.csv"

# Load model
model = load_model(model_path)

# Đọc file class.csv mà không có tiêu đề
class_names = pd.read_csv(class_file_path, header=None)

# Chuyển đổi DataFrame thành một danh sách chứa tên các biển báo
class_labels = class_names[0].values

# Hàm để dự đoán biển báo từ hình ảnh
def predict_traffic_sign(image_path):
    # Đọc hình ảnh và resize về kích thước mong muốn
    image = cv2.imread(image_path)
    image = cv2.resize(image, (30, 30))  # Giả sử model của bạn yêu cầu kích thước 30x30
    image = image.astype('float32') / 255.0  # Chuẩn hóa hình ảnh
    image = np.expand_dims(image, axis=0)  # Thêm kích thước batch

    # Dự đoán biển báo
    predictions = model.predict(image)
    predicted_class = np.argmax(predictions)  # Lấy lớp có xác suất cao nhất

    return class_labels[predicted_class]  # Trả về tên biển báo tương ứng

# Ví dụ sử dụng hàm
image_path = "C:\\AI\\do an nganh\\Self-driving-Car-Using-Raspberry-Pi-master\\Self-driving-Car-Using-Raspberry-Pi-master\\code test tren may\\Dataset_trafficsignsVN-20241102T083235Z-001\\Dataset_trafficsignsVN\\Train\\101_DuongCam\\1 - Copy (3).png"
predicted_sign = predict_traffic_sign(image_path)
print(f"Predicted Traffic Sign: {predicted_sign}")