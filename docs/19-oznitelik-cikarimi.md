**Öznitelik ve Öznitelik Çıkarımı** 
-----------------------------------

Öznitelik bizim için en anlamlı tanım olarak  "bir nesnenin veya bireyin nitel özelliğidir", TÜBA Sözlüğe göre de "Bir sistemi, bir nesneyi veya bir sınıfı niteleyen, ayırt edilmesini sağlayan özellik" yani ayırt edici özelliktir. Bu tanımlardan yola çıkarsak nesneyi tanımlayan ve açıkca değiştirilmediği sürece nesneyi tanımlayan özelliklerdir yani bir canlı için cinsiyeti veya insan yüzünde burnun bulunması genel itibari ile o nesnenin bir üzelliğidir. 

## Öznitelik Çıkarımı (Feature Extraction)

Görüntü işleme, makine öğrenmesi, derin öğrenme, veri madenciliği ve örüntü tanıma uygulamalarında sıklıkla başvurulan bir yöntemdir. Bizim ilgilendiğimiz alanı ise görüntü üzerindeki nesnelerin ayırt edilebilmesidir. Bir çok algoritma tarafından kolayca çözülen bir problem olan yüz tespitini düşünün, siz olsaydanız bir insan yüzünü nasıl tanımlardınız?

 - İnsan yüzünde iki göz bulunur. 
 - İnsan yüzünde bir burun bulunur.
 - İnsan yüzünde bir ağız vardır.

 Peki ya göz, burun veya ağız nedir? Algoritmik olarak problemi ele aldığımızda insan yüzünü tanımlayan bir çok özellik ve bu özellikleri tanımlayan bir çok özellik vardır ve bunlar kendi içlerinde ayrı bir problem teşkil etmektedir. Bundan on beş veya yirmi yıl (neden yıllar önce olduğuna değineceğim) gibi bir süre önce bu problemi çözecek bir yazılım geliştirmeye çalışan birisi olduğunuzda bu süreç sizin için sancılı olacaktır. Çünkü nesnenin özniteliklerini tanımak ayrı bir mühendislik gerektirecekti. Gözün, burnun ve ağzın tüm özniteliklerini tanımlayan algoritmayı geliştirdikten sonra geriye kalan bunları birleştirmek olacak. Öznitelik çıkarımını başka amaçlar içinde kullanabilirsiniz. Örneğin nesneyi tespit etmek yerine aynı cins iki nesneyi bir biri ile karşılaştırmak/eşleştirmek **feature matching** için kullanabilirsiniz. Çünkü aynı cins iki nesne benzer öz niteliklere sahip olacaktır.

 ## OpenCV Uygulamaları

**Öznitelik Çıkarma (Feature Extraction)**

- SIFT
- SURF
- BRIEF
- ORB
- FAST
- BRISK

**Öznitelik Eşleştirme (Feature Matching)**

- Brute-Force
- FLANN


### Teorik Temel — SIFT ve Öznitelik Eşleştirme

**Scale-Space Extrema Tespiti (SIFT):**
$$L(x,y,\sigma) = G(x,y,\sigma) * I(x,y)$$
$$D(x,y,\sigma) = L(x,y,k\sigma) - L(x,y,\sigma)$$
DoG (Difference of Gaussians) ile ölçek uzayı anahtar noktaları bulunur. $k=\sqrt{2}$.

**Gradient Histogramı ve 128-boyutlu Descriptor:**
$$m(x,y) = \sqrt{(L_{x+1}-L_{x-1})^2 + (L_{y+1}-L_{y-1})^2}$$
$$\theta(x,y) = \arctan\left(\frac{L_{y+1}-L_{y-1}}{L_{x+1}-L_{x-1}}\right)$$
16×16 pencere → 4×4 alt bölge × 8 yön histogramı = 128 boyut. L2 normalize edilir.

**Lowe Oran Testi (Ratio Test):**
İki en iyi eşleşme $d_1 < d_2$ ise: $d_1 / d_2 < 0.7$ koşuluyla iyi eşleşme kabul edilir.
Yanlış eşleşmeleri (outlier) etkili biçimde eleme yöntemidir.

Referans: Lowe, "Distinctive Image Features from Scale-Invariant Keypoints", IJCV 2004 (https://doi.org/10.1023/B:VISI.0000029664.99615.94)

#### SIFT (Scale-Invariant Feature Transform - Ölçeklemeden Bağımsız Özellik Dönüşümü)

SIFT algoritması David  Lowe tarafından 1999 yılında duyruldu. Bu algoritma sayesinde karşılaştırılan iki farklı giriş nesnesinin boyutu/ölçeği değişse veya belirli bir eşik seviyesine kadar gürültülü bile olsa başarılı olarak öznitelikler çıkarılıp eşleştirilebilmektedir. SIFT 3D Modelleme, nesne tanıma, nesne eşleme, nesne takibi vb. gibi bir çok alanda kullanılan bir algoritmadır. SIFT algoritmasının çalışması dört aşamada incelenir. Bu aşamalar; "Scale-Space Extrema Detection",  "Keypoint Localization", "Orientation Assignment" ve "Keypoint Descriptor".

#### SURF (Speeded up Robust Features)

SIFT algoritmasını hızlandırmak amacıyla ortaya çıkan bu algoritma 2006 yılında Herbert Bay tarafından duyruldu. SIFT algoritmasına göre x2 x3 kat daha hızlı çalışan bu algoritma yine SIFT de olduğu gibi ölçeklemeden bağımsız çalışmaktadır. SURF algoritmasının çalışması üç aşamada incelenir. Bu aşamalar; "Interest point detection", "local neighborhood description" ve "matching".


![Oznitelik Algoritmaları Versus](static/surfvssift.png)

Orjinal Görsel Kaynağı: http://www.willpowell.co.uk/blog/2014/09/07/feature-extractor-descriptor-performance-ios-ipad-iphones/


---

## Python Kod Örnekleri

### ORB ile Öznitelik Çıkarımı ve Görselleştirme

ORB (Oriented FAST and Rotated BRIEF), ücretsiz ve hızlı çalışan bir öznitelik çıkarım algoritmasıdır. (SIFT ve SURF patentli olduğundan `opencv-contrib-python` gerektirir.)

```python
import cv2
import numpy as np

img = cv2.imread("goruntu.jpg", cv2.IMREAD_GRAYSCALE)

orb = cv2.ORB_create(nfeatures=500)
keypoints, descriptors = orb.detectAndCompute(img, None)

img_kp = cv2.drawKeypoints(img, keypoints, None,
                            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("ORB Anahtar Noktalar", img_kp)
cv2.waitKey(0)
print(f"Bulunan anahtar nokta sayısı: {len(keypoints)}")
```

### SIFT ile Öznitelik Çıkarımı

> Not: SIFT kullanmak için `pip install opencv-contrib-python` gereklidir.

```python
import cv2

img = cv2.imread("goruntu.jpg", cv2.IMREAD_GRAYSCALE)

sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(img, None)

img_kp = cv2.drawKeypoints(img, keypoints, None)
cv2.imshow("SIFT Anahtar Noktalar", img_kp)
cv2.waitKey(0)
print(f"Descriptor boyutu: {descriptors.shape}")  # (N, 128)
```

### Brute-Force ile Öznitelik Eşleştirme

```python
import cv2
import numpy as np

img1 = cv2.imread("nesne.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("sahne.jpg", cv2.IMREAD_GRAYSCALE)

orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Brute-Force Matcher — ORB için Hamming mesafesi kullan
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

# Mesafeye göre sırala — en iyi eşleşmeler önce
matches = sorted(matches, key=lambda x: x.distance)

# İlk 20 eşleşmeyi göster
result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:20], None,
                         flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imshow("Brute-Force Eşleştirme", result)
cv2.waitKey(0)
```

### FLANN ile Hızlı Öznitelik Eşleştirme

FLANN (Fast Library for Approximate Nearest Neighbors), büyük veri setlerinde BFMatcher'a göre çok daha hızlı çalışır.

```python
import cv2
import numpy as np

img1 = cv2.imread("nesne.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("sahne.jpg", cv2.IMREAD_GRAYSCALE)

sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# FLANN parametreleri
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

# Lowe'un oran testi — kötü eşleşmeleri filtrele
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

result = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None,
                         flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imshow(f"FLANN — {len(good_matches)} iyi eşleşme", result)
cv2.waitKey(0)
```

### Homografi ile Nesne Konumu Bulma

Eşleştirilen öznitelikleri kullanarak bir nesnenin sahnedeki konumunu bul:

```python
import cv2
import numpy as np

img1 = cv2.imread("nesne.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("sahne.jpg", cv2.IMREAD_GRAYSCALE)

sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

flann = cv2.FlannBasedMatcher(
    dict(algorithm=1, trees=5), dict(checks=50)
)
matches = flann.knnMatch(des1, des2, k=2)
good = [m for m, n in matches if m.distance < 0.7 * n.distance]

if len(good) >= 4:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    h, w = img1.shape
    corners = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
    scene_corners = cv2.perspectiveTransform(corners, H)

    img2_color = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    cv2.polylines(img2_color, [np.int32(scene_corners)], True, (0, 255, 0), 3)
    cv2.imshow("Nesne Konumu", img2_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print(f"Yeterli eşleşme yok: {len(good)} / 4")
```

### SIFT + FLANN + ORB Kapsamlı Örnek

```python
import cv2
import numpy as np

img1 = cv2.imread("sorgu.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("sahne.jpg", cv2.IMREAD_GRAYSCALE)
if img1 is None or img2 is None:
    raise FileNotFoundError("sorgu.jpg veya sahne.jpg bulunamadı")

# SIFT öznitelik çıkarımı
sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)
print(f"Görüntü 1: {len(kp1)} anahtar nokta")
print(f"Görüntü 2: {len(kp2)} anahtar nokta")

# FLANN tabanlı eşleştirme
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

# Lowe oran testi
good = [m for m, n in matches if m.distance < 0.7 * n.distance]
print(f"İyi eşleşme: {len(good)}/{len(matches)}")

# Homografi (4+ iyi eşleşme gerekir)
if len(good) >= 4:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    print(f"RANSAC inlier: {mask.sum()}/{len(good)}")

# ORB — patent-free alternatif
orb = cv2.ORB_create(nfeatures=500)
kp1_orb, des1_orb = orb.detectAndCompute(img1, None)
kp2_orb, des2_orb = orb.detectAndCompute(img2, None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches_orb = sorted(bf.match(des1_orb, des2_orb), key=lambda x: x.distance)

# Eşleşmeleri görselleştir
result = cv2.drawMatches(img1, kp1, img2, kp2,
                          [m for m in good[:20]], None,
                          flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imshow("SIFT Eşleşmeleri", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Özet & İleri Okuma
- SIFT ölçek ve rotasyon değişmez öznitelikler üretir; patent süresi dolmuştur (2020+)
- DoG scale-space extrema ile anahtar noktalar bulunur; 128-boyutlu descriptor hesaplanır
- Lowe oran testi (d1/d2 < 0.7) yanlış eşleşmeleri etkili biçimde eler
- FLANN, BruteForce'tan çok daha hızlı büyük öznitelik setlerinde eşleştirme yapar
- ORB patent-free ve SIFT'ten ~100x daha hızlıdır; gerçek zamanlı uygulamalar için idealdir
- Referans: Lowe 2004 (https://doi.org/10.1023/B:VISI.0000029664.99615.94)
