# Renk Uzayları ve Histogram

Kırmızı bir topu RGB renk değerine bakarak tespit etmeye çalıştığınızı düşünün. İç mekanda ölçüm: (220, 40, 30). Güneşli dışarıda: (255, 100, 80). Aynı top, ama farklı ışık koşulları tamamen farklı RGB değerleri veriyor. Bu problem renk uzaylarını neden öğrenmek gerektiğini özetler. Bu bölümde rengin farklı temsil biçimlerini, ışıktan bağımsız nesne tespitini ve görüntünün parlaklık dağılımını analiz etmeyi ele alıyoruz.

## Renk Uzayı Neden Gerekli?

RGB modelinde kırmızı, yeşil ve mavi bileşenler hem renk tonunu hem de parlaklığı birlikte kodlar. Işık değişince üç kanal da değişir — renk tonu sabit kalsa bile. Bu durum renk tabanlı segmentasyonu kararsız hale getirir.

HSV (Hue-Saturation-Value) modelinde ise renk tonu (H) parlaklıktan ayrı tutulur. Kırmızı top hangi ışıkta olursa olsun hue kanalında benzer bir değer verir; sadece value (parlaklık) değişir. Bu ayrım, nesne tespitini çok daha güvenilir kılar.

## RGB/BGR Kanalları

OpenCV görüntüsü BGR sırası kullanan NumPy dizisidir. `cv2.split` ile kanalları ayrı ayrı inceleyebiliriz.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

# Kanalları ayır
b, g, r = cv2.split(img)

# Her kanalı renkli göster — diğerlerini sıfırla
sifir = np.zeros_like(b)

mavi_gosterim = cv2.merge([b, sifir, sifir])
yesil_gosterim = cv2.merge([sifir, g, sifir])
kirmizi_gosterim = cv2.merge([sifir, sifir, r])

karsilastirma = np.hstack([img, mavi_gosterim, yesil_gosterim, kirmizi_gosterim])
cv2.imshow("Orijinal | B | G | R", karsilastirma)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Her kanalı tek başına gri olarak göstermek yerine renkli merge ile gösteriyoruz — böylece her kanalın görüntüye katkısını daha net anlayabilirsiniz.

> **💡 İpucu:** `cv2.split` her kanalı ayrı kopya olarak döndürür — bellek kullanır. Sadece bir kanalı istiyorsanız `b = img[:, :, 0]` daha verimlidir.

## Gri Tonlama

Renk bilgisi gereksizse görüntüyü griye dönüştürmek hem işlem yükünü üçte bire indirir hem de birçok algoritmanın çalışma koşulunu sağlar.

```python
import cv2

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(f"Renkli: {img.shape}, Gri: {gri.shape}")

cv2.imshow("Gri", gri)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

OpenCV'nin gri dönüşüm formülü $G = 0.114B + 0.587G + 0.299R$ — insan gözünün yeşile daha duyarlı olmasını hesaba katar. Basit bir ortalama değil, ağırlıklı bir birleştirme.

Ne zaman gri kullanın: kenar tespiti, eşikleme, şablon eşleştirme, optik akış gibi algoritmaların büyük çoğunluğu tek kanallı girdi bekler.

## HSV Renk Uzayı

HSV renk silindiril bir koordinat sistemi kullanır:
- **H (Hue — Ton):** 0–179° — rengin kendisi. Kırmızı 0° civarında, yeşil 60°, mavi 120°.
- **S (Saturation — Doyum):** 0–255 — rengin canlılığı. 0 = gri, 255 = tam doygun.
- **V (Value — Değer):** 0–255 — parlaklık. 0 = siyah, 255 = tam parlak.

OpenCV'de hue değeri 0–360 yerine 0–179 aralığındadır (8-bit'e sığdırmak için ikiye bölünmüştür).

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Sarı renk maskesi (HSV: H≈25-35, S>100, V>100)
alt_sinir = np.array([20, 100, 100])
ust_sinir = np.array([40, 255, 255])

maske = cv2.inRange(hsv, alt_sinir, ust_sinir)

# Maskeyi orijinal görüntüye uygula
sonuc = cv2.bitwise_and(img, img, mask=maske)

cv2.imshow("Orijinal", img)
cv2.imshow("Maske", maske)
cv2.imshow("Sarı Bölgeler", sonuc)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`cv2.inRange` belirtilen alt ve üst sınırlar arasındaki pikselleri 255, dışındakileri 0 yapan ikili maske üretir. `cv2.bitwise_and` ile bu maske orijinal görüntüye uygulanır.

### Yaygın Renk HSV Aralıkları

| Renk | H Alt | H Üst | S Alt | S Üst | V Alt | V Üst |
|------|-------|-------|-------|-------|-------|-------|
| Kırmızı (1) | 0 | 10 | 100 | 255 | 100 | 255 |
| Kırmızı (2) | 160 | 179 | 100 | 255 | 100 | 255 |
| Turuncu | 10 | 25 | 100 | 255 | 100 | 255 |
| Sarı | 20 | 40 | 100 | 255 | 100 | 255 |
| Yeşil | 40 | 80 | 50 | 255 | 50 | 255 |
| Mavi | 100 | 130 | 50 | 255 | 50 | 255 |
| Mor | 130 | 160 | 50 | 255 | 50 | 255 |

> **💡 İpucu:** Kırmızı 0° civarında (0–10) ve 170° civarında (160–179) iki ayrı aralıkta bulunur çünkü renk dairesi 0°/360° noktasında birleşir. Her iki maskeyi `cv2.bitwise_or(maske1, maske2)` ile birleştirmeniz gerekir.

### Gerçek Zamanlı Renk Tespiti

Kameradan canlı akışta sarı nesneyi tespit eden tam örnek:

```python
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Kamera açılamadı")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Sarı renk aralığı
    alt = np.array([20, 100, 100])
    ust = np.array([40, 255, 255])
    maske = cv2.inRange(hsv, alt, ust)

    # Gürültüyü temizle
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    maske = cv2.morphologyEx(maske, cv2.MORPH_OPEN, kernel)

    sonuc = cv2.bitwise_and(frame, frame, mask=maske)

    # İkisini yan yana göster
    gosterim = np.hstack([frame, sonuc])
    cv2.imshow("Kamera | Sarı Tespit", gosterim)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

Maskeye morphological opening uyguladık — bu küçük gürültü piksellerini temizler. Sonraki bölümde morfoloji detaylı ele alınacak.

## Lab Renk Uzayı

CIE L*a*b* (kısaca Lab) insan gözünün renk algısını modelleyen bir uzaydır:
- **L:** Parlaklık (0–100)
- **a:** Kırmızı-Yeşil ekseni (negatif = yeşil, pozitif = kırmızı)
- **b:** Mavi-Sarı ekseni (negatif = mavi, pozitif = sarı)

```python
import cv2

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
l, a, b = cv2.split(lab)

print(f"L kanalı ort: {l.mean():.1f}, a ort: {a.mean():.1f}, b ort: {b.mean():.1f}")
```

Lab'ın temel avantajı renk mesafeleri — iki renk arasındaki öklidyen mesafe, insan gözünün algıladığı farka daha yakındır. Deri tonu tespiti, görüntü bölütleme ve renk karşılaştırma uygulamalarında tercih edilir.

## Histogram

Histogram, görüntüdeki her parlaklık değerinin kaç piksel tarafından taşındığını gösterir. Karanlık bir fotoğrafın histogramı sola (düşük değerlere) yığılmış, aşırı parlak görüntünün histogramı sağa (yüksek değerlere) yığılmış olur. Bu bilgi görüntünün "kişiliğini" bir bakışta ortaya koyar.

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Gri histogram: [kanal listesi], [maske], [kutu sayısı], [değer aralığı]
hist_gri = cv2.calcHist([gri], [0], None, [256], [0, 256])

# Renkli histogram: her kanal ayrı ayrı
renkler = ('b', 'g', 'r')
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
axes[0].set_title("Görüntü")
axes[0].axis('off')

axes[1].plot(hist_gri, color='gray', label='Gri')
for kanal_idx, renk in enumerate(renkler):
    hist = cv2.calcHist([img], [kanal_idx], None, [256], [0, 256])
    axes[1].plot(hist, color=renk, alpha=0.7)

axes[1].set_xlim([0, 256])
axes[1].set_title("Histogram")
axes[1].set_xlabel("Piksel Değeri")
axes[1].set_ylabel("Piksel Sayısı")
plt.tight_layout()
plt.savefig("histogram.png", dpi=150)
plt.show()
```

Histogram çubuk grafiği değil çizgi grafiği olarak çizmek tercih edilir — 256 nokta olduğunda çizgi daha temiz görünür.

## Histogram Eşitleme

Düşük kontrastlı bir görüntüde piksellerin çoğu dar bir değer aralığına sıkışmıştır — histogram dar ve yüksektir. Eşitleme bu dağılımı 0–255 aralığına yayar, kontrast artar.

Sezgi: Frekansları eşit dağılmış bir histogram hedefliyoruz. Cumulative Distribution Function (CDF) kullanılarak piksel değerleri yeniden haritalanır.

```python
import cv2
import numpy as np

path = "karanlik_goruntu.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Global histogram eşitleme
esitlenmis = cv2.equalizeHist(gri)

# CLAHE: Contrast Limited Adaptive Histogram Equalization
# clipLimit: yerel zirveyi kırpar (aşırı parlaklaşmayı önler)
# tileGridSize: görüntüyü kaç parçaya böleceği
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe_sonuc = clahe.apply(gri)

# Üçlü karşılaştırma
karsilastirma = np.hstack([gri, esitlenmis, clahe_sonuc])
cv2.imshow("Orijinal | equalizeHist | CLAHE", karsilastirma)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Global eşitleme tüm görüntüyü tek bir histograma göre ayarlar — bazı bölgeler aşırı parlaklaşabilir. CLAHE görüntüyü küçük bloklara böler ve her blok için ayrı eşitleme yapar; `clipLimit` ile de lokal zirveyi kırpar. Sonuç çok daha dengeli ve doğal görünür.

> **💡 İpucu:** Tıbbi görüntüleme (X-ray, MR), uydu fotoğrafları ve düşük ışık koşullarında CLAHE globalden belirgin şekilde üstündür. Renkli görüntülerde sadece parlaklık kanalına (Lab'daki L veya HSV'deki V) uygulayın — renk bozulmasını önler.

### Histogram Eşitleme Yöntemleri Karşılaştırması

| Yöntem | Avantaj | Dezavantaj | Ne Zaman |
|--------|---------|------------|----------|
| `equalizeHist` | Hızlı, basit | Aşırı kontrast, gürültü artışı | Homojen aydınlatma |
| CLAHE | Dengeli, doğal | Daha yavaş, parametre gerektirir | Tıbbi görüntü, uydu |

## Özet & İleri Okuma

- RGB'de renk tonu ve parlaklık ayrılmaz; ışık değişince tüm kanallar değişir. HSV bu sorunu çözer.
- HSV'de Hue renk tonunu, Saturation doyumu, Value parlaklığı kodlar. OpenCV'de H aralığı 0–179.
- Kırmızı iki ayrı hue aralığında bulunur (0–10 ve 160–179); `cv2.bitwise_or` ile birleştirin.
- `cv2.inRange` ile renk maskesi + `cv2.bitwise_and` ile uygulama: renge dayalı segmentasyonun temel akışı.
- Lab renk uzayı insan algısına yakın mesafe ölçümü için uygundur.
- Histogram görüntünün parlaklık dağılımını özetler; `cv2.calcHist` ile hesaplanır.
- `equalizeHist` global, CLAHE yerel kontrast iyileştirme sağlar. Renkli görüntülerde sadece parlaklık kanalına uygulayın.

**Referanslar**

- OpenCV Color Conversions: [docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html](https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html)
- Zuiderveld, K. (1994). "Contrast Limited Adaptive Histogram Equalization." Graphics Gems IV, Academic Press.
