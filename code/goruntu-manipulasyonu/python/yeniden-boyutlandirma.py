import numpy as np
import cv2 as cv
img = cv.imread('turkey-logo.jpg')
height, width = img.shape[:2]
#Orijinal boyutunu 2 kat büyütelim (2*width, 2*height)
sonuc = cv.resize(img,(2*width, 2*height), interpolation = cv.INTER_CUBIC)
cv.imshow("Boyutlandirilmis Goruntu", sonuc)
cv.waitKey(0)