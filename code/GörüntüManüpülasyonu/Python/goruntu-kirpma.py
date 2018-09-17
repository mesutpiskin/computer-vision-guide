import cv2
frame = cv2.imread("turkey-logo.jpg")
#Alınan görüntüyü 10,100 - 100,200 şeklinde kırp
kesilmis_frame = frame[10:100, 100:200]
cv2.imshow("Kırpilmis Goruntu", kesilmis_frame)
cv2.waitKey(0)