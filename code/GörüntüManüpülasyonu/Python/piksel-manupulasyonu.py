import cv2
import numpy as np

 
frame = cv2.imread('turkey-logo.jpg')
#nump ile frame matrisi üzerinde kolayca karşılaştırma ve değer değiştirme yapabiliyoruz
frame[np.where((frame == [255,255,255]).all(axis = 2))] = [0,0,0]
#yeni görüntüyü kaydedelim ve görüntüleyelim
cv2.imwrite('turkey-logo-output.jpg', frame)
cv.imshow("Yeni Goruntu", frame)
cv.waitKey(0)