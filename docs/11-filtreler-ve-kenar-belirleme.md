# Filtreler ve Kenar Belirleme

Kamera sensöründen gelen her görüntü bir miktar gürültü içerir — özellikle düşük ışıkta piksel değerleri gerçekten olması gerekenden sapabilir. Bu rastgele dalgalanmalar kenar tespiti gibi hassas algoritmalar için ciddi sorun çıkarır: gürültü piksel de "kenar" gibi görünür. Bu bölümde görüntüyü temizleyen filtreleri ve sonrasında kenarları temiz bir şekilde bulan algoritmaları ele alıyoruz.

## Konvolüsyon Sezgisi

Konvolüsyon, küçük bir pencere (çekirdek/kernel) görüntü üzerinde adım adım kaydığında gerçekleşir. Her konumda: penceredeki piksel değerleri ile çekirdek katsayıları çarpılır, toplamı yeni piksel değeri olur. Farklı çekirdekler farklı efektler üretir — ortalama alan çekirdek bulanıklaştırır, fark alan çekirdek kenarları vurgular.

Matematiksel olarak (2D ayrık konvolüsyon):

$$G[i, j] = \sum_{m} \sum_{n} I[i+m, j+n] \cdot K[m, n]$$

Burada $I$ kaynak görüntü, $K$ çekirdek, $G$ çıktı görüntüsüdür. Sınır piksellerinde özel davranış (padding) gerekir — OpenCV varsayılan olarak yansıtma kullanır.

## Bulanıklaştırma Filtreleri

### Ortalama Filtre

Kerne'deki tüm piksel değerlerini eşit ağırlıkla ortalar. Hızlı ama kenarları bozar.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

# (5, 5) çekirdek boyutu — tek sayı ve pozitif olmalı
ortalama = cv2.blur(img, (5, 5))

cv2.imshow("Orijinal | Ortalama 5x5", np.hstack([img, ortalama]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Gaussian Filtre

Merkezdeki piksellere daha yüksek, uzaktakilere daha düşük ağırlık verir. İnsan gözünün flu algısına daha yakın — görsel açıdan daha doğal.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

# sigmaX=0: çekirdek boyutundan otomatik hesapla
gaussian = cv2.GaussianBlur(img, (5, 5), sigmaX=0)

cv2.imshow("Orijinal | Gaussian 5x5", np.hstack([img, gaussian]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Gaussian sigma değeri bulanıklık miktarını kontrol eder. `sigmaX=0` verdiğinizde OpenCV çekirdek boyutundan formülle hesaplar: $\sigma = 0.3 \cdot ((k-1) \cdot 0.5 - 1) + 0.8$.

### Median Filtre

Komşuluktaki tüm piksel değerlerini sıralar ve medyanı alır. Salt-and-pepper (tuz-biber) gürültüsü için çok etkilidir çünkü aşırı değerleri (0 veya 255) komşuluğun medyanı hiçbir zaman olmaz.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

# Yapay salt-and-pepper gürültüsü ekle
gurultulu = img.copy()
gurultu_maskesi = np.random.random(img.shape[:2])
gurultulu[gurultu_maskesi < 0.02] = 0    # %2 siyah piksel
gurultulu[gurultu_maskesi > 0.98] = 255  # %2 beyaz piksel

# ksize tek sayı ve >= 3 olmalı
median = cv2.medianBlur(gurultulu, 5)

cv2.imshow("Gurultulu | Median", np.hstack([gurultulu, median]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Median filtre özellikle barkod okuyucu ve taranmış belge gibi salt-and-pepper gürültüsünün yaygın olduğu uygulamalar için tercih edilir.

### Bilateral Filtre

Kenarları koruyarak gürültüyü siler. Klasik Gaussian filtreye ek olarak piksel yoğunluk farkını da ağırlığa dahil eder: komşu piksel hem uzaktaysa hem de değerce farklıysa (yani kenar noktasıysa) düşük ağırlık alır.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

# d=9: komşuluk çapı, sigmaColor=75: renk farkı toleransı, sigmaSpace=75: uzaklık toleransı
bilateral = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

cv2.imshow("Orijinal | Bilateral", np.hstack([img, bilateral]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Bilateral filtrenin bedeli performanstır — diğer filtrelerden belirgin şekilde daha yavaştır. Gerçek zamanlı uygulamalarda dikkatli kullanın.

### Filtre Karşılaştırması

| Filtre | Gürültü Türü | Kenar Koruma | Hız | Kullanım |
|--------|-------------|--------------|-----|---------|
| Ortalama | Genel | Zayıf | Çok hızlı | Hızlı prototip |
| Gaussian | Gaussian gürültüsü | Orta | Hızlı | Genel amaç, Canny öncesi |
| Median | Salt-and-pepper | İyi | Orta | Barkod, taranmış belge |
| Bilateral | Genel | Çok iyi | Yavaş | Yüz işleme, sanatsal efekt |

### Dört Filtre Karşılaştırması

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

ortalama   = cv2.blur(img, (5, 5))
gaussian   = cv2.GaussianBlur(img, (5, 5), 0)
median     = cv2.medianBlur(img, 5)
bilateral  = cv2.bilateralFilter(img, 9, 75, 75)

def etiket(img, metin):
    k = img.copy()
    cv2.putText(k, metin, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return k

satir1 = np.hstack([etiket(img, "Orijinal"), etiket(ortalama, "Ortalama")])
satir2 = np.hstack([etiket(gaussian, "Gaussian"), etiket(median, "Median")])
satir3 = np.hstack([etiket(bilateral, "Bilateral"), np.zeros_like(img)])

sonuc = np.vstack([satir1, satir2])
cv2.imshow("Filtre Karsilastirma", sonuc)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Gaussian ve Median filtreleri aynı boyuttaki çekirdekle karşılaştırdığınızda kenar bölgelerindeki fark net görülür.

## Kenar Belirleme

Sezgi: Kenar, görüntüde komşu pikseller arasındaki yoğunluk farkının büyük olduğu yerdir. Bir nesnenin sınırı, farklı renkteki iki bölgenin buluştuğu çizgidir. Bu farkı ölçmek için görüntünün türevini hesaplıyoruz.

## Sobel Operatörü

Sobel, görüntünün yatay ve dikey gradyanlarını hesaplar. Yatay gradyan ($G_x$) dikey kenarlara, dikey gradyan ($G_y$) yatay kenarlara duyarlıdır.

Matematiksel olarak gradyan büyüklüğü:

$$|G| = \sqrt{G_x^2 + G_y^2}$$

Bu değer bir pikseldeki yoğunluk değişim hızını gösterir — büyükse o piksel kenar noktasıdır.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gri = cv2.GaussianBlur(gri, (3, 3), 0)  # önce gürültü azalt

# CV_64F: negatif gradyanları da yakalamak için 64-bit float
sobel_x = cv2.Sobel(gri, cv2.CV_64F, 1, 0, ksize=3)   # yatay gradyan
sobel_y = cv2.Sobel(gri, cv2.CV_64F, 0, 1, ksize=3)   # dikey gradyan

# Büyüklük hesapla, uint8'e dönüştür
magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
magnitude = np.uint8(np.clip(magnitude, 0, 255))

# Görüntüye sığdırmak için normalize et
sobel_x_goster = cv2.convertScaleAbs(sobel_x)
sobel_y_goster = cv2.convertScaleAbs(sobel_y)

cv2.imshow("Sobel X | Y | Büyüklük",
           np.hstack([sobel_x_goster, sobel_y_goster, magnitude]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`CV_64F` kullanmak önemli — `uint8` ile negatif gradyanlar sıfıra kırpılır ve bazı kenarlar kaybolur. İşlem bitince `convertScaleAbs` ile görselleştirmek için uint8'e döndürüyoruz.

## Canny Kenar Dedektörü

Canny, günümüzde hâlâ en yaygın kullanılan kenar dedektörüdür. Dört aşamalı pipeline ile temiz, ince ve bağlı kenarlar üretir:

1. **Gaussian gürültü azaltma:** küçük gürültüler kenar gibi görünmesin.
2. **Sobel gradyan hesaplama:** her pikselin kenar gücü ve yönü.
3. **Non-maximum suppression:** kenar yönünde yerel maksimum olmayan pikseller silinir — kenarlar incelir.
4. **Çift eşik (Hysteresis):** güçlü kenarlar ($> t_{high}$) kabul edilir; zayıf ama güçlüye bağlı olanlar ($t_{low} < x < t_{high}$) dahil edilir; geri kalanlar atılır.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gri = cv2.GaussianBlur(gri, (5, 5), 0)

# Manuel eşikler
canny_manuel = cv2.Canny(gri, threshold1=50, threshold2=150)

# Otomatik eşik: medyana göre
sigma = 0.33
medyan = float(np.median(gri))
low = int(max(0, (1.0 - sigma) * medyan))
high = int(min(255, (1.0 + sigma) * medyan))
canny_otomatik = cv2.Canny(gri, low, high)

print(f"Otomatik eşikler — low: {low}, high: {high}")

cv2.imshow("Canny Manuel | Otomatik",
           np.hstack([canny_manuel, canny_otomatik]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Otomatik eşik formülü: görüntünün medyan parlaklık değerine göre $t_{low} = (1-\sigma) \cdot \text{median}$ ve $t_{high} = (1+\sigma) \cdot \text{median}$. $\sigma = 0.33$ çoğu görüntü için iyi sonuç verir.

> **💡 İpucu:** Otomatik eşik formülü: `sigma=0.33`, `low=int((1.0-sigma)*median)`, `high=int((1.0+sigma)*median)`. Bu formül kez kez işe yarayan bir başlangıç noktası — görüntüye özel fine-tune yapabilirsiniz.

> **⚠️ Dikkat:** Canny'nin girdi parametresi çok önemli — Gaussian sigma değeri de ayrıca ayarlanabilir. Canny'yi çağırmadan önce manuel `GaussianBlur` uygularsanız daha iyi kontrol elde edersiniz.

### Canny vs Sobel Karşılaştırması

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gri_blur = cv2.GaussianBlur(gri, (5, 5), 0)

# Sobel
sobel_x = cv2.Sobel(gri_blur, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gri_blur, cv2.CV_64F, 0, 1, ksize=3)
sobel_mag = cv2.convertScaleAbs(np.sqrt(sobel_x**2 + sobel_y**2))

# Canny — otomatik eşik
medyan = float(np.median(gri_blur))
canny = cv2.Canny(gri_blur,
                  int(max(0, 0.67 * medyan)),
                  int(min(255, 1.33 * medyan)))

def etiket(goruntu, metin):
    k = cv2.cvtColor(goruntu, cv2.COLOR_GRAY2BGR)
    cv2.putText(k, metin, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return k

sonuc = np.hstack([etiket(sobel_mag, "Sobel"), etiket(canny, "Canny")])
cv2.imshow("Sobel vs Canny", sonuc)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Canny kenarları Sobel'den çok daha ince ve bağlıdır — non-maximum suppression sayesinde her kenar tek piksel kalınlığında. Sobel ise ham gradyanı verir, daha kalın ama daha hızlı.

## Laplacian Operatörü

Sobel birinci türevi (gradyan) hesaplarken Laplacian ikinci türevi hesaplar. İkinci türev sıfır geçişlerinde kenar bulur — tek seferde tüm yönlerde çalışır.

Matematiksel olarak: $\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}$

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gri = cv2.GaussianBlur(gri, (3, 3), 0)

laplacian = cv2.Laplacian(gri, cv2.CV_64F)
laplacian_abs = cv2.convertScaleAbs(laplacian)

cv2.imshow("Laplacian", laplacian_abs)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Laplacian gürültüye çok duyarlıdır — her zaman önce Gaussian bulanıklaştırma uygulanmalıdır. Pratikte Canny'nin yerini almaz ama görüntü odak analizi (hangi bölge daha keskin?) gibi uygulamalarda kullanılır.

## Özet & İleri Okuma

- Konvolüsyon: çekirdek görüntü üzerinde kaydırılarak her konumda nokta çarpım toplamı alınır — çekirdek şekli sonucu belirler.
- Gaussian filtre genel amaçlı gürültü azaltma için en iyi başlangıç noktasıdır; kenar tespiti öncesi standart ön işlemdir.
- Median filtre salt-and-pepper gürültüsü için idealdir — diğer filtreler bu tür gürültüyü sadece yayar.
- Bilateral filtre kenarları koruyarak gürültü siler ama yavaştır — gerçek zamanlı kullanımda dikkatli olun.
- Sobel yatay ve dikey gradyanları ayrı hesaplar; `CV_64F` ile negatif gradyanları kaybetmeyin.
- Canny dört aşamalı pipeline ile en temiz kenarları üretir; non-maximum suppression ile tek-piksel kalınlıkta kenar sağlar.
- Otomatik Canny eşiği: `sigma=0.33`, `low=(1-sigma)*median`, `high=(1+sigma)*median`.
- Laplacian ikinci türev — gürültüye çok duyarlı, her zaman önce bulanıklaştırın.

**Referanslar**

- Canny, J. (1986). "A Computational Approach to Edge Detection." *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 8(6), 679–698.
- Gonzalez, R. C. & Woods, R. E. (2017). *Digital Image Processing* (4th ed.). Pearson.
