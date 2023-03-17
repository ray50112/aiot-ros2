import cv2
import numpy as np
img = cv2.imread('output1.jpg')
cv2.imshow('output1',img)
cv2.waitKey(0)
cv2.destoryAllWindows()