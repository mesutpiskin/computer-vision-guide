# Dijital Görüntü Temelleri

Bir güvenlik kamerası kaydını bilgisayarın nasıl "gördüğünü" hiç düşündünüz mü? Ekrandaki o güzel fotoğraf, bilgisayar için onlarca milyon sayıdan oluşan bir tablodur. Bu bölümde dijital görüntünün matematiksel yapısını kavrayacak, OpenCV ile görüntü okuyup gösterecek ve kameradan gerçek zamanlı veri akışı kuracağız.

## Dijital Görüntü Nedir?

Bir siyah-beyaz fotoğrafı kağıda basılmış bir kareler ızgarası olarak hayal edin. Her kare, o noktadaki parlaklığı temsil eden tek bir sayı taşır. Izgara ne kadar sık, görüntü o kadar keskin. Renkli fotoğrafta ise her kare tek değil, üç sayı taşır: kırmızı, yeşil ve mavi bileşenler.

Matematiksel olarak yazarsak: $f(x, y) \to [0, 255]$ — koordinata renk değeri atayan bir fonksiyon. Gri bir görüntü H×W boyutlu iki boyutlu bir matristir; renkli görüntü ise H×W×3 boyutlu üç boyutlu bir tensör.

**Neden 0–255 aralığı?** Çünkü her piksel 8 bit ile temsil edilir: $2^8 = 256$ farklı değer. 0 tam siyah, 255 tam beyazdır. 8-bit görüntüler en yaygın format olduğu için OpenCV varsayılan olarak `uint8` veri tipini kullanır.

> **📌 Not:** 16-bit ve 32-bit görüntüler de var — tıbbi görüntüleme (MRI, CT) ve HDR fotoğrafçılık bu formatları kullanır. 32-bit float görüntülerde değer aralığı 0.0–1.0 olur.

## BGR ve RGB: OpenCV'nin Renk Sırası

Renkli bir piksel üç kanaldan oluşur. Ama hangi sırada? Çoğu uygulama ve kütüphane RGB (Kırmızı-Yeşil-Mavi) sırasını kullanır. OpenCV ise tarihsel bir sebeple BGR (Mavi-Yeşil-Kırmızı) sırası kullanır: geliştirme döneminde Windows bitmap formatı bu sırayı tercih ediyordu ve bu durum standart hale geldi.

Pratikte tek fark: OpenCV'nin döndürdüğü bir görüntü dizisinde `img[:, :, 0]` mavi kanalı, `img[:, :, 2]` ise kırmızı kanalı verir.

> **⚠️ Dikkat:** Matplotlib'de görüntü gösterirken `COLOR_BGR2RGB` dönüşümünü yapmazsanız renkler yanlış çıkar — kırmızı nesneler mavi, mavi nesneler kırmızı görünür.

## Görüntü Okuma ve Gösterme

OpenCV'nin en temel işlemi: diskten görüntü okumak, ekranda göstermek ve kaydetmek. Aşağıdaki kod görüntüyü okur, boyutunu ve veri tipini yazdırır, ekranda gösterir ve yeni bir dosyaya kaydeder.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

# Görüntü hakkında temel bilgiler
print(f"Boyut (H×W×C): {img.shape}")   # örn. (480, 640, 3)
print(f"Veri tipi: {img.dtype}")         # uint8
print(f"Min/Max değer: {img.min()}, {img.max()}")

cv2.imshow("Orjinal Görüntü", img)
cv2.waitKey(0)               # herhangi bir tuşa basılana kadar bekle
cv2.destroyAllWindows()

# Diske kaydet
cv2.imwrite("cikti.jpg", img)
print("Görüntü kaydedildi: cikti.jpg")
```

`img.shape` size üç sayı verir: (yükseklik, genişlik, kanal sayısı). Yükseklik önce gelir çünkü matris indeksleme satır-sütun sırasını izler. Gri görüntülerde shape `(H, W)` olur, üçüncü boyut yoktur.

> **💡 İpucu:** `cv2.imread` başarısız olduğunda `None` döner ve hata mesajı vermez. Bu yüzden her okumadan sonra `if img is None` kontrolü kritiktir.

### `cv2.imread` Bayrakları

| Bayrak | Değer | Açıklama |
|--------|-------|----------|
| `cv2.IMREAD_COLOR` | 1 (varsayılan) | Renkli oku, alfa kanalını at |
| `cv2.IMREAD_GRAYSCALE` | 0 | Gri olarak oku |
| `cv2.IMREAD_UNCHANGED` | -1 | PNG alfa kanalı dahil oku |

## Kameradan Gerçek Zamanlı Görüntü Okuma

Statik görüntüden sonra sıra canlı video akışında. OpenCV'de kamera ve video aynı `VideoCapture` arayüzüyle açılır; tek fark argümandır.

`cv2.VideoCapture(0)` işletim sistemindeki ilk kamerayı açar (genellikle dahili webcam). Birden fazla kamera varsa `1`, `2` indekslerini deneyin.

```python
import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Kamera açılamadı")

# Kamera özellikleri
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Kamera: {width}×{height} @ {fps:.1f} FPS")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Kamera", frame)

    # 'q' tuşuna basılınca çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

`cap.read()` iki değer döner: `ret` (başarı bayrağı) ve `frame` (görüntü). `cv2.waitKey(1)` yaklaşık 1 ms bekler — bu değer ne kadar küçükse kare hızı o kadar yüksek olur, ama 0 verirseniz ilk kareyi gösterip durur.

> **💡 İpucu:** `& 0xFF` maskesi bazı sistemlerde tuş kodunun üst bitlerinden kaynaklanan sorunları önler. Güvenli bir alışkanlık olarak her zaman kullanın.

### Kamera Özelliklerini Ayarlama

`cap.set()` ile çözünürlük ve FPS gibi değerleri değiştirebilirsiniz:

```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)
```

> **📌 Not:** Kamera donanımı istenen değeri desteklemiyorsa en yakın desteklenen değere düşer. Ayarladıktan sonra `cap.get()` ile gerçek değeri kontrol edin.

## Video Dosyası ve IP Kamera

Aynı `VideoCapture` yapısı MP4, AVI gibi video dosyalarını ve ağ akışlarını da açar.

```python
import cv2

# Video dosyası
cap = cv2.VideoCapture("traffic.mp4")

# IP kamera RTSP akışı — satırın başındaki # kaldırıp bağlantıyı kendi URL'nize göre düzenleyin
# cap = cv2.VideoCapture("rtsp://192.168.1.100:554/stream")

# HTTP MJPEG akışı
# cap = cv2.VideoCapture("http://192.168.1.100:8080/video")

if not cap.isOpened():
    raise IOError("Video kaynağı açılamadı")

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Toplam kare: {total_frames}, FPS: {fps:.1f}")
print(f"Tahmini süre: {total_frames / fps:.1f} saniye")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Video", frame)

    # FPS'e göre bekleme süresi hesapla
    bekleme = max(1, int(1000 / fps))
    if cv2.waitKey(bekleme) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

Video dosyasında bekleme süresini FPS'e göre hesaplıyoruz: 30 FPS için `1000/30 ≈ 33 ms`, 25 FPS için `40 ms`. Bu olmadan video gerçek hızından çok daha hızlı oynar.

> **📌 Not:** IP Kamera URL Formatları
>
> - RTSP (en yaygın): `rtsp://kullanici:sifre@192.168.1.100:554/live`
> - HTTP MJPEG: `http://192.168.1.100:8080/video`
> - GStreamer pipeline (Linux): `"v4l2src ! videoconvert ! appsink"`
>
> RTSP bağlantı sorunlarında `cv2.VideoCapture("rtsp://...", cv2.CAP_FFMPEG)` bayrağını deneyin.

## Piksel Manipülasyonu

NumPy dizisi olan bir OpenCV görüntüsünde tek piksel ve bölge erişimi doğrudan dizi indeksleme ile yapılır.

Koordinat sistemi dikkat gerektiriyor: `img[y, x]` şeklinde önce satır (dikey eksende konum = y), sonra sütun (yatay = x) gelir. Bu matris indeksleme standartıdır.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} bulunamadı")

# Tek piksel okuma — img[satir, sutun] yani img[y, x]
piksel = img[100, 200]
print(f"(200, 100) koordinatındaki piksel BGR: {piksel}")

# Piksel yazma — o noktayı kırmızıya boya
img_kopya = img.copy()
img_kopya[100, 200] = [0, 0, 255]   # BGR: kırmızı

# ROI (Region of Interest) kırpma
# img[y_baslangic:y_bitis, x_baslangic:x_bitis]
roi = img[100:300, 150:400].copy()
print(f"ROI boyutu: {roi.shape}")

# ROI'yi kaydet
cv2.imwrite("roi_cikti.jpg", roi)

# ROI'yi vurgula — orijinal üzerine dikdörtgen çiz
img_vurgulu = img.copy()
cv2.rectangle(img_vurgulu, (150, 100), (400, 300), (0, 255, 0), 2)

cv2.imshow("ROI Vurgulanmış", img_vurgulu)
cv2.imshow("ROI", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

NumPy dilimleme görünüm (view) döndürür — yani `roi = img[100:300, 150:400]` ile alınan `roi` üzerindeki değişiklikler orijinal `img`'yi de etkiler. Bağımsız çalışmak istiyorsanız `.copy()` şarttır.

> **⚠️ Dikkat:** `img[100, 200]` ifadesinde önce 100 satır (y=100), sonra 200 sütun (x=200) gelir. Kartezyen koordinatlarda (x=200, y=100) olan nokta budur. Bu sıralamayı karıştırmak sinir bozucu hatalara yol açar — özellikle `cv2.circle(img, (x, y), ...)` gibi OpenCV fonksiyonları Kartezyen sıra kullanırken NumPy indeksleme matris sırası kullanır.

## Özet & İleri Okuma

- Dijital görüntü, $f(x,y) \to [0,255]$ fonksiyonunun ayrık örneklemesidir; gri görüntü H×W matris, renkli görüntü H×W×3 tensördür.
- OpenCV BGR sırası kullanır; matplotlib ile göstermeden önce `cv2.COLOR_BGR2RGB` dönüşümü zorunludur.
- `cv2.imread` başarısızlıkta `None` döner — her okumadan sonra `if img is None` kontrolü yapın.
- `cv2.VideoCapture` kamera, video dosyası ve IP kamera için aynı arayüzü sunar; argüman sırasıyla `0`, `"dosya.mp4"` veya RTSP URL'sidir.
- Her video döngüsünde `if not ret: break` ve döngü bitiminde `cap.release(); cv2.destroyAllWindows()` şarttır.
- Piksel erişimi `img[y, x]` — önce satır (y), sonra sütun (x).
- ROI kırpma `img[y1:y2, x1:x2]` NumPy dilimleme ile yapılır; bağımsız kopya için `.copy()` ekleyin.

**Referanslar**

- Bradski, G. & Kaehler, A. (2017). *Learning OpenCV 3*. O'Reilly Media.
- OpenCV Dokümantasyonu: [docs.opencv.org/4.x](https://docs.opencv.org/4.x/)
