#!/usr/bin/env python
#-*- coding: utf -*-
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
ret, hframe = cap.read()
print(cap.get(3), cap.get(4))

cv2.imshow('image', hqframe)
cap.set(3, 320)
cap.set(4, 240)

print(cap.get(3), cap.get(4))

while(True):
    ret, hframe = cap.read()
    cv2.imshow('half image', hframe)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()