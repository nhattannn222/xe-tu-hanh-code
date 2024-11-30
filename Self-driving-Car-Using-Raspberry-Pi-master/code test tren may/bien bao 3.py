#!/usr/bin/env python3
import cv2
import numpy as np
import tensorflow as tf
import pandas as pd
import os
from sklearn.model_selection import train_test_split

# Đường dẫn tới các tệp và thư mục
TRAIN_DIR = "C:/AI/do an nganh/Self-driving-Car-Using-Raspberry-Pi-master/Self-driving-Car-Using-Raspberry-Pi-master/code test tren may/Dataset_trafficsignsVN-20241102T083235Z-001/Dataset_trafficsignsVN/Train"
EXCEL_PATH = "C:/AI/do an nganh/Self-driving-Car-Using-Raspberry-Pi-master/Self-driving-Car-Using-Raspberry-Pi-master/code test tren may/Dataset_trafficsignsVN-20241102T083235Z-001/Dataset_trafficsignsVN/class.csv"
MODEL_PATH = "C:/AI/do an nganh/Self-driving-Car-Using-Raspberry-Pi-master/Self-driving-Car-Using-Raspberry-Pi-master/code test tren may/Dataset_trafficsignsVN/CNN_SignTrafficVN_new.h5"

# Đọc danh sách biển báo từ class.csv
class_labels_df = pd.read_csv(EXCEL_PATH, header=None)
classes = class_labels_df.iloc[0].tolist()  # Lấy danh sách biển báo từ hàng đầu tiên
num_classes = len(classes)

# Hàm chuẩn bị dữ liệu từ thư mục huấn luyện
def load_data(data_dir):
    images, labels = [], []
    classes = os.listdir(data_dir)
    
    print("Các lớp đã tìm thấy:", classes)  # Dòng in để gỡ lỗi
    for label, class_name in enumerate(classes):
        class_dir = os.path.join(data_dir, class_name)
        if os.path.isdir(class_dir):
            print(f"Tải ảnh từ {class_dir}")
            for file in os.listdir(class_dir):
                img_path = os.path.join(class_dir, file)
                img = cv2.imread(img_path)
                if img is not None:
                    img = cv2.resize(img, (32, 32))  # Đổi kích thước thành 32x32
                    images.append(img)
                    labels.append(label)
                else:
                    print(f"Không thể tải ảnh: {img_path}")
        else:
            print(f"Thư mục không tồn tại: {class_dir}")
    
    print(f"Tổng số ảnh đã tải: {len(images)}")  # Dòng in để gỡ lỗi
    return np.array(images), np.array(labels)

# Chuẩn bị dữ liệu từ thư mục huấn luyện
X, y = load_data(TRAIN_DIR)

# Chuẩn hóa và one-hot encode nhãn
X = X / 255.0
y = tf.keras.utils.to_categorical(y, num_classes)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Xây dựng mô hình CNN
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

# Biên dịch mô hình
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Huấn luyện mô hình
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), verbose=1)

# Lưu mô hình đã huấn luyện vào tệp .h5 mới
model.save(MODEL_PATH)
print("Mô hình đã được lưu tại:", MODEL_PATH)
