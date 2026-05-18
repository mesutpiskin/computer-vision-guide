# Segmentasyon

Patoloji laboratuvarında bir mikroskop görüntüsünde tümör hücrelerini tespit etmek istiyorsunuz. Nesne tespiti size "bu bölgede tümör var" diyebilir, ama "tam olarak hangi pikseller tümöre ait?" sorusunu yanıtlamaz. Hücre sınırını piksel düzeyinde çizmeniz gerekir: kaç hücre var, toplam alan ne kadar, birbirine bitişik mi? Bu bölümde görüntüdeki her pikseli doğru nesne veya sınıfa atayan segmentasyon yöntemlerini öğreneceğiz.

## Segmentasyon Türleri

Üç farklı segmentasyon yaklaşımı vardır ve hangi soruyu sorduğunuza göre seçim yapılır.

**Semantik segmentasyon:** Her piksel bir sınıfa atanır. Görüntüde beş insan varsa hepsi "insan" sınıfına girer — birbirinden ayırt edilmez. "Bu görüntünün neresinde yol var, neresinde bina var?" sorusunu yanıtlar.

**Örnek segmentasyonu (Instance segmentation):** Her nesne bağımsızdır. Beş insan varsa "insan_1", "insan_2", ... olarak ayrı maskeler alır. "Kaç hücre var ve her biri nerede?" sorusunu yanıtlar.

**Panoptik segmentasyon:** İkisini birleştirir. Sayılabilir nesneler (insan, araba) örnek segmentasyonuyla; arka plan sınıfları (gökyüzü, yol, zemin) semantik segmentasyonla işlenir.

| Tür | Her nesne ayrı mı? | Arka plan sınıfı var mı? | Örnek Kullanım |
|-----|-------------------|--------------------------|----------------|
| Semantik | Hayır | Evet | Sürücüsüz araç şerit tespiti |
| Örnek | Evet | Hayır | Hücre sayma, kalabalık analizi |
| Panoptik | Evet | Evet | Sahne anlama, otonom navigasyon |

## Klasik Yöntem: Watershed

Görüntüyü bir arazi haritası gibi düşünün: parlak bölgeler dağ tepesi, karanlık bölgeler vadi. Vadiyi su ile doldurun — suların birleşmeden önce kenarlar oluşturduğu sınırlar, nesnelerin sınırlarıdır. Bu sezgiden türeyen Watershed algoritması, şekli önceden bilinen nesneleri (hücreler, mineral tanecikleri) ayırmak için kullanılır.

```python
import cv2
import numpy as np

def watershed_hucre_say(goruntu_yolu: str) -> int:
    """Watershed ile parlak nesneleri (hücreler) say ve say."""
    img = cv2.imread(goruntu_yolu)
    if img is None:
        raise FileNotFoundError(f"{goruntu_yolu} bulunamadı")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Eşikleme — parlak hücreler beyaz
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Gürültü gider
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Kesin arka plan ve ön plan bölgeleri
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
    sure_fg = sure_fg.astype(np.uint8)

    # Belirsiz bölge
    unknown = cv2.subtract(sure_bg, sure_fg)

    # İşaretçi (marker) matrisi
    _, markers = cv2.connectedComponents(sure_fg)
    markers += 1
    markers[unknown == 255] = 0

    # Watershed uygula
    cv2.watershed(img, markers)
    img[markers == -1] = [0, 0, 255]   # Sınırları kırmızı yap

    # Her bölgeye farklı renk ver
    hucre_sayisi = markers.max() - 1   # 1 = arka plan
    print(f"Tespit edilen hücre sayısı: {hucre_sayisi}")

    cv2.imshow("Watershed Sonucu", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return int(hucre_sayisi)

if __name__ == "__main__":
    sayi = watershed_hucre_say("hucreler.jpg")
```

> **💡 İpucu:** Watershed, nesnelerin birbirine yakın veya temas hâlinde olduğu durumlarda (hücreler, mineral tanecikleri) klasik eşiklemenin başarısız olduğu yerlerde parlar. Mesafe dönüşümü (distance transform) her pikselin en yakın arka plana olan uzaklığını hesaplar — bu uzaklık haritasındaki tepe noktaları her nesnenin merkezi olur.

## YOLOv8-seg: Gerçek Zamanlı Örnek Segmentasyonu

YOLOv8, nesne tespiti boru hattının üstüne piksel maskesi üretmeyi de ekler. Nesne tespit başlığı (head) yanında bir maske başlığı daha çalışır — her tespit kutusu için ikili (binary) piksel maskesi üretir.

```bash
pip install ultralytics opencv-python numpy
```

```python
import cv2
import numpy as np
from ultralytics import YOLO

def yolov8_segmentasyon_kamera() -> None:
    """YOLOv8-seg ile kameradan gerçek zamanlı örnek segmentasyonu."""
    model = YOLO("yolov8n-seg.pt")   # Nano model; hız öncelikli

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Kamera açılamadı")

    # Renk paleti — her sınıfa sabit renk
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(80, 3), dtype=np.uint8)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)
        overlay = frame.copy()

        if results[0].masks is not None:
            masks = results[0].masks.data.cpu().numpy()    # (N, H, W)
            boxes = results[0].boxes
            h, w = frame.shape[:2]

            for i, mask in enumerate(masks):
                # Maske orijinal boyuta ölçeklendir
                mask_resized = cv2.resize(mask, (w, h))
                mask_bool = mask_resized > 0.5

                # Sınıf rengini al
                cls_id = int(boxes.cls[i].item())
                color = colors[cls_id % len(colors)].tolist()

                # Yarı saydam renk bindirme
                overlay[mask_bool] = (
                    overlay[mask_bool] * 0.4 + np.array(color) * 0.6
                ).astype(np.uint8)

                # Etiket
                conf = float(boxes.conf[i].item())
                label = f"{model.names[cls_id]} {conf:.2f}"
                x1, y1 = int(boxes.xyxy[i][0]), int(boxes.xyxy[i][1])
                cv2.putText(overlay, label, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Orijinal ve overlay'i karıştır
        result_frame = cv2.addWeighted(frame, 0.3, overlay, 0.7, 0)
        cv2.imshow("YOLOv8-seg", result_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    yolov8_segmentasyon_kamera()
```

`results[0].masks.data` tensörü `(N, H, W)` boyutundadır — N tespit sayısı, H ve W küçük ölçekli maske boyutlarıdır. Orijinal görüntü boyutuna ölçeklendirmek için `cv2.resize` gerekir.

> **⚠️ Dikkat:** Maske tensörü CUDA'daysa önce `.cpu()` ile CPU'ya, sonra `.numpy()` ile NumPy dizisine dönüştürün. Aynı anda ikisini atlarsanız hata alırsınız.

## SAM: Evrensel Segmentasyon

Meta'nın Segment Anything Model (SAM) modeli eğitim gerektirmeyen bir segmentasyon paradigması sunar: bir noktaya tıklayın, o noktanın ait olduğu nesnenin maskesi çıkar. Dikdörtgen çizin, içindeki nesneyi segmente eder. 1 milyarı aşkın maskeli görüntü üzerinde eğitilen SAM, hiç görmediği nesne türlerinde de genelleme yapar.

```bash
pip install segment-anything
# Model ağırlıkları (vit_b ≈ 375 MB)
# wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
```

```python
import cv2
import numpy as np
from segment_anything import sam_model_registry, SamPredictor

def sam_nokta_segmentasyon(goruntu_yolu: str, nokta_x: int, nokta_y: int) -> None:
    """SAM ile tek nokta girerek nesne segmentasyonu yap."""
    img = cv2.imread(goruntu_yolu)
    if img is None:
        raise FileNotFoundError(f"{goruntu_yolu} bulunamadı")

    # SAM RGB bekler
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Model yükleme (vit_b, vit_l, vit_h)
    sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b_01ec64.pth")
    predictor = SamPredictor(sam)
    predictor.set_image(img_rgb)

    # Tahmin — nokta koordinatı ve etiket (1 = ön plan, 0 = arka plan)
    masks, scores, _ = predictor.predict(
        point_coords=np.array([[nokta_x, nokta_y]]),
        point_labels=np.array([1]),
        multimask_output=True   # 3 alternatif maske üret
    )

    # En yüksek skorlu maskeyi seç
    en_iyi = np.argmax(scores)
    maske = masks[en_iyi]

    print(f"Maske skoru   : {scores[en_iyi]:.3f}")
    print(f"Maske alanı   : {maske.sum()} piksel "
          f"({100 * maske.mean():.1f}% görüntü)")

    # Görselleştir
    overlay = img.copy()
    overlay[maske] = (overlay[maske] * 0.4 + np.array([0, 120, 255]) * 0.6).astype(np.uint8)
    cv2.circle(overlay, (nokta_x, nokta_y), 8, (255, 0, 0), -1)

    cv2.imshow("SAM Segmentasyon", overlay)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("sam_sonuc.jpg", overlay)
    print("sam_sonuc.jpg kaydedildi.")

if __name__ == "__main__":
    sam_nokta_segmentasyon("laboratuvar.jpg", nokta_x=320, nokta_y=240)
```

`multimask_output=True` ile SAM üç farklı granülaritede maske üretir (parça, nesne, grup). Çoğu durumda en yüksek skorlu maske istenen segmenti verir.

> **📌 Not:** SAM büyük model ağırlıkları gerektirir (vit_b: 375 MB, vit_h: 2.4 GB). Gerçek zamanlı uygulamalar için daha hafif MobileSAM veya EfficientSAM türevlerini inceleyebilirsiniz.

## Değerlendirme: IoU ve mIoU

Tahmin maskesi ne kadar doğru? Bunu ölçmek için **IoU (Intersection over Union)** kullanılır.

Sezgi: Modelin tahmin ettiği maske ile gerçek maskenin örtüşme oranı. Tam örtüşme → 1, hiç örtüşme yok → 0.

$$\text{IoU} = \frac{|P \cap G|}{|P \cup G|}$$

Payı kesişim (her iki maskede de 1 olan piksel sayısı), paydası birleşim (en az birinde 1 olan piksel sayısı).

```python
import numpy as np

def iou_hesapla(tahmin: np.ndarray, gercek: np.ndarray) -> float:
    """
    İki ikili maske arasında IoU hesapla.
    tahmin, gercek: bool veya uint8 (0/1) ndarray
    """
    tahmin = tahmin.astype(bool)
    gercek = gercek.astype(bool)

    kesisim = (tahmin & gercek).sum()
    birlesim = (tahmin | gercek).sum()

    if birlesim == 0:
        return 1.0   # Her ikisi de boşsa mükemmel örtüşme

    return float(kesisim) / float(birlesim)

def miou_hesapla(tahminler: list, gercekler: list) -> float:
    """Birden fazla sınıf veya örnek için mIoU hesapla."""
    iou_degerleri = [iou_hesapla(t, g) for t, g in zip(tahminler, gercekler)]
    return float(np.mean(iou_degerleri))

# Test
pred = np.array([[1, 1, 0], [1, 0, 0]], dtype=bool)
gt   = np.array([[1, 1, 1], [0, 0, 0]], dtype=bool)
print(f"IoU: {iou_hesapla(pred, gt):.3f}")   # 2/4 = 0.5
```

**mIoU (mean IoU)**, tüm sınıflar veya örnekler üzerinden IoU değerlerinin ortalamasıdır. Segmentasyon modellerinin standart değerlendirme metriğidir; raporlarda "COCO val mIoU" olarak görürsünüz.

> **💡 İpucu:** IoU 0.5 eşiği yaygın kabul görmüş bir başarı kriteri olarak kullanılır (PASCAL VOC standardı). Tıbbi görüntülemede genellikle daha yüksek eşikler (0.7-0.9) beklenir.

## Yöntem Karşılaştırması

| Yöntem | Hız | Doğruluk | Eğitim Gerekir mi? | En İyi Kullanım |
|--------|-----|----------|-------------------|-----------------|
| **Watershed** | Çok hızlı | Sınırlı | Hayır | Bilinen şekilli nesneler, hücre sayımı |
| **YOLOv8n-seg** | Hızlı (~30 FPS GPU) | Orta-yüksek | Fine-tune opsiyonel | Gerçek zamanlı, çok sınıflı |
| **YOLOv8x-seg** | Yavaş (~5 FPS GPU) | Çok yüksek | Fine-tune opsiyonel | Hassasiyet kritik uygulamalar |
| **SAM (vit_b)** | Orta | Çok yüksek | Hayır | İnteraktif segmentasyon, veri etiketleme |

> **📌 Not:** SAM gerçek zamanlı video için çok yavaştır; ancak veri etiketleme araçlarına (Roboflow, Label Studio) entegre edilerek etiketleme iş yükünü büyük ölçüde azaltır.

## Özet & İleri Okuma

- Semantik segmentasyon piksel sınıfını verir, örnek segmentasyonu her nesneyi ayrı tutar, panoptik ise ikisini birleştirir.
- Watershed, mesafe dönüşümü ve işaretçi tabanlı yaklaşımıyla temas eden nesneleri ayırmada klasik bir araçtır.
- YOLOv8-seg `results[0].masks.data` ile `(N, H, W)` boyutlu maske tensörü döndürür; orijinal boyuta `cv2.resize` ile ölçeklendirilir.
- Yarı saydam maske bindirmesi için `cv2.addWeighted` veya NumPy alfa karıştırması kullanılır.
- SAM eğitim gerektirmeden nokta/kutu girdisiyle herhangi bir nesneyi segmente eder; vit_b modeli 375 MB'tır.
- IoU, tahmin ve gerçek maske örtüşmesini 0-1 arasında ölçer; mIoU tüm sınıflar üzerinden ortalamasıdır.
- Maske tensörü CUDA'daysa `.cpu().numpy()` dönüşümü unutulmamalıdır.

### Referanslar

- He, K. et al. (2017). "Mask R-CNN." *ICCV 2017*: https://arxiv.org/abs/1703.06870
- Kirillov, A. et al. (2023). "Segment Anything." *ICCV 2023*: https://arxiv.org/abs/2304.02643
- Jocher, G. et al. (2023). "Ultralytics YOLOv8." https://github.com/ultralytics/ultralytics
- Watershed Belgeleri (OpenCV): https://docs.opencv.org/4.x/d3/db4/tutorial_py_watershed.html
