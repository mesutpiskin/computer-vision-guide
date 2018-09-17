import cv2

# Video dosyasını aç
cap = cv2.VideoCapture("videodosyasi.avi")

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