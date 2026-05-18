# Morfolojik Görüntü İşleme

Eşikleme yaptınız, ikili görüntü elde ettiniz — ama görüntüde ufak gürültü lekeleri var ve tespit ettiğiniz nesnelerin içinde delikler bulunuyor. Bu iki sorun morfolojik işlemlerin tam çözüm alanıdır. Morfoloji, ikili görüntülerdeki şekilleri küçülterek, büyüterek, birleştirerek ve ayırarak temizler. Bu bölümde eşikleme yöntemleri ve temel morfolojik operatörler ele alınacak.

## Neden Morfoloji?

Gerçek bir senaryo: Fabrika konveyör bandında geçen parçaları saymak için kamera kullanıyorsunuz. Eşikleme ile nesneleri arkaplan'dan ayırdınız. Ama sonuçta şu sorunlar var:

1. Nesnenin etrafında küçük gürültü pikselleri var — her biri sahte nesne sayılıyor.
2. Nesnenin ortasında delik var — nesne iki parça gibi görünüyor.

Erosion (aşındırma) birinci problemi çözer, Dilation (genişletme) ikincisini. Bunların kombinasyonları olan Opening ve Closing her iki durumu birlikte yönetir.

## Eşikleme — İkili Görüntüye Geçiş

Morfoloji ikili (binary) görüntü üzerinde çalışır. Gri görüntüyü ikili hale getirmenin üç temel yolu:

**Basit eşikleme:** Belirlediğiniz bir eşik değeri altındaki pikseller 0, üstündekiler 255 olur.

```python
import cv2
import numpy as np

path = "nesne.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Sabit eşik
_, basit = cv2.threshold(gri, 127, 255, cv2.THRESH_BINARY)

# Otsu: eşiği otomatik hesapla (bimodal histogram için ideal)
_, otsu = cv2.threshold(gri, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Adaptif: her bölge için kendi eşiği (değişen aydınlatma için)
adaptif = cv2.adaptiveThreshold(
    gri, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    blockSize=11,    # komşuluk boyutu (tek sayı, >1)
    C=2              # ortalamadan çıkarılan sabit
)

karsilastirma = np.hstack([basit, otsu, adaptif])
cv2.imshow("Sabit | Otsu | Adaptif", karsilastirma)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Otsu algoritması görüntünün histogramını analiz ederek iki sınıf arasındaki varyansı maksimize eden eşiği bulur — elle eşik belirlemek yerine `THRESH_OTSU` bayrağı eklemek yeterli. Adaptif eşikleme ise gölgeli veya eşit aydınlatılmamış görüntülerde (el yazısı, kitap sayfası) çok daha iyi sonuç verir.

| Yöntem | Ne Zaman Kullan |
|--------|-----------------|
| Sabit eşik | Kontrollü stüdyo aydınlatması, basit test |
| Otsu | Homojen arka plan, bimodal histogram |
| Adaptif | Değişen aydınlatma, gölge, doğal ortam |

## Yapısal Eleman (Structuring Element)

Morfoloji operasyonlarının "fırçası" yapısal elemandır. Boyutu ve şekli operasyonun nasıl davranacağını belirler.

Sezgi: Büyük bir fırça küçük detayları ezer, ince bir fırça hassas iş yapar. Yuvarlak şekli yuvarlak nesneleri işlerken, dikdörtgen şekli keskin köşeli nesneleri işlerken kullanırsınız.

```python
import cv2

# Dikdörtgen çekirdek 5×5
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Elips çekirdek 5×5 — yuvarlak nesneler için
ellipse_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Artı/çapraz çekirdek
cross_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))

print("Dikdörtgen çekirdek:\n", rect_kernel)
print("Elips çekirdek:\n", ellipse_kernel)
```

Elips çekirdeği dikdörtgenin köşelerini kırpar — yuvarlak nesnelerde daha doğal sonuç üretir.

## Erosion (Aşındırma)

Nesneyi küçültür: çekirdeğin tamamen nesne üzerinde olduğu konumlar beyaz kalır, diğerleri siyaha döner. Sonuç olarak nesne içten dışa eriyip küçülür.

Sezgi: Bir nesnenin etrafına sert bir fırça bastırıyorsunuz ve fırça tamamen nesne içinde kalmadığı her yerde siyah boya sürüyorsunuz. Nesne küçülüyor, ince bağlantılar kopuyor, küçük gürültüler tamamen siliniyor.

```python
import cv2
import numpy as np

path = "ikili_goruntu.jpg"
binary = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if binary is None:
    raise FileNotFoundError(f"{path} bulunamadı")

_, binary = cv2.threshold(binary, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

eroded = cv2.erode(binary, kernel, iterations=1)

cv2.imshow("Orijinal | Eroded", np.hstack([binary, eroded]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`iterations` parametresi işlemi kaç kez tekrarlayacağını belirtir. 2 iterasyon, 2 kez ardışık erosion uygulamakla eşdeğerdir.

## Dilation (Genişletme)

Erosion'un tersi: çekirdeğin herhangi bir noktasının nesne üzerine denk geldiği konum beyaz kalır. Nesne dışa doğru büyür.

Sezgi: Nesnenin her noktasından aynı fırçayı bastırıyorsunuz. Nesne şişiyor, delikler kapanıyor, yakın nesneler birleşiyor.

```python
import cv2
import numpy as np

path = "ikili_goruntu.jpg"
binary = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if binary is None:
    raise FileNotFoundError(f"{path} bulunamadı")

_, binary = cv2.threshold(binary, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

dilated = cv2.dilate(binary, kernel, iterations=1)

cv2.imshow("Orijinal | Dilated", np.hstack([binary, dilated]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Opening = Erosion → Dilation

Önce aşındırma, sonra genişletme. İki adım birlikte küçük gürültüleri siler ama büyük nesneleri korur. Erosion gürültüleri yok eder, ardından Dilation büyük nesneyi yaklaşık orijinal boyutuna geri getirir.

Sezgi: Küçük bir taşı ve büyük bir bloğu düşünün. Erosion ikisini de küçültür — ama küçük taş tamamen yok olur, büyük blok sadece hafif küçülür. Sonraki Dilation büyük bloğu restore eder, küçük taş artık yok.

```python
import cv2
import numpy as np

path = "ikili_goruntu.jpg"
binary = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if binary is None:
    raise FileNotFoundError(f"{path} bulunamadı")

_, binary = cv2.threshold(binary, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

cv2.imshow("Orijinal | Opening", np.hstack([binary, opened]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Closing = Dilation → Erosion

Önce genişletme, sonra aşındırma. Nesne içindeki delikleri kapatır, ama nesne boyutunu korur. Dilation delikleri doldurur, ardından Erosion nesneyi orijinal sınırlarına döndürür.

Sezgi: Önce nesneyi şişiriyorsunuz — delikler kapanıyor. Sonra küçültüyorsunuz — nesne eski boyutuna dönüyor ama artık deliksiz.

```python
import cv2
import numpy as np

path = "ikili_goruntu.jpg"
binary = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if binary is None:
    raise FileNotFoundError(f"{path} bulunamadı")

_, binary = cv2.threshold(binary, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

cv2.imshow("Orijinal | Closing", np.hstack([binary, closed]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Morphological Gradient

Dilation ile Erosion arasındaki fark alınır: nesnenin sınırı — yani kenarı — elde edilir.

Matematiksel olarak: $\text{Gradient} = \text{Dilation}(A) - \text{Erosion}(A)$

Sonuç, nesnenin dış sınırını gösterir. Canny gibi gradyan tabanlı kenar dedektörlerinden farkı: morfoloji ikili görüntü üzerinde çalışır, genellikle daha kalın ama daha gürültüsüz kenarlar üretir.

```python
import cv2
import numpy as np

path = "ikili_goruntu.jpg"
binary = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if binary is None:
    raise FileNotFoundError(f"{path} bulunamadı")

_, binary = cv2.threshold(binary, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

cv2.imshow("Binary | Gradient", np.hstack([binary, gradient]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Karşılaştırma Tablosu

| Operasyon | Formül | Amaç | Ne Zaman Kullan |
|-----------|--------|-------|-----------------|
| Erosion | $E = A \ominus B$ | Nesneyi küçültür, gürültüyü siler | Küçük gürültü pikselleri |
| Dilation | $D = A \oplus B$ | Nesneyi büyütür, delikleri kapatır | Parçalanmış nesneler |
| Opening | Erosion → Dilation | Gürültü sil, nesne koru | Nesne çevresinde gürültü |
| Closing | Dilation → Erosion | Delikleri kapat, nesne koru | Nesne içinde delik |
| Gradient | Dilation - Erosion | Nesne sınırını çıkar | Kenar/kontur tespiti |

## Tüm Operasyonlar: Tek Örnekte

Aşağıdaki kod tek bir görüntü üzerinde tüm 6 operasyonu uygular ve yan yana gösterir:

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

eroded   = cv2.erode(binary, kernel, iterations=1)
dilated  = cv2.dilate(binary, kernel, iterations=1)
opened   = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
closed   = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

# Etiket ekle
def etiket_ekle(goruntu, metin):
    kopyasi = cv2.cvtColor(goruntu, cv2.COLOR_GRAY2BGR)
    cv2.putText(kopyasi, metin, (5, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return kopyasi

satir1 = np.hstack([
    etiket_ekle(binary, "Binary"),
    etiket_ekle(eroded, "Erosion"),
    etiket_ekle(dilated, "Dilation"),
])
satir2 = np.hstack([
    etiket_ekle(opened, "Opening"),
    etiket_ekle(closed, "Closing"),
    etiket_ekle(gradient, "Gradient"),
])

sonuc = np.vstack([satir1, satir2])
cv2.imshow("Morfolojik Operasyonlar", sonuc)
cv2.imwrite("morfoloji_karsilastirma.jpg", sonuc)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Altı kare tek bir pencerede görünür. İlk satır: Binary, Erosion, Dilation. İkinci satır: Opening, Closing, Gradient. Her operasyonun görüntüyü nasıl değiştirdiğini yan yana görmek kavramları pekiştirmenin en hızlı yoludur.

> **⚠️ Dikkat:** Morfolojik operasyonlar için görüntünün ikili (0 veya 255) olması zorunludur. Gri görüntü üzerinde de çalışır ama sonuçlar farklı yorumlanır — gri morfoloji ayrı bir konudur.

## Özet & İleri Okuma

- Eşikleme gri görüntüyü ikili hale getirir. Otsu otomatik eşik, Adaptif değişen aydınlatma için kullanılır.
- Yapısal eleman (kernel) morfoloji operasyonunun fırçasıdır — boyut ve şekil sonucu etkiler.
- Erosion nesneyi küçültür ve küçük gürültüleri siler; Dilation nesneyi büyütür ve delikleri kapatır.
- Opening = Erosion + Dilation: nesne çevresindeki gürültüyü temizler.
- Closing = Dilation + Erosion: nesne içindeki delikleri kapatır.
- Gradient = Dilation - Erosion: nesne sınırını (kenarını) çıkarır.
- `cv2.morphologyEx` Opening, Closing ve Gradient için tek fonksiyon sunar.

**Referanslar**

- Serra, J. (1982). *Image Analysis and Mathematical Morphology*. Academic Press.
- OpenCV Morphological Transformations: [docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
