import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    ret, frame = cap.read()
    guasianBlur = cv2.GaussianBlur(frame,(5,5),1)
    
    cv2.imshow('Gaussian Blur', guasianBlur)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()