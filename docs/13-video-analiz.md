# Video Analiz: Optik Akış ve Nesne Takibi

Bir drone'un kamerasından gelen video akışında hedef nesne kaybolmasın istiyorsunuz. Her kare ayrı bir fotoğraf gibi değil, bir önceki kareyle ilişkili — bu ilişkiyi modelleyen araçlar optik akış ve tracker'lardır. Bu bölümde noktaları kareler arasında takip etmekten tam çözünürlüklü hareket haritalarına, klasik OpenCV tracker'lardan modern çoklu-nesne algoritmalarına kadar video analizinin temellerini öğreneceksiniz.

## Optik Akış: Hareketi Sayısal İfade Etmek

Bir ırmakta sürüklenen yaprak düşünün. Yaprak bir kareden diğerine yer değiştirir. Optik akış, her pikselin (ya da seçilmiş noktaların) bu yer değişimini vektör olarak ifade eder — sanki rüzgarı görünür kılıyorsunuz.

Temel varsayım **parlaklık sürekliliği** (brightness constancy): Bir nesnenin yüzeyindeki piksel parlaklığı art arda iki kare arasında değişmez. Matematiksel olarak:

$$I(x, y, t) = I(x + \Delta x, y + \Delta y, t + \Delta t)$$

Bu varsayım mükemmel değildir — ışık değişimi ya da doku tekrarı yanıltabilir — ama pratik uygulamalarda şaşırtıcı derecede iyi çalışır.

## Lucas-Kanade: Seyrek Optik Akış

Her pikseli takip etmek hesaplı açıdan pahalıdır. Lucas-Kanade yöntemi bunun yerine seçilmiş anahtar noktaları takip eder: köşeler, keskin kenarlar gibi kolay ayırt edilebilen noktalar. Az sayıda nokta, yüksek hız.

**Piramidal LK** bu yöntemin genişletilmiş halidir. Önce görüntüyü küçültülmüş versiyonlarında (piramit katmanları) akışı hesaplar, büyük hareketlerde de kararlı kalır. Tek ölçekte Lucas-Kanade hızlı hareket eden nesnelerde kaybolabilir; piramidal yapı bu sorunu çözer.

```python
import cv2
import numpy as np

cap = cv2.VideoCapture(0)  # 0: varsayılan kamera; video dosyası için yol girin

ret, prev_frame = cap.read()
if not ret:
    raise RuntimeError("Kamera açılamadı")

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Takip edilecek iyi köşeleri bul
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
prev_pts = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)

# Yörünge rengi ve çizim maskesi
colors = np.random.randint(0, 255, (100, 3))
mask = np.zeros_like(prev_frame)

lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Noktaları bir sonraki kareye taşı
    next_pts, status, _ = cv2.calcOpticalFlowPyrLK(
        prev_gray, gray, prev_pts, None, **lk_params
    )

    # Başarılı takip edilen noktaları filtrele
    if next_pts is not None:
        good_new = next_pts[status == 1]
        good_old = prev_pts[status == 1]

        # Yörüngeleri çiz
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel().astype(int)
            c, d = old.ravel().astype(int)
            mask = cv2.line(mask, (a, b), (c, d), colors[i % 100].tolist(), 2)
            frame = cv2.circle(frame, (a, b), 4, colors[i % 100].tolist(), -1)

    output = cv2.add(frame, mask)
    cv2.imshow("Lucas-Kanade Optik Akış", output)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

    prev_gray = gray.copy()
    prev_pts = good_new.reshape(-1, 1, 2) if next_pts is not None else prev_pts

cap.release()
cv2.destroyAllWindows()
```

Her renkli çizgi bir noktanın izlediği yolu gösterir — sanki nesnenin hareketini boya fırçasıyla çiziyorsunuz. Noktaların azaldığını fark ederseniz, yeniden `goodFeaturesToTrack` çağırarak tazeleyebilirsiniz.

> **📌 Not:** `status == 1` filtresi, optik akış algoritmasının güvenilir bulamadığı noktaları eler. Her zaman bu filtreyi uygulayın, aksi hâlde kayıp noktalar hatalı vektörler üretir.

## Farneback: Yoğun Optik Akış

Lucas-Kanade seçilmiş noktalara bakarken Farneback yöntemi her piksel için akış vektörü hesaplar. Sonuç, tüm görüntüyü kaplayan bir hareket haritasıdır — video stabilizasyonu ve hareket yoğunluğu analizi için idealdir.

Farneback yöntemi görüntüyü polinom fonksiyonlarla yaklaşık ifade eder ve bu yaklaşımın iki kare arasındaki değişiminden hareket vektörünü türetir. Hesaplama maliyeti yüksektir ama elde ettiğiniz bilgi de o kadar zengindir.

```python
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

ret, prev_frame = cap.read()
if not ret:
    raise RuntimeError("Kamera açılamadı")

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yoğun optik akış hesapla
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, gray,
        None,
        pyr_scale=0.5,   # Piramit küçültme oranı
        levels=3,        # Piramit katman sayısı
        winsize=15,      # Ortalama pencere boyutu
        iterations=3,    # Her katmanda iterasyon
        poly_n=5,        # Polinom yaklaşımı komşuluk boyutu
        poly_sigma=1.2,  # Gauss standart sapması
        flags=0,
    )

    # HSV ile görselleştir: Hue=yön, Value=büyüklük
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv = np.zeros_like(prev_frame)
    hsv[..., 1] = 255                                        # Doygunluk maksimum
    hsv[..., 0] = angle * 180 / np.pi / 2                   # Yön → renk
    hsv[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    bgr_flow = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    combined = np.hstack([frame, bgr_flow])
    cv2.imshow("Orijinal | Farneback Akış", combined)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

    prev_gray = gray.copy()

cap.release()
cv2.destroyAllWindows()
```

Çıktıda renkler yönü, parlaklık ise hareket hızını temsil eder: kırmızı sağa, mavi sola, yeşil yukarı giden hareketi gösterir. Durağan arka plan siyah kalırken hareket eden nesneler renkli parlar.

> **💡 İpucu:** Video stabilizasyonunda Farneback akışından hesaplanan global dönüşüm matrisi görüntüyü karşı yönde kaydırır — titreyen videoyu sabitlemek için bu teknik kullanılır.

## OpenCV Object Trackers

Optik akış pikseller arasındaki genel hareketi modeller. OpenCV tracker'lar ise farklı bir sorunu çözer: kullanıcı bir nesneyi işaret eder, tracker onu bir film boyunca peşinden gider.

Çalışma mantığı:
1. İlk karede `tracker.init(frame, bbox)` — nesneyi tanıt
2. Her yeni karede `tracker.update(frame)` — yeni konumu al
3. Dönen `(success, bbox)` çiftini değerlendir

**CSRT** (Channel and Spatial Reliability Tracking): Kanal güvenilirliği filtreleri kullanır, kısmi örtme ve boyut değişimine karşı dirençlidir. Yavaştır ama doğrudur.

**KCF** (Kernelized Correlation Filters): Frekans alanında korelasyon filtresi kullanır, gerçek zamanlı hıza ulaşır. Hızlı ama büyük boyut değişimlerinde takibi kaybedebilir.

```python
import cv2

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if not ret:
    raise RuntimeError("Kamera açılamadı")

# İlk karede kullanıcıdan ROI seç
# Mouse ile dikdörtgen çiz, ENTER ile onayla, C ile iptal et
bbox = cv2.selectROI("Nesne Seç", frame, fromCenter=False, showCrosshair=True)
cv2.destroyWindow("Nesne Seç")

# Tracker oluştur — CSRT veya KCF seçin
tracker = cv2.TrackerCSRT_create()
# tracker = cv2.TrackerKCF_create()  # Daha hızlı alternatif

tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    success, bbox = tracker.update(frame)

    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Takip Ediliyor", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Nesne Kayboldu", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Nesne Takibi", frame)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

> **💡 İpucu:** Tek nesne takibi için CSRT, gerçek zamanlı çoklu nesne için KCF tercih edin. Kaybolan nesneyi yeniden bulmak istiyorsanız tracker'ı sıfırlayıp yeniden init etmeniz gerekir — tracker'lar kayıp nesneyi kendiliğinden aramaz.

> **⚠️ Dikkat:** OpenCV 4.5+ sürümünden itibaren bazı tracker'lar `opencv-contrib-python` paketinde bulunur. `pip install opencv-contrib-python` kurulu değilse `TrackerCSRT_create()` çağrısı hata verir.

## Modern Çoklu Nesne Takibi

OpenCV tracker'lar tek nesne için tasarlanmıştır. Fabrika bandındaki onlarca ürünü ya da kalabalıktaki tüm insanları takip etmek farklı bir yaklaşım gerektirir.

**DeepSORT**: YOLO gibi bir dedektörün her karede bulduğu nesneleri Kalman filtresiyle tahmin edilen konumlarla eşleştirir. Nesne bir süre görünmese bile ID'yi korur, yeniden göründüğünde tanır. Re-identification özelliği ile aynı nesneye tutarlı ID atar.

**ByteTrack**: DeepSORT'tan daha basit ve daha hızlıdır. Düşük güven skorlu tespitleri de takibe dahil ederek kayıp nesne sayısını azaltır. Kalabalık sahnelerde DeepSORT'tan üstün performans gösterir.

Her iki yöntem de aynı pipeline'ı izler: tespit → özellik çıkarımı → Kalman tahmini → Macar algoritması eşleştirmesi → ID atama.

## Yöntem Karşılaştırması

| Yöntem | Doğruluk | Hız | Nesne Sayısı | Kullanım |
|--------|----------|-----|--------------|----------|
| LK Sparse | Orta | Çok hızlı | Çok nokta | Kamera hareketi, yer imlemleri |
| Farneback Dense | Yüksek | Yavaş | Tüm pikseller | Stabilizasyon, hareket analizi |
| CSRT | Yüksek | ~25 FPS | 1 nesne | Hassas takip, kısmi örtme |
| KCF | Orta | ~100 FPS | 1 nesne | Gerçek zamanlı, düz hareket |
| DeepSORT/ByteTrack | Çok yüksek | GPU gerekli | Çok nesne | Endüstriyel çoklu takip |

## Özet

- Optik akış, iki kare arasındaki piksel hareketini vektör alanı olarak modeller.
- Parlaklık sürekliliği varsayımı optik akışın temelidir; ışık değişiminde hassasiyeti düşer.
- Lucas-Kanade seyrek nokta takibi için hızlı ve güvenilirdir; piramidal yapı büyük hareketleri de yakalar.
- Farneback her piksel için akış hesaplar; video stabilizasyonu ve hareket yoğunluğu haritaları için uygundur.
- CSRT doğruluk, KCF hız odaklıdır; her ikisi de tek nesne içindir.
- Çoklu nesne takibinde DeepSORT ve ByteTrack endüstri standardıdır.
- `tracker.update()` her çağrıda `(success, bbox)` döner; `success=False` olduğunda nesnenin kaybolduğu anlaşılır.

## İleri Okuma

- Bouguet, J.Y., "Pyramidal Implementation of the Lucas Kanade Feature Tracker" (2001) — LK piramit uygulamasının orijinal teknik raporu
- Farneback, G., "Two-Frame Motion Estimation Based on Polynomial Expansion" (SCIA 2003) — Farneback yönteminin temel makalesi
- Bewley et al., "Simple Online and Realtime Tracking" (ICIP 2016): https://arxiv.org/abs/1602.00763 — SORT algoritması, DeepSORT'un temeli
- Zhang et al., "ByteTrack" (ECCV 2022): https://arxiv.org/abs/2110.06864 — ByteTrack makalesi
