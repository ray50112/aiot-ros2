#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import matplotlib
matplotlib.use('TkAgg', warn = False, force = True)
from matplotlib import pyplot as plt

img = cv2.imread('123.jpg')
img = cv2.resize(img, (400, 400))
img1 = cv2.resize(img, (400, 400), interpolation.INTER_NEAREST)
img2 = cv2.resize(img, (400, 400), interpolation.INTER_LINEAR)
img3 = cv2.resize(img, (400, 400), interpolation.INTER_AREA)
img4 = cv2.resize(img, (400, 400), interpolation.INTER_CUBIC)
img5 = cv2.resize(img, (400, 400), interpolation.INTER_LANCZOS4)

img0_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
img3_rgb = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
img4_rgb = cv2.cvtColor(img4, cv2.COLOR_BGR2RGB)
img5_rgb = cv2.cvtColor(img5, cv2.COLOR_BGR2RGB)

titles = ['Original Image', 'INTER_NEAREST', 'INTER_LINEAR', 'INTER_AREA', 'INTER_CUBIC', 'INTER_LANCZOS4']
images = [img0_rgb, img1_rgb, img2_rgb, img3_rgb, img4_rgb, img5_rgb]
for i in range(6):
    plt.subplot(2, 3, i+1)
    plt.imshow(images[i])
    plt.title(tiltes[i])
    plt.xticks([]), plt.yticks([])
plt.show()