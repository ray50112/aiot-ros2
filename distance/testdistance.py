import cv2
import numpy as np
import serial
import time
port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)
# 載入人臉檢測器（使用OpenCV內建的Haar分類器）
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 設定攝影機的參數（需根據實際情況進行調整）
focal_length = 800  # 估計的焦距，單位：像素
baseline = 10  # 立體視覺相機的基線長度，單位：任意單位（例如米）

# 初始化攝像頭
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame,(1000,600))
    # 將影像轉為灰階
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Camera", frame)

    # 按空格鍵拍攝照片
    key = cv2.waitKey(1)
    if key == ord(' '):
        cv2.imwrite('captured_photo.jpg', frame)
        print("照片已拍攝並保存為 captured_photo.jpg")

        # 進行人臉檢測
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # 計算人臉中心座標
            center_x = x + w // 2
            center_y = y + h // 2

            # 計算視差
            disparity = focal_length * baseline / w

            # 估算距離
            distance = disparity
            a = (distance/10)
            # 在影像上標記人臉位置並顯示距離信息
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Distance: {distance:.2f} units", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 將距離信息寫入文件
        with open('distance.txt', 'w') as file:
            file.write(f"Distance: {distance:.2f} units")
            cv2.imwrite('captured_photo.jpg', frame)
        cv2.imshow("Camera", frame)
        cv2.waitKey(0)  # 等待按任意鍵繼續
        while (a > 1):
            port.write('W'.encode('ascii'))
            time.sleep(1)
            a = a-1
        port.write('X'.encode('ascii'))
        time.sleep(1)
        # 關閉攝影機並退出迴圈
        cap.release()
        cv2.destroyAllWindows()
        break
    elif key == ord('q'):
        break