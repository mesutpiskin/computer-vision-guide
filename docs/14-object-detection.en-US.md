[Türkçe](./14-nesne-tespiti.md) | English

# Object Detection

Hundreds of products pass on a factory conveyor every second. Spotting defects by eye is slow and error-prone. The camera needs to look at each frame and say "this product is defective, here are the coordinates" — that's exactly what object detection solves. This chapter covers everything from classical Haar Cascades to template matching, and then to modern YOLOv8, plus how to evaluate detection quality.

## Classification vs Detection?

These two concepts are often confused, but they answer different questions:

**Classification:** "What's in this image?" → Single answer: "cat"

**Detection:** "What's in this image, and where?" → Bounding box + class + confidence: `[x1=120, y1=45, x2=380, y2=290, class="cat", confidence=0.87]`

The factory example: classification says "there's a product," detection says "there's a product on the left with a crack in this region." Real applications mostly need detection.

## Haar Cascade: Classical and Lightweight

Developed by Paul Viola and Michael Jones in 2001, this was the gold standard before deep learning. Still used in embedded systems and low-resource environments.

Mechanism: a sliding window scans the image, computing Haar-like features at each location (brightness differences between adjacent rectangular regions). A cascade of boosted classifiers quickly rejects "no object" regions, focusing detailed inspection on promising areas.

```python
import cv2

img = cv2.imread("face.jpg")
if img is None:
    raise FileNotFoundError("face.jpg not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Pre-trained model — included with OpenCV
detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# scaleFactor: image shrinking per step
# minNeighbors: required neighbors for a detection (higher = fewer false positives)
faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

print(f"{len(faces)} faces detected")
cv2.imshow("Face Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Haar Cascades are fast and need no setup. But they only recognize objects they were trained on, and struggle with profile views or poor lighting.

> **⚠️ Warning:** `scaleFactor=1.05` catches small faces but slows down; `scaleFactor=1.3` is fast but misses small objects. Tune for your application.

## Template Matching: Pattern Search

You're searching for a screw-cap with fixed appearance on a production line. You have a reference photo — template matching is perfect for this.

Slide a small template image across a large image computing similarity. `TM_CCOEFF_NORMED` returns values −1 to +1; closer to 1 = strong match.

```python
import cv2
import numpy as np

img = cv2.imread("production_line.jpg")
template = cv2.imread("screw_template.jpg")
if img is None:
    raise FileNotFoundError("production_line.jpg not found")
if template is None:
    raise FileNotFoundError("screw_template.jpg not found")

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
tmpl_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
h, w = tmpl_gray.shape

result = cv2.matchTemplate(img_gray, tmpl_gray, cv2.TM_CCOEFF_NORMED)
_, max_val, _, max_loc = cv2.minMaxLoc(result)

print(f"Best match: {max_val:.3f}")

if max_val > 0.8:  # Confidence threshold
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 2)
    cv2.putText(img, f"{max_val:.2f}", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

cv2.imshow("Template Matching", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Template matching fails when objects rotate, change scale, or are partially occluded. It works in controlled environments where objects maintain a fixed view.

## YOLOv8: Modern Real-Time Detection

YOLO (You Only Look Once) processes the image just once to detect all objects simultaneously. Unlike R-CNN (propose regions first, then classify), YOLO does both in one pass: where and what in a single shot.

Intuition: divide the image into grid cells. Each cell predicts whether an object center lies within it, what class it is, and how big the bounding box is. All predictions compute simultaneously.

YOLOv8, developed by Ultralytics, is the modern version. Install with `pip install ultralytics`.

```python
import cv2
from ultralytics import YOLO

# Model sizes: n (nano) → s → m → l → x (extra-large)
# Larger = more accurate but slower
model = YOLO("yolov8n.pt")  # Auto-downloads on first run

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # conf: minimum confidence threshold
    results = model.predict(frame, conf=0.5, verbose=False)

    # Draw each detection
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

    cv2.imshow("YOLOv8 Real-Time Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

`model.names` is a dictionary mapping class ID to "person", "car", "bicycle" etc. YOLOv8n trained on COCO recognizes 80 classes.

> **💡 Tip:** `yolov8n` (nano) is ideal for quick demos; `yolov8x` (extra-large) gives maximum accuracy. In production, `yolov8s` or `yolov8m` usually balance speed and accuracy well.

> **📌 Note:** Train on your own dataset with `model.train(data="dataset.yaml", epochs=100)`. Ultralytics documentation provides step-by-step custom training.

## Evaluation Metrics

What makes a good detection? Some concrete examples:

**IoU (Intersection over Union):** "How much does the predicted box overlap with the ground truth?"

Intuition: place two rectangles on top of each other. Intersection area vs. total covered area:

$$\text{IoU} = \frac{|A \cap B|}{|A \cup B|}$$

IoU = 1.0 is perfect overlap, IoU = 0.0 is no overlap. Typically IoU > 0.5 counts as "correct detection."

**Precision:** Of the objects you detected, how many were actually correct?

$$\text{Precision} = \frac{TP}{TP + FP}$$

"I detected 100 objects, 85 were real" → Precision = 0.85

**Recall:** Of all real objects in the image, how many did you find?

$$\text{Recall} = \frac{TP}{TP + FN}$$

"Image contains 120 objects, I found 85" → Recall = 0.71

**mAP (mean Average Precision):** Average precision across different confidence thresholds, averaged over classes. YOLOv8n achieves ~0.37 mAP@0.5 on COCO, YOLOv8x achieves ~0.54.

> **📌 Note:** High precision can mean low recall — the model only reports what it's very sure about, missing many. Choose emphasis based on your application: security (prioritize recall) vs. inventory (prioritize precision).

## Method Comparison

| Method | Speed | Accuracy | Setup | Best For |
|--------|-------|----------|-------|----------|
| Haar Cascade | Very fast | Low-medium | Zero | Face detection, embedded |
| Template Matching | Fast | Variable | Zero | Fixed-appearance objects |
| YOLOv8n (nano) | ~60 FPS CPU | Medium | pip install | Real-time demo |
| YOLOv8x (xlarge) | ~10 FPS GPU | Very high | pip install | Maximum accuracy |

## Summary

- Object detection differs from classification: it returns location (bounding box) too.
- Haar Cascade from 2001 is still valid; lightweight and fast but single-class, requires frontal view.
- Template matching works well if object appearance is stable, in controlled environments.
- YOLO single-shot architecture processes image once; far faster than R-CNN approaches.
- YOLOv8 installs via `pip install ultralytics`; `model.predict()` works in one line.
- IoU measures geometric accuracy, Precision/Recall measure classification performance.
- mAP summarizes overall performance across confidence thresholds with one number.

## Further Reading

- Viola & Jones, "Rapid Object Detection using a Boosted Cascade of Simple Features" (CVPR 2001) — original Haar Cascade paper
- Redmon & Farhadi, "YOLOv3: An Incremental Improvement" (2018): https://arxiv.org/abs/1804.02767
- Jocher et al., Ultralytics YOLOv8 Documentation: https://docs.ultralytics.com
- Everingham et al., "The Pascal Visual Object Classes (VOC) Challenge" (IJCV 2010) — mAP metric standard definition
