[Türkçe](./17-yuz-tanima.md) | English

# Face Recognition

Picture a building's security system: a camera captures footage to check if someone authorized is inside. To make this work, you must first answer "Does this image contain a face?" and then "Who is this person?" The first is detection, the second is recognition — they complement each other but are completely different problems. In this chapter, you'll learn both classical and modern approaches to each step.

## The Difference Between Detection and Recognition

**Face detection:** "Is there a face in this image? Where?" → Returns bounding box coordinates.

**Face recognition:** "Who does this face belong to?" → Returns an identity or "unknown".

The security system pipeline flows like this: camera → detection (find the face) → crop → recognition (query the identity) → access decision. You cannot start recognition without detection; without recognition, you only know "someone's face is here."

## Face Detection

### Fast Detection with Haar Cascade

The classical approach: it's fast, requires no setup, and works reliably for frontal faces.

```python
import cv2

img = cv2.imread("group_photo.jpg")
if img is None:
    raise FileNotFoundError("group_photo.jpg not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

faces = face_cascade.detectMultiScale(
    gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

print(f"{len(faces)} faces detected")
cv2.imshow("Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

> **📌 Note:** For profile faces, use `haarcascade_profileface.xml`; this model is weak for frontal views.

### More Reliable Detection with DNN

The Caffe model is far more powerful than Haar Cascade: it works across different angles, poor lighting, and partial occlusion.

```python
import cv2
import numpy as np

# Model files: deploy.prototxt + res10_300x300_ssd_iter_140000.caffemodel
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

img = cv2.imread("group_photo.jpg")
if img is None:
    raise FileNotFoundError("group_photo.jpg not found")

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

cv2.imshow("DNN Face Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Classical Face Recognition

### Eigenfaces (PCA-Based)

Every human face can be expressed as a linear combination of a few fundamental "archetypes" (eigenfaces). These basis faces are learned via PCA (Principal Component Analysis) from hundreds of training photographs. Representing a new face through these components compresses high-dimensional pixel data into a small vector.

```python
import cv2
import numpy as np
import os

# Training data: face images and labels for each person
faces = []
labels = []
label_names = {}

# Folder structure: dataset/0_Alice/, dataset/1_Bob/, ...
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

# Eigenfaces model
model = cv2.face.EigenFaceRecognizer_create()
model.train(faces, np.array(labels))

# Test image
test_img = cv2.imread("test_face.jpg", cv2.IMREAD_GRAYSCALE)
if test_img is None:
    raise FileNotFoundError("test_face.jpg not found")

test_resized = cv2.resize(test_img, (100, 100))
predicted_label, confidence = model.predict(test_resized)

print(f"Prediction: {label_names.get(predicted_label, 'Unknown')}")
print(f"Confidence score: {confidence:.1f}  (lower = more similar)")
```

### LBPH: Recognition via Local Texture

LBPH (Local Binary Patterns Histograms) encodes each pixel as binary based on whether its 8 neighbors are greater or less than it, using the histogram of these patterns as a fingerprint representing facial identity. It's far more robust to lighting changes than Eigenfaces.

```python
import cv2
import numpy as np

# LBPH model — resistant to lighting changes
model = cv2.face.LBPHFaceRecognizer_create(
    radius=1,       # LBP calculation radius
    neighbors=8,    # Number of neighboring pixels
    grid_x=8,       # Horizontal grid cell count
    grid_y=8,       # Vertical grid cell count
)

# Training data (same structure as Eigenfaces example)
faces = []
labels = []

for label_id in range(3):  # 3 people, for example
    for i in range(10):    # 10 photos per person
        img = cv2.imread(f"dataset/{label_id}_{i}.jpg", cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        faces.append(cv2.resize(img, (100, 100)))
        labels.append(label_id)

if faces:
    model.train(faces, np.array(labels))
    model.save("lbph_model.xml")

    # Prediction
    test_img = cv2.imread("test_face.jpg", cv2.IMREAD_GRAYSCALE)
    if test_img is None:
        raise FileNotFoundError("test_face.jpg not found")

    test_resized = cv2.resize(test_img, (100, 100))
    label, confidence = model.predict(test_resized)
    print(f"Predicted person ID: {label}, Confidence: {confidence:.1f}")
    # For LBPH, confidence < 80 is typically a reliable match
```

LBPH works with limited data, trains quickly, and makes updates easy (`model.update()` lets you add new people). In complex environments it may fall short.

## Deep Learning: Face Embedding

The modern approach's intuition is this: Convert every face into a vector of 128 (or 512) dimensions. Two different photos of the same person should be close to each other in this vector space; photos of different people should be far apart. This vector is called a "face embedding."

Comparison via Euclidean distance:

$$d = \|f_1 - f_2\|_2$$

If below a threshold (e.g., d < 0.6), it's the same person; above it, a different person.

**FaceNet** learns this intuition using "triplet loss": an anchor (reference), positive (same person), and negative (different person) triple are forced apart during training.

**ArcFace** adds an angular margin — keeping the angle between class centers clear to learn more discriminative embeddings. It performs better than FaceNet on large datasets like CASIA-WebFace and MS-Celeb-1M.

## DeepFace: One API, Multiple Models

The DeepFace library presents VGG-Face, FaceNet, and ArcFace models through a single interface. Install with `pip install deepface`.

```python
from deepface import DeepFace
import cv2

# Compare two face images
result = DeepFace.verify(
    img1_path="person_a.jpg",
    img2_path="person_b.jpg",
    model_name="ArcFace",       # VGG-Face, FaceNet, ArcFace, Dlib, OpenFace
    distance_metric="cosine",   # cosine, euclidean, euclidean_l2
    enforce_detection=True,     # Raise error if face not detected
)

print(f"Same person: {result['verified']}")
print(f"Distance: {result['distance']:.4f}  (threshold: {result['threshold']:.4f})")

# Age, gender, and emotion analysis
analysis = DeepFace.analyze(
    img_path="person_a.jpg",
    actions=["age", "gender", "emotion"],
    enforce_detection=False,
)

print(f"Estimated age: {analysis[0]['age']}")
print(f"Gender: {analysis[0]['dominant_gender']}")
print(f"Dominant emotion: {analysis[0]['dominant_emotion']}")
```

To visually compare two faces, let's display them side by side:

```python
from deepface import DeepFace
import cv2
import numpy as np

img1 = cv2.imread("person_a.jpg")
img2 = cv2.imread("person_b.jpg")
if img1 is None:
    raise FileNotFoundError("person_a.jpg not found")
if img2 is None:
    raise FileNotFoundError("person_b.jpg not found")

result = DeepFace.verify("person_a.jpg", "person_b.jpg", model_name="ArcFace", enforce_detection=False)

# Resize both images to the same height
h = max(img1.shape[0], img2.shape[0])
img1_r = cv2.resize(img1, (int(img1.shape[1] * h / img1.shape[0]), h))
img2_r = cv2.resize(img2, (int(img2.shape[1] * h / img2.shape[0]), h))

combined = np.hstack([img1_r, img2_r])

verdict = "SAME PERSON" if result["verified"] else "DIFFERENT PEOPLE"
color = (0, 200, 0) if result["verified"] else (0, 0, 200)
cv2.putText(combined, f"{verdict}  d={result['distance']:.3f}",
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

cv2.imshow("Face Comparison", combined)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

> **⚠️ Warning:** DeepFace raises an error by default if `enforce_detection=True` and no face is found. Use `enforce_detection=False` on uncertain images.

> **💡 Tip:** `DeepFace.find(img_path, db_path)` indexes all faces in a folder and searches the database for a query face — it's a ready-made solution for small-scale face recognition systems.

## Method Comparison

| Method | Data Requirement | Accuracy | Speed | Usage |
|--------|-----------------|----------|-------|--------|
| LBPH | Small (~10/person) | Medium | Very fast | Prototype, simple environment |
| Eigenfaces | Medium | Low-medium | Fast | Academic example |
| FaceNet | Large data | High | GPU recommended | Production, multi-person |
| ArcFace | Large data | Very high | GPU required | Security system |

## Summary

- Face detection returns location; face recognition returns identity. Detection always comes first in the pipeline.
- Haar Cascade is fast and setup-free; it's reliable for frontal views but weak for profiles.
- DNN-based detection is far more robust across angles, lighting, and occlusion.
- LBPH works with limited data and is resistant to lighting changes; it suits simple environments.
- Face embedding converts a face to a numerical vector; identity is decided via Euclidean or cosine distance.
- ArcFace uses angular margin to learn more discriminative embeddings; it outperforms FaceNet.
- The DeepFace library exposes multiple models through a single API; it's ideal for rapid prototyping.

## Further Reading

- Schroff et al., "FaceNet: A Unified Embedding for Face Recognition and Clustering" (CVPR 2015): https://arxiv.org/abs/1503.03832
- Deng et al., "ArcFace: Additive Angular Margin Loss for Deep Face Recognition" (CVPR 2019): https://arxiv.org/abs/1801.07698
- Serengil, S.I. & Ozpinar, A., "DeepFace: A Lightweight Face Recognition Library" (2020): https://github.com/serengil/deepface
