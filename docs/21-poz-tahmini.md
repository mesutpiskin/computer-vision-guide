**Poz Tahmini (Pose Estimation)**
----------------------------------

Poz tahmini, görüntü veya video üzerindeki insan vücudunun eklem noktalarını (keypoint) tespit ederek iskelet yapısını çıkarmayı amaçlar. Güvenlik kameraları, spor analizi, rehabilitasyon takibi ve insan-bilgisayar etkileşimi gibi alanlarda yaygın kullanım alanı bulur.

## Temel Kavramlar

**Keypoint (Anahtar Nokta):** Dirsek, diz, omuz, kalça gibi vücut eklemlerinin görüntü üzerindeki koordinatları.

**Skeleton (İskelet):** Anahtar noktaların birbirine bağlanmasıyla oluşan stick-figure temsil.

**Single-person vs Multi-person:** Tek kişi veya çoklu kişi tespiti. Çoklu kişi tespiti (bottom-up veya top-down yaklaşım) daha karmaşıktır.

---

### Teorik Temel — Poz Tahmini

**Keypoint Heatmap:**
Her keypoint $k$ için Gaussian heatmap:
$$S_k(p) = \exp\left(-\frac{\|p - p_k^*\|_2^2}{2\sigma^2}\right)$$
$p_k^*$: gerçek keypoint konumu, $\sigma$: yayılım parametresi.

**OKS (Object Keypoint Similarity) — COCO Metriği:**
$$\text{OKS} = \frac{\sum_i \exp\left(-d_i^2 / 2s^2\sigma_i^2\right) \cdot \delta(v_i > 0)}{\sum_i \delta(v_i > 0)}$$
$d_i$: tahmin/gerçek mesafesi, $s$: nesne ölçeği, $\sigma_i$: keypoint tipine özgü sabit.
OKS, IoU'nun keypoint tespitine uyarlanmış halidir.

Referans: Cao et al., "OpenPose: Realtime Multi-Person 2D Pose Estimation", IEEE TPAMI 2021 (https://arxiv.org/abs/1812.08008)

---

## MediaPipe Pose ile Poz Tahmini

MediaPipe Pose, Google tarafından geliştirilen ve mobil cihazlarda gerçek zamanlı çalışabilen hafif bir poz tahmini çözümüdür. 33 anahtar nokta tespit eder.

```bash
pip install mediapipe
```

### Gerçek Zamanlı Poz Tespiti

```python
import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    model_complexity=1  # 0=Lite, 1=Full, 2=Heavy
) as pose:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style()
            )

        cv2.imshow("MediaPipe Pose", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
```

### Anahtar Nokta Koordinatlarına Erişim

```python
import mediapipe as mp
import cv2

mp_pose = mp.solutions.pose

img = cv2.imread("insan.jpg")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

with mp_pose.Pose(static_image_mode=True) as pose:
    results = pose.process(rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        h, w = img.shape[:2]

        # Sol omuz koordinatları
        sol_omuz = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        x = int(sol_omuz.x * w)
        y = int(sol_omuz.y * h)
        print(f"Sol Omuz: ({x}, {y}), Görünürlük: {sol_omuz.visibility:.2f}")

        # Tüm landmark isimleri
        for idx, lm in enumerate(mp_pose.PoseLandmark):
            print(f"{idx}: {lm.name}")
```

### Açı Hesaplama (Hareket Analizi)

```python
import numpy as np
import mediapipe as mp
import cv2

def calculate_angle(a, b, c):
    """Üç nokta arasındaki açıyı hesapla (b merkez nokta)"""
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180 else angle

mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            h, w = frame.shape[:2]

            # Dirsek açısı (sol kol)
            omuz = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w,
                    lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h]
            dirsek = [lm[mp_pose.PoseLandmark.LEFT_ELBOW].x * w,
                      lm[mp_pose.PoseLandmark.LEFT_ELBOW].y * h]
            bilek = [lm[mp_pose.PoseLandmark.LEFT_WRIST].x * w,
                     lm[mp_pose.PoseLandmark.LEFT_WRIST].y * h]

            angle = calculate_angle(omuz, dirsek, bilek)
            cv2.putText(frame, f"{angle:.1f}°",
                        tuple(map(int, dirsek)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        cv2.imshow("Açı Analizi", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
```

---

## YOLOv8 Pose ile Çoklu Kişi Poz Tespiti

Ultralytics YOLOv8-pose modeli, aynı anda birden fazla kişinin poz tespitini yapar.

```bash
pip install ultralytics
```

```python
from ultralytics import YOLO
import cv2

model = YOLO("yolov8n-pose.pt")

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, stream=True)
    for result in results:
        annotated = result.plot()
        cv2.imshow("YOLOv8 Pose", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

Tespit edilen her kişi için 17 anahtar nokta (COCO formatı) döndürülür.

```python
for result in results:
    if result.keypoints is not None:
        for person_kps in result.keypoints.xy:
            # person_kps: (17, 2) tensor — her satır bir anahtar noktanın x,y koordinatı
            burun = person_kps[0]
            sol_omuz = person_kps[5]
            sag_omuz = person_kps[6]
            print(f"Burun: {burun}, Sol Omuz: {sol_omuz}")
```

---

## Karşılaştırma

| Çözüm | Kişi Sayısı | Hız | Doğruluk | Notlar |
|-------|------------|-----|---------|--------|
| MediaPipe Pose | Tek/Çoklu | ★★★★★ | ★★★★ | Mobil uyumlu |
| YOLOv8-pose | Çoklu | ★★★★ | ★★★★★ | GPU önerilir |
| OpenPose | Çoklu | ★★ | ★★★★★ | CUDA zorunlu |

---

### MediaPipe Açı Hesaplama — Kapsamlı Örnek

```python
import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    """Üç nokta arasındaki açıyı hesapla (derece)."""
    v1 = np.array(a) - np.array(b)
    v2 = np.array(c) - np.array(b)
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
    return np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Kamera açılamadı")

with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
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
            lms = results.pose_landmarks.landmark
            # Sol dirsek açısı: omuz (11) → dirsek (13) → bilek (15)
            shoulder = [lms[11].x, lms[11].y]
            elbow    = [lms[13].x, lms[13].y]
            wrist    = [lms[15].x, lms[15].y]
            angle = calculate_angle(shoulder, elbow, wrist)
            cv2.putText(frame, f"Dirsek: {angle:.1f}",
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Poz Tahmini", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
```

### Özet & İleri Okuma
- Keypoint heatmap her eklem için Gaussian olasılık haritası üretir
- OKS, IoU'nun keypoint tespitine uyarlanmış versiyonudur; COCO benchmark kullanır
- MediaPipe 33 vücut landmarkını gerçek zamanlı tespit eder
- Landmark koordinatları normalize [0,1] aralığında; görüntü boyutuna çarpılmalı
- calculate_angle fonksiyonu herhangi üç landmark arası açı hesaplar
- Referans: OpenPose (https://arxiv.org/abs/1812.08008)
