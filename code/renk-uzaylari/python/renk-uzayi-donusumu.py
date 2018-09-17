import cv2
frame = cv2.imread("people.jpg")
#RGB Renk uzayından gri renk uzayına dönüşüm
sonuc = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
cv2.imshow("Sonuc", sonuc)
cv2.waitKey(0)