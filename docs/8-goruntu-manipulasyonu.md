# Görüntü Manipülasyonu ve Geometrik Dönüşümler

Tarayıcı uygulamanız bir belge fotoğrafı çekti ama belge eğik durmuş. Ya da nesne tanıma modelinizi her açıdan tutarlı çalıştırmanız gerekiyor ama kamera sabit değil. Geometrik dönüşümler bu sorunların çözümüdür: bir görüntüdeki pikselleri sistematik kurallara göre yeni konumlara taşır. Bu bölümde yeniden boyutlandırmadan perspektif düzeltmeye kadar temel dönüşümleri ve görüntü üzerine çizim işlemlerini ele alıyoruz.

## Neden Geometrik Dönüşüm?

İki pratik senaryo düşünün: Birincisi, taranmış bir belge fotoğrafı — kamera tam yukarıdan bakmadığı için belge yamuk görünür, OCR kalitesi düşer. İkincisi, konveyör bandındaki ürünlerin kalite kontrolü — kamera farklı açılardan görüntü alıyor ama modelinizin açıdan bağımsız çalışması gerekiyor. Her iki durumda da geometrik dönüşüm, piksel koordinatlarını yeni bir düzene oturtarak problemi çözer.

## Temel Dönüşümler

### Yeniden Boyutlandırma

Görüntüyü küçülteceğinizde bilgi kaybediyorsunuz — bu kaçınılmaz. Ama bu kaybın kalitesini enterpolasyon yöntemi belirler.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

h, w = img.shape[:2]

# Piksel boyutu ile yeniden boyutlandırma
kucuk = cv2.resize(img, (320, 240), interpolation=cv2.INTER_AREA)

# Oran ile yeniden boyutlandırma (yüzde 150'ye büyüt)
buyuk = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

print(f"Orijinal: {img.shape[:2]}, Küçük: {kucuk.shape[:2]}, Büyük: {buyuk.shape[:2]}")

cv2.imshow("Kucuk", kucuk)
cv2.imshow("Buyuk", buyuk)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`INTER_AREA` küçültürken piksel bloklarını ortalar — en temiz küçültme. `INTER_LINEAR` büyütürken çevresindeki 4 pikseli enterpolasyon yapar — hızlı ve yeterince kaliteli. Kalite öncelikliyse `INTER_CUBIC` veya `INTER_LANCZOS4` kullanın, daha yavaştır.

| Enterpolasyon | Kullanım Durumu | Hız |
|---------------|-----------------|-----|
| `INTER_NEAREST` | Piksel sanatı, maske görüntüler | En hızlı |
| `INTER_LINEAR` | Genel büyütme | Hızlı |
| `INTER_AREA` | Küçültme | Orta |
| `INTER_CUBIC` | Kaliteli büyütme | Yavaş |
| `INTER_LANCZOS4` | Maksimum kalite | En yavaş |

### Çevirme

Görüntüyü yatay, dikey veya her iki eksende aynalama işlemi:

```python
import cv2

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

dikey_cevir = cv2.flip(img, 0)    # 0: dikey eksen (yukarı-aşağı)
yatay_cevir = cv2.flip(img, 1)    # 1: yatay eksen (sol-sağ ayna)
her_iki = cv2.flip(img, -1)       # -1: her iki eksen

karsilastirma = np.hstack([img, yatay_cevir, dikey_cevir])
cv2.imshow("Orijinal | Yatay | Dikey", karsilastirma)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Üç görüntü yan yana gelince farkı anında görürsünüz: yatay çevirme aynaya bakmak gibi, dikey çevirme ise baş aşağı.

### Döndürme

Döndürme işleminin arkasındaki fikir: görüntüdeki her pikseli seçilen merkez noktası etrafında belirli bir açı kadar döndürmek. Matematiksel olarak:

$$[x', y'] = R \cdot [x, y]^T$$

Burada $R$ döndürme matrisidir. OpenCV merkez ve ölçek parametrelerini de içeren genişletilmiş bir form kullanır.

```python
import cv2

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

h, w = img.shape[:2]
merkez = (w // 2, h // 2)

# Merkez: görüntü ortası, açı: 45°, ölçek: 1.0 (boyut değişmesin)
M = cv2.getRotationMatrix2D(merkez, 45, 1.0)
dondurulmus = cv2.warpAffine(img, M, (w, h))

# Kırpılmadan döndür — canvas'ı büyüt
M2 = cv2.getRotationMatrix2D(merkez, 30, 1.0)
dondurulmus2 = cv2.warpAffine(img, M2, (w, h), borderMode=cv2.BORDER_REPLICATE)

cv2.imshow("Dondurulmus 45", dondurulmus)
cv2.imshow("Dondurulmus 30 Replicate", dondurulmus2)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`warpAffine`'in son iki argümanı çıktı boyutudur. Görüntü köşelerinin kesilmesini istemiyorsanız köşegen uzunluğunu canvas boyutu olarak kullanabilirsiniz: `int(np.sqrt(h**2 + w**2))`.

## Affine Dönüşüm

Affine dönüşüm bir görüntüdeki paralel çizgilerin çıkışta da paralel kalacağını garanti eder. Ölçekleme, döndürme, kaydırma ve yansıma hepsi affine dönüşümlerdir. Anahtar nokta: 3 kaynak noktası ve onların hedef konumları yeterli — 6 bilinmeyeni çözmek için 3 nokta çifti yetişir.

Sezgi: Üçgen şeklindeki üç noktayı tutup çekiyorsunuz, görüntünün geri kalanı bu harekete uygun şekilde gerilip bükülüyor, ama paralel çizgiler paralel kalıyor.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

h, w = img.shape[:2]

# Kaynak noktalari: sol üst, sağ üst, sol alt
src_pts = np.float32([
    [0, 0],
    [w - 1, 0],
    [0, h - 1]
])

# Hedef noktalar: hafif yamultma efekti
dst_pts = np.float32([
    [0, 0],
    [w - 1, 0],
    [50, h - 1]
])

M = cv2.getAffineTransform(src_pts, dst_pts)
affine_sonuc = cv2.warpAffine(img, M, (w, h))

cv2.imshow("Orijinal", img)
cv2.imshow("Affine", affine_sonuc)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Sol alt köşeyi 50 piksel sağa kaydırdık — görüntü yamultulmuş ama üst kenar düz kaldı. Dikkat edin: affine dönüşümde paralel çizgiler korunur.

## Perspektif Dönüşümü (Homografi)

Perspektif dönüşümü daha güçlü bir araçtır — artık paralel çizgilerin korunmasını garanti etmez, ama gerçek dünya perspektifini modellemenizi sağlar. Akıllı telefon belge tarayıcıları tam bunu yapar: fotoğraftaki belgenin 4 köşesini tespit edip "düzleştirir".

Matematiksel olarak 3×3 homografi matrisi, kaynak ve hedef düzlemler arasındaki dönüşümü kodlar. 4 nokta çifti 8 bilinmeyeni çözmeye yeter.

Senaryo: Eğik çekilen bir tahta fotoğrafını düzeltelim. Tahtanın 4 köşesini biliyoruz.

```python
import cv2
import numpy as np

path = "tahta.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

# Orijinal görüntüdeki 4 köşe (saat yönünde: sol üst, sağ üst, sağ alt, sol alt)
src_pts = np.float32([
    [120, 50],   # sol üst
    [620, 80],   # sağ üst
    [580, 430],  # sağ alt
    [80, 400]    # sol alt
])

# Hedef: düzgün dikdörtgen
cikti_gen, cikti_yuk = 600, 400
dst_pts = np.float32([
    [0, 0],
    [cikti_gen - 1, 0],
    [cikti_gen - 1, cikti_yuk - 1],
    [0, cikti_yuk - 1]
])

M = cv2.getPerspectiveTransform(src_pts, dst_pts)
duzlenmis = cv2.warpPerspective(img, M, (cikti_gen, cikti_yuk))

cv2.imshow("Orijinal (Egik)", img)
cv2.imshow("Duzlenmis", duzlenmis)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`warpPerspective` 3×3 homografi matrisini alır ve her kaynak pikselini hedef koordinata dönüştürür. Çıktı boyutunu kendiniz belirliyorsunuz — belgenin gerçek en-boy oranını biliyorsanız buna göre ayarlayın.

> **💡 İpucu:** Gerçek uygulamada köşeleri elle girmek yerine `cv2.findContours` ile belge sınırlarını otomatik tespit edebilirsiniz. 4 köşeli kontur en büyük alan ile en iyi belge adayıdır.

> **⚠️ Dikkat:** Perspektif dönüşümü bilgi kaybeder — özellikle köşelerin dışında kalan alanlar. Döküman tarama gibi uygulamalarda kaynak koordinatlarını mümkün olduğunca doğru seçin.

## Görüntü Üzerine Çizim

OpenCV'de tüm çizim fonksiyonları görüntüyü yerinde (in-place) değiştirir. Orijinali korumak istiyorsanız önce `img.copy()` alın.

```python
import cv2
import numpy as np

# Boş siyah kanvas oluştur
kanvas = np.zeros((500, 700, 3), dtype=np.uint8)

# Dikdörtgen: sol üst köşe, sağ alt köşe, renk (BGR), kalınlık (-1 = dolu)
cv2.rectangle(kanvas, (50, 50), (300, 200), (0, 255, 0), 2)
cv2.rectangle(kanvas, (350, 50), (650, 200), (255, 0, 0), -1)  # dolu mavi

# Daire: merkez, yarıçap, renk, kalınlık
cv2.circle(kanvas, (150, 350), 80, (0, 0, 255), 3)
cv2.circle(kanvas, (500, 350), 60, (0, 255, 255), -1)  # dolu sarı

# Çizgi: başlangıç, bitiş, renk, kalınlık
cv2.line(kanvas, (0, 480), (700, 480), (200, 200, 200), 1)

# Metin: text, konum (sol alt köşe), font, ölçek, renk, kalınlık
cv2.putText(
    kanvas, "OpenCV Cizim", (50, 470),
    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2
)

cv2.imshow("Cizim Ornekleri", kanvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Renk argümanı her zaman `(B, G, R)` tuple'ıdır. `thickness=-1` şekli doldurur. `cv2.putText` koordinatı metnin sol alt köşesidir — üst değil.

> **⚠️ Dikkat:** `cv2.putText` Türkçe karakterleri (ş, ğ, ü, ç, ö, ı) desteklemez. Türkçe metin için PIL/Pillow kütüphanesi kullanın.

### Çizim Fonksiyonları Özeti

| Fonksiyon | Temel Parametreler | Not |
|-----------|-------------------|-----|
| `cv2.rectangle` | sol üst, sağ alt, renk, kalınlık | `-1` kalınlık = dolu |
| `cv2.circle` | merkez, yarıçap, renk, kalınlık | `-1` kalınlık = dolu |
| `cv2.line` | başlangıç, bitiş, renk, kalınlık | |
| `cv2.ellipse` | merkez, eksenler, açı, başlangıç, bitiş | |
| `cv2.polylines` | nokta dizisi, kapalı mı, renk, kalınlık | |
| `cv2.putText` | metin, konum, font, ölçek, renk, kalınlık | ASCII karakterler |

## ROI Kırpma

ROI (Region of Interest — İlgi Bölgesi) belirli bir bölgeyi görüntüden çıkarmanın en basit yoludur. NumPy dilimleme kullanır.

```python
import cv2

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

# img[y1:y2, x1:x2] — önce dikey (satır), sonra yatay (sütun)
roi = img[80:280, 100:400].copy()

print(f"Orijinal: {img.shape[:2]}, ROI: {roi.shape[:2]}")

# Orijinal üzerinde ROI sınırını göster
gosterim = img.copy()
cv2.rectangle(gosterim, (100, 80), (400, 280), (0, 255, 0), 2)

cv2.imshow("ROI Gosterim", gosterim)
cv2.imshow("ROI", roi)
cv2.imwrite("kirpilan_bolge.jpg", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

ROI kırpma sıfır maliyetli değerlendirme (lazy evaluation) yapar — `.copy()` çağırana kadar yeni bellek ayrılmaz, sadece orijinal diziye bir "pencere" açılır. İşlem hattında ROI üzerinde işlem yapıp sonucu geri koyacaksanız bu özelliği kullanabilirsiniz: `img[y1:y2, x1:x2] = islenmis_roi`.

## Özet & İleri Okuma

- Enterpolasyon seçimi görüntü kalitesini doğrudan etkiler: küçültürken `INTER_AREA`, büyütürken `INTER_LINEAR` veya `INTER_CUBIC`.
- Affine dönüşüm paralel çizgileri korur — 3 nokta çifti yeterli; `cv2.getAffineTransform` + `cv2.warpAffine`.
- Perspektif dönüşümü (homografi) paralel çizgileri korumaz ama 4 köşe ile düzlem-düzlem dönüşümü modeller — belge tarama uygulamasının temelidir.
- `cv2.warpPerspective` perspektif düzeltme için, `cv2.warpAffine` affine/döndürme/kaydırma için kullanılır.
- Çizim fonksiyonları görüntüyü yerinde değiştirir; orijinali korumak için önce `.copy()` alın.
- ROI kırpma `img[y1:y2, x1:x2]` — bağımsız kopya için `.copy()` zorunlu.
- `cv2.putText` ASCII-only; Türkçe karakterler için PIL/Pillow kullanın.

**Referanslar**

- Bradski, G. & Kaehler, A. (2017). *Learning OpenCV 3*. O'Reilly Media.
- OpenCV Geometric Transformations: [docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html)
