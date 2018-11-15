**OCR (Optical Character Recognition - Optik Karakter Tanıma)** 
---------------------------------------------------------------

Optik karakter tanıma; taranmış, fotoğraflanmış veya dijital olarak üretilmiş herhangi bir görüntü üzerinde yer alan metinlerin görüntü üzerinde tespit edilerek değiştirilebilir metin haline dönüştürülebilmesidir. OCR dijital olarak oluşturulmuş veya el yazısı ile yazılmış karakterleri tanıma yeteneğine sahiptir.

![Optik Karakter Tanıma](static/ocr.png)

Algoritmaya göre bu aşamalar değişmekle birlikte OCR temel olarak üç aşamalı bir süreçtir;

1. Önişleme
2. Karakter Tespiti
3. Sınıflandırma

şimdi bu süreçlere bir göz atalım.

**1. Önişleme**

Görüntünün önişlenmesi; görüntü işlemenin ilgilendiği temelalanlardan bir tanesidir. Önişleme ile, görüntü üzerindeki gürültüler temizlenir, ışık dengesi yapılır, kırpma, boyutlandırma yapılır ve renk uzayı dönüşümleri gerçekleştirilebilir. Önişleme süreci kullanılan algoritmaya göre değiklik göstermekle birlikte bir çok algoritma için ise geliştirici tarafından önişlenmiş görüntünün girdi olarak verilmesi beklenir.

**2. Karakter Tespiti**

Bu bölümde görüntü üzerinde yer alan alfabatik karakterlerin tespit işlemi gerçekleştirilir. Görüntü üzerinde alfabatik karakterler dışında bir çok nesne yer alabilir, karakterler ile bu nesnelerin ayıklanması gerekmektedir bu işlemler karakter tespiti aşamasında gerçekleştirilir. Karakter tespiti aşamasında tespit edilen karakterlerin ne olduğu yani tanımlanması yapılmaz.

**3. Sınıflandırma**

Önişlenmiş ve karakter tespiti yapılmış görüntü üzerine karakterlerin ASCI karşılıklarının belirlenmesi sürecidir. Görüntü üzerinde yer alan metinler bir çok farklı fontla, farklı dille farklı şekilde yazılmış olabilir, bu da farklı veri setleri ile eğitilmiş bir sınıflandırıcı ihtiyacı doğurur. OCR algoritmasının başarı oranını etkileyen en önemli faktör buradaki sınıflandırıcının başarı oranıdır.


# Tesseract Kütüphanesi ile OCR

OCR için geliştirilmiş birçok kütüphane ve algoritma mevcuttur. Açık kaynak olarak geliştirilmiş ücretsiz en iyi kütüphanelerden birisi hiç şüphesiz ki **tesseract**'dır.

![Tesseract](static/tesseract.png)

Tesseract 1985-1994 yılları arasında HP tarafından C++ ile geliştirilmiş bir kütüphanedir. 2006 yılından beri ise Google desteği ile geliştirilmeye devam etmektedir. En kararlı sürümü şuan için 4.0'dır. Tesseract UTF-8 desteğine sahiptir ve 100 den fazla dili desteklemektedir. 4. sürümü ile bilikte RNN(Recurrent Neural Network) çeşidi olan LTSM desteğine kavuşmuştur, bu sayede derin öğrenmeden yararlanarak daha iyi sonuçlar elde etmenize yardımcı olmaktadır.

# Kurulum

Python örneği için **pytesseract** kullanacağız, bunun için öncelikle bu python paketini kuralım.

```Bash
pip install pytesseract
```
Tesseract farklı dillerdeki metinleri tanıyabilmek için eksra bir modele ihtiyaç duyar, bu modeli aşağıdaki bağlantıdan indirebilirsiniz. 

- https://github.com/tesseract-ocr/tessdata

İsterseniz binary dosyaları işletim sisteminize doğrudan kurabilirsiniz. Bunun için buradaki bağlantı üzerinden işletim sistemine ve istediğiniz OCR diline göre özelleştirilmiş kurulum adımlarını izleyebilirsiniz. https://github.com/tesseract-ocr/tesseract/wiki

Örneğin MacOS için;

```Bash
brew install tesseract
```


# Örnek Proje

OpenCV ile bir görüntü yükleyelim ve bu görüntüyü tesseract ile metne çevirelim. Benim sistemimde İngilizce **tessdata** paketi olduğu için İngilizce seçtim, Türkçe için **lang = 'tur'** kullanabilirsiniz. Dil paketleri için [buraya](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files) göz atabilirsiniz.

```Python
import cv2
import pytesseract


#OpenCV ile goruntuyu oku
frame = cv2.imread("metin.png");

#Matris goruntuyu tesseract ile metne çevir
print(pytesseract.image_to_string(frame, lang='eng'))
```

Yukarıdaki projeyi çalıştırdığınızda görüntü metne çevrilecektir. Daha detaylı kullanımlar için bu bölümün örnek projelerine göz atabilirsiniz.
