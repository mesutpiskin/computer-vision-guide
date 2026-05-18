# OpenCV Nedir?

Bir araç otonom frenleme kararı verecekse, bir ameliyathane robotu milimetrik hassasiyetle hareket edecekse ya da bir güvenlik kamerası kalabalıkta kayıp bir çocuğu tanıyacaksa, temelinde aynı soru vardır: makine, gördüğünü nasıl anlayacak? Bu bölümde bilgisayarlı görünün ne olduğunu ve bu alanda 25 yıldır endüstri standardı olan OpenCV kütüphanesini tanıyacağız. Sonunda kendi geliştirme ortamınız hazır olacak ve ilk görüntüyü okuyup işleyebileceksiniz.

## Bilgisayarlı Görü: Makinelere Görme Yeteneği Kazandırmak

İnsan gözü bir sahneye baktığında renk, derinlik, hareket ve bağlamı eş zamanlı işler — bu işlem milyonlarca yıllık evrimsel mühendisliğin ürünüdür. Bilgisayarlı görü (computer vision), bu yeteneği sayısal sistemlere aktarmaya çalışan disiplindir. Ham piksel değerlerinden anlam çıkarmak: bir görüntüdeki nesneyi tanımlamak, iki kare arasındaki hareketi ölçmek, bir sahnenin üç boyutlu yapısını yeniden inşa etmek.

Uygulamalar artık herkesin günlük hayatına girmiş durumda:

- **Sürücüsüz araçlar:** Şerit takibi, yayaya dönük nesne tespiti, trafik levhası okuma
- **Tıbbi görüntüleme:** MR görüntülerinde tümör segmentasyonu, dermatolojik görüntülerde cilt kanseri taraması
- **Endüstriyel kalite kontrolü:** Üretim bandında mikron düzeyinde kusur tespiti
- **Artırılmış gerçeklik:** Yüz filtreleri, sanal mobilya yerleştirme, navigasyon katmanları

Bu uygulamaların hepsinde ortak bir araç seti vardır: OpenCV.

## OpenCV Nedir?

OpenCV (Open Source Computer Vision Library), bilgisayarlı görü ve makine öğrenmesi için 2500'ü aşkın optimize algoritma içeren açık kaynaklı bir kütüphanedir. 1999 yılında Intel'de çalışan Gary Bradski tarafından başlatılan proje, bugün Itseez, Google, Intel ve topluluk geliştiricilerinin katkılarıyla büyümeye devam etmektedir.

Kütüphanenin mimarisi katmanlıdır: **C++ çekirdeği** maksimum performans için yazılmış; **Python, Java ve C#** sarmalayıcıları (wrapper) bu çekirdeği erişilebilir kılmaktadır. Pikselleri gerçek zamanlı manipüle etmenin gerektirdiği hız, C++'ın bellek erişim verimliliğiyle gelir; ama prototip geliştiricinin buna ihtiyacı yoktur — Python arayüzü, `numpy` ile uyumlu bir soyutlama sunar.

Rakamlar ölçeği anlatır: haftada 3 milyonun üzerinde indirme, 47.000+ GitHub yıldızı, 90'dan fazla ülkede aktif geliştirici topluluğu. OpenCV, akademik prototipten üretim sistemine tek bir bağımlılıkla geçebileceğiniz nadir kütüphanelerden biridir.

## Neden OpenCV?

Pek çok görüntü işleme kütüphanesi varken OpenCV'nin öne çıkması rastlantı değildir. Gerçek zamanlı uygulamalar, piksel seviyesinde hızdan taviz verilmesine izin vermez — ve OpenCV bu noktada rakiplerinden ayrışır.

**Donanım hızlandırma:** CUDA (NVIDIA GPU), OpenCL (genel GPU), AVX/SSE (CPU vektörizasyonu) ve NEON (ARM) desteği sayesinde aynı algoritma masaüstü GPU'sundan Raspberry Pi'ya kadar optimize çalışır. Bir Gaussian blur operasyonunu CPU'da çalıştırmak ile CUDA ile çalıştırmak arasında 10-50x hız farkı olabilir.

**Ekosistem derinliği:** Yalnızca görüntü işleme değil — video analizi, kamera kalibrasyonu, 3D yeniden yapılandırma, makine öğrenmesi, derin öğrenme çıkarımı (inference) tek çatı altında. PyTorch ve TensorFlow modellerini `cv2.dnn` modülüyle doğrudan çalıştırabilirsiniz.

**Endüstri güvencesi:** Google Lens, Intel RealSense SDK, Sony kamera yazılımı, Microsoft HoloLens — hepsi OpenCV kullanır. Bir üretim sisteminde ihtiyaç duyabileceğiniz destek ve dokümantasyon zaten orada.

> **📌 Not:** OpenCV'nin Python paketi `opencv-python`, C++ çekirdeğinin derlenmiş ikili dosyasını içerir. Yani `pip install opencv-python` demek, aynı zamanda yüksek performanslı C++ kodunu da yüklemek demektir — Python sadece bu kodu çağırır.

## Alternatifler Ne Zaman Kullanılır?

OpenCV her derde deva değildir. Doğru aracı seçmek, projenin başarısını doğrudan etkiler.

| Kütüphane | Güçlü Yön | Ne Zaman Kullan |
|-----------|-----------|-----------------|
| **OpenCV** | Klasik CV algoritmaları, gerçek zamanlı işlem, video | Kamera akışı, nesne tespiti, klasik filtreler, üretim sistemi |
| **scikit-image** | Araştırma kalitesi, iyi dokümantasyon, NumPy uyumu | Akademik çalışma, hızlı prototipleme, sinyal işleme araştırması |
| **Pillow (PIL)** | Basit dosya okuma/yazma, temel dönüşümler | Format dönüştürme, yeniden boyutlandırma, web uygulaması thumbnail'leri |
| **torchvision** | PyTorch ile sıkı entegrasyon, veri artırma, model zoo | PyTorch modeli eğitimi, veri ön işleme boru hatları |
| **imageio** | Çok formatlı okuma (TIFF stack, DICOM, video) | Tıbbi görüntüler, çok sayfalı dosyalar, video dosyası okuma |

Pratikte bu kütüphaneler birbirini dışlamaz — bir projede scikit-image ile prototip kurup OpenCV ile üretime geçebilirsiniz.

## OpenCV Modülleri

OpenCV, işlevselliğe göre modüllere ayrılmıştır. Hangi modülün hangi sorunu çözdüğünü bilmek, doğru fonksiyonu bulmayı kolaylaştırır.

| Modül | Ad | Ne Yapar |
|-------|----|----------|
| `core` | Çekirdek | Temel veri yapıları (Mat), aritmetik, bellek yönetimi |
| `imgproc` | Görüntü İşleme | Filtreler, geometrik dönüşümler, renk uzayı dönüşümleri, morfoloji |
| `highgui` | Yüksek Seviye GUI | Pencere aç, görüntü/video göster, fare/klavye olayları |
| `videoio` | Video G/Ç | Kamera ve video dosyası okuma/yazma, codec yönetimi |
| `video` | Video Analizi | Optik akış, arka plan çıkarma, nesne takibi |
| `calib3d` | Kalibrasyon ve 3D | Kamera kalibrasyonu, stereo görü, perspektif dönüşümü |
| `features2d` | Öznitelik Dedektörleri | SIFT, ORB, AKAZE anahtar noktası tespiti ve tanımlayıcıları |
| `dnn` | Derin Sinir Ağları | ONNX, TensorFlow, Caffe, PyTorch modellerini yükle ve çalıştır |
| `ml` | Makine Öğrenmesi | SVM, k-NN, karar ağaçları, rastgele orman |
| `objdetect` | Nesne Tespiti | Haar cascade, HOG+SVM dedektörleri, QR/barkod |
| `photo` | Fotoğraf İşleme | Gürültü giderme, HDR birleştirme, renk transferi |
| `stitching` | Panorama | Çoklu görüntü birleştirme, sferikal projeksiyon |

> **💡 İpucu:** `cv2.getBuildInformation()` çıktısını okuyun. Hangi modüllerin etkinleştirildiği, CUDA desteği olup olmadığı ve hangi derleyiciyle derlendiği bu çıktıda görünür — özellikle ortam sorunlarını ayıklarken değerlidir.

## OpenCV 4.x / 5.0 Yenilikleri

### G-API: Grafik Tabanlı Pipeline

Geleneksel OpenCV kodu satır satır çalışır — her fonksiyon çağrısı hemen işlem yapar. G-API (Graph API) ise işlemleri önce bir hesaplama grafiği olarak tanımlar, sonra bir bütün olarak optimize edip çalıştırır. Bu, özellikle çok aşamalı boru hatlarında bellek bant genişliği kullanımını önemli ölçüde azaltır.

```python
import cv2 as cv

# G-API ile pipeline tanımı
g_in = cv.GMat()
g_gray = cv.gapi.BGR2Gray(g_in)
g_blur = cv.gapi.gaussianBlur(g_gray, (5, 5), 1.5)
g_edges = cv.gapi.Canny(g_blur, 50, 150)
comp = cv.GComputation(g_in, g_edges)

# Çalıştırma — pipeline optimize edilmiş şekilde bir kez geçirilir
img = cv.imread("goruntu.jpg")
result = comp.apply(img)
```

### Gelişmiş DNN Modülü

OpenCV 4.7+ ile gelen ONNX Runtime entegrasyonu, model uyumluluğunu önemli ölçüde genişletti. `cv2.dnn.readNetFromONNX()` artık `opset 17`'ye kadar destekler; transformer tabanlı modeller çalışır.

### QR Kod ve Barkod Modülü

```python
import cv2
import numpy as np

img = cv2.imread("qr.jpg")
if img is None:
    raise FileNotFoundError("qr.jpg bulunamadı")

detector = cv2.QRCodeDetector()
data, points, _ = detector.detectAndDecode(img)

if data:
    print(f"QR içerik: {data}")
    # Köşe noktalarını görselleştir
    if points is not None:
        pts = points.astype(int).reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

cv2.imshow("QR Kod", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`cv2.barcode.BarcodeDetector` ile EAN-13, Code128 gibi 1D barkodlar da okunabilir — ek bağımlılık gerekmez.

## Kurulum ve İlk Kod

### Kurulum

```bash
# Temel kurulum — çoğu kullanım durumu için yeterli
pip install opencv-python numpy

# Katkı modülleri (SIFT ve ek algoritmalar dahil)
pip install opencv-contrib-python numpy

# Headless sunucu ortamı (GUI penceresi açmayacaksan — daha küçük boyut)
pip install opencv-python-headless numpy
```

> **⚠️ Dikkat:** `opencv-python` ve `opencv-contrib-python` aynı ortamda birlikte kurulamaz — ikisi de `cv2` modülünü sağlar ve çakışır. Birini seçip diğerini kaldırın: `pip uninstall opencv-python`.

### Sürüm ve Derleme Bilgileri

```python
import cv2
import numpy as np

# Sürüm bilgileri
print(f"OpenCV sürümü : {cv2.__version__}")
print(f"NumPy sürümü  : {np.__version__}")

# Derleme detayları — CUDA, OpenCL, optimizasyon bayrakları
build_info = cv2.getBuildInformation()

# Yalnızca ilgili satırları filtrele
for line in build_info.splitlines():
    if any(kw in line for kw in ("CUDA", "OpenCL", "AVX", "NEON", "Python")):
        print(line.strip())
```

Tipik çıktı:
```
OpenCV sürümü : 4.9.0
NumPy sürümü  : 1.26.4
  CUDA:                      YES (ver 12.2, CUFFT CUBLAS)
  OpenCL:                    YES (no extra features)
  AVX:                       YES
  Python 3:                  /usr/bin/python3 (ver 3.11.0)
```

### İlk Görüntü: Oku, Göster, Kaydet

```python
import cv2
import numpy as np

def goruntu_isle(giris_yolu: str, cikis_yolu: str) -> None:
    """Görüntüyü oku, temel bilgileri göster ve gri tonlamaya çevirip kaydet."""
    # Okuma
    img = cv2.imread(giris_yolu)
    if img is None:
        raise FileNotFoundError(f"{giris_yolu} bulunamadı")

    # Temel bilgiler
    yukseklik, genislik, kanal_sayisi = img.shape
    print(f"Boyut     : {genislik}x{yukseklik} piksel")
    print(f"Kanallar  : {kanal_sayisi}  (BGR sırası — OpenCV RGB okumaz!)")
    print(f"Veri tipi : {img.dtype}   (uint8 = 0-255 aralığı)")
    print(f"Bellek    : {img.nbytes / 1024:.1f} KB")

    # Renk uzayı dönüşümü
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Ekranda göster
    cv2.imshow("Orijinal", img)
    cv2.imshow("Gri Tonlama", gray)
    cv2.waitKey(0)           # Herhangi bir tuşa basılınca kapat
    cv2.destroyAllWindows()

    # Kaydet
    cv2.imwrite(cikis_yolu, gray)
    print(f"Kaydedildi: {cikis_yolu}")

if __name__ == "__main__":
    goruntu_isle("test.jpg", "test_gri.jpg")
```

> **⚠️ Dikkat:** OpenCV görüntüleri **BGR** sırasıyla okur, **RGB** değil. Matplotlib veya PyTorch'a görüntü geçirirken `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` ile dönüştürün — aksi hâlde renkler yanlış görünür.

### Kameradan Gerçek Zamanlı Görüntü

```python
import cv2

cap = cv2.VideoCapture(0)   # 0 = varsayılan kamera; dosya yolu da girilebilir
if not cap.isOpened():
    raise RuntimeError("Kamera açılamadı")

print(f"Çözünürlük : {cap.get(cv2.CAP_PROP_FRAME_WIDTH):.0f}x"
      f"{cap.get(cv2.CAP_PROP_FRAME_HEIGHT):.0f}")
print(f"FPS        : {cap.get(cv2.CAP_PROP_FPS):.1f}")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Basit işlem: yatay ayna
    mirrored = cv2.flip(frame, 1)
    cv2.imshow("Kamera", mirrored)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

> **💡 İpucu:** `cv2.waitKey(1)` bir milisaniye bekler ve basılan tuşun ASCII kodunu döndürür. `& 0xFF` maskesi, bazı platformlarda waitKey'in 32 bit döndürmesinden kaynaklanan sorunu giderir. Video döngülerinde her zaman bu kalıbı kullanın.

## Özet & İleri Okuma

- OpenCV, 2500+ algoritmayla bilgisayarlı görünün tek durağıdır; C++ çekirdeği Python arayüzüyle kullanılır.
- CUDA, OpenCL ve AVX desteği sayesinde aynı kod masaüstünden gömülü sisteme kadar optimize çalışır.
- `opencv-python` ile `opencv-contrib-python` aynı ortamda kurulamaz; ihtiyaca göre birini seçin.
- OpenCV **BGR** okur — Matplotlib, PyTorch veya web'e geçişte RGB dönüşümü unutulmamalıdır.
- G-API çok aşamalı pipeline'ları tek geçişte optimize ederek gereksiz bellek kopyasını ortadan kaldırır.
- `cap.release()` ve `cv2.destroyAllWindows()` video kodunun her çıkış yolunda çağrılmalıdır — aksi hâlde kamera kaynağı serbest bırakılmaz.
- `cv2.getBuildInformation()` ortam sorunlarını ayıklamada ilk bakılacak yerdir.

### Referanslar

- Bradski, G. (2000). "The OpenCV Library." *Dr. Dobb's Journal of Software Tools.* — kütüphanenin orijinal makalesi
- OpenCV Belgeleri: https://docs.opencv.org/4.x/
- OpenCV GitHub: https://github.com/opencv/opencv
- Kaehler, A. & Bradski, G. (2016). *Learning OpenCV 3.* O'Reilly Media.
