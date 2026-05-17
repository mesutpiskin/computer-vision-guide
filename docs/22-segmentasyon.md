**Segmentasyon (Semantic & Instance Segmentation)**
----------------------------------------------------

Nesne tespiti bir nesnenin nerede olduğunu dikdörtgen bir kutu ile gösterirken, segmentasyon piksel düzeyinde nesnelerin sınırlarını çizer. Bu bölümde semantik segmentasyon, örnek segmentasyonu ve segment anything modelini ele alacağız.

## Segmentasyon Türleri

* **Semantik Segmentasyon:** Her piksele bir sınıf etiketi atar. Yol, araç, insan gibi. Birden fazla insanı birbirinden ayırt etmez.
* **Örnek Segmentasyonu (Instance Segmentation):** Her nesne örneğini ayrı ayrı maskeler. 3 farklı insan, 3 farklı maske.
* **Panoptik Segmentasyon:** Semantik + Instance — hem saydılabilir hem sayılamaz nesneleri birlikte işler.

---

### Teorik Temel — Segmentasyon

**Semantic vs Instance Segmentation:**
- Semantic: her piksel → sınıf etiketi (aynı sınıf, tek renk)
- Instance: her nesne örneği ayrı maske
- Panoptic: ikisinin birleşimi

**mIoU (Mean Intersection over Union):**
$$\text{mIoU} = \frac{1}{C}\sum_{c=1}^C \frac{TP_c}{TP_c + FP_c + FN_c}$$
$C$: sınıf sayısı. Segmentasyonun standart değerlendirme metriği.

**SAM (Segment Anything Model) Bileşenleri:**
1. Image Encoder: ViT-H ile görüntü embedding (1024 boyut)
2. Prompt Encoder: nokta/kutu/maske prompt'u kodlar
3. Mask Decoder: 2 katmanlı transformer ile maske üretir

Zero-shot: eğitim görmediği nesneleri segmente eder.

Referans: He et al., "Mask R-CNN", ICCV 2017 (https://arxiv.org/abs/1703.06870)
Referans: Kirillov et al., "Segment Anything", ICCV 2023 (https://arxiv.org/abs/2304.02643)

---

## YOLOv8 ile Instance Segmentasyon

```bash
pip install ultralytics
```

```python
from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolov8n-seg.pt")

img = cv2.imread("sahne.jpg")
results = model(img)

for result in results:
    if result.masks is not None:
        masks = result.masks.data.cpu().numpy()
        boxes = result.boxes
        for i, mask in enumerate(masks):
            mask = (mask * 255).astype(np.uint8)
            mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
            color = np.random.randint(0, 255, 3).tolist()
            colored = np.zeros_like(img)
            colored[:] = color
            img = np.where(mask[:, :, np.newaxis] > 128,
                           cv2.addWeighted(img, 0.5, colored, 0.5, 0),
                           img)

cv2.imshow("YOLOv8 Segmentasyon", img)
cv2.waitKey(0)
```

**Görsel çıktıyı otomatik oluştur:**
```python
results = model("sahne.jpg")
for result in results:
    annotated = result.plot()
    cv2.imshow("Segmentasyon", annotated)
    cv2.waitKey(0)
```

---

## SAM (Segment Anything Model) ile Segmentasyon

SAM, Meta AI tarafından geliştirilen ve herhangi bir nesneyi nokta veya kutu verilen prompt ile segmente edebilen temel bir modeldir.

```bash
pip install segment-anything
# Model ağırlığı: https://github.com/facebookresearch/segment-anything#model-checkpoints
# wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
```

**Nokta tabanlı segmentasyon:**

```python
import cv2
import numpy as np
from segment_anything import sam_model_registry, SamPredictor

sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b_01ec64.pth")
predictor = SamPredictor(sam)

img = cv2.imread("nesne.jpg")
predictor.set_image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Nesnenin üzerindeki bir noktayı ver
input_point = np.array([[250, 300]])  # x, y koordinatı
input_label = np.array([1])  # 1=ön plan, 0=arka plan

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True
)

# En iyi maskeyi seç
best_mask = masks[np.argmax(scores)]
overlay = img.copy()
overlay[best_mask] = [0, 120, 255]
result = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)
cv2.imshow("SAM Segmentasyon", result)
cv2.waitKey(0)
```

**Kutu tabanlı segmentasyon:**

```python
input_box = np.array([100, 150, 400, 500])  # x1, y1, x2, y2

masks, scores, _ = predictor.predict(
    box=input_box[np.newaxis, :],
    multimask_output=False
)
```

**SAM2 (2024):**
SAM2, video segmentasyonu desteği ekleyen güncel versiyondur.

```bash
pip install sam2
```

```python
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

model = build_sam2("sam2_hiera_small.yaml", "sam2_hiera_small.pt")
predictor = SAM2ImagePredictor(model)
predictor.set_image(img_rgb)
masks, scores, _ = predictor.predict(point_coords=input_point,
                                      point_labels=input_label)
```

---

## OpenCV DNN ile Semantik Segmentasyon

```python
import cv2
import numpy as np

# DeepLab v3+ PASCAL VOC modeli
net = cv2.dnn.readNetFromTensorflow(
    "deeplabv3_mnv2_pascal_train_aug_2018_01_29.pb"
)

img = cv2.imread("sahne.jpg")
blob = cv2.dnn.blobFromImage(img, 1.0/127.5, (513, 513), (127.5, 127.5, 127.5))
net.setInput(blob)
score = net.forward()

# Sınıf haritası
classmap = np.argmax(score[0], axis=0)
classmap = cv2.resize(classmap.astype(np.uint8),
                      (img.shape[1], img.shape[0]),
                      interpolation=cv2.INTER_NEAREST)

# Renklendirme
colored = cv2.applyColorMap(classmap * 10, cv2.COLORMAP_JET)
result = cv2.addWeighted(img, 0.5, colored, 0.5, 0)
cv2.imshow("Semantik Segmentasyon", result)
cv2.waitKey(0)
```

---

## Karşılaştırma

| Yöntem | Tip | Hız | Doğruluk | Notlar |
|--------|-----|-----|---------|--------|
| YOLOv8-seg | Instance | ★★★★ | ★★★★ | Çoklu nesne |
| SAM / SAM2 | Interactive | ★★ | ★★★★★ | Prompt tabanlı |
| DeepLab DNN | Semantic | ★★★ | ★★★ | OpenCV ile doğrudan |

---

### YOLOv8-seg — Kapsamlı Örnek

```python
from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolov8n-seg.pt")

img = cv2.imread("resim.jpg")
if img is None:
    raise FileNotFoundError("resim.jpg bulunamadı")

results = model.predict(img, conf=0.5, verbose=False)
result = results[0]

output = img.copy()
if result.masks is not None:
    masks = result.masks.data.cpu().numpy()   # (N, H, W)
    classes = result.boxes.cls.cpu().numpy()
    names = model.names

    for i, (mask, cls) in enumerate(zip(masks, classes)):
        mask_resized = cv2.resize(mask, (img.shape[1], img.shape[0]))
        mask_bool = mask_resized > 0.5

        color = np.random.randint(50, 200, 3).tolist()
        output[mask_bool] = (output[mask_bool] * 0.5 + np.array(color) * 0.5).astype(np.uint8)

        contours, _ = cv2.findContours(
            mask_resized.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        cv2.drawContours(output, contours, -1, color, 2)
        print(f"Nesne {i+1}: {names[int(cls)]}")

cv2.imshow("YOLOv8 Segmentasyon", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Özet & İleri Okuma
- Semantic segmentation her piksele sınıf, instance segmentation her nesneye ayrı maske atar
- mIoU standart segmentasyon metriğidir; sınıf başına IoU ortalamasıdır
- YOLOv8-seg tek geçişte nesne tespiti ve instance segmentation yapar
- SAM zero-shot çalışır: nokta veya kutu prompt ile herhangi bir nesneyi segmente eder
- Mask R-CNN ROIAlign ile piksel hizalı maske üretir
- Referans: Mask R-CNN (https://arxiv.org/abs/1703.06870), SAM (https://arxiv.org/abs/2304.02643)
