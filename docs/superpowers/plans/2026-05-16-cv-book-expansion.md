# CV Kitabı Kapsamlı Revizyon & Genişletme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 15 mevcut bölümü akademik derinlikle revize et, 6 yeni bölüm ekle — her bölüm teori+formül+kod+referans şablonunu izler.

**Architecture:** Her görev bağımsız bir `.md` dosyasını hedefler. Görevler tam paralel çalışabilir — shared state yok. Her agent aşağıdaki standart şablonu uygular. GRUP A/B/C/D aynı anda başlayabilir, sonunda README + terimler güncellenir.

**Tech Stack:** Markdown, Python 3.10+, OpenCV 4.9+, PyTorch, Ultralytics YOLOv8, MediaPipe, scikit-learn

---

## STANDART ŞABLON (Her Bölüm İçin)

Her revize/yeni bölüm şu yapıyı izler:

```markdown
## [Bölüm Adı]

### Teorik Temel
[Akademik tanım, tarihsel bağlam]
[Matematiksel formüller: inline $...$ veya blok $$...$$]
[Her formülün Türkçe sezgisel açıklaması]
[Referanslar: Yazar et al., Yıl — https://arxiv.org/...]

### Algoritma Detayı
[Adım adım numaralı açıklama]
[Karşılaştırma tablosu: yöntemler arası avantaj/dezavantaj]

### Pratik Uygulama
[Tam çalışan Python kodu, ```python bloğu içinde]
[Gerçek dünya senaryosu]

### Özet & İleri Okuma
[5-7 madde kilit çıkarım]
[Önerilen kaynaklar]
```

**Başarı kriterleri (her bölüm için):**
- En az 1 akademik paper referansı (arXiv veya DOI linki ile)
- En az 1 matematiksel formül (Türkçe sezgisel açıklamalı)
- En az 1 tam çalışan Python kodu bloğu (`python` tag zorunlu)
- Türkçe açıklamalar, kod değişkenleri İngilizce

---

## GRUP A — Temel Bölümler

---

### Task 1: Bölüm 6 — Giriş ve Temel Kavramlar

**Files:**
- Modify: `docs/6-giris-temel-kavramlar.md`

- [ ] **Step 1: Mevcut dosyayı oku**

  `docs/6-giris-temel-kavramlar.md` dosyasını oku ve mevcut içeriği not al.

- [ ] **Step 2: Teorik Temel bölümü yaz**

  Şu konuları ekle:

  **Dijital Görüntü Matematiği:**
  - Görüntüyü $f(x,y)$ fonksiyonu olarak tanımla: $f: \mathbb{Z}^2 \rightarrow \mathbb{Z}^k$ — $(x,y)$ piksel koordinatı, $k$ kanal sayısı
  - Gri tonlamalı görüntü: $k=1$, RGB: $k=3$, RGBA: $k=4$
  - Örnekleme (sampling) ve nicemleme (quantization) kavramları
  - Bit derinliği: 8-bit → $[0, 255]$, 16-bit → $[0, 65535]$
  - Referans: Gonzalez & Woods, "Digital Image Processing" (4. baskı)

  **Konvolüsyon Temeli:**
  $$g(x,y) = f(x,y) * h(x,y) = \sum_{s}\sum_{t} f(s,t) \cdot h(x-s, y-t)$$
  Açıklama: $f$ giriş görüntüsü, $h$ çekirdek (kernel), $g$ çıkış — her piksel komşularının ağırlıklı ortalaması.

  **NumPy ile Görüntü Temsili:**
  - RGB görüntü shape: `(H, W, 3)` — yükseklik × genişlik × kanal
  - OpenCV'de kanal sırası BGR: `img[:, :, 0]` = Blue, `img[:, :, 1]` = Green, `img[:, :, 2]` = Red

- [ ] **Step 3: Pratik Uygulama bölümü yaz**

  Aşağıdaki kodu ekle:

  ```python
  import cv2
  import numpy as np

  # Görüntü okuma ve temel bilgiler
  img = cv2.imread("resim.jpg")
  print(f"Shape: {img.shape}")        # (H, W, 3)
  print(f"Dtype: {img.dtype}")        # uint8
  print(f"Min/Max: {img.min()}/{img.max()}")

  # Piksel erişimi
  b, g, r = img[100, 200]            # (y=100, x=200) pikselinin BGR değerleri
  print(f"B={b}, G={g}, R={r}")

  # Gri tonlamaya dönüşüm: Y = 0.299R + 0.587G + 0.114B
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Görüntü istatistikleri
  mean, std = cv2.meanStdDev(img)
  print(f"Kanal ortalamaları (BGR): {mean.flatten()}")

  # Kameradan görüntü okuma
  cap = cv2.VideoCapture(0)
  ret, frame = cap.read()
  if ret:
      cv2.imshow("Kamera", frame)
      cv2.waitKey(0)
  cap.release()
  cv2.destroyAllWindows()
  ```

- [ ] **Step 4: Özet & İleri Okuma ekle**

  ```markdown
  ### Özet & İleri Okuma
  - Dijital görüntü, $f(x,y)$ fonksiyonu olarak 2D/3D matris şeklinde temsil edilir
  - 8-bit görüntüde her piksel [0,255] aralığında tam sayı değer taşır
  - OpenCV BGR kanal sırası kullanır (RGB değil)
  - NumPy `shape` → `(yükseklik, genişlik, kanal)` sırasını izler
  - Konvolüsyon, görüntü işlemenin temel matematiksel operasyonudur
  - `cv2.imread` varsayılan olarak BGR okur; `cv2.IMREAD_GRAYSCALE` ile gri ton
  - Referans: Gonzalez & Woods — Digital Image Processing (https://www.imageprocessingplace.com)
  ```

- [ ] **Step 5: Commit**

  ```bash
  git add docs/6-giris-temel-kavramlar.md
  git commit -m "docs: revize ch6 - piksel matematiği, konvolüsyon teorisi, NumPy temsili"
  ```

---

### Task 2: Bölüm 8 — Görüntü Manipülasyonu

**Files:**
- Modify: `docs/8-goruntu-manipulasyonu.md`

- [ ] **Step 1: Mevcut dosyayı oku**

  `docs/8-goruntu-manipulasyonu.md` dosyasını oku.

- [ ] **Step 2: Affine Dönüşüm Matematiği ekle**

  ```markdown
  ### Teorik Temel

  **Affine Dönüşüm:**
  $$\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} a_{00} & a_{01} & t_x \\ a_{10} & a_{11} & t_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

  Affine dönüşüm paralel çizgileri korur. 6 serbestlik derecesi vardır: öteleme (2), döndürme (1), ölçekleme (2), kesme (1).

  **Perspektif Dönüşüm (Homografi):**
  $$\begin{bmatrix} x' \\ y' \\ w' \end{bmatrix} = H \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}, \quad H \in \mathbb{R}^{3\times3}$$

  Perspektif dönüşüm paralel çizgileri korumaz, 8 serbestlik derecesi vardır. En az 4 nokta çifti gereklidir.

  **İnterpolasyon Yöntemleri:**
  - En Yakın Komşu: $f(x,y) = f(\lfloor x \rceil, \lfloor y \rceil)$ — hızlı, pikselleşme
  - Bilineer: $f(x,y) = \sum_{i,j} f(i,j) \cdot \max(0, 1-|x-i|) \cdot \max(0, 1-|y-j|)$ — pürüzsüz
  - Bicubic: 4×4 komşuluk, daha yüksek kalite

  Referans: Hartley & Zisserman, "Multiple View Geometry in Computer Vision" (https://www.robots.ox.ac.uk/~vgg/hzbook/)
  ```

- [ ] **Step 3: Pratik Uygulama ekle**

  ```python
  import cv2
  import numpy as np

  img = cv2.imread("resim.jpg")
  h, w = img.shape[:2]

  # Döndürme — merkez etrafında 45 derece
  center = (w // 2, h // 2)
  M_rot = cv2.getRotationMatrix2D(center, angle=45, scale=1.0)
  rotated = cv2.warpAffine(img, M_rot, (w, h))

  # Öteleme — 50px sağa, 30px aşağı
  M_trans = np.float32([[1, 0, 50], [0, 1, 30]])
  translated = cv2.warpAffine(img, M_trans, (w, h))

  # Perspektif dönüşüm — 4 kaynak → 4 hedef nokta
  src_pts = np.float32([[0,0], [w,0], [w,h], [0,h]])
  dst_pts = np.float32([[50,30], [w-20,10], [w-50,h-30], [20,h-20]])
  H = cv2.getPerspectiveTransform(src_pts, dst_pts)
  warped = cv2.warpPerspective(img, H, (w, h))

  # Yeniden boyutlandırma — interpolasyon karşılaştırması
  small = cv2.resize(img, (w//4, h//4), interpolation=cv2.INTER_AREA)
  large_nn = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
  large_cubic = cv2.resize(small, (w, h), interpolation=cv2.INTER_CUBIC)
  ```

- [ ] **Step 4: Özet ekle ve commit at**

  ```bash
  git add docs/8-goruntu-manipulasyonu.md
  git commit -m "docs: revize ch8 - affine/homografi matematiği, interpolasyon teorisi"
  ```

---

### Task 3: Bölüm 9 — Renk Uzayları

**Files:**
- Modify: `docs/9-renk-uzaylari.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: Renk Uzayı Dönüşüm Matrisleri ekle**

  ```markdown
  ### Teorik Temel

  **RGB → Gri Ton (ITU-R BT.601):**
  $$Y = 0.299R + 0.587G + 0.114B$$
  İnsan gözü yeşile daha duyarlıdır — bu yüzden Green katsayısı en büyük.

  **RGB → HSV Dönüşümü:**
  $$V = \max(R,G,B)$$
  $$S = \begin{cases} \frac{V - \min(R,G,B)}{V} & V \neq 0 \\ 0 & V = 0 \end{cases}$$
  $$H = \begin{cases} 60 \cdot \frac{G-B}{V-\min} & V=R \\ 60 \cdot \frac{B-R}{V-\min} + 120 & V=G \\ 60 \cdot \frac{R-G}{V-\min} + 240 & V=B \end{cases}$$

  HSV'nin avantajı: renk (Hue) ve parlaklık (Value) ayrışır → renk tabanlı segmentasyon kolaylaşır.

  **RGB → Lab (CIE L*a*b*):**
  Önce RGB → XYZ (doğrusal dönüşüm matrisi ile), sonra XYZ → Lab:
  $$L^* = 116 f(Y/Y_n) - 16, \quad a^* = 500[f(X/X_n) - f(Y/Y_n)]$$
  Lab'ın avantajı: perceptually uniform — iki renk arasındaki Öklid mesafesi insan algısıyla orantılı.

  Referans: Poynton, "Digital Video and HD" (https://www.poynton.ca/ColorFAQ.html)

  **Histogram Eşitleme:**
  $$s_k = T(r_k) = (L-1)\sum_{j=0}^{k} p_r(r_j)$$
  $L$: toplam gri düzey sayısı (256), $p_r$: olasılık yoğunluğu. CDF tabanlı dönüşüm kontrası dengeler.
  ```

- [ ] **Step 3: Pratik kod ekle**

  ```python
  import cv2
  import numpy as np

  img = cv2.imread("resim.jpg")

  # Renk uzayı dönüşümleri
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  lab  = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)

  # HSV ile renk maskesi — sarı nesneleri seç
  lower_yellow = np.array([20, 100, 100])
  upper_yellow = np.array([30, 255, 255])
  mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
  result = cv2.bitwise_and(img, img, mask=mask)

  # Histogram eşitleme (gri ton)
  eq = cv2.equalizeHist(gray)

  # CLAHE — adaptif histogram eşitleme (daha iyi lokal kontrast)
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
  clahe_img = clahe.apply(gray)

  # Lab renk uzayında histogram eşitleme (renkli görüntü için)
  l, a, b = cv2.split(lab)
  l_eq = clahe.apply(l)
  lab_eq = cv2.merge([l_eq, a, b])
  result_color = cv2.cvtColor(lab_eq, cv2.COLOR_Lab2BGR)
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/9-renk-uzaylari.md
  git commit -m "docs: revize ch9 - renk dönüşüm matrisleri, histogram matematiği, CLAHE"
  ```

---

### Task 4: Bölüm 10 — Morfolojik Görüntü İşleme

**Files:**
- Modify: `docs/10-morfolojik-goruntu-isleme.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: Morfoloji Matematiği ekle**

  ```markdown
  ### Teorik Temel

  **Erosion (Aşındırma) — Minkowski Farkı:**
  $$A \ominus B = \{z \mid B_z \subseteq A\}$$
  $B_z$: $B$ yapı elemanının $z$ noktasına ötelenmiş hali. Her piksel: yalnızca yapı elemanının tamamen sığdığı yerlerde 1 kalır.

  **Dilation (Genişletme) — Minkowski Toplamı:**
  $$A \oplus B = \{z \mid (\hat{B})_z \cap A \neq \emptyset\}$$
  $\hat{B}$: $B$'nin orijine göre yansıması. Yapı elemanı herhangi bir 1-pikselini kapsayan her yerde çıkış 1 olur.

  **Opening (Açınım):** $A \circ B = (A \ominus B) \oplus B$ — Önce erosion sonra dilation. Küçük nesneleri siler, büyükleri korur.

  **Closing (Kapanım):** $A \bullet B = (A \oplus B) \ominus B$ — Önce dilation sonra erosion. Küçük delikleri kapatır.

  **Morfolojik Gradyan:** $\text{grad}(A) = (A \oplus B) - (A \ominus B)$ — Nesne kenarlarını verir.

  Referans: Serra, J. "Image Analysis and Mathematical Morphology" (1982)
  ```

- [ ] **Step 3: Pratik kod ekle**

  ```python
  import cv2
  import numpy as np

  img = cv2.imread("resim.jpg", cv2.IMREAD_GRAYSCALE)
  _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

  # Yapı elemanları
  kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
  kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
  kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))

  eroded   = cv2.erode(binary, kernel_rect, iterations=1)
  dilated  = cv2.dilate(binary, kernel_rect, iterations=1)
  opened   = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_ellipse)
  closed   = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_ellipse)
  gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel_rect)
  tophat   = cv2.morphologyEx(binary, cv2.MORPH_TOPHAT, kernel_rect)   # parlak bölgeler
  blackhat = cv2.morphologyEx(binary, cv2.MORPH_BLACKHAT, kernel_rect) # karanlık bölgeler
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/10-morfolojik-goruntu-isleme.md
  git commit -m "docs: revize ch10 - Minkowski morfoloji matematiği, yapı elemanı seçimi"
  ```

---

### Task 5: Bölüm 11 — Filtreler ve Kenar Belirleme

**Files:**
- Modify: `docs/11-filtreler-ve-kenar-belirleme.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: Konvolüsyon ve Canny Matematiği ekle**

  ```markdown
  ### Teorik Temel

  **Gaussian Filtresi:**
  $$G(x,y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}$$
  $\sigma$ (standart sapma) bulanıklık derecesini belirler. Büyük $\sigma$ → daha güçlü gürültü bastırma.

  **Sobel Operatörü — Gradyan:**
  $$G_x = \begin{bmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{bmatrix} * I, \quad G_y = \begin{bmatrix}-1&-2&-1\\0&0&0\\1&2&1\end{bmatrix} * I$$
  $$|\nabla I| = \sqrt{G_x^2 + G_y^2}, \quad \theta = \arctan\left(\frac{G_y}{G_x}\right)$$

  **Laplacian (İkinci türev):**
  $$\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}$$
  Laplacian gürültüye duyarlıdır → Gaussian ile birleştirilen LoG (Laplacian of Gaussian) tercih edilir.

  **Canny Kenar Belirleme (4 Aşama):**
  1. Gaussian ile gürültü bastırma
  2. Sobel ile gradyan büyüklük/yönü
  3. Non-maximum suppression — gradyan yönünde yerel olmayan maksimumları sıfırla
  4. Double thresholding: güçlü kenar $>T_h$, zayıf kenar $T_l < \cdot < T_h$, bağlantısız zayıfları sil

  Referans: Canny, J. "A Computational Approach to Edge Detection", IEEE TPAMI 1986 (https://doi.org/10.1109/TPAMI.1986.4767851)
  ```

- [ ] **Step 3: Pratik kod ekle**

  ```python
  import cv2
  import numpy as np

  img = cv2.imread("resim.jpg")
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Gaussian bulanıklaştırma
  blurred = cv2.GaussianBlur(gray, (5, 5), sigmaX=1.4)

  # Sobel gradyanları
  sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
  sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
  magnitude = np.sqrt(sobelx**2 + sobely**2).astype(np.uint8)

  # Laplacian
  laplacian = cv2.Laplacian(gray, cv2.CV_64F)
  laplacian_abs = np.uint8(np.absolute(laplacian))

  # Canny — T_low=50, T_high=150 (2:3 oranı önerilir)
  edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

  # Otomatik eşik (medyan tabanlı)
  v = np.median(gray)
  sigma = 0.33
  lower = int(max(0, (1.0 - sigma) * v))
  upper = int(min(255, (1.0 + sigma) * v))
  auto_edges = cv2.Canny(gray, lower, upper)
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/11-filtreler-ve-kenar-belirleme.md
  git commit -m "docs: revize ch11 - Gaussian/Sobel/Laplacian matematiği, Canny 4-aşama"
  ```

---

### Task 6: Bölüm 12 — Arkaplan Çıkarma

**Files:**
- Modify: `docs/12-arka-plan-cikarma.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: GMM İstatistiksel Model ekle**

  ```markdown
  ### Teorik Temel

  **Gaussian Mixture Model (GMM):**
  Her piksel $x$'in arkaplan olasılığı $K$ Gaussian bileşenin ağırlıklı toplamıyla modellenir:
  $$P(x) = \sum_{k=1}^{K} w_k \cdot \mathcal{N}(x; \mu_k, \sigma_k^2)$$
  $w_k$: bileşen ağırlığı, $\mu_k$: ortalama, $\sigma_k$: standart sapma.

  MOG2 algoritması her piksel için $K=5$ Gaussian tutar ve zamanla günceller:
  $$\mu_k^{t+1} = (1-\rho)\mu_k^t + \rho x_t$$
  $$\sigma_k^{t+1} = (1-\rho)\sigma_k^t + \rho(x_t - \mu_k^t)^2$$
  $\rho$: öğrenme hızı. Düşük $\rho$ → yavaş adaptasyon, yüksek → gürültüye duyarlı.

  Referans: Zivkovic, "Improved Adaptive Gaussian Mixture Model for Background Subtraction", ICPR 2004
  ```

- [ ] **Step 3: Pratik kod ekle**

  ```python
  import cv2

  cap = cv2.VideoCapture("video.mp4")

  # MOG2 — Gaussian Mixture, gölge tespiti aktif
  mog2 = cv2.createBackgroundSubtractorMOG2(
      history=500, varThreshold=16, detectShadows=True
  )

  # KNN tabanlı arkaplan çıkarma
  knn = cv2.createBackgroundSubtractorKNN(
      history=500, dist2Threshold=400.0, detectShadows=True
  )

  while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
          break

      fg_mask = mog2.apply(frame)
      # 127: gölge pikselleri, 255: ön plan
      fg_only = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)[1]

      # Morfoloji ile gürültü temizleme
      kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
      clean  = cv2.morphologyEx(fg_only, cv2.MORPH_OPEN, kernel)

      cv2.imshow("Foreground", clean)
      if cv2.waitKey(30) & 0xFF == ord('q'):
          break

  cap.release()
  cv2.destroyAllWindows()
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/12-arka-plan-cikarma.md
  git commit -m "docs: revize ch12 - GMM istatistiksel model, MOG2/KNN pratik örnek"
  ```

---

## GRUP B — Orta Seviye Revizyon

---

### Task 7: Bölüm 13 — Video Analiz ve Nesne Takibi

**Files:**
- Modify: `docs/13-video-analiz.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: Optik Akış Denklemleri ekle**

  ```markdown
  ### Teorik Temel

  **Optik Akış Kısıtı (Brightness Constancy):**
  $$\frac{\partial I}{\partial x}u + \frac{\partial I}{\partial y}v + \frac{\partial I}{\partial t} = 0$$
  $I_x, I_y$: uzamsal gradyanlar, $I_t$: zamansal gradyan, $(u,v)$: akış vektörü.
  Bu denklem aperture problemi yaratır — tek denklem, iki bilinmeyen.

  **Lucas-Kanade Çözümü (Lokal Least Squares):**
  $$\begin{bmatrix} I_x^2 & I_xI_y \\ I_xI_y & I_y^2 \end{bmatrix} \begin{bmatrix} u \\ v \end{bmatrix} = -\begin{bmatrix} I_xI_t \\ I_yI_t \end{bmatrix}$$
  Pencere içindeki tüm piksellerin sabit akış paylaştığı varsayılır. $A^TA$ matrisi Harris köşe matrisiyle aynıdır.

  **Kalman Filtresi (Nesne Takibi):**
  Tahmin: $\hat{x}_k^- = F\hat{x}_{k-1}$, $P_k^- = FP_{k-1}F^T + Q$
  Güncelleme: $K_k = P_k^- H^T(HP_k^-H^T + R)^{-1}$
  $F$: durum geçiş matrisi, $H$: gözlem matrisi, $Q/R$: süreç/gözlem gürültüsü.

  Referans: Lucas & Kanade, "An Iterative Image Registration Technique", IJCAI 1981
  ```

- [ ] **Step 3: Pratik kod ekle**

  ```python
  import cv2
  import numpy as np

  cap = cv2.VideoCapture("video.mp4")
  ret, old_frame = cap.read()
  old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

  # Shi-Tomasi köşe noktaları
  feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
  p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

  lk_params = dict(winSize=(15,15), maxLevel=2,
                   criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

  mask = np.zeros_like(old_frame)

  while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
          break
      frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

      # Lucas-Kanade optik akış
      p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

      if p1 is not None:
          good_new = p1[st == 1]
          good_old = p0[st == 1]

          for (new, old) in zip(good_new, good_old):
              a, b = new.ravel().astype(int)
              c, d = old.ravel().astype(int)
              mask = cv2.line(mask, (a, b), (c, d), (0, 255, 0), 2)
              frame = cv2.circle(frame, (a, b), 5, (0, 0, 255), -1)

      output = cv2.add(frame, mask)
      cv2.imshow("Optik Akış", output)
      if cv2.waitKey(30) & 0xFF == ord('q'):
          break

      old_gray = frame_gray.copy()
      p0 = good_new.reshape(-1, 1, 2)

  cap.release()
  cv2.destroyAllWindows()
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/13-video-analiz.md
  git commit -m "docs: revize ch13 - optik akış denklemi, Lucas-Kanade, Kalman filtresi"
  ```

---

### Task 8: Bölüm 14 — Nesne Tespiti

**Files:**
- Modify: `docs/14-nesne-tespiti.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: YOLO Mimarisi ve Metrik Matematiği ekle**

  ```markdown
  ### Teorik Temel

  **YOLO Loss Fonksiyonu (YOLOv3):**
  $$\mathcal{L} = \lambda_{coord}\sum_{i}\sum_{j} \mathbb{1}_{ij}^{obj}[(x_i-\hat{x}_i)^2 + (y_i-\hat{y}_i)^2]$$
  $$+ \lambda_{coord}\sum_{i}\sum_{j} \mathbb{1}_{ij}^{obj}[(\sqrt{w_i}-\sqrt{\hat{w}_i})^2 + (\sqrt{h_i}-\sqrt{\hat{h}_i})^2]$$
  $$+ \sum_{i}\sum_{j} \mathbb{1}_{ij}^{obj}[(C_i-\hat{C}_i)^2] + \text{BCE}(p_i, \hat{p}_i)$$

  **IoU (Intersection over Union):**
  $$\text{IoU} = \frac{|A \cap B|}{|A \cup B|}$$
  Genellikle IoU > 0.5 "doğru tespit" sayılır. mAP@0.5:0.95 birden fazla eşikte ortalamasını alır.

  **Precision-Recall:**
  $$\text{Precision} = \frac{TP}{TP+FP}, \quad \text{Recall} = \frac{TP}{TP+FN}$$
  $$\text{AP} = \int_0^1 p(r)\,dr \approx \sum_{k} (r_{k+1}-r_k) \cdot p(r_{k+1})$$

  Referans: Redmon & Farhadi, "YOLOv3: An Incremental Improvement", 2018 (https://arxiv.org/abs/1804.02767)
  ```

- [ ] **Step 3: YOLOv8 pratik kod ekle**

  ```python
  from ultralytics import YOLO
  import cv2

  # YOLOv8 ile nesne tespiti
  model = YOLO("yolov8n.pt")  # nano, small, medium, large, xlarge

  # Tek görüntü üzerinde çıkarım
  results = model.predict("resim.jpg", conf=0.5, iou=0.45)
  for result in results:
      boxes = result.boxes
      for box in boxes:
          x1, y1, x2, y2 = box.xyxy[0].int().tolist()
          conf = float(box.conf[0])
          cls  = int(box.cls[0])
          name = model.names[cls]
          print(f"{name}: {conf:.2f} @ [{x1},{y1},{x2},{y2}]")

  # Gerçek zamanlı kamera
  cap = cv2.VideoCapture(0)
  while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
          break
      results = model.predict(frame, conf=0.5, verbose=False)
      annotated = results[0].plot()
      cv2.imshow("YOLOv8", annotated)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
  cap.release()
  cv2.destroyAllWindows()

  # Özel veri setiyle eğitim
  # model = YOLO("yolov8n.pt")
  # model.train(data="dataset.yaml", epochs=50, imgsz=640, batch=16)
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/14-nesne-tespiti.md
  git commit -m "docs: revize ch14 - YOLO loss/IoU/mAP matematiği, YOLOv8 Ultralytics API"
  ```

---

### Task 9: Bölüm 15 — Kamera Kalibrasyonu ve 3D Görü

**Files:**
- Modify: `docs/15-kamera-kalibrasyonu-ve-3d-goru.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: Pinhole Model ve Epipolar Geometri ekle**

  ```markdown
  ### Teorik Temel

  **Pinhole Kamera Modeli:**
  $$\begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \frac{1}{Z}\begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} X \\ Y \\ Z \end{bmatrix}$$
  $f_x, f_y$: odak uzunlukları (piksel cinsinden), $(c_x, c_y)$: görüntü merkezi, $(X,Y,Z)$: 3D dünya noktası.

  **Lens Bozulması:**
  $$x_d = x(1+k_1r^2+k_2r^4+k_3r^6), \quad r^2=x^2+y^2$$
  $k_1, k_2, k_3$: radyal bozulma katsayıları. Balık gözü lenste $k_1 < 0$ (yastık bozulması).

  **Epipolar Geometri:**
  Temel Matris $F$: $p'^T F p = 0$ — iki görüntü arasındaki nokta ilişkisi.
  Temel (Essential) Matris $E = K'^T F K$: kalibre edilmiş kameralar için.

  Referans: Hartley & Zisserman, "Multiple View Geometry" (https://www.robots.ox.ac.uk/~vgg/hzbook/)
  ```

- [ ] **Step 3: Kalibrasyon kodu ekle**

  ```python
  import cv2
  import numpy as np
  import glob

  # Satranç tahtası boyutu
  CHECKERBOARD = (9, 6)
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

  obj_points, img_points = [], []
  objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
  objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

  for fname in glob.glob("calibration_images/*.jpg"):
      img = cv2.imread(fname)
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
      if ret:
          obj_points.append(objp)
          corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
          img_points.append(corners2)

  ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
      obj_points, img_points, gray.shape[::-1], None, None
  )
  print(f"Kalibrasyon hatası (RMS): {ret:.4f}")
  print(f"Kamera matrisi K:\n{K}")
  print(f"Bozulma katsayıları: {dist}")

  # Görüntü düzeltme
  test_img = cv2.imread("test.jpg")
  h, w = test_img.shape[:2]
  new_K, roi = cv2.getOptimalNewCameraMatrix(K, dist, (w,h), 1, (w,h))
  undistorted = cv2.undistort(test_img, K, dist, None, new_K)
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/15-kamera-kalibrasyonu-ve-3d-goru.md
  git commit -m "docs: revize ch15 - pinhole model, epipolar geometri, kalibrasyon kodu"
  ```

---

### Task 10: Bölüm 17 — Yüz Tanıma

**Files:**
- Modify: `docs/17-yuz-tanima.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: PCA/LDA ve Triplet Loss ekle**

  ```markdown
  ### Teorik Temel

  **PCA (Eigenfaces) — Kovaryans Matrisi:**
  $$\Sigma = \frac{1}{N}\sum_{i=1}^N (x_i - \mu)(x_i - \mu)^T$$
  Özdeğer ayrışımı: $\Sigma v_k = \lambda_k v_k$. En büyük $k$ özdeğere ait özvektörler "eigenfaces".

  **FaceNet Triplet Loss:**
  $$\mathcal{L} = \sum_{i} [\|f(x_i^a) - f(x_i^p)\|_2^2 - \|f(x_i^a) - f(x_i^n)\|_2^2 + \alpha]_+$$
  $x^a$: anchor (referans yüz), $x^p$: positive (aynı kişi), $x^n$: negative (farklı kişi), $\alpha$: margin.
  Amaç: aynı kişi embedding'lerini yaklaştır, farklıları uzaklaştır.

  **ArcFace Margin:**
  $$\mathcal{L} = -\log \frac{e^{s(\cos(\theta_{y_i}+m))}}{e^{s(\cos(\theta_{y_i}+m))} + \sum_{j\neq y_i}e^{s\cos\theta_j}}$$
  Açısal margin $m$ ekleyerek sınıflar arası ayrımı artırır.

  Referans: Schroff et al., "FaceNet", CVPR 2015 (https://arxiv.org/abs/1503.03832)
  Referans: Deng et al., "ArcFace", CVPR 2019 (https://arxiv.org/abs/1801.07698)
  ```

- [ ] **Step 3: DeepFace pratik kod ekle**

  ```python
  from deepface import DeepFace
  import cv2

  # Yüz doğrulama (verification)
  result = DeepFace.verify(
      img1_path="kisi1.jpg",
      img2_path="kisi2.jpg",
      model_name="ArcFace",      # FaceNet, VGG-Face, ArcFace, Facenet512
      detector_backend="retinaface"
  )
  print(f"Aynı kişi mi: {result['verified']}, Mesafe: {result['distance']:.4f}")

  # Yüz tanıma — veritabanında ara
  dfs = DeepFace.find(
      img_path="sorgu.jpg",
      db_path="yuzler_klasoru/",
      model_name="ArcFace",
      distance_metric="cosine"
  )
  print(dfs[0][["identity", "distance"]].head())

  # Yüz analizi (yaş, cinsiyet, duygu, ırk)
  analysis = DeepFace.analyze(
      img_path="resim.jpg",
      actions=["age", "gender", "emotion"]
  )
  print(f"Yaş: {analysis[0]['age']}, Cinsiyet: {analysis[0]['gender']}")
  print(f"Duygu: {analysis[0]['dominant_emotion']}")
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/17-yuz-tanima.md
  git commit -m "docs: revize ch17 - PCA/triplet loss/ArcFace matematiği, DeepFace API"
  ```

---

### Task 11: Bölüm 18 — Optik Karakter Tanıma

**Files:**
- Modify: `docs/18-optik-karakter-tanima.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: CTC Loss ve Attention ekle**

  ```markdown
  ### Teorik Temel

  **CTC (Connectionist Temporal Classification) Loss:**
  Değişken uzunluklu çıktı dizilerini etiketlemek için. Tüm olası hizalamaların toplamı:
  $$p(l|x) = \sum_{\pi \in \mathcal{B}^{-1}(l)} p(\pi|x), \quad p(\pi|x) = \prod_{t=1}^T p(\pi_t|x)$$
  $\mathcal{B}$: blank sembolü kaldırma ve tekrar azaltma operatörü.
  Avantaj: hizalama etiketi gerektirmez, sadece metin etiketi yeterli.

  **CRNN Mimarisi (CNN + RNN + CTC):**
  1. CNN: görüntü öznitelikleri çıkar → özellik haritası
  2. Sütun bazlı özellik vektörleri → sekans
  3. Bidirectional LSTM: bağlamsal kodlama
  4. CTC: karakter olasılıkları → metin

  Referans: Shi et al., "An End-to-End Trainable Neural Network for Image-based Sequence Recognition", IEEE TPAMI 2017 (https://arxiv.org/abs/1507.05717)
  ```

- [ ] **Step 3: EasyOCR ve PaddleOCR kod ekle**

  ```python
  import easyocr
  import cv2

  # EasyOCR — Türkçe dahil 80+ dil
  reader = easyocr.Reader(["tr", "en"], gpu=False)
  results = reader.readtext("belge.jpg")

  for (bbox, text, confidence) in results:
      print(f"Metin: {text!r}, Güven: {confidence:.2f}")
      # Bounding box çiz
      pts = [(int(p[0]), int(p[1])) for p in bbox]
      img = cv2.imread("belge.jpg")
      cv2.polylines(img, [np.array(pts)], True, (0,255,0), 2)

  # Tesseract ile Türkçe OCR
  import pytesseract
  from PIL import Image

  img_pil = Image.open("belge.jpg")
  text = pytesseract.image_to_string(img_pil, lang="tur")
  print(text)

  # Tesseract bounding box
  data = pytesseract.image_to_data(img_pil, lang="tur",
                                    output_type=pytesseract.Output.DICT)
  for i, word in enumerate(data["text"]):
      if word.strip() and int(data["conf"][i]) > 60:
          x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
          print(f"{word}: güven={data['conf'][i]}")
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/18-optik-karakter-tanima.md
  git commit -m "docs: revize ch18 - CTC loss matematiği, CRNN mimarisi, EasyOCR/Tesseract"
  ```

---

## GRUP C — İleri Seviye Revizyon

---

### Task 12: Bölüm 1 — OpenCV Nedir

**Files:**
- Modify: `docs/1-opencv-nedir.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: OpenCV 5.0 ekosistem haritası ve alternatif karşılaştırması ekle**

  ```markdown
  ### OpenCV Ekosistemi (2024+)

  **Sürüm Durumu:**
  - OpenCV 4.9.x: Kararlı, aktif destek
  - OpenCV 5.0 beta: C++20, yeniden yazılmış Python binding'leri, gelişmiş DNN

  **Alternatif Kütüphane Karşılaştırması:**

  | Kütüphane | Dil | Güçlü Yön | Zayıf Yön |
  |-----------|-----|-----------|-----------|
  | OpenCV | C++/Python/Java | Kapsamlı, hızlı, üretim-ready | Deep learning yetersiz |
  | scikit-image | Python | Akademik, saf Python | Yavaş, real-time zor |
  | PIL/Pillow | Python | Basit görüntü I/O | Görüntü işleme sınırlı |
  | PyTorch/torchvision | Python | Modern DL, GPU | OpenCV gibi klasik CV yok |
  | SimpleCV | Python | Kolay API | Eski, bakımsız |

  **OpenCV Modülleri (temel):**
  - `core`: Mat, temel matematiksel operasyonlar
  - `imgproc`: görüntü işleme (filtreler, geometrik dönüşümler)
  - `dnn`: derin öğrenme çıkarımı (ONNX, TensorFlow, Caffe)
  - `video`: video analiz, optik akış
  - `calib3d`: kamera kalibrasyonu, 3D görü
  - `features2d`: SIFT, ORB, AKAZE
  - `cuda`: GPU hızlandırma

  Referans: Bradski & Kaehler, "Learning OpenCV 3" (O'Reilly)
  OpenCV resmi dok: https://docs.opencv.org/4.x/
  ```

- [ ] **Step 3: Commit**

  ```bash
  git add docs/1-opencv-nedir.md
  git commit -m "docs: revize ch1 - OpenCV 5.0 ekosistem haritası, kütüphane karşılaştırması"
  ```

---

### Task 13: Bölüm 19 — Öznitelik Çıkarımı

**Files:**
- Modify: `docs/19-oznitelik-cikarimi.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: SIFT Matematiksel Türetim ekle**

  ```markdown
  ### Teorik Temel

  **Scale-Space Extrema (SIFT):**
  $$L(x,y,\sigma) = G(x,y,\sigma) * I(x,y)$$
  $$D(x,y,\sigma) = L(x,y,k\sigma) - L(x,y,\sigma)$$
  DoG (Difference of Gaussians) ile scale-space anahtar noktaları bulunur. $k=\sqrt{2}$.

  **Keypoint Yönelimi:**
  Her anahtar nokta çevresinde gradyan histogramı hesaplanır:
  $$m(x,y) = \sqrt{(L_{x+1}-L_{x-1})^2 + (L_{y+1}-L_{y-1})^2}$$
  $$\theta(x,y) = \arctan\left(\frac{L_{y+1}-L_{y-1}}{L_{x+1}-L_{x-1}}\right)$$
  En yüksek histogram zirvesi yönelim olarak atanır → rotasyon değişmezliği.

  **128-boyutlu Descriptor:**
  16×16 pencere → 4×4 alt bölge × 8 yön histogramı = 128 boyut. L2 normalize edilir.

  **RANSAC (Hatalı Eşleşme Eleme):**
  $n$ iterasyon boyunca rastgele 4 nokta seçilir, homografi hesaplanır, inlier sayılır. En fazla inlier veren model döndürülür.

  Referans: Lowe, "Distinctive Image Features from Scale-Invariant Keypoints", IJCV 2004 (https://doi.org/10.1023/B:VISI.0000029664.99615.94)
  ```

- [ ] **Step 3: SIFT/ORB/FLANN kod ekle**

  ```python
  import cv2
  import numpy as np

  img1 = cv2.imread("sorgu.jpg", cv2.IMREAD_GRAYSCALE)
  img2 = cv2.imread("sahne.jpg", cv2.IMREAD_GRAYSCALE)

  # SIFT öznitelik çıkarımı
  sift = cv2.SIFT_create()
  kp1, des1 = sift.detectAndCompute(img1, None)
  kp2, des2 = sift.detectAndCompute(img2, None)

  # FLANN eşleştirme
  FLANN_INDEX_KDTREE = 1
  index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
  search_params = dict(checks=50)
  flann = cv2.FlannBasedMatcher(index_params, search_params)
  matches = flann.knnMatch(des1, des2, k=2)

  # Lowe'un oran testi (ratio test)
  good = [m for m, n in matches if m.distance < 0.7 * n.distance]
  print(f"İyi eşleşme: {len(good)}/{len(matches)}")

  # Homografi hesaplama (4+ iyi eşleşme gerekir)
  if len(good) >= 4:
      src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
      dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)
      H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
      inliers = mask.sum()
      print(f"RANSAC inlier: {inliers}/{len(good)}")

  # ORB (patent-free, hızlı alternatif)
  orb = cv2.ORB_create(nfeatures=500)
  kp1_orb, des1_orb = orb.detectAndCompute(img1, None)
  kp2_orb, des2_orb = orb.detectAndCompute(img2, None)
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
  matches_orb = sorted(bf.match(des1_orb, des2_orb), key=lambda x: x.distance)
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/19-oznitelik-cikarimi.md
  git commit -m "docs: revize ch19 - SIFT matematiksel türetim, RANSAC, FLANN eşleştirme"
  ```

---

### Task 14: Bölüm 21 — Poz Tahmini

**Files:**
- Modify: `docs/21-poz-tahmini.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: PAF ve OKS Matematiği ekle**

  ```markdown
  ### Teorik Temel

  **Keypoint Heatmap (Isı Haritası):**
  Her keypoint $k$ için Gaussian heatmap: $S_k(p) = \exp\left(-\frac{\|p - p_k^*\|_2^2}{2\sigma^2}\right)$
  $p_k^*$: gerçek keypoint konumu, $\sigma$: yayılım parametresi.

  **Part Affinity Fields (PAF — OpenPose):**
  İki keypoint arasındaki bağlantı vektör alanıyla temsil edilir:
  $$L_c(p) = \begin{cases} v & \text{if } p \text{ limb üzerinde} \\ 0 & \text{otherwise} \end{cases}$$
  $v$: limb yönünde birim vektör. Bu alan, hangi kollerin aynı kişiye ait olduğunu belirler.

  **OKS (Object Keypoint Similarity) — COCO Metriği:**
  $$\text{OKS} = \frac{\sum_i \exp\left(-d_i^2 / 2s^2\sigma_i^2\right) \cdot \delta(v_i > 0)}{\sum_i \delta(v_i > 0)}$$
  $d_i$: tahmin/gerçek mesafesi, $s$: nesne ölçeği, $\sigma_i$: keypoint tipine özgü sabit.

  Referans: Cao et al., "OpenPose: Realtime Multi-Person 2D Pose Estimation", IEEE TPAMI 2021 (https://arxiv.org/abs/1812.08008)
  ```

- [ ] **Step 3: MediaPipe Pose kod ekle**

  ```python
  import cv2
  import mediapipe as mp

  mp_pose = mp.solutions.pose
  mp_drawing = mp.solutions.drawing_utils

  cap = cv2.VideoCapture(0)

  with mp_pose.Pose(
      static_image_mode=False,
      model_complexity=1,          # 0=lite, 1=full, 2=heavy
      smooth_landmarks=True,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5
  ) as pose:

      while cap.isOpened():
          ret, frame = cap.read()
          if not ret:
              break

          rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          results = pose.process(rgb)

          if results.pose_landmarks:
              mp_drawing.draw_landmarks(
                  frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
              )

              # Dirsek açısı hesaplama (landmark indeksleri: 11=omuz, 13=dirsek, 15=bilek)
              lms = results.pose_landmarks.landmark
              shoulder = np.array([lms[11].x, lms[11].y])
              elbow    = np.array([lms[13].x, lms[13].y])
              wrist    = np.array([lms[15].x, lms[15].y])

              v1 = shoulder - elbow
              v2 = wrist - elbow
              cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
              angle = np.degrees(np.arccos(np.clip(cos_angle, -1, 1)))
              cv2.putText(frame, f"Dirsek: {angle:.1f}°", (50,50),
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

          cv2.imshow("Poz Tahmini", frame)
          if cv2.waitKey(1) & 0xFF == ord('q'):
              break

  cap.release()
  cv2.destroyAllWindows()
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/21-poz-tahmini.md
  git commit -m "docs: revize ch21 - PAF/OKS matematiği, MediaPipe açı hesaplama"
  ```

---

### Task 15: Bölüm 22 — Segmentasyon

**Files:**
- Modify: `docs/22-segmentasyon.md`

- [ ] **Step 1: Mevcut dosyayı oku**

- [ ] **Step 2: Mask R-CNN ve SAM Mimarisi ekle**

  ```markdown
  ### Teorik Temel

  **Semantic vs Instance Segmentation:**
  - Semantic: her piksel → sınıf etiketi (aynı sınıf tüm nesneler aynı renk)
  - Instance: her nesne örneği ayrı maske (aynı sınıftan 3 araba → 3 farklı maske)
  - Panoptic: ikisinin birleşimi (stuff + things)

  **Mask R-CNN:**
  Faster R-CNN + paralel maske dalı. ROI Align (piksel hizalaması ile):
  $$\text{ROIAlign}: \text{sürekli koordinat örnekleme (bilineer interpolasyon)}$$
  Her ROI için $28\times28$ ikili maske tahmini → orijinal boyuta upscale.

  **IoU (Segmentation):**
  $$\text{mIoU} = \frac{1}{C}\sum_{c=1}^C \frac{TP_c}{TP_c + FP_c + FN_c}$$
  $C$: sınıf sayısı. COCO değerlendirmesinde 0.5:0.05:0.95 eşiklerinde ortalama alınır.

  **SAM (Segment Anything Model):**
  3 bileşen: Image Encoder (ViT-H), Prompt Encoder (nokta/kutu/maske), Mask Decoder (2-katman transformer).
  Zero-shot: eğitim görmediği nesneleri de segmente eder.

  Referans: He et al., "Mask R-CNN", ICCV 2017 (https://arxiv.org/abs/1703.06870)
  Referans: Kirillov et al., "Segment Anything", ICCV 2023 (https://arxiv.org/abs/2304.02643)
  ```

- [ ] **Step 3: YOLOv8-seg kod ekle**

  ```python
  from ultralytics import YOLO
  import cv2
  import numpy as np

  model = YOLO("yolov8n-seg.pt")

  results = model.predict("resim.jpg", conf=0.5)
  result = results[0]

  img = cv2.imread("resim.jpg")

  if result.masks is not None:
      masks = result.masks.data.cpu().numpy()   # (N, H, W)
      classes = result.boxes.cls.cpu().numpy()

      for i, (mask, cls) in enumerate(zip(masks, classes)):
          mask_resized = cv2.resize(mask, (img.shape[1], img.shape[0]))
          mask_bool = mask_resized > 0.5

          # Rastgele renk ata
          color = np.random.randint(0, 255, 3).tolist()
          img[mask_bool] = img[mask_bool] * 0.5 + np.array(color) * 0.5

          # Kontur çiz
          contours, _ = cv2.findContours(
              mask_resized.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
          )
          cv2.drawContours(img, contours, -1, color, 2)

  cv2.imshow("Segmentasyon", img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/22-segmentasyon.md
  git commit -m "docs: revize ch22 - Mask R-CNN/SAM mimarisi, mIoU, YOLOv8-seg"
  ```

---

## GRUP D — Yeni Bölümler

---

### Task 16: Bölüm 26 — Vision Transformers

**Files:**
- Create: `docs/26-vision-transformers.md`

- [ ] **Step 1: Dosyayı oluştur, şablon başlığı yaz**

  ```markdown
  # Vision Transformers (ViT, DETR, Swin Transformer)

  Vision Transformer'lar (ViT), 2020 yılında görüntü sınıflandırma görevlerine transformer mimarisinin uygulanmasıyla ortaya çıktı ve kısa sürede bilgisayarlı görünün baskın paradigması haline geldi. Bu bölümde teorik temellerden pratik uygulamalara kadar ViT ekosistemini inceleyeceğiz.
  ```

- [ ] **Step 2: Teorik Temel yaz**

  ```markdown
  ### Teorik Temel

  **Patch Embedding:**
  Görüntü $H \times W \times C$ boyutunda. $P \times P$ patch'lere bölünür:
  $$N = \frac{HW}{P^2} \quad \text{(patch sayısı)}$$
  Her patch düzleştirilir ve lineer projeksiyon ile $D$ boyutlu embedding'e dönüştürülür:
  $$z_0 = [x_{cls}; x_p^1 E; x_p^2 E; \ldots; x_p^N E] + E_{pos}$$
  $E \in \mathbb{R}^{(P^2 \cdot C) \times D}$: embedding matrisi, $E_{pos}$: pozisyon kodlaması.

  **Multi-Head Self-Attention (MHSA):**
  $$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
  $Q = XW_Q$, $K = XW_K$, $V = XW_V$. $d_k = D/h$ — $h$ kafa sayısı.
  $$\text{MHSA}(X) = \text{concat}(\text{head}_1, \ldots, \text{head}_h)W_O$$
  Her kafa farklı dikkat pattern'i öğrenir. Karmaşıklık: $O(N^2 D)$ — büyük görüntülerde yavaş.

  **Swin Transformer — Shifted Window Attention:**
  Global self-attention yerine lokal pencere içinde dikkat. Karmaşıklık: $O(N \cdot w^2 D)$ — doğrusal ölçekleme.
  Shifted window ile pencereler arası bilgi akışı sağlanır.

  **DETR (Detection Transformer):**
  CNN backbone + Transformer encoder-decoder + bipartite matching loss.
  NMS (Non-Maximum Suppression) yerine set prediction: Macar algoritması ile optimal atama.

  Referans: Dosovitskiy et al., "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale", ICLR 2021 (https://arxiv.org/abs/2010.11929)
  Referans: Liu et al., "Swin Transformer", ICCV 2021 (https://arxiv.org/abs/2103.14030)
  Referans: Carion et al., "DETR", ECCV 2020 (https://arxiv.org/abs/2005.12872)
  ```

- [ ] **Step 3: Pratik Uygulama yaz**

  ```python
  import torch
  from transformers import ViTForImageClassification, ViTImageProcessor
  from PIL import Image

  # HuggingFace ViT ile görüntü sınıflandırma
  processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
  model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")
  model.eval()

  img = Image.open("resim.jpg").convert("RGB")
  inputs = processor(images=img, return_tensors="pt")

  with torch.no_grad():
      outputs = model(**inputs)
      logits = outputs.logits

  predicted_class = logits.argmax(-1).item()
  print(f"Tahmin: {model.config.id2label[predicted_class]}")

  # Swin Transformer ile transfer learning
  from transformers import SwinForImageClassification

  swin = SwinForImageClassification.from_pretrained(
      "microsoft/swin-tiny-patch4-window7-224",
      num_labels=10,          # özel sınıf sayısı
      ignore_mismatched_sizes=True
  )

  # Attention haritası görselleştirme
  from transformers import ViTModel
  vit = ViTModel.from_pretrained("google/vit-base-patch16-224", output_attentions=True)
  with torch.no_grad():
      outputs = vit(**inputs)

  # Son katman dikkat ağırlıkları: (batch, heads, patches+1, patches+1)
  attentions = outputs.attentions[-1]
  cls_attention = attentions[0, :, 0, 1:].mean(0)  # CLS token → tüm patch'ler
  print(f"Dikkat haritası shape: {cls_attention.shape}")
  ```

- [ ] **Step 4: Özet & Commit**

  ```markdown
  ### Özet & İleri Okuma
  - ViT, görüntüyü 16×16 patch'lere bölerek NLP transformer'ı görüntüye uyarlar
  - Self-attention mekanizması global bağlam yakalar; CNN'nin lokal yapısından farklı
  - Swin Transformer pencere tabanlı dikkatle doğrusal ölçekleme sağlar
  - DETR, object detection'ı set prediction problemine dönüştürür; NMS gerektirmez
  - ViT büyük veri setiyle pre-training gerektirir; küçük veri için Swin daha iyi
  - HuggingFace `transformers` kütüphanesi ViT/Swin/DETR modellerini hazır sunar

  **İleri Okuma:**
  - https://arxiv.org/abs/2010.11929 (ViT)
  - https://arxiv.org/abs/2103.14030 (Swin)
  - https://huggingface.co/docs/transformers/model_doc/vit
  ```

  ```bash
  git add docs/26-vision-transformers.md
  git commit -m "docs: add ch26 - vision transformers (ViT/Swin/DETR) teori ve kod"
  ```

---

### Task 17: Bölüm 27 — Generatif Modeller ve Diffusion

**Files:**
- Create: `docs/27-generatif-modeller.md`

- [ ] **Step 1: Dosyayı oluştur**

- [ ] **Step 2: Teorik Temel yaz**

  ```markdown
  # Generatif Modeller ve Diffusion

  ### Teorik Temel

  **GAN (Generative Adversarial Network):**
  Generator $G$ ve Discriminator $D$ minimax oyunu:
  $$\min_G \max_D \mathbb{E}_{x\sim p_{data}}[\log D(x)] + \mathbb{E}_{z\sim p_z}[\log(1-D(G(z)))]$$
  $G$: gürültüden gerçekçi görüntü üretir. $D$: gerçek/sahte ayırt eder. Nash dengesinde $D(x)=0.5$.
  Sorunlar: mode collapse, eğitim kararsızlığı.

  **VAE (Variational Autoencoder):**
  ELBO (Evidence Lower Bound) maksimize edilir:
  $$\mathcal{L}_{ELBO} = \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{KL}(q_\phi(z|x) \| p(z))$$
  Reparameterization trick: $z = \mu + \sigma \cdot \epsilon$, $\epsilon \sim \mathcal{N}(0,I)$ — gradyan akışını sağlar.

  **DDPM (Denoising Diffusion Probabilistic Models):**
  Forward süreç: $q(x_t|x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t}x_{t-1}, \beta_t I)$
  $T$ adımda görüntüye gürültü eklenir. Reverse süreç: $p_\theta(x_{t-1}|x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t,t), \Sigma_\theta)$
  Model $\epsilon_\theta(x_t, t)$ ile eklenen gürülüyü tahmin eder:
  $$\mathcal{L}_{simple} = \mathbb{E}_{t,x_0,\epsilon}\left[\|\epsilon - \epsilon_\theta(\sqrt{\bar\alpha_t}x_0 + \sqrt{1-\bar\alpha_t}\epsilon, t)\|^2\right]$$

  **Stable Diffusion Mimarisi:**
  Latent Diffusion Model: piksel uzayı yerine VAE encoder'ın latent uzayında diffusion.
  - VAE Encoder: $x \rightarrow z$ (görüntü → latent, 8× sıkıştırma)
  - U-Net Denoiser: $\epsilon_\theta(z_t, t, c)$ — $c$: text conditioning (CLIP embedding)
  - VAE Decoder: $z \rightarrow x$ (latent → görüntü)

  Referans: Ho et al., "Denoising Diffusion Probabilistic Models", NeurIPS 2020 (https://arxiv.org/abs/2006.11239)
  Referans: Rombach et al., "High-Resolution Image Synthesis with Latent Diffusion Models", CVPR 2022 (https://arxiv.org/abs/2112.10752)
  ```

- [ ] **Step 3: Pratik kod yaz**

  ```python
  # Stable Diffusion ile görüntü üretimi (diffusers kütüphanesi)
  from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
  import torch

  model_id = "runwayml/stable-diffusion-v1-5"
  pipe = StableDiffusionPipeline.from_pretrained(
      model_id,
      torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
  )
  pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
  pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

  # Metin → görüntü
  prompt = "a photorealistic cat sitting on a wooden table, natural lighting"
  negative_prompt = "blurry, low quality, cartoon"

  image = pipe(
      prompt,
      negative_prompt=negative_prompt,
      num_inference_steps=20,   # DPMSolver ile 20 adım yeterli
      guidance_scale=7.5,       # CFG scale: prompt'a bağlılık
      height=512, width=512
  ).images[0]

  image.save("uretilen.png")

  # ControlNet — kenara göre görüntü üretimi
  from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
  import cv2
  import numpy as np
  from PIL import Image

  controlnet = ControlNetModel.from_pretrained(
      "lllyasviel/sd-controlnet-canny", torch_dtype=torch.float16
  )
  pipe_cn = StableDiffusionControlNetPipeline.from_pretrained(
      "runwayml/stable-diffusion-v1-5",
      controlnet=controlnet,
      torch_dtype=torch.float16
  ).to("cuda")

  # Kaynak görüntüden Canny kenarları çıkar
  src = cv2.imread("kaynak.jpg")
  gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
  edges = cv2.Canny(gray, 100, 200)
  control_image = Image.fromarray(edges).convert("RGB")

  result = pipe_cn(
      "a beautiful landscape painting",
      image=control_image,
      num_inference_steps=20
  ).images[0]
  result.save("controlnet_sonuc.png")
  ```

- [ ] **Step 4: Özet & Commit**

  ```markdown
  ### Özet & İleri Okuma
  - GAN generator/discriminator minimax oyunuyla çalışır; mode collapse riski taşır
  - VAE latent uzayda sürekli dağılım öğrenir; reparameterization trick kritiktir
  - Diffusion modeller forward gürültü ekleme → reverse gürültü kaldırma prensibini izler
  - Stable Diffusion latent uzayda çalışarak hesaplama verimliliği sağlar
  - ControlNet yapısal koşullama (kenar, derinlik, iskelet) ile üretimi yönlendirir
  - Guidance scale arttıkça prompt'a bağlılık artar, çeşitlilik azalır

  **İleri Okuma:**
  - https://arxiv.org/abs/2006.11239 (DDPM)
  - https://arxiv.org/abs/2112.10752 (LDM/Stable Diffusion)
  - https://huggingface.co/docs/diffusers
  ```

  ```bash
  git add docs/27-generatif-modeller.md
  git commit -m "docs: add ch27 - GAN/VAE/Diffusion teori, Stable Diffusion/ControlNet kod"
  ```

---

### Task 18: Bölüm 28 — 3D Vision

**Files:**
- Create: `docs/28-3d-vision.md`

- [ ] **Step 1: Dosyayı oluştur**

- [ ] **Step 2: Teorik Temel yaz**

  ```markdown
  # 3D Vision: Nokta Bulutu, NeRF ve Derinlik Tahmini

  ### Teorik Temel

  **Nokta Bulutu (Point Cloud):**
  $N$ adet 3D nokta kümesi: $\mathcal{P} = \{(x_i, y_i, z_i)\}_{i=1}^N$
  Optik olarak düzensiz (unordered) — permutation invariant olmalı.

  **PointNet:**
  Her nokta bağımsız işlenir: $f(\{x_1,...,x_N\}) \approx g(h(x_1),...,h(x_N))$
  $g$: max-pooling (permutation invariant global öznitelik). $h$: shared MLP.

  **Monoküler Derinlik Tahmini:**
  Tek kameradan $d: \mathbb{R}^{H\times W} \rightarrow \mathbb{R}^{H\times W}$ tahmin.
  Scale-ambiguity problemi: mutlak ölçek bilinmez, yalnızca göreli derinlik.

  **NeRF (Neural Radiance Field):**
  Sahne sürekli bir fonksiyon olarak temsil edilir:
  $$F_\theta: (\mathbf{x}, \mathbf{d}) \rightarrow (\mathbf{c}, \sigma)$$
  $\mathbf{x}=(x,y,z)$: 3D konum, $\mathbf{d}=(\theta,\phi)$: görüş yönü,
  $\mathbf{c}=(r,g,b)$: renk, $\sigma$: yoğunluk (density).

  Volume rendering ile piksel rengi:
  $$C(\mathbf{r}) = \int_{t_n}^{t_f} T(t)\sigma(\mathbf{r}(t))\mathbf{c}(\mathbf{r}(t),\mathbf{d})\,dt$$
  $T(t) = \exp\left(-\int_{t_n}^t \sigma(\mathbf{r}(s))\,ds\right)$: transmittance.

  Referans: Qi et al., "PointNet", CVPR 2017 (https://arxiv.org/abs/1612.00593)
  Referans: Mildenhall et al., "NeRF", ECCV 2020 (https://arxiv.org/abs/2003.08934)
  ```

- [ ] **Step 3: Derinlik tahmini kod yaz**

  ```python
  import torch
  import cv2
  import numpy as np
  from transformers import DPTForDepthEstimation, DPTImageProcessor

  # DPT (Dense Prediction Transformer) ile monoküler derinlik tahmini
  processor = DPTImageProcessor.from_pretrained("Intel/dpt-large")
  model = DPTForDepthEstimation.from_pretrained("Intel/dpt-large")
  model.eval()

  img = cv2.imread("resim.jpg")
  rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  from PIL import Image
  pil_img = Image.fromarray(rgb)
  inputs = processor(images=pil_img, return_tensors="pt")

  with torch.no_grad():
      outputs = model(**inputs)
      depth = outputs.predicted_depth  # (1, H, W)

  depth_np = depth.squeeze().numpy()
  depth_norm = cv2.normalize(depth_np, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
  depth_color = cv2.applyColorMap(depth_norm, cv2.COLORMAP_MAGMA)

  cv2.imshow("Derinlik Haritası", depth_color)
  cv2.waitKey(0)

  # Open3D ile nokta bulutu oluşturma
  try:
      import open3d as o3d
      depth_image = o3d.geometry.Image(depth_norm)
      color_image = o3d.geometry.Image(rgb)
      rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
          color_image, depth_image, depth_scale=1000.0
      )
      # Kamera intrinsic (örnek değerler — kalibrasyondan alınmalı)
      intrinsic = o3d.camera.PinholeCameraIntrinsic(
          width=img.shape[1], height=img.shape[0],
          fx=525.0, fy=525.0,
          cx=img.shape[1]/2, cy=img.shape[0]/2
      )
      pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, intrinsic)
      o3d.visualization.draw_geometries([pcd])
  except ImportError:
      print("open3d kurulu değil: pip install open3d")
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/28-3d-vision.md
  git commit -m "docs: add ch28 - PointNet/NeRF teorisi, DPT derinlik tahmini, Open3D"
  ```

---

### Task 19: Bölüm 29 — Video Sınıflandırma

**Files:**
- Create: `docs/29-video-siniflandirma.md`

- [ ] **Step 1: Dosyayı oluştur**

- [ ] **Step 2: Teorik Temel yaz**

  ```markdown
  # Video Anlama ve Eylem Tanıma

  ### Teorik Temel

  **Two-Stream Architecture:**
  Spatial stream: RGB kareler → CNN (görünüş)
  Temporal stream: optik akış → CNN (hareket)
  Sonuç: iki stream'in softmax skorlarının ortalama füzyonu.

  **3D Konvolüsyon (C3D/I3D):**
  2D konvolüsyon yerine $k\times k\times k$ 3D çekirdek: uzamsal + zamansal birlikte.
  $$\text{out}(t,x,y) = \sum_{\tau}\sum_{i}\sum_j \text{in}(t-\tau, x-i, y-j) \cdot W(\tau,i,j)$$
  I3D: 2D ImageNet ağırlıklarını 3D'ye "inflate" ederek başlatır.

  **SlowFast Network:**
  Slow pathway: düşük FPS, yüksek kanal sayısı (görünüş)
  Fast pathway: yüksek FPS, düşük kanal sayısı (hareket)
  Lateral bağlantılar iki pathway'i birleştirir.

  **VideoMAE (Masked Autoencoder):**
  Rastgele tube maskeleme (uzamsal-zamansal): video voxel'larının %90'ı maskelenir.
  Encoder maskelenmemiş patch'leri, decoder tüm video'yu reconstruct eder.
  Self-supervised pre-training → fine-tuning ile yüksek doğruluk.

  Referans: Feichtenhofer et al., "SlowFast Networks for Video Recognition", ICCV 2019 (https://arxiv.org/abs/1812.03982)
  Referans: Tong et al., "VideoMAE", NeurIPS 2022 (https://arxiv.org/abs/2203.12602)
  ```

- [ ] **Step 3: Pratik kod yaz**

  ```python
  import cv2
  import torch
  import numpy as np
  from transformers import VideoMAEForVideoClassification, VideoMAEImageProcessor

  # VideoMAE ile eylem tanıma
  processor = VideoMAEImageProcessor.from_pretrained("MCG-NJU/videomae-base-finetuned-kinetics")
  model = VideoMAEForVideoClassification.from_pretrained("MCG-NJU/videomae-base-finetuned-kinetics")
  model.eval()

  def load_video_frames(path, num_frames=16, target_size=(224, 224)):
      cap = cv2.VideoCapture(path)
      total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
      indices = np.linspace(0, total - 1, num_frames, dtype=int)
      frames = []
      for idx in indices:
          cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
          ret, frame = cap.read()
          if ret:
              frame = cv2.resize(frame, target_size)
              frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
              frames.append(frame)
      cap.release()
      return frames  # list of (H, W, 3) numpy arrays

  frames = load_video_frames("video.mp4", num_frames=16)

  inputs = processor(frames, return_tensors="pt")
  with torch.no_grad():
      outputs = model(**inputs)
      logits = outputs.logits

  predicted_label = logits.argmax(-1).item()
  print(f"Tahmin edilen eylem: {model.config.id2label[predicted_label]}")

  top5 = torch.topk(logits, 5)
  for score, idx in zip(top5.values[0], top5.indices[0]):
      label = model.config.id2label[idx.item()]
      print(f"  {label}: {score.item():.3f}")
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/29-video-siniflandirma.md
  git commit -m "docs: add ch29 - SlowFast/VideoMAE teorisi, eylem tanıma kod örneği"
  ```

---

### Task 20: Bölüm 30 — Model Eğitimi ve Değerlendirme

**Files:**
- Create: `docs/30-model-egitimi-ve-degerlendirme.md`

- [ ] **Step 1: Dosyayı oluştur**

- [ ] **Step 2: Teorik Temel yaz**

  ```markdown
  # Model Eğitimi, Augmentation ve Değerlendirme

  ### Teorik Temel

  **Transfer Learning:**
  ImageNet pre-trained model $\theta^*$ → hedef görev fine-tuning.
  Feature extraction: backbone dondurulur, yalnızca classifier katmanı eğitilir.
  Fine-tuning: tüm ağ veya son katmanlar düşük learning rate ile eğitilir.

  **Veri Artırma (Augmentation):**
  Eğitim dağılımını genişletir → overfitting azalır. Geometrik:
  $$x_{aug} = T(x), \quad T \in \{\text{flip, rotate, crop, scale, shear}\}$$
  Fotometrik: parlaklık, kontrast, doygunluk, gürültü.
  Mixup: $\tilde{x} = \lambda x_i + (1-\lambda)x_j$, $\tilde{y} = \lambda y_i + (1-\lambda)y_j$, $\lambda \sim \text{Beta}(\alpha,\alpha)$

  **Confusion Matrix ve Metrikler:**
  $$\text{Precision} = \frac{TP}{TP+FP}, \quad \text{Recall} = \frac{TP}{TP+FN}, \quad F_1 = \frac{2 \cdot P \cdot R}{P+R}$$
  Çok sınıflı: macro average (sınıf ağırlıksız) vs micro average (örnek ağırlıklı).

  **Learning Rate Schedule:**
  Cosine annealing: $\eta_t = \eta_{min} + \frac{1}{2}(\eta_{max}-\eta_{min})(1+\cos(\pi t/T))$
  Warm-up + decay: ilk $W$ adım doğrusal artış, sonra azalma.

  Referans: He et al., "Deep Residual Learning for Image Recognition", CVPR 2016 (https://arxiv.org/abs/1512.03385)
  ```

- [ ] **Step 3: Eğitim pipeline kodu yaz**

  ```python
  import torch
  import torch.nn as nn
  from torch.utils.data import DataLoader, Dataset
  from torchvision import transforms, models
  from torchvision.datasets import ImageFolder
  import numpy as np
  from sklearn.metrics import classification_report, confusion_matrix
  import matplotlib.pyplot as plt

  # Veri artırma pipeline
  train_transforms = transforms.Compose([
      transforms.RandomResizedCrop(224, scale=(0.7, 1.0)),
      transforms.RandomHorizontalFlip(p=0.5),
      transforms.RandomVerticalFlip(p=0.2),
      transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
      transforms.RandomRotation(15),
      transforms.ToTensor(),
      transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # ImageNet stats
  ])

  val_transforms = transforms.Compose([
      transforms.Resize(256),
      transforms.CenterCrop(224),
      transforms.ToTensor(),
      transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
  ])

  # Dataset ve DataLoader
  train_ds = ImageFolder("data/train", transform=train_transforms)
  val_ds   = ImageFolder("data/val",   transform=val_transforms)
  train_dl = DataLoader(train_ds, batch_size=32, shuffle=True,  num_workers=4, pin_memory=True)
  val_dl   = DataLoader(val_ds,   batch_size=32, shuffle=False, num_workers=4, pin_memory=True)

  # Transfer learning: ResNet50 fine-tuning
  model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
  num_features = model.fc.in_features
  model.fc = nn.Sequential(
      nn.Dropout(0.4),
      nn.Linear(num_features, len(train_ds.classes))
  )

  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  model = model.to(device)

  criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
  optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.01)
  scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=20)

  # Eğitim döngüsü
  def train_epoch(model, loader, optimizer, criterion, device):
      model.train()
      total_loss, correct = 0, 0
      for imgs, labels in loader:
          imgs, labels = imgs.to(device), labels.to(device)
          optimizer.zero_grad()
          outputs = model(imgs)
          loss = criterion(outputs, labels)
          loss.backward()
          optimizer.step()
          total_loss += loss.item() * imgs.size(0)
          correct += (outputs.argmax(1) == labels).sum().item()
      return total_loss / len(loader.dataset), correct / len(loader.dataset)

  def eval_epoch(model, loader, criterion, device):
      model.eval()
      total_loss, correct = 0, 0
      all_preds, all_labels = [], []
      with torch.no_grad():
          for imgs, labels in loader:
              imgs, labels = imgs.to(device), labels.to(device)
              outputs = model(imgs)
              loss = criterion(outputs, labels)
              total_loss += loss.item() * imgs.size(0)
              preds = outputs.argmax(1)
              correct += (preds == labels).sum().item()
              all_preds.extend(preds.cpu().numpy())
              all_labels.extend(labels.cpu().numpy())
      return total_loss / len(loader.dataset), correct / len(loader.dataset), all_preds, all_labels

  for epoch in range(20):
      train_loss, train_acc = train_epoch(model, train_dl, optimizer, criterion, device)
      val_loss, val_acc, preds, labels = eval_epoch(model, val_dl, criterion, device)
      scheduler.step()
      print(f"Epoch {epoch+1:2d} | Train: {train_acc:.3f} | Val: {val_acc:.3f}")

  # Sınıflandırma raporu
  print(classification_report(labels, preds, target_names=train_ds.classes))
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/30-model-egitimi-ve-degerlendirme.md
  git commit -m "docs: add ch30 - transfer learning, augmentation, eğitim pipeline, metrikler"
  ```

---

### Task 21: Bölüm 31 — Vision-Language Modeller

**Files:**
- Create: `docs/31-vision-language-modeller.md`

- [ ] **Step 1: Dosyayı oluştur**

- [ ] **Step 2: Teorik Temel yaz**

  ```markdown
  # Vision-Language Modeller: CLIP, LLaVA ve Multimodal Reasoning

  ### Teorik Temel

  **CLIP (Contrastive Language-Image Pre-training):**
  Görüntü encoder $f$ ve metin encoder $g$ ile contrastive learning:
  $$\mathcal{L}_{CLIP} = -\frac{1}{N}\sum_{i=1}^N \log \frac{\exp(\text{sim}(f(I_i), g(T_i))/\tau)}{\sum_{j=1}^N \exp(\text{sim}(f(I_i), g(T_j))/\tau)}$$
  $\tau$: öğrenilebilir sıcaklık parametresi. 400M (görüntü, metin) çiftinde pre-training.
  Zero-shot sınıflandırma: sınıf isimleri prompt olarak verilir, en yüksek cosine benzerliği seçilir.

  **LLaVA (Large Language and Vision Assistant):**
  Visual encoder (CLIP ViT-L/14) + Projection Layer + LLM (Vicuna/LLaMA).
  Görüntü patch'leri token'a dönüştürülür ve metin token'larıyla birlikte LLM'e beslenir.
  Multi-turn conversation: görüntü hakkında doğal dil ile soru-cevap.

  **BLIP-2:**
  Q-Former: sabit image encoder ile LLM arasında öğrenilebilir köprü.
  32 öğrenilebilir query token, image feature'larla cross-attention.
  İki aşamalı eğitim: vision-language representation + generative learning.

  Referans: Radford et al., "Learning Transferable Visual Models From Natural Language Supervision", ICML 2021 (https://arxiv.org/abs/2103.00020)
  Referans: Liu et al., "LLaVA", NeurIPS 2023 (https://arxiv.org/abs/2304.08485)
  ```

- [ ] **Step 3: Pratik CLIP ve LLaVA kodu yaz**

  ```python
  import torch
  from PIL import Image
  from transformers import CLIPProcessor, CLIPModel

  # CLIP ile zero-shot sınıflandırma
  model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
  processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
  model.eval()

  img = Image.open("resim.jpg")
  siniflar = ["bir kedi", "bir köpek", "bir araba", "bir uçak", "bir insan"]

  inputs = processor(
      text=siniflar,
      images=img,
      return_tensors="pt",
      padding=True
  )

  with torch.no_grad():
      outputs = model(**inputs)
      logits_per_image = outputs.logits_per_image  # (1, N_sinif)
      probs = logits_per_image.softmax(dim=1)

  for sinif, prob in zip(siniflar, probs[0]):
      print(f"{sinif}: {prob.item():.3f}")

  # CLIP ile görüntü arama (semantic search)
  from transformers import CLIPModel, CLIPProcessor
  import numpy as np

  model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
  processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

  def get_image_embedding(img_path):
      img = Image.open(img_path)
      inputs = processor(images=img, return_tensors="pt")
      with torch.no_grad():
          return model.get_image_features(**inputs).squeeze().numpy()

  def get_text_embedding(text):
      inputs = processor(text=[text], return_tensors="pt", padding=True)
      with torch.no_grad():
          return model.get_text_features(**inputs).squeeze().numpy()

  # Cosine benzerliği ile arama
  query_emb = get_text_embedding("sunset over the ocean")
  # img_embs: görüntü embedding'lerinin listesi
  # similarities = [np.dot(query_emb, e) / (np.linalg.norm(query_emb)*np.linalg.norm(e)) for e in img_embs]

  # LLaVA ile görüntü hakkında soru-cevap
  from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration

  processor_llava = LlavaNextProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
  model_llava = LlavaNextForConditionalGeneration.from_pretrained(
      "llava-hf/llava-v1.6-mistral-7b-hf",
      torch_dtype=torch.float16,
      device_map="auto"
  )

  img = Image.open("resim.jpg")
  conversation = [
      {"role": "user", "content": [
          {"type": "image"},
          {"type": "text", "text": "Bu görüntüde ne görüyorsun? Türkçe açıkla."}
      ]}
  ]

  prompt = processor_llava.apply_chat_template(conversation, add_generation_prompt=True)
  inputs = processor_llava(prompt, img, return_tensors="pt").to(model_llava.device)

  output = model_llava.generate(**inputs, max_new_tokens=200)
  response = processor_llava.decode(output[0], skip_special_tokens=True)
  print(response)
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add docs/31-vision-language-modeller.md
  git commit -m "docs: add ch31 - CLIP contrastive loss, LLaVA mimarisi, zero-shot kod"
  ```

---

## TAMAMLAMA GÖREVLERİ

---

### Task 22: README Güncelleme

**Files:**
- Modify: `README.md`

- [ ] **Step 1: README'yi oku**

- [ ] **Step 2: Dokümantasyon tablosuna yeni bölümleri ekle**

  Mevcut tablonun sonuna şu satırları ekle:

  ```markdown
  | [Vision Transformers](/docs/26-vision-transformers.md) | ViT patch embedding, multi-head self-attention, DETR, Swin Transformer — teorik temel ve HuggingFace ile uygulama. |
  | [Generatif Modeller ve Diffusion](/docs/27-generatif-modeller.md) | GAN, VAE, DDPM matematiği, Stable Diffusion mimarisi ve ControlNet ile koşullu görüntü üretimi. |
  | [3D Vision](/docs/28-3d-vision.md) | Nokta bulutu (PointNet), Neural Radiance Fields (NeRF), monoküler derinlik tahmini. |
  | [Video Anlama ve Eylem Tanıma](/docs/29-video-siniflandirma.md) | SlowFast, VideoMAE mimarileri ve HuggingFace ile eylem tanıma uygulaması. |
  | [Model Eğitimi ve Değerlendirme](/docs/30-model-egitimi-ve-degerlendirme.md) | Transfer learning, augmentation, eğitim pipeline, Precision/Recall/F1/mAP metrikleri. |
  | [Vision-Language Modeller](/docs/31-vision-language-modeller.md) | CLIP contrastive learning, LLaVA, BLIP-2 mimarileri ve zero-shot uygulamalar. |
  ```

- [ ] **Step 3: Sürüm notlarına v3.0 bölümü ekle**

  ```markdown
  ### v3.0 — Mayıs 2026 (Akademik Genişletme)

  **Revize Edilen Bölümler (15 bölüm):**
  - Tüm temel bölümler akademik referanslar, matematiksel formüller ve tam çalışan Python kodlarıyla zenginleştirildi.

  **Yeni Bölümler (6 bölüm):**
  - **Bölüm 26:** Vision Transformers (ViT, DETR, Swin)
  - **Bölüm 27:** Generatif Modeller ve Diffusion (GAN, VAE, Stable Diffusion, ControlNet)
  - **Bölüm 28:** 3D Vision (PointNet, NeRF, Derinlik Tahmini)
  - **Bölüm 29:** Video Anlama ve Eylem Tanıma (SlowFast, VideoMAE)
  - **Bölüm 30:** Model Eğitimi ve Değerlendirme
  - **Bölüm 31:** Vision-Language Modeller (CLIP, LLaVA, BLIP-2)
  ```

- [ ] **Step 4: Commit**

  ```bash
  git add README.md
  git commit -m "docs: README güncelle - 6 yeni bölüm, v3.0 sürüm notları"
  ```

---

### Task 23: Terimler Sözlüğü Güncelleme

**Files:**
- Modify: `docs/terimler.md`

- [ ] **Step 1: Mevcut terimler.md dosyasını oku**

- [ ] **Step 2: Yeni akademik terimleri ekle**

  Mevcut sözlüğün uygun yerine şu terimleri alfabetik sırayla ekle:

  ```markdown
  | Türkçe | İngilizce | Açıklama |
  |--------|-----------|---------|
  | Dikkat Mekanizması | Attention Mechanism | Girişin farklı bölgelerine ağırlık veren nöral ağ bileşeni |
  | Yayınım Modeli | Diffusion Model | Gürültü ekleme ve kaldırma süreciyle görüntü üreten generatif model |
  | Gömme | Embedding | Veri noktasının yoğun vektör uzayında temsili |
  | İnce Ayar | Fine-tuning | Önceden eğitilmiş modeli yeni göreve uyarlama |
  | Üretici Çekişmeli Ağ | GAN | İki ağın (üretici/ayırt edici) rekabetine dayalı generatif model |
  | Isı Haritası | Heatmap | Piksel değerlerini yoğunluk/olasılık olarak görselleştiren harita |
  | Homoğrafi | Homography | İki düzlem arasındaki perspektif dönüşüm matrisi (3×3) |
  | Etiketleyici | Labeling / Annotation | Eğitim verisi için görüntülere kategori/koordinat bilgisi ekleme |
  | Gizli Uzay | Latent Space | Kodlayıcı ağın ürettiği düşük boyutlu temsil uzayı |
  | Bölüt | Mask | Görüntüde nesnenin piksel bazlı ikili haritası |
  | Minkowski Toplamı | Minkowski Sum | Morfolojik genişletme operasyonunun matematiksel temeli |
  | Nokta Bulutu | Point Cloud | 3D uzayda koordinat kümesiyle temsil edilen nesne |
  | Yamaçlar | Patches | Vision Transformer'da görüntünün bölündüğü sabit boyutlu dikdörtgen parçalar |
  | Sinir Işınım Alanı | NeRF (Neural Radiance Field) | 3D sahneleri sürekli nöral fonksiyonla temsil eden yöntem |
  | Öz-dikkat | Self-attention | Her girdi elemanının diğer elemanlarla ilişkisini hesaplayan mekanizma |
  | Anlam Segmentasyonu | Semantic Segmentation | Görüntüdeki her pikseli sınıf etiketiyle ilişkilendirme |
  | Sıcaklık | Temperature | Softmax dağılımının keskinliğini kontrol eden ölçekleme parametresi |
  | Aktarım Öğrenmesi | Transfer Learning | Büyük veri setinde öğrenilen bilgiyi farklı göreve aktarma |
  | Görme-Dil Modeli | Vision-Language Model | Görüntü ve metin modalitelerini birlikte işleyen model (CLIP, LLaVA) |
  | Sıfır-atışlı | Zero-shot | Eğitim verisi görmeden yeni sınıfları sınıflandırabilme özelliği |
  ```

- [ ] **Step 3: Commit**

  ```bash
  git add docs/terimler.md
  git commit -m "docs: terimler sözlüğü güncelle - 20 yeni akademik terim eklendi"
  ```

---

## Yürütme Sırası

```
GRUP A (Task 1-6)  ─┐
GRUP B (Task 7-11) ─┤── Tam paralel başlayabilir
GRUP C (Task 12-15)─┤
GRUP D (Task 16-21)─┘
                     │
              Tüm gruplar bitince
                     │
            Task 22 (README) ─┐── Paralel
            Task 23 (Terimler)─┘
```
