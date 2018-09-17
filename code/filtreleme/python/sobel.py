import cv2

img = cv2.imread('image.jpg')
output = cv2.Sobel(img,cv2.CV_8U,1,0,ksize=5)

cv2.imshow("Sonuc", output)
cv2.waitKey(0)