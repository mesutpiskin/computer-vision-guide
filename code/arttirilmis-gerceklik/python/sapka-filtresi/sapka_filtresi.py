# Python v3, OpenCV v3.4
# -*- coding: utf-8 -*-
#######################################
__file__ = "sapka_filtresi.py"
__author__ = "Mesut Pişkin"
__version__ = "1.0"
__email__ = "mesutpiskin@outlook.com"
#######################################
import cv2
import numpy as np


#Aşağıdaki değerler yüzün tespitinde her zaman aynı en boy değerleri yakalanamayabileceği için bunu elimine etmeye yönelik
#kaydırma değerleridir W ve H ile şapka genişlik yükseklik, X,Y ile de 2 boyutlu düzlemde şapka koordinatlarına müdehale edebilirsiniz

shiftValueW =25
shiftValueH = 35
shiftValueX = 0
shiftValueY = -10

'''Arka plan renklerini elimine etmek için piksel renk değeri bu değerden büyükse o piksel görüntü üzerine eklenmeyecek
Beyaz arka plana sahip görüntüler için işe yara bir yöntemdir, disable etmek isterseniz 255 den büyük bir değere çekebilirsiniz '''
bgColorThresholdValue = 230 

# Yüz tespiti için haarcascade modeli
haarCascadeForFace = "data/haarcascade_frontalface_default.xml"  # for face detection
faceCascade = cv2.CascadeClassifier(haarCascadeForFace)

#Görüntü modeli yani şapkamız
image_model = cv2.imread('img/fes.png')

#Varsayılan video kamerayı başlat
capture = cv2.VideoCapture(0) 
while True:

    # Kameradan bir görüntü al
    ret, frame = capture.read()
    '''Görüntüyü boyutlandır, isterseniz boyutlandırmayı kaldırabilirsiniz, kameranız 600x300 den küçükse buranın
       zaten bir anlamı olamyacaktır.'''
    frame = cv2.resize(frame, (600, 300)) 
    # Renk uzayını BGR dan GRAY e dönüştür
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Görüntüdeki yüzleri tespit et
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40,40)
    )

    # Tespit edilen yüzlerin koordinatlarını dön
    for (x, y, w, h) in faces:
        # Yüz koordinatlarına kaydırma değerlerini ekle yüzün genişlik ve yüksekliğini al modeli boyutlandır
        x = x + shiftValueX
        y = y + shiftValueY
        model_width = w + shiftValueW
        model_height = int(0.35 * h) + shiftValueH

        # Modeli yüze göre boyutlandır
        image_model = cv2.resize(image_model,(model_width, model_height))

        # Modelin tüm pikselleri içerisinde dön renk değeri eşik değerinden küçük olamları kamera görüntüsü üzerine ekle
        for i in range(model_height):
            for j in range(model_width):
                for k in range(3):
                    if image_model[i][j][k] < bgColorThresholdValue:
                        frame[y+i-int(0.25*h)][x+j][k] = image_model[i][j][k]
            
    # Sonucu görüntüle       
    cv2.imshow('Sonuc', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
