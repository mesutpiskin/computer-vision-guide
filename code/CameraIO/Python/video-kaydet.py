import cv2

cap = cv2.VideoCapture(0)

# VideoWriter nesnesini oluştur
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('kayit.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        # geçerli frame'i yaz
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()