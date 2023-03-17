#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np

img = cv2.imread('123.jpg')
print(img.shape)
rows, cols, channel = img.shape

dst = cv2.resize(img, (2*cols, rows), interpolation = cv2.INTER_CUBIC)
dst1 = cv2.resize(img, (cols, 2*rows), interpolation = cv2.INTER_LINEAR)
dst2 = cv2.resize(img, (int(cols/2), int(rows/2)), interpolation = cv2.INTER_AREA)

cv2.imshow('Original', img)
cv2.imshow('INTER_CUBIC', dst)
cv2.imshow('INTER_LINEAR', dst1)
cv2.imshow('INTER_AREA', dst2)
cv2.waitKey(0)
cv2.destroyAllWindows()