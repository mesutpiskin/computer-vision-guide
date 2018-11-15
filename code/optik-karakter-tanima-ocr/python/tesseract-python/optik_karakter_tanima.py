import cv2
import pytesseract


# OpenCV ile goruntuyu oku
frame = cv2.imread("metin.png")

# tessdata dizinini göster, data dizini içerisinde Türkçe ve İngilizce yer almaktadır. 
# Diğer diller için https://github.com/tesseract-ocr/tesseract/wiki/Data-Files
config = r'--tessdata-dir "data"'

# Matris goruntuyu tesseract ile metne çevir
print(pytesseract.image_to_string(frame, lang='tur', config=config))


# PDF olarak çıktı al
# pdf = pytesseract.image_to_pdf_or_hocr('metin.png', extension='pdf')
