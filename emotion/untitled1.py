import cv2
from keras.models import model_from_json
import numpy as np

# 打開存有神經網絡模型結構的JSON文件
json_file = open("facialemotionmodel.json", "r")
model_json = json_file.read()
json_file.close()

# 從JSON文件中載入神經網絡模型
model = model_from_json(model_json)

# 載入神經網絡權重
model.load_weights("facialemotionmodel.h5")

# 載入Haar級聯分類器，用於人臉檢測
haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)

# 定義函數，用於提取圖像特徵
def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0  # 正規化圖像特徵

# 打開電腦攝像頭
webcam = cv2.VideoCapture(0)

# 定義情感標籤字典
labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

while True:
    # 讀取攝像頭捕獲的畫面
    ret, frame = webcam.read()
    
    # 顯示攝像頭的視窗
    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)

    if key == ord('z'):
        # 按下 "Z" 鍵拍照
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        
        try:
            for (p, q, r, s) in faces:
                image = gray[q:q + s, p:p + r]
                cv2.rectangle(frame, (p, q), (p + r, q + s), (255, 0, 0), 2)
                image = cv2.resize(image, (48, 48))
                img = extract_features(image)
                pred = model.predict(img)
                prediction_label = labels[pred.argmax()]
                cv2.putText(frame, '%s' % (prediction_label), (p - 10, q - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))
            
            cv2.imshow("Output", frame)
            
        except cv2.error:
            pass
    
    # 按下 "q" 鍵退出程式
    if key == ord('q'):
        break

# 釋放攝像頭資源
webcam.release()
cv2.destroyAllWindows()