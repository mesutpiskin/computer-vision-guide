# Arka Plan Çıkarma ve Hareket Tespiti

Bir otopark güvenlik kamerası saatler boyunca kayıt yapıyor. Kaydın büyük bölümü boş bir otopark — sizi ilgilendiren sadece araçların gelip gittiği anlar. Her kareyi ayrı ayrı analiz etmek hem yavaş hem gereksiz. Arka plan çıkarma bu problemi şu yaklaşımla çözer: "normal durumu" öğren, değişen pikselleri ön plan (hareket eden nesne) say. Bu bölümde üç farklı arka plan çıkarma yöntemi ele alınacak.

## Frame Differencing — Kare Farkı

En basit yöntem: art arda iki kareyi birbirinden çıkar. Fark büyükse o piksel hareket ediyor demektir.

Sezgi: Durağan arka plan kare kare değişmez, dolayısıyla iki kare farkı sıfıra yakındır. Hareket eden bir nesne ise bir karede sağda, sonraki karede solda — fark büyük.

```python
import cv2
import numpy as np

cap = cv2.VideoCapture("traffic.mp4")

if not cap.isOpened():
    raise IOError("Video açılamadı")

ret, prev_frame = cap.read()
if not ret:
    raise IOError("İlk kare okunamadı")

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Mutlak fark
    fark = cv2.absdiff(prev_gray, gray)

    # Eşikleme: küçük farklılıkları gürültü say
    _, maske = cv2.threshold(fark, 25, 255, cv2.THRESH_BINARY)

    # Gürültü temizle
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    maske = cv2.morphologyEx(maske, cv2.MORPH_OPEN, kernel)

    sonuc = cv2.bitwise_and(frame, frame,
                            mask=maske)

    cv2.imshow("Kare | Maske | Hareket",
               np.hstack([frame, cv2.cvtColor(maske, cv2.COLOR_GRAY2BGR), sonuc]))

    prev_gray = gray

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

Yavaş hareket eden nesneler iki ardışık kare arasında az yer değiştirir — bu yöntemle yakalanmayabilir. Kamera titremesi ise tüm piksellerde fark yaratır ve sahte alarm verir. Bu sınırlamalar daha gelişmiş yöntemlere yönlendirir.

## MOG2 — Gaussian Karışımı ile Arka Plan Modeli

MOG2 (Mixture of Gaussians 2) her piksel için bir "normal değer dağılımı" öğrenir. Bunu yapabilmek için birkaç yüz kare boyunca arka planı gözlemler. Öğrenilen dağılımın dışında kalan piksel = ön plan.

Sezgi: Her piksel için "bu piksel normalde ne değerinde olur?" sorusunu cevaplayan bir istatistik tutuluyor. Bir araç geldiğinde o pikselin değeri modelden sapıyor — ön plan. Gündüzden geceye geçiş gibi yavaş değişimler ise modeli zamanla güncelliyor.

```python
import cv2
import numpy as np

cap = cv2.VideoCapture("traffic.mp4")

if not cap.isOpened():
    raise IOError("Video açılamadı")

# history: kaç kare geriye bakılsın
# varThreshold: piksel foreground sayılma hassasiyeti (düşük = hassas)
# detectShadows: gölgeleri ayrıca işaretle
mog2 = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=16,
    detectShadows=True
)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

kare_sayaci = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    kare_sayaci += 1

    # apply: hem arka planı öğrenir hem maske üretir
    fg_mask = mog2.apply(frame)

    # detectShadows=True iken gölgeler 127 (gri) olarak işaretlenir — bunları sil
    _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

    # Morfoloji ile temizle
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)   # küçük gürültü
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)  # nesne içi delik

    # Kontur tespiti ile nesne sayısı
    konturlar, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Küçük konturları gürültü say (alan < 500 piksel)
    gercek_nesneler = [k for k in konturlar if cv2.contourArea(k) > 500]

    # Çerçeve çiz
    sonuc = frame.copy()
    cv2.drawContours(sonuc, gercek_nesneler, -1, (0, 255, 0), 2)

    # Nesne sayısını göster
    cv2.putText(sonuc, f"Nesne: {len(gercek_nesneler)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    gosterim = np.hstack([
        frame,
        cv2.cvtColor(fg_mask, cv2.COLOR_GRAY2BGR),
        sonuc
    ])
    cv2.imshow("Kamera | Maske | Tespit", gosterim)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

`mog2.apply(frame)` iki işi birden yapar: hem arka plan modelini günceller hem de ön plan maskesini döndürür. `learning_rate` parametresiyle güncelleme hızını ayarlayabilirsiniz — `mog2.apply(frame, learningRate=0.005)` yavaş uyum için.

> **💡 İpucu:** MOG2 ilk 100–200 karede arka planı öğrenir — bu süre zarfında hatalı tespitler normaldir. `cap.set(cv2.CAP_PROP_POS_FRAMES, 200)` ile ilk kareleri atlayabilirsiniz.

> **⚠️ Dikkat:** `detectShadows=True` ile gölgeler 127 değerinde işaretlenir. Bunu `cv2.threshold(fg_mask, 200, 255, ...)` ile süzgeçleyerek gölgeleri ön plan saymaktan kaçının — aksi takdirde her nesnenin gölgesi sahte ikinci nesne olarak görünür.

### MOG2 Parametre Rehberi

| Parametre | Varsayılan | Etki |
|-----------|-----------|------|
| `history` | 500 | Kaç kare geriye bakılır — uzun = yavaş uyum |
| `varThreshold` | 16 | Eşik değeri — düşük = daha fazla ön plan |
| `detectShadows` | True | Gölge tespiti — işlem maliyeti artar |

## KNN Subtractor

K-En Yakın Komşu tabanlı arka plan modeli. MOG2'nin Gaussian varsayımı yapmak yerine son N karenin piksel değerlerini doğrudan depolar ve KNN mesafesi ile sınıflandırır.

```python
import cv2
import numpy as np

cap = cv2.VideoCapture("traffic.mp4")

if not cap.isOpened():
    raise IOError("Video açılamadı")

knn = cv2.createBackgroundSubtractorKNN(
    history=500,
    dist2Threshold=400.0,
    detectShadows=True
)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fg_mask = knn.apply(frame)

    # Gölgeleri temizle
    _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

    sonuc = cv2.bitwise_and(frame, frame, mask=fg_mask)

    cv2.imshow("KNN Sonucu", sonuc)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

KNN, çok sayıda nesnenin hareket ettiği sahnelerde (kalabalık, yoğun trafik) MOG2'den daha kararlı çalışır. Ancak bellek kullanımı daha yüksektir çünkü piksel değerlerini doğrudan depolar.

## Karşılaştırma Tablosu

| Yöntem | Hız | Doğruluk | Adaptasyon | Ne Zaman |
|--------|-----|----------|------------|----------|
| Frame Diff | Çok hızlı | Düşük | Yok | Hızlı prototip, çok az hareket |
| MOG2 | Hızlı | Yüksek | Kademeli | Genel amaç, ışık değişimi |
| KNN | Orta | Çok yüksek | Kademeli | Yoğun sahne, karmaşık arka plan |

## Özet & İleri Okuma

- Frame differencing iki ardışık kareyi çıkararak hareketi tespit eder — basit ama yavaş harekete kör, kamera titremesine hassas.
- MOG2 her piksel için Gaussian karışımı modeliyle "normal değer aralığı" öğrenir; yavaş arka plan değişimlerine otomatik adapte olur.
- `detectShadows=True` gölgeleri 127 ile işaretler — `threshold(fg_mask, 200, 255)` ile süzgecin.
- MOG2 ilk 100–200 karede öğrenim aşamasındadır; bu süredeki tespitler güvenilir değil.
- Morfoloji (opening + closing) MOG2 maskesini temizlemek için standart son adımdır.
- KNN yoğun sahnelerde MOG2'den daha kararlı, bellek maliyeti daha yüksek.
- Gerçek uygulamada kontur alanı filtresi (`contourArea > eşik`) küçük gürültü konturlarını ayıklamak için şart.

**Referanslar**

- Zivkovic, Z. (2004). "Improved Adaptive Gaussian Mixture Model for Background Subtraction." *International Conference on Pattern Recognition (ICPR)*. [doi:10.1109/ICPR.2004.1333992](https://doi.org/10.1109/ICPR.2004.1333992)
- Zivkovic, Z. & van der Heijden, F. (2006). "Efficient Adaptive Density Estimation per Image Pixel for the Task of Background Subtraction." *Pattern Recognition Letters*, 27(7), 773–780.
