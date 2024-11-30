#!/usr/bin/env python3
# OpenCV và GPIO cho phát hiện biển báo và điều khiển xe tự hành
import math
import cv2
import numpy as np
import RPi.GPIO as GPIO

# Thiết lập GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Định nghĩa chân GPIO cho tín hiệu điều khiển
LEFT_PIN = 17
RIGHT_PIN = 27
STRAIGHT_PIN = 22
STOP_PIN = 23

# Thiết lập các chân làm output
GPIO.setup(LEFT_PIN, GPIO.OUT)
GPIO.setup(RIGHT_PIN, GPIO.OUT)
GPIO.setup(STRAIGHT_PIN, GPIO.OUT)
GPIO.setup(STOP_PIN, GPIO.OUT)

# Nạp mô hình nhận diện biển báo giao thông
model = cv2.dnn.readNetFromONNX("traffic_sign_classifier_lenet_v2.onnx")

# Hàm lọc và lấy bounding boxes từ hình ảnh mask
def filter_signs_by_color(img):
    # Code xử lý hình ảnh, trả về mask chứa các biển báo theo màu
    pass  # Giả sử đã có mã lọc màu

def get_boxes_from_mask(mask):
    # Code lấy bounding boxes từ mask
    pass  # Giả sử đã có mã lấy box từ mask

# Hàm phát hiện biển báo
def detect_traffic_signs(img, model, draw=None):
    """Phát hiện biển báo"""
    classes = ['unknown', 'left', 'no_left', 'right', 'no_right', 'straight', 'stop']
    mask = filter_signs_by_color(img)
    bboxes = get_boxes_from_mask(mask)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0

    signs = []
    for bbox in bboxes:
        x, y, w, h = bbox
        sub_image = img[y:y+h, x:x+w]
        if sub_image.shape[0] < 20 or sub_image.shape[1] < 20:
            continue
        sub_image = cv2.resize(sub_image, (32, 32))
        sub_image = np.expand_dims(sub_image, axis=0)
        model.setInput(sub_image)
        preds = model.forward()[0]
        cls = preds.argmax()
        score = preds[cls]
        if cls == 0 or score < 0.9:
            continue
        signs.append([classes[cls], x, y, w, h])
        if draw is not None:
            text = classes[cls] + ' ' + str(round(score, 2))
            cv2.rectangle(draw, (x, y), (x+w, y+h), (0, 255, 255), 4)
            cv2.putText(draw, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    return signs

# Hàm xử lý điều khiển dựa trên biển báo phát hiện được
def process_control(signs):
    GPIO.output(LEFT_PIN, GPIO.LOW)
    GPIO.output(RIGHT_PIN, GPIO.LOW)
    GPIO.output(STRAIGHT_PIN, GPIO.LOW)
    GPIO.output(STOP_PIN, GPIO.LOW)

    for sign in signs:
        cls = sign[0]
        if cls == 'left':
            GPIO.output(LEFT_PIN, GPIO.HIGH)
            print("Đi sang trái")
        elif cls == 'right':
            GPIO.output(RIGHT_PIN, GPIO.HIGH)
            print("Đi sang phải")
        elif cls == 'straight':
            GPIO.output(STRAIGHT_PIN, GPIO.HIGH)
            print("Đi thẳng")
        elif cls == 'stop':
            GPIO.output(STOP_PIN, GPIO.HIGH)
            print("Dừng lại")
        break  # Chỉ xử lý lệnh đầu tiên phát hiện

# Chạy phát hiện biển báo liên tục trên các ảnh đầu vào
try:
    for i, img in enumerate(bgr_images):  # bgr_images là các ảnh từ camera
        draw = img.copy()
        signs = detect_traffic_signs(img, model, draw=draw)
        process_control(signs)
        cv2.imshow("Detected Signs", draw)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    GPIO.cleanup()  # Dọn dẹp GPIO sau khi thoát
    cv2.destroyAllWindows()
