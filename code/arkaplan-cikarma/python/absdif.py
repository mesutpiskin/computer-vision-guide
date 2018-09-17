import numpy as np
import cv2
videoCapture = cv2.VideoCapture(0)
while(1):
    ret, cameraFrame = videoCapture.read()
    img2 = cv2.imread('resim.jpg')
    fark = cv2.absdiff(cameraFrame, img2)
    cv2.imshow('GORUNTU',fark)

videoCapture.release()
cv2.destroyAllWindows()