import cv2
import RPi.GPIO as GPIO
import time 
import numpy as np

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
cap = cv2.VideoCapture(0)

while(True):
    ret, hframe = cap.read()
    cv2.imshow('images', hframe)
    btn_state = GPIO.input(17)
    if (not btn_state):
        time.sleep(0.3)
        cv2.imwrite('output.jpg', hframe)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
