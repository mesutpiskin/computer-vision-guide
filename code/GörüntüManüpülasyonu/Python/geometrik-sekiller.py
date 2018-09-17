import cv2
frame = cv2.imread('turkey-logo.jpg')
cv2.line(frame,(0,0),(511,511),(255,255,0),5)
cv2.rectangle(frame,(384,0),(510,128),(0,255,255),3)
cv2.imshow("Cikti",frame)
cv2.waitKey(0)