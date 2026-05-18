# Poz Tahmini

Spor salonunda squat yapan bir kişinin diz açısını gerçek zamanlı olarak ölçmek istiyorsunuz: açı 90°'nin altına inince sayacı artırın, tekrar 160°'nin üstüne çıkınca hazır duruma geçin. Ya da bir fizik tedavi kliniğinde hastanın omuz hizasını ve bel açısını otomatik olarak değerlendirin. Her iki senaryo da aynı temel soruyu sorar: görüntüdeki insan vücudunun eklem noktaları nerede? Bu bölümde bu soruyu gerçek zamanlı çözen araçları öğreneceğiz.

## Poz Tahmini Nedir?

İnsan vücudundaki anatomik anahtar noktaların (keypoint) görüntü koordinatlarını tespit etmek ve bu noktalardan iskelet yapısını oluşturmak, poz tahminin (pose estimation) tanımıdır.

**COCO veri seti standardı** 17 anahtar nokta tanımlar: burun, sol/sağ göz, sol/sağ kulak, sol/sağ omuz, sol/sağ dirsek, sol/sağ bilek, sol/sağ kalça, sol/sağ diz, sol/sağ ayak bileği. Her nokta için model üç değer çıkarır: piksel koordinatları `(x, y)` ve güven skoru `visibility`.

Güven skoru 0 ile 1 arasındadır — noktanın görüntüde var olup olmadığını ve modelin ne kadar emin olduğunu gösterir. Kameranın dışında kalan veya başka bir nesnenin arkasında gizlenen uzuvlar düşük güven skoruyla işaretlenir.

> **📌 Not:** Poz tahmini, nesne tespitinden farklıdır. Nesne tespiti "burada bir insan var" der; poz tahmini "bu insanın diz noktası şurada" der. İkisi genellikle ardışık çalışır.

## MediaPipe Pose

Google'ın MediaPipe kütüphanesi, poz tahmini için hafif ve gerçek zamanlı bir çözüm sunar. Masaüstü bilgisayarlarda 30+ FPS'de çalışırken mobil cihazlarda da akıcı kalır. COCO'nun 17 noktasına ek olarak el parmaklarını ve yüz noktalarını da kapsayan **33 landmark** tanımlar.

```bash
pip install mediapipe opencv-python numpy
```

```python
import cv2
import mediapipe as mp
import numpy as np

def kamera_poz_tespiti() -> None:
    """MediaPipe Pose ile kameradan gerçek zamanlı iskelet tespiti."""
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Kamera açılamadı")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # MediaPipe RGB bekler — BGR'den dönüştür
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            # İskeleti çiz
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            # Sol omuz koordinatlarını al
            landmarks = results.pose_landmarks.landmark
            sol_omuz = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]

            if sol_omuz.visibility > 0.5:
                h, w = frame.shape[:2]
                cx = int(sol_omuz.x * w)
                cy = int(sol_omuz.y * h)
                cv2.circle(frame, (cx, cy), 8, (0, 255, 255), -1)
                cv2.putText(frame, "Sol Omuz", (cx + 10, cy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        cv2.imshow("MediaPipe Pose", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    pose.close()

if __name__ == "__main__":
    kamera_poz_tespiti()
```

> **⚠️ Dikkat:** Görünürlük (`visibility`) skoru 0.5'in altındaki noktaları hesaplara katmayın — o nokta kameranın dışında veya başka bir nesnenin arkasında olabilir. Düşük güven skorlu nokta koordinatları anlamsız olabilir.

MediaPipe landmark koordinatları **normalize** gelir: `x` ve `y` değerleri görüntü genişliği/yüksekliğine bölünmüş 0-1 aralığındadır. Piksel koordinatına çevirmek için `int(landmark.x * width)` kullanın.

## Açı Hesaplama

İskelet noktaları elimizde; şimdi eklem açılarını ölçeceğiz. Üç nokta ver: A (omuz), B (dirsek), C (bilek) — dirsek açısını hesapla.

İki vektör tanımlanır: **BA** (dirseğden omuza) ve **BC** (dirseğden bileğe). Bu vektörler arasındaki açı, eklem açısıdır.

`np.arccos` yaklaşımı, büyük açılarda sayısal kararsızlığa yol açabilir. `np.arctan2` ise iki bileşeni ayrı ayrı aldığı için tüm açı aralığında kararlıdır ve işaret belirsizliği yaşamaz.

```python
import numpy as np

def aci_hesapla(a: list, b: list, c: list) -> float:
    """
    Üç nokta verilen B'deki açıyı derece cinsinden hesapla.
    a, b, c: [x, y] koordinat listeleri
    """
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    # b merkezli vektörler
    ba = a - b
    bc = c - b

    # arctan2 ile kararlı açı hesabı
    # np.cross → vektörler arası z-bileşeni (sin θ'ya orantılı)
    # np.dot   → iç çarpım (cos θ'ya orantılı)
    aci = np.degrees(
        np.arctan2(np.cross(ba, bc), np.dot(ba, bc))
    )

    return abs(float(aci))

# Test
print(aci_hesapla([0, 2], [0, 0], [2, 0]))   # Beklenen: 90.0
print(aci_hesapla([0, 1], [0, 0], [1, 0]))   # Beklenen: 90.0
```

## Gerçek Zamanlı Dirsek Açısı Ekranında Göster

```python
import cv2
import mediapipe as mp
import numpy as np

def aci_hesapla(a, b, c) -> float:
    a, b, c = np.array(a, float), np.array(b, float), np.array(c, float)
    ba, bc = a - b, c - b
    return abs(np.degrees(np.arctan2(np.cross(ba, bc), np.dot(ba, bc))))

def dirsek_acisi_goster() -> None:
    """Kameradan sol dirsek açısını gerçek zamanlı göster."""
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Kamera açılamadı")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks,
                                      mp_pose.POSE_CONNECTIONS)
            lm = results.pose_landmarks.landmark

            sol_omuz = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
            sol_dirsek = lm[mp_pose.PoseLandmark.LEFT_ELBOW]
            sol_bilek = lm[mp_pose.PoseLandmark.LEFT_WRIST]

            if all(p.visibility > 0.5 for p in [sol_omuz, sol_dirsek, sol_bilek]):
                a = [sol_omuz.x * w, sol_omuz.y * h]
                b = [sol_dirsek.x * w, sol_dirsek.y * h]
                c = [sol_bilek.x * w, sol_bilek.y * h]

                aci = aci_hesapla(a, b, c)

                # Dirsek noktasında açıyı yaz
                bx, by = int(b[0]), int(b[1])
                cv2.putText(frame, f"{aci:.1f}",
                            (bx - 30, by - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        cv2.imshow("Dirsek Açısı", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    pose.close()

if __name__ == "__main__":
    dirsek_acisi_goster()
```

## Squat Sayacı

Açı hesabını durum makinesine bağlayarak sayaç oluşturabiliriz. Diz açısı 90°'nin altına inince "aşağı" durumuna geç; 160°'nin üstüne çıkınca "yukarı" durumuna geç ve sayacı artır.

```python
import cv2
import mediapipe as mp
import numpy as np

def aci_hesapla(a, b, c) -> float:
    a, b, c = np.array(a, float), np.array(b, float), np.array(c, float)
    ba, bc = a - b, c - b
    return abs(np.degrees(np.arctan2(np.cross(ba, bc), np.dot(ba, bc))))

def squat_sayaci() -> None:
    """Sol diz açısına göre squat tekrar sayacı."""
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Kamera açılamadı")

    sayac = 0
    asama = None   # "asagi" veya "yukari"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            kalca = lm[mp_pose.PoseLandmark.LEFT_HIP]
            diz = lm[mp_pose.PoseLandmark.LEFT_KNEE]
            ayak = lm[mp_pose.PoseLandmark.LEFT_ANKLE]

            if all(p.visibility > 0.5 for p in [kalca, diz, ayak]):
                a = [kalca.x * w, kalca.y * h]
                b = [diz.x * w, diz.y * h]
                c = [ayak.x * w, ayak.y * h]
                aci = aci_hesapla(a, b, c)

                # Durum makinesi
                if aci < 90:
                    asama = "asagi"
                if aci > 160 and asama == "asagi":
                    asama = "yukari"
                    sayac += 1

                # HUD
                cv2.rectangle(frame, (0, 0), (200, 80), (0, 0, 0), -1)
                cv2.putText(frame, f"Tekrar: {sayac}", (10, 35),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
                cv2.putText(frame, str(asama or "-"), (10, 65),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Aci: {aci:.1f}", (10, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 0), 1)

        cv2.imshow("Squat Sayaci", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    pose.close()

if __name__ == "__main__":
    squat_sayaci()
```

> **💡 İpucu:** Açı eşiği değerleri (90° ve 160°) bireyden bireye değişir. Gerçek bir uygulamada kullanıcı kalibrasyonu veya ayarlanabilir eşikler düşünün.

## YOLOv8-Pose: Çok Kişili Senaryolar

MediaPipe tek kişi için tasarlanmıştır — karede birden fazla insan varsa yalnızca en belirgin kişiyi işler. Çok kişili senaryolarda YOLOv8-Pose kullanın: her kişiyi ayrı bir tespit kutusu içinde bulur ve her birine ayrı iskelet çıkarır.

```bash
pip install ultralytics
```

```python
import cv2
import numpy as np
from ultralytics import YOLO

def yolov8_poz_tespiti(video_yolu: str) -> None:
    """YOLOv8-Pose ile çok kişili poz tespiti."""
    model = YOLO("yolov8n-pose.pt")   # Hafif model; yolov8x-pose.pt daha doğru

    cap = cv2.VideoCapture(video_yolu)
    if not cap.isOpened():
        raise FileNotFoundError(f"{video_yolu} bulunamadı")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)
        annotated = results[0].plot()   # İskeleti ve kutuları çiz

        # Ham keypoint koordinatlarına erişim
        if results[0].keypoints is not None:
            kp_xy = results[0].keypoints.xy    # (N_kisi, 17, 2) tensör
            kp_conf = results[0].keypoints.conf  # (N_kisi, 17) güven skorları
            kisi_sayisi = kp_xy.shape[0]
            print(f"Karede {kisi_sayisi} kişi tespit edildi", end="\r")

        cv2.imshow("YOLOv8-Pose", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    yolov8_poz_tespiti("spor_salonu.mp4")
```

`results[0].keypoints.xy` bir PyTorch tensörüdür; `.cpu().numpy()` ile NumPy dizisine dönüştürülebilir. Keypoint sırası COCO standardını izler.

> **⚠️ Dikkat:** `yolov8n-pose.pt` (nano) hızlıdır ama hassasiyet düşüktür. Ölçüm gerektiren uygulamalarda (fizik tedavi, spor analizi) `yolov8m-pose.pt` veya `yolov8x-pose.pt` kullanın.

## Yöntem Karşılaştırması

| Yöntem | Kişi Sayısı | Hız (CPU) | Doğruluk | Platform |
|--------|-------------|-----------|----------|----------|
| **MediaPipe Pose** | 1 (varsayılan) | ~30 FPS | Yüksek | Mobil, masaüstü, web |
| **YOLOv8n-Pose** | Çok kişi | ~20 FPS | Orta | Masaüstü, sunucu |
| **YOLOv8x-Pose** | Çok kişi | ~5 FPS | Çok yüksek | GPU gerektirir |

> **📌 Not:** Masaüstünde GPU varsa YOLOv8 hız/doğruluk dengesi açısından öne geçer. Mobil veya tarayıcı hedefli projelerde MediaPipe tercih edilir.

## Özet & İleri Okuma

- Poz tahmini, görüntüdeki insan vücudunun anatomik noktalarını `(x, y, visibility)` üçlüsü olarak tespit eder.
- MediaPipe Pose 33 landmark ile gerçek zamanlı çalışır; mobil cihazlarda da akıcıdır.
- Landmark koordinatları normalize gelir (0-1); piksel koordinatına dönüştürmek için görüntü boyutuyla çarpılır.
- Görünürlük skoru 0.5'in altındaki noktalar hesaba katılmamalıdır.
- Eklem açısı için `np.arctan2` kullanan vektör yöntemi, `arccos`'tan daha kararlıdır.
- Sayaç uygulamalarında durum makinesi (aşama: "aşağı" / "yukarı") histerezis sağlar — gürültüden kaynaklanan sahte sayımları engeller.
- Çok kişili senaryolarda YOLOv8-Pose MediaPipe'a kıyasla daha iyi performans gösterir.

### Referanslar

- Cao, Z. et al. (2021). "OpenPose: Realtime Multi-Person 2D Pose Estimation." *IEEE TPAMI*: https://arxiv.org/abs/1812.08008
- Lugaresi, C. et al. (2019). "MediaPipe: A Framework for Building Perception Pipelines." https://arxiv.org/abs/1906.08172
- Jocher, G. et al. (2023). "Ultralytics YOLOv8." https://github.com/ultralytics/ultralytics
- MediaPipe Pose Belgeleri: https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
