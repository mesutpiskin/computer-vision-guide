# Kamera Kalibrasyonu ve 3D Görü

Aksiyon kameranızla çektiğiniz fotoğraflarda düz çizgiler eğri görünür. Robot kolunun kamerası mesafeyi hatalı hesaplıyor ve kol yanlış yere iniyor. Bu iki problem aynı kaynaktan gelir: kamera modeli bilinmeden piksel koordinatları gerçek dünya koordinatlarına çevrilemez. Kalibrasyon bu modeli öğrenir; stereo görü ise iki kalibre edilmiş kameradan derinlik bilgisi çıkarır.

## Pinhole Kamera Modeli

Karanlık bir odanın duvarına küçük bir delik açın — dışarının ters ve canlı bir görüntüsü oluşur. Kamera obscura olarak bilinen bu ilke modern kamera modelinin temelidir.

Odak uzaklığı (f) bu analojide deliğin duvara olan mesafesi gibidir: büyük f dar açıyı (telefoto), küçük f geniş açıyı (balık gözü) tanımlar. Gerçek dünya noktası (X, Y, Z) görüntü pikseliyle (u, v) şu ilişkiyle bağlıdır:

$$\begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = K \cdot \begin{bmatrix} X/Z \\ Y/Z \\ 1 \end{bmatrix}$$

Burada **K kamera iç parametreleri matrisidir**:

$$K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}$$

$f_x, f_y$: piksel cinsinden odak uzaklığı (sensör fiziksel boyutu ve piksel büyüklüğüne bağlı); $c_x, c_y$: görüntü merkezi. Bu matrisi bilmeden "pikselde 150 birim uzakta" ifadesinin gerçekte kaç metre olduğunu hesaplayamazsınız.

## Lens Bozulmaları

Gerçek lensler mükemmel pinhole değildir. İki ana bozulma türü vardır:

**Radyal bozulma:** Görüntü merkezinden uzaklaştıkça hatalar büyür.
- *Barrel (fıçı):* Kenarlar dışa şişer. Aksiyon kameral arının karakteristik balık gözü görünümü.
- *Pincushion (iğne yastığı):* Kenarlar içe çöker. Eski telefoto lenslerde yaygın.

**Teğetsel bozulma:** Lens ile sensör tam paralel olmadığında oluşur; görüntü bir yönde hafifçe yamulur.

Düzelme formülü radyal için: $x_{corrected} = x(1 + k_1 r^2 + k_2 r^4 + k_3 r^6)$

$k_1, k_2, k_3$ katsayıları kalibrasyonla öğrenilir. Bunlara teğetsel katsayılar $p_1, p_2$ eklenerek `dist = [k1, k2, p1, p2, k3]` vektörü oluşur.

## Satranç Tahtası Kalibrasyonu

Neden satranç tahtası? Köşe noktaları matematiksel kesinlikle bulunabilir — köşe tam olarak iki siyah ve iki beyaz karenin buluştuğu noktadır. 15-20 farklı açı ve mesafeden fotoğraf, kamera parametrelerini güvenilir biçimde kısıtlar.

```python
import cv2
import numpy as np
import glob

# Satranç tahtası iç köşe sayısı (6x9 tahta için 5x8)
BOARD_W, BOARD_H = 9, 6
SQUARE_SIZE = 25.0  # mm cinsinden kare boyutu

# 3D dünya koordinatları — Z=0 düzleminde
objp = np.zeros((BOARD_H * BOARD_W, 3), np.float32)
objp[:, :2] = np.mgrid[0:BOARD_W, 0:BOARD_H].T.reshape(-1, 2) * SQUARE_SIZE

obj_points = []  # 3D gerçek dünya noktaları
img_points = []  # 2D görüntü noktaları
img_size = None

images = glob.glob("kalibrasyon/*.jpg")
if not images:
    raise FileNotFoundError("kalibrasyon/ klasöründe görüntü bulunamadı")

for path in images:
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_size = gray.shape[::-1]  # (genişlik, yükseklik)

    ret, corners = cv2.findChessboardCorners(gray, (BOARD_W, BOARD_H), None)

    if ret:
        # Köşe konumlarını alt-piksel hassasiyetiyle iyileştir
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        obj_points.append(objp)
        img_points.append(corners_refined)

print(f"{len(obj_points)} kalibrasyon görüntüsü kullanıldı")

# Kamera matrisini ve bozulma katsayılarını hesapla
rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    obj_points, img_points, img_size, None, None
)

print(f"RMS yeniden projeksiyon hatası: {rms:.4f} piksel")
print("Kamera matrisi K:\n", K)
print("Bozulma katsayıları:", dist.ravel())

# Kalibrasyonu dosyaya kaydet
np.save("camera_matrix.npy", K)
np.save("dist_coeffs.npy", dist)

# Örnek görüntüye undistort uygula
test_img = cv2.imread(images[0])
undistorted = cv2.undistort(test_img, K, dist)

comparison = np.hstack([test_img, undistorted])
cv2.imshow("Orijinal | Düzeltilmiş", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

RMS hatası < 0.5 piksel iyi kalibrasyon göstergesidir. 1.0'ın üzerindeyse daha fazla ve daha çeşitli açılardan görüntü ekleyin.

> **⚠️ Dikkat:** Kalibrasyon görüntülerini aynı odak uzaklığında çekin. Zoom yaptıysanız veya kamera ayarları değiştiyse yeniden kalibre edin — K matrisi lens ayarına bağlıdır.

> **💡 İpucu:** `cv2.getOptimalNewCameraMatrix()` undistort sonrası kaybolan kenar piksellerini telafi eden daha geniş bir alan hesaplar. Görüntü kenarları önemliyse bu fonksiyonu kullanın.

## Stereo Görü ve Derinlik

Sağ gözünüzü kapayın, sol gözünüzle bir kaleme bakın. Sonra gözleri değiştirin — kalem yer değiştirmiş gibi görünür. Bu paralaks (disparity) etkisi, beynin iki göz arasındaki farkı kullanarak derinliği algılamasının temelidir.

İki kamera aynı ilkeyi uygular: soldan ve sağdan bakılan aynı noktanın görüntü koordinatları arasındaki fark (disparity) derinliği verir:

$$Z = \frac{f \cdot B}{d}$$

Burada $f$ odak uzaklığı, $B$ iki kamera arasındaki mesafe (baseline), $d$ ise disparity'dir. Disparity büyüdükçe nesne yakınlaşır.

```python
import cv2
import numpy as np

# Stereo görüntüleri yükle
left_img = cv2.imread("stereo_left.jpg")
right_img = cv2.imread("stereo_right.jpg")
if left_img is None or right_img is None:
    raise FileNotFoundError("Stereo görüntü dosyaları bulunamadı")

left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

# Semi-Global Block Matching — SGBM
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=128,   # 16'nın katı olmalı
    blockSize=11,
    P1=8 * 3 * 11**2,    # Küçük disparity değişimi için ceza
    P2=32 * 3 * 11**2,   # Büyük disparity değişimi için ceza
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32,
)

disparity = stereo.compute(left_gray, right_gray).astype(np.float32) / 16.0

# Normalize et ve renklendir
disp_normalized = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
disp_color = cv2.applyColorMap(disp_normalized, cv2.COLORMAP_JET)

cv2.imshow("Sol Görüntü", left_img)
cv2.imshow("Derinlik Haritası", disp_color)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Derinlik haritasında sıcak renkler (kırmızı) yakın nesneleri, soğuk renkler (mavi) uzak nesneleri temsil eder. Düz yüzeylerde ve kenar bölgelerde hesaplama güçleşir.

> **📌 Not:** Stereo derinliğinin güvenilir olması için iki kameranın rektifiye edilmesi gerekir — yani sol ve sağ kamera görüntülerinin aynı yatay epipolar çizgiye hizalanması. `cv2.stereoRectify()` ve `cv2.initUndistortRectifyMap()` bu işlemi yapar.

## Pratik: Piksel Boyutundan Gerçek Boyuta

Kalibrasyon sayesinde görüntüdeki bir nesnenin gerçek boyutunu ölçebilirsiniz. Yöntem: bilinen boyutlu referans nesneyi aynı karede tutun, pikselden metreye dönüşüm katsayısını hesaplayın.

```python
import cv2
import numpy as np

# Referans nesne: bilinen genişliği W_mm olan bir kart
W_mm = 85.6  # Kredi kartı genişliği (mm)

img = cv2.imread("olcum.jpg")
if img is None:
    raise FileNotFoundError("olcum.jpg bulunamadı")

# Kayıtlı kamera matrisini yükle
K = np.load("camera_matrix.npy")
dist = np.load("dist_coeffs.npy")

# Bozulmayı gider
img = cv2.undistort(img, K, dist)

# Referans nesnenin piksel genişliğini manuel veya otomatik ölç
# Burada örnek olarak elle belirtiyoruz
ref_pixel_width = 320  # Ölçülen piksel genişliği
focal_length_px = K[0, 0]  # f_x

# Derinlik kestirimi — nesne kameranın önünde Z mesafesinde
# Gerçek uygulamada stereo veya bilinen mesafe kullanılır
Z_mm = 500.0  # Nesne 500 mm uzakta

# Piksel / mm dönüşüm katsayısı
px_per_mm = ref_pixel_width / W_mm

print(f"Ölçek: {px_per_mm:.2f} piksel/mm")
print(f"1 piksel ≈ {1/px_per_mm:.3f} mm bu mesafede")
```

## Yöntem Karşılaştırması

| Konu | Yöntem | Ne Zaman |
|------|--------|----------|
| Lens bozulması giderme | `cv2.undistort()` | Her zaman, kalibrasyon sonrası |
| Tek kamera derinlik | Monoküler derinlik (DPT, MiDaS) | Stereo kamera yoksa |
| Stereo derinlik | StereoSGBM | Yüksek doğruluk, kontrollü ortam |
| 3D nokta bulutu | `cv2.reprojectImageTo3D()` | Stereo sonrası 3D model |

## Özet

- Kamera iç parametreleri K matrisi piksel koordinatlarını gerçek dünya koordinatlarına bağlar.
- Radyal bozulma kenarları şişirir (barrel) veya çökertir (pincushion); teğetsel bozulma görüntüyü yamultur.
- Satranç tahtası kalibrasyonu 15-20 görüntüyle K matrisini ve bozulma katsayılarını öğrenir.
- RMS yeniden projeksiyon hatası < 0.5 piksel iyi kalibrasyon kalitesini gösterir.
- Stereo görüde disparity derinliği verir: yakın nesne büyük disparity, uzak nesne küçük disparity.
- SGBM stereo eşleşme algoritması OpenCV'de direkt kullanılabilir; rektifikasyon şarttır.
- Kalibrasyon tamamlandıktan sonra piksel ölçümlerini milimetreye çevirmek mümkündür.

## İleri Okuma

- Hartley & Zisserman, "Multiple View Geometry in Computer Vision" (2. baskı, 2004) — alandaki temel kaynak kitap
- Zhang, Z., "A Flexible New Technique for Camera Calibration" (IEEE TPAMI 2000) — satranç tahtası kalibrasyonunun matematiksel temeli
- OpenCV Kamera Kalibrasyon Dokümantasyonu: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
