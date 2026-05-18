# Yüz Tanıma

Bir bina güvenlik sisteminde kapı otomatik açılacak: kamera görüntü alacak, içeride yetkili biri var mı kontrol edecek. Bunun için önce "Bu görüntüde yüz var mı?" sorusuna cevap vermek, ardından "Bu yüz kim?" sorusunu yanıtlamak gerekir. İlki tespit, ikincisi tanımadır — birbirini tamamlar ama tamamen farklı problemlerdir. Bu bölümde her iki adımın klasik ve modern yöntemlerini öğreneceksiniz.

## Tespit ve Tanıma Farkı

**Yüz tespiti:** "Bu görüntüde yüz var mı, nerede?" → Bounding box koordinatları döner.

**Yüz tanıma:** "Bu yüz kime ait?" → Kimlik ya da "bilinmiyor" döner.

Güvenlik sisteminde pipeline şöyledir: kamera → tespit (yüzü bul) → kırp → tanıma (kimliği sorgula) → erişim kararı. Tespit olmadan tanıma başlayamaz; tanıma olmadan sadece "burada birinin yüzü var" bilgisi vardır.

## Yüz Tespiti

### Haar Cascade ile Hızlı Tespit

Klasik yaklaşım: hızlıdır, kurulum gerektirmez, cepheden bakışta güvenilirdir.

```python
import cv2

img = cv2.imread("grup_fotografi.jpg")
if img is None:
    raise FileNotFoundError("grup_fotografi.jpg bulunamadı")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

faces = face_cascade.detectMultiScale(
    gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

print(f"{len(faces)} yüz tespit edildi")
cv2.imshow("Tespit", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

> **📌 Not:** Profil yüz için `haarcascade_profileface.xml` kullanın; cepheden bakışta bu model zayıftır.

### DNN ile Daha Güvenilir Tespit

Caffe modeli Haar Cascade'den çok daha güçlüdür: farklı açılar, zayıf aydınlatma, kısmi örtmede çalışır.

```python
import cv2
import numpy as np

# Model dosyaları: deploy.prototxt + res10_300x300_ssd_iter_140000.caffemodel
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

img = cv2.imread("grup_fotografi.jpg")
if img is None:
    raise FileNotFoundError("grup_fotografi.jpg bulunamadı")

h, w = img.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104, 177, 123))
net.setInput(blob)
detections = net.forward()

for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.5:
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        x1, y1, x2, y2 = box.astype(int)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"{confidence:.2f}", (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

cv2.imshow("DNN Yüz Tespiti", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Klasik Yüz Tanıma

### Eigenfaces (PCA Tabanlı)

Her insan yüzü birkaç temel "arketip yüzün" (eigenface) doğrusal kombinasyonu olarak ifade edilebilir. Bu temel yüzler yüzlerce örnek fotoğraftan PCA (Temel Bileşen Analizi) ile öğrenilir. Yeni yüzü bu bileşenler üzerinden temsil etmek, yüksek boyutlu piksel verisini küçük bir vektöre sıkıştırır.

```python
import cv2
import numpy as np
import os

# Eğitim verisi: her kişi için yüz görüntüleri ve etiketler
faces = []
labels = []
label_names = {}

# Klasör yapısı: dataset/0_Ali/, dataset/1_Ayse/, ...
for label_id, person_dir in enumerate(sorted(os.listdir("dataset"))):
    person_path = os.path.join("dataset", person_dir)
    if not os.path.isdir(person_path):
        continue
    label_names[label_id] = person_dir.split("_", 1)[-1]
    for img_file in os.listdir(person_path):
        img_path = os.path.join(person_path, img_file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        img_resized = cv2.resize(img, (100, 100))
        faces.append(img_resized)
        labels.append(label_id)

# Eigenfaces modeli
model = cv2.face.EigenFaceRecognizer_create()
model.train(faces, np.array(labels))

# Test görüntüsü
test_img = cv2.imread("test_yuz.jpg", cv2.IMREAD_GRAYSCALE)
if test_img is None:
    raise FileNotFoundError("test_yuz.jpg bulunamadı")

test_resized = cv2.resize(test_img, (100, 100))
predicted_label, confidence = model.predict(test_resized)

print(f"Tahmin: {label_names.get(predicted_label, 'Bilinmiyor')}")
print(f"Güven skoru: {confidence:.1f}  (düşük = daha benzer)")
```

### LBPH: Yerel Doku ile Tanıma

LBPH (Local Binary Patterns Histograms) her pikseli 8 komşusundan büyük mü küçük mü olduğuna göre ikili kodlar, bu desenlerin histogramını yüzün kimliğini temsil eden parmak izi olarak kullanır. Aydınlatma değişimine Eigenfaces'ten çok daha dayanıklıdır.

```python
import cv2
import numpy as np

# LBPH modeli — aydınlatma değişimine karşı dayanıklı
model = cv2.face.LBPHFaceRecognizer_create(
    radius=1,       # LBP hesaplama yarıçapı
    neighbors=8,    # Komşu piksel sayısı
    grid_x=8,       # Yatay ızgara hücre sayısı
    grid_y=8,       # Dikey ızgara hücre sayısı
)

# Eğitim verisi (Eigenfaces örneğiyle aynı yapı)
faces = []
labels = []

for label_id in range(3):  # 3 kişi için örnek
    for i in range(10):    # Kişi başına 10 fotoğraf
        img = cv2.imread(f"dataset/{label_id}_{i}.jpg", cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        faces.append(cv2.resize(img, (100, 100)))
        labels.append(label_id)

if faces:
    model.train(faces, np.array(labels))
    model.save("lbph_model.xml")

    # Tahmin
    test_img = cv2.imread("test_yuz.jpg", cv2.IMREAD_GRAYSCALE)
    if test_img is None:
        raise FileNotFoundError("test_yuz.jpg bulunamadı")

    test_resized = cv2.resize(test_img, (100, 100))
    label, confidence = model.predict(test_resized)
    print(f"Tahmin edilen kişi ID: {label}, Güven: {confidence:.1f}")
    # LBPH için confidence < 80 genellikle güvenilir eşleşme
```

LBPH az veriyle çalışır, hızlı eğitilir ve güncelleme kolaylaşır (`model.update()` ile yeni kişi eklenebilir). Karmaşık ortamlarda yetersiz kalır.

## Derin Öğrenme: Face Embedding

Modern yaklaşımın sezgisi şudur: Her yüzü 128 (ya da 512) boyutlu bir vektöre dönüştür. Aynı kişinin iki farklı fotoğrafı bu vektör uzayında birbirine yakın olmalı, farklı kişilerin fotoğrafları uzak olmalı. Bu vektöre "face embedding" denir.

Öklid mesafesiyle karşılaştırma:

$$d = \|f_1 - f_2\|_2$$

Eşik altındaysa (örneğin d < 0.6) aynı kişi, üstündeyse farklı kişi kararı verilir.

**FaceNet** bu sezgiyi "triplet loss" ile öğrenir: anchor (referans), positive (aynı kişi), negative (farklı kişi) üçlüsü eğitimde ayrılmaya zorlanır.

**ArcFace** ise açısal marjin ekler — sınıf merkezleri arasındaki açıyı açık tutarak daha ayırt edici embedding öğrenir. CASIA-WebFace ve MS-Celeb-1M gibi büyük veri setlerinde FaceNet'ten daha iyi sonuç verir.

## DeepFace: Tek API, Çok Model

DeepFace kütüphanesi VGG-Face, FaceNet ve ArcFace modellerini tek bir arayüzden sunar. `pip install deepface` ile kurulur.

```python
from deepface import DeepFace
import cv2

# İki yüz görüntüsünü karşılaştır
result = DeepFace.verify(
    img1_path="kisi_a.jpg",
    img2_path="kisi_b.jpg",
    model_name="ArcFace",       # VGG-Face, FaceNet, ArcFace, Dlib, OpenFace
    distance_metric="cosine",   # cosine, euclidean, euclidean_l2
    enforce_detection=True,     # Yüz bulunamazsa hata fırlat
)

print(f"Aynı kişi mi: {result['verified']}")
print(f"Mesafe: {result['distance']:.4f}  (eşik: {result['threshold']:.4f})")

# Yaş, cinsiyet ve duygu analizi
analysis = DeepFace.analyze(
    img_path="kisi_a.jpg",
    actions=["age", "gender", "emotion"],
    enforce_detection=False,
)

print(f"Tahmini yaş: {analysis[0]['age']}")
print(f"Cinsiyet: {analysis[0]['dominant_gender']}")
print(f"Baskın duygu: {analysis[0]['dominant_emotion']}")
```

Görsel karşılaştırma için iki yüzü yan yana gösterelim:

```python
from deepface import DeepFace
import cv2
import numpy as np

img1 = cv2.imread("kisi_a.jpg")
img2 = cv2.imread("kisi_b.jpg")
if img1 is None:
    raise FileNotFoundError("kisi_a.jpg bulunamadı")
if img2 is None:
    raise FileNotFoundError("kisi_b.jpg bulunamadı")

result = DeepFace.verify("kisi_a.jpg", "kisi_b.jpg", model_name="ArcFace", enforce_detection=False)

# Her iki görüntüyü aynı boyuta getir
h = max(img1.shape[0], img2.shape[0])
img1_r = cv2.resize(img1, (int(img1.shape[1] * h / img1.shape[0]), h))
img2_r = cv2.resize(img2, (int(img2.shape[1] * h / img2.shape[0]), h))

combined = np.hstack([img1_r, img2_r])

verdict = "AYNI KISIYIZ" if result["verified"] else "FARKLI KISILER"
color = (0, 200, 0) if result["verified"] else (0, 0, 200)
cv2.putText(combined, f"{verdict}  d={result['distance']:.3f}",
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

cv2.imshow("Yüz Karşılaştırma", combined)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

> **⚠️ Dikkat:** DeepFace `enforce_detection=True` varsayılanında yüz tespit edemezse hata fırlatır. Belirsiz görüntülerde `enforce_detection=False` kullanın.

> **💡 İpucu:** `DeepFace.find(img_path, db_path)` bir klasördeki tüm yüzleri indeksler ve sorgu yüzünü veritabanında arar — küçük ölçekli yüz tanıma sistemleri için hazır çözümdür.

## Yöntem Karşılaştırması

| Yöntem | Veri İhtiyacı | Doğruluk | Hız | Kullanım |
|--------|--------------|----------|-----|----------|
| LBPH | Az (~10/kişi) | Orta | Çok hızlı | Prototip, basit ortam |
| Eigenfaces | Orta | Düşük-orta | Hızlı | Akademik örnek |
| FaceNet | Büyük veri | Yüksek | GPU önerilir | Üretim, çoklu kişi |
| ArcFace | Büyük veri | Çok yüksek | GPU gerekli | Güvenlik sistemi |

## Özet

- Yüz tespiti konum döndürür, yüz tanıma kimlik döndürür; pipeline'da tespit her zaman önce gelir.
- Haar Cascade hızlı ve kurulumsuzdur; cephe görüşünde güvenilir, profilden zayıftır.
- DNN tabanlı tespit farklı açı, aydınlatma ve örtmede çok daha sağlamdır.
- LBPH az veriyle çalışır ve aydınlatma değişimine dirençlidir; basit ortamlar için uygundur.
- Face embedding yüzü sayısal vektöre çevirir; Öklid veya cosine mesafesiyle kimlik kararı verilir.
- ArcFace açısal marjin kullanarak daha ayırt edici embedding öğrenir; FaceNet'ten üstün performans gösterir.
- DeepFace kütüphanesi birden fazla modeli tek API'den sunar; hızlı prototipleme için idealdir.

## İleri Okuma

- Schroff et al., "FaceNet: A Unified Embedding for Face Recognition and Clustering" (CVPR 2015): https://arxiv.org/abs/1503.03832
- Deng et al., "ArcFace: Additive Angular Margin Loss for Deep Face Recognition" (CVPR 2019): https://arxiv.org/abs/1801.07698
- Serengil, S.I. & Ozpinar, A., "DeepFace: A Lightweight Face Recognition Library" (2020): https://github.com/serengil/deepface
