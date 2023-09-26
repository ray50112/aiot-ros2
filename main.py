import requests
import speech_recognition as sr
from playrobot import TTS
from googleapiclient.discovery import build
import webbrowser
import cv2
from tensorflow.keras.models import model_from_json
import numpy as np

# 使用Google語音識別進行語音轉文字
def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("請說話...")
        TTS.wordToSound("請說話...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='zh-TW')
        print(f"您說的是：{text}")
        TTS.wordToSound("您說的是：")
        TTS.wordToSound(text)
        return text
    except sr.UnknownValueError:
        print("抱歉，無法辨識你的語音")
        TTS.wordToSound("抱歉，無法辨識你的語音")
        return None

# 使用YouTube API進行搜尋
def search_on_youtube(query):
    api_key = 'AIzaSyCMxpyjGy1Q5nPspq9Vfga9JAvk0SSle20'  # 請填入你的YouTube API金鑰
    youtube = build('youtube', 'v3', developerKey=api_key)

    search_response = youtube.search().list(q=query, part='id', maxResults=1, type='video').execute()

    if 'items' in search_response and len(search_response['items']) > 0:
        video_id = search_response['items'][0]['id']['videoId']
        video_url = 'https://www.youtube.com/watch?v=' + video_id
        return video_url

    print("找不到相關視頻")
    return None

# 播放音樂
def play_music(query):
    video_url = search_on_youtube(query)
    if video_url:
        play_video(video_url)
    else:
        print("找不到相關音樂")

# 播放影片
def play_video(url):
    webbrowser.open(url)

# 表情偵測函數
def detect_emotion(model):
    webcam = cv2.VideoCapture(0)
    labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

    # 載入Haar級聯分類器，用於人臉檢測
    haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(haar_file)

    while True:
        ret, frame = webcam.read()
        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1)

        if key == ord('z'):
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
        
        if key == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()

# 定義函數，用於提取圖像特徵
def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0  # 正規化圖像特徵

def main():
    # 打開存有神經網絡模型結構的JSON文件
    json_file = open("facialemotionmodel.json", "r")
    model_json = json_file.read()
    json_file.close()

    # 從JSON文件中載入神經網絡模型
    model = model_from_json(model_json)

    # 載入神經網絡權重
    model.load_weights("facialemotionmodel.h5")

    while True:
        text = transcribe_speech()
        if text:
            if '音樂' in text:
                query = ask_for_song()
                if query:
                    play_music(query)
            elif '天氣' in text:
                city_name = ask_for_city()
                if city_name:
                    get_weather(city_name)
            elif '表情' in text:
                detect_emotion(model)  # 將模型傳遞給 detect_emotion 函數
            elif '停止' in text:
                print("程序已停止")
                TTS.wordToSound("程序已停止")
                break
    

# 使用語音辨識詢問使用者要查詢哪個歌曲
def ask_for_song():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("請告訴我要查詢哪首歌曲：")
        TTS.wordToSound("請告訴我要查詢哪首歌曲：")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        song_name = recognizer.recognize_google(audio, language='zh-TW')
        print(f"你想查詢的歌曲是：{song_name}")
        TTS.wordToSound("你想查詢的歌曲是：")
        TTS.wordToSound(song_name)
        return song_name
    except sr.UnknownValueError:
        print("抱歉，無法辨識你的語音")
        TTS.wordToSound("抱歉，無法辨識你的語音")
        return None

# 使用語音辨識詢問使用者要查詢哪個縣市的天氣
def ask_for_city():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("請告訴我要查詢哪個縣市的天氣：")
        TTS.wordToSound("請告訴我要查詢哪個縣市的天氣：")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        city_name = recognizer.recognize_google(audio, language='zh-TW')
        print(f"你想查詢的縣市是：{city_name}")
        TTS.wordToSound("你想查詢的縣市是：")
        TTS.wordToSound(city_name)
        return city_name
    except sr.UnknownValueError:
        print("抱歉，無法辨識你的語音")
        TTS.wordToSound("抱歉，無法辨識你的語音")
        return None

# 取得天氣資訊
def get_weather(city_name):
    # 將 "台" 轉換成 "臺"
    if city_name.startswith("台"):
        city_name = city_name.replace("台", "臺")

    url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-ECE35607-AEC5-4515-BAEB-BE5CAFCE5FF1&format=JSON&locationName={city_name}&elementName=Wx,PoP'
    data = requests.get(url)

    # 檢查 API 請求是否成功
    if data.status_code != 200:
        print(f"API 請求失敗，錯誤代碼：{data.status_code}")
        TTS.wordToSound("API 請求失敗，請稍後再試")
        return

    data_json = data.json()
    location = data_json['records']['location']

    # 檢查 location 是否為空
    if not location:
        print(f"找不到 {city_name} 的天氣資料")
        TTS.wordToSound(f"找不到 {city_name} 的天氣資料")
        return

    # 只顯示該城市的天氣預報結果
    for i in location:
        if i['locationName'] == city_name:
            city = i['locationName']
            wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']
            pop8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']
            print(f'{city}:\n未來8小時 {wx8}\n\t  降雨機率 {pop8} %\n')
            TTS.wordToSound(city_name + "未來8小時" + wx8 + "降雨機率" + pop8)
            return

if __name__ == '__main__':
    main()