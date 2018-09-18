#Cascade modelleri https://github.com/opencv/opencv/tree/master/data/haarcascades
import cv2

capture = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:

    ret, frame = capture.read()   
    faces = cascade.detectMultiScale(frame, 1.5, 3)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)
       
        
    cv2.imshow('Kamera',frame)
    if cv2.waitKey(30) & 0xff ==27:
        break

capture.release()
cv2.destroyAllWindows()