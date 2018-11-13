# Python v3, OpenCV v3.4
# -*- coding: utf-8 -*-
#######################################
__file__ = "yuz_tespiti.py"
__author__ = "Mesut Pişkin"
__version__ = "1.0"
__email__ = "mesutpiskin@outlook.com"
#######################################

import numpy as np
import cv2

# Tespit edilen yuz karesinin ne kadar genisletilecegini ifade eder.
shiftValue = 20 

# Kamera goruntusunu boyutlandırmak ıcın bu degerler kullanılacak.
resizeX = 460
resizeY = 300

# Basari oranı bu esik degerine gore kıyaslanacak, esikden kucukse o tahmin elenir.
thresholdValue = 0.3

# Model dosyalarini oku ve dnn agini olustur.
dnnNetwork = cv2.dnn.readNetFromCaffe("data/deploy.prototxt.txt", "data/res10SSD.caffemodel")

# Kamerayi baslat.
videoCapture = cv2.VideoCapture(0)

while True:
    	
	# Kamera goruntusunu oku.
	ret, frame = videoCapture.read()

	# Kamera goruntusunu boyutlandir. Daha dusuk cozunurluk daha hızlı sonuclar almanızı saglar (DNN icin gecerli degil).
	frame = cv2.resize(frame, (resizeX, resizeY)) 

	# Satir sutun sayısını al (genislik yukseklik).
	(h, w) = frame.shape[:2]

	# Sinir agi 300x300 seklinde bir input beklemektedir.
	# Sinir ağı için görüntüyü 300x300 haline getir ve giriş için hazırla.
	dnnBlobObject = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
		(300, 300), (104.0, 177.0, 123.0))
 
	# Goruntuyu sinir agina input olarak olarak ver.
	dnnNetwork.setInput(dnnBlobObject)
	resultDetections = dnnNetwork.forward()

	# Tum sinir agi ciktilari
	for i in range(0, resultDetections.shape[2]):
    		
		# Sinir agi buldugu nesne icin ne kadarlık bir basari oranı belirlemis
		confidence = resultDetections[0, 0, i, 2]

		# Basari oranı thresholdValue den kucukse o tahmini kabul etme.
		if confidence < thresholdValue:
			continue

		# Tespit edilen nesnenin, int tipinde (x1, y1) (genislik, yukseklik) koordinatları .
		resultArea = resultDetections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = resultArea.astype("int")
 
		# DNN sonucu dogruluk oranı yuzdelik formata cevrilir.
		percent = "{:.2f}%".format(confidence * 100)

		# Koordinatlara ve genislik yukseklik verisine gore nesne dortgen icerisinde isaretlenecek.
		y = startY - 10 if startY - 10 > 10 else startY + 10
		cv2.rectangle(frame, (startX - shiftValue, startY - shiftValue), (endX + shiftValue, endY + shiftValue),(0, 255, 255), 1)		
		cv2.putText(frame, percent, (startX - shiftValue , y - shiftValue),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
			

	# Sonucu frame icerisinde goruntule.
	cv2.imshow("DNN ILE YUZ TESPITI", frame)

	# ESC ile uygulamayi kapat.
	key = cv2.waitKey(1) & 0xFF
	if key == 27:
    		break

# Pencereleri ve kamera nesnesini sonlandir.
cv2.destroyAllWindows()
videoCapture.stop()