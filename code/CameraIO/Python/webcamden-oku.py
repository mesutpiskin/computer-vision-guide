import cv2

#Varsayılan kamera aygıtına bağlan
cap = cv2.VideoCapture(0)

while(True):
    # görüntü oku
    ret, frame = cap.read()

    # alınan görüntüyü göster
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# kamerayı kapat
cap.release()
cv2.destroyAllWindows()