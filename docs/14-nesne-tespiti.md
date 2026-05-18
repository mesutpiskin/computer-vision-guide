# Nesne Tespiti

Fabrika bandında saniyede yüzlerce ürün geçiyor. Hatalı olanları insan gözüyle ayırt etmek hem yavaş hem hatalıdır. Kameranın her kareye bakıp "Bu ürün kusurlu, şu nesne yanlış konumda" demesi gerekiyor — bu tam olarak nesne tespitinin çözdüğü problemdir. Bu bölümde klasik Haar Cascade'den template matching'e, oradan modern YOLOv8'e kadar tespit yöntemlerini ve nasıl değerlendirileceğini öğreneceksiniz.

## Sınıflandırma mı, Tespit mi?

Bu iki kavram sıkça karıştırılır ama farklı sorulara cevap verir:

**Sınıflandırma:** "Bu görüntüde ne var?" → Tek bir cevap: "kedi"

**Tespit:** "Bu görüntüde ne var, nerede?" → Bounding box + sınıf + güven skoru: `[x1=120, y1=45, x2=380, y2=290, class="kedi", confidence=0.87]`

Fabrika bandı örneğinde sınıflandırma "ürün var" der, tespit ise "soldaki ürünün sol kenarında çatlak var, koordinatlar şunlar" der. Gerçek uygulamaların büyük çoğunluğu tespite ihtiyaç duyar.

## Haar Cascade: Klasik ve Hafif

2001'de Paul Viola ve Michael Jones'un geliştirdiği bu yöntem, derin öğrenme öncesi dönemin altın standardıydı. Hâlâ gömülü sistemlerde ve düşük kaynaklı ortamlarda kullanılır.

Çalışma mantığı: Görüntü üzerinde kayan pencere, her konumda Haar benzeri özellikler (yatay/dikey komşu bölgelerin parlaklık farkları) hesaplar. Güçlendirilmiş sınıflandırıcıların kademeli filtresi (cascade) hızla "nesne yok" kararı verir, "nesne var" olasılığı olan bölgeler detaylı incelenir.

```python
import cv2

img = cv2.imread("yuz.jpg")
if img is None:
    raise FileNotFoundError("yuz.jpg bulunamadı")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Önceden eğitilmiş model — OpenCV kurulumunda gelir
detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# scaleFactor: Her adımda görüntüyü ne kadar küçültür
# minNeighbors: Tespit için kaç komşu tespit gerekli (daha yüksek = az yanlış pozitif)
faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

print(f"{len(faces)} yüz tespit edildi")
cv2.imshow("Yüz Tespiti", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Haar Cascade hızlıdır ve kurulum gerektirmez. Ancak yalnızca eğitildiği nesne sınıfını tanır ve yüzü profilden gördüğünde ya da kötü aydınlatmada başarısız olur.

> **⚠️ Dikkat:** `scaleFactor=1.05` küçük yüzleri yakalar ama yavaşlar; `scaleFactor=1.3` hızlıdır ama küçük nesneleri kaçırır. Uygulamanıza göre ayarlayın.

## Template Matching: Şablon Arama

Bir üretim hattında sabit görünümlü vidalı bir kapak arıyorsunuz. Kapağın referans fotoğrafı var — template matching tam bu duruma özel.

Küçük şablon görüntüyü büyük görüntü üzerinde piksel piksel kaydırarak benzerlik hesaplar. `TM_CCOEFF_NORMED` yöntemi −1 ile +1 arasında değer döndürür; 1'e yakın değer güçlü eşleşmedir.

```python
import cv2
import numpy as np

img = cv2.imread("uretim_bandi.jpg")
template = cv2.imread("vida_sablon.jpg")
if img is None:
    raise FileNotFoundError("uretim_bandi.jpg bulunamadı")
if template is None:
    raise FileNotFoundError("vida_sablon.jpg bulunamadı")

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
tmpl_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
h, w = tmpl_gray.shape

result = cv2.matchTemplate(img_gray, tmpl_gray, cv2.TM_CCOEFF_NORMED)
_, max_val, _, max_loc = cv2.minMaxLoc(result)

print(f"En yüksek benzerlik: {max_val:.3f}")

if max_val > 0.8:  # Güven eşiği
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 2)
    cv2.putText(img, f"{max_val:.2f}", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

cv2.imshow("Template Matching", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Template matching nesne döndüğünde, ölçek değiştiğinde ya da kısmen örtüldüğünde başarısız olur. Kontrollü ortamda, sabit açıyla görünen nesneler için uygundur.

## YOLOv8: Modern Gerçek Zamanlı Tespit

YOLO (You Only Look Once) görüntüyü yalnızca bir kez işleyerek tüm nesneleri aynı anda tespit eder. R-CNN gibi önce "aday bölge öner, sonra sınıflandır" demez — tek geçişte hem nereyi hem neyi bulur.

Sezgi: Görüntüyü ızgara hücrelerine böl. Her hücre kendi bölgesinde nesne merkezi olup olmadığını, varsa sınıfını ve bounding box boyutlarını tahmin eder. Tüm tahminler aynı anda hesaplanır.

YOLOv8, Ultralytics tarafından geliştirilen modern versiyondur. `pip install ultralytics` ile kurulur.

```python
import cv2
from ultralytics import YOLO

# Model boyutları: n (nano) → s → m → l → x (extra-large)
# Daha büyük = daha doğru ama daha yavaş
model = YOLO("yolov8n.pt")  # İlk çalıştırmada otomatik indirilir

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # conf: minimum güven eşiği
    results = model.predict(frame, conf=0.5, verbose=False)

    # Tespit edilen her nesneyi çiz
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = f"{model.names[cls_id]} {conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("YOLOv8 Gerçek Zamanlı Tespit", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

`model.names` sözlüğü sınıf ID'sini "kişi", "araba", "bisiklet" gibi isimlere çevirir. COCO veri seti üzerinde eğitilmiş YOLOv8n 80 sınıfı tanır.

> **💡 İpucu:** `yolov8n` (nano) hızlı demo için idealdir, `yolov8x` (extra-large) maksimum doğruluk için. Üretim ortamında `yolov8s` veya `yolov8m` genellikle iyi denge sağlar.

> **📌 Not:** Kendi veri setinizde eğitmek için `model.train(data="dataset.yaml", epochs=100)` çağrısı yeterlidir. Ultralytics dokümantasyonu özel model eğitimi için adım adım rehber sunar.

## Değerlendirme Metrikleri

İyi bir tespit ne demektir? Sezgisel anlaşılması için somut örnekler:

**IoU (Intersection over Union):** "Tahmin kutusun gerçek kutuyla ne kadar örtüşüyor?"

Gerçek yöntemi sezgiyle açıklayalım: İki dikdörtgeni üst üste koyun. Kesişim alanı (ortak bölge) ne kadar büyükse, birleşim alanına (toplam kaplanan bölge) oranı o kadar yüksek.

$$\text{IoU} = \frac{|A \cap B|}{|A \cup B|}$$

IoU = 1.0 mükemmel örtüşme, IoU = 0.0 hiç örtüşme yok. Genellikle IoU > 0.5 "doğru tespit" sayılır.

**Precision:** Tespit ettiğin nesnelerin ne kadarı gerçekten doğru?

$$\text{Precision} = \frac{TP}{TP + FP}$$

"100 nesne tespit ettim, 85'i gerçekten nesneydi" → Precision = 0.85

**Recall:** Gerçek nesnelerin ne kadarını buldun?

$$\text{Recall} = \frac{TP}{TP + FN}$$

"Görüntüde 120 nesne vardı, ben 85'ini buldum" → Recall = 0.71

**mAP (mean Average Precision):** Farklı güven eşiklerinde hesaplanan average precision değerlerinin sınıflar üzerindeki ortalaması. YOLOv8n COCO'da mAP@0.5 yaklaşık 0.37, YOLOv8x ise 0.54'tür.

> **📌 Not:** Yüksek precision düşük recall anlamına gelebilir — model yalnızca çok emin olduğu nesneleri söyler, kaçırdıkları fazladır. Hedefin güvenlik sistemi mi yoksa envanter sayımı mı olduğuna göre hangisine öncelik vereceğiniz değişir.

## Yöntem Karşılaştırması

| Yöntem | Hız | Doğruluk | Kurulum | En İyi Kullanım |
|--------|-----|----------|---------|-----------------|
| Haar Cascade | Çok hızlı | Düşük-orta | Sıfır | Yüz tespiti, gömülü sistem |
| Template Matching | Hızlı | Değişken | Sıfır | Sabit görünümlü nesne arama |
| YOLOv8n (nano) | ~60 FPS CPU | Orta | pip install | Gerçek zamanlı demo |
| YOLOv8x (xlarge) | ~10 FPS GPU | Çok yüksek | pip install | Maksimum doğruluk |

## Özet

- Nesne tespiti sınıflandırmadan farklıdır: konum bilgisi (bounding box) de döndürür.
- Haar Cascade 2001'den bu yana hâlâ geçerlidir; hafif ve hızlıdır ama tek sınıf, cephe görüşü gerektirir.
- Template matching nesne görünümü sabitse kontrollü ortamlarda güvenilirdir.
- YOLO single-shot mimariyle görüntüyü tek geçişte işler; R-CNN tabanlı yöntemlere göre çok daha hızlıdır.
- YOLOv8 `pip install ultralytics` ile kurulur; `model.predict()` tek satırda çalışır.
- IoU tespitin geometrik doğruluğunu, precision/recall ise sınıflandırma performansını ölçer.
- mAP, farklı eşik değerlerindeki precision'ın ortalamasıdır — tek sayıyla genel performansı özetler.

## İleri Okuma

- Viola & Jones, "Rapid Object Detection using a Boosted Cascade of Simple Features" (CVPR 2001) — Haar Cascade'in orijinal makalesi
- Redmon & Farhadi, "YOLOv3: An Incremental Improvement" (2018): https://arxiv.org/abs/1804.02767
- Jocher et al., Ultralytics YOLOv8 Dokümantasyonu: https://docs.ultralytics.com
- Everingham et al., "The Pascal Visual Object Classes (VOC) Challenge" (IJCV 2010) — mAP metriğinin standart tanımı
