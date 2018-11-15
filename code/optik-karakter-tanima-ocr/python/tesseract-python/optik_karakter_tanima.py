import cv2
import pytesseract


#OpenCV ile goruntuyu oku
frame = cv2.imread("metin.png");

#Matris goruntuyu tesseract ile metne çevir
print(pytesseract.image_to_string(frame, lang='eng'))