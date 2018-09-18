# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 18:48:48 2018

@author: mesutpiskin
"""


import cv2
import numpy as np

# Santraç tahtasının satır ve sütün sayısı 
rows = 9
cols = 6

# Kendi içerisinde yinelemeli olarak çalışan algoritmalar için durdurma/karar verme ölçütü
criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)

# İhtiyaç duyacağımız değişkenler
objectPoints = np.zeros((rows * cols, 3), np.float32)
objectPoints[:, :2] = np.mgrid[0:rows, 0:cols].T.reshape(-1, 2)
objectPointsArray = []
imgPointsArray = []

capture = cv2.VideoCapture(0) # Varsayılan kameraya bağlanır
found = 0 
# 10 defa başarılı kalibrasyon yapılana kadar tekrarlansın
while(found < 10):
    # Kameradan bir frame alıp bunu gri renk uzayına çevirir
    retCam,img = capture.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Frame içerisindeki santraç tahtasının köşelerini bul 
    isSucces, corners = cv2.findChessboardCorners(gray, (rows, cols), None)

    # Köşeler bulunabildi mi?
    if isSucces:
        '''
        Eğer belirttiğimiz satır ve sütün sayısınca köşe doğru olarak tespit edilmişse 
        cornerSubPix() metodu ile köşelerin veya radyal sırt noktalarının alt pikselinin, 
        doğru konumunu bulmak için kendi içerisinde yineler.
        '''
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        # Elde ettiğimiz bu noktaları saklayalım
        objectPointsArray.append(objectPoints)
        imgPointsArray.append(corners)

        # Testip edilen köşeleri çizelim
        cv2.drawChessboardCorners(img, (rows, cols), corners, isSucces)
        found += 1
    
    
    cv2.imshow('Kalibrasyon', img)
    cv2.waitKey(500)
cv2.destroyAllWindows()
# Elde ettiğimiz K ve D değerlerini npz arşivi olarak kaydedelim (txt, xml, yaml da kullanabilirsiniz)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectPointsArray, imgPointsArray, gray.shape[::-1], None, None)
np.savez('calibrationdata.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)


# Kalibrasyon verilerini kullanarak görüntüyü düzeltelim
cap = cv2.VideoCapture(0)
while True:
    # Gri renk uzayında frame okuyalım
    ret3,img = cap.read()
    h, w = img.shape[:2]
	
    '''
    Kalibrasyon ile elde ettiğimiz K ve D verileri ve OpenCV undistort* metotlarını kullanarak 
    bozuk görüntüyü düzeltebiliriz. Bu metotlar parametre olarak K ve D verilerine ihtiyaç duyar, 
    sonuç olarak ise size düzeltilmiş görüntü dönecektir.
    '''
    newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    undistortedImg = cv2.undistort(img, mtx, dist, None, newCameraMtx)
	
    cv2.imshow('Duzeltilmis Goruntu', undistortedImg)
    cv2.waitKey(0)
    
cv2.destroyAllWindows()