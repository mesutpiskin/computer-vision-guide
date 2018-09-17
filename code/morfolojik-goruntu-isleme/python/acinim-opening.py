import cv2
import numpy as np

frame = cv2.imread('kus.png',0)
#Numpy ile kernel matris tanımı
kernel = np.ones((25,25),np.uint8)

#Açma
sonuc = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
cv2.imshow("Sonuc", sonuc)

cv2.waitKey(0)