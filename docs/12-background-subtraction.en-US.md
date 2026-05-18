[Türkçe](./12-arka-plan-cikarma.md) | English

# Background Subtraction and Motion Detection

A parking lot security camera records for hours. Most of the recording is empty parking — you only care about when vehicles arrive and leave. Analyzing each frame independently is both slow and wasteful. Background subtraction solves this: learn what "normal" looks like, then flag pixels that change as foreground (moving objects). This chapter covers three different background subtraction methods.

## Frame Differencing — Frame Difference

Simplest method: subtract two consecutive frames. If the difference is large, that pixel is moving.

Intuition: a stationary background doesn't change frame to frame, so difference is near zero. A moving object is in one place in one frame, a different place in the next — large difference.

```python
import cv2
import numpy as np

cap = cv2.VideoCapture("traffic.mp4")

if not cap.isOpened():
    raise IOError("Cannot open video")

ret, prev_frame = cap.read()
if not ret:
    raise IOError("Cannot read first frame")

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Absolute difference
    diff = cv2.absdiff(prev_gray, gray)

    # Threshold: treat small differences as noise
    _, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    # Clean noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    result = cv2.bitwise_and(frame, frame,
                            mask=mask)

    cv2.imshow("Frame | Mask | Motion",
               np.hstack([frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), result]))

    prev_gray = gray

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

Slow-moving objects might move little between frames — this method misses them. Camera jitter affects all pixels and triggers false alarms. These limitations drive more advanced approaches.

## MOG2 — Background Model with Gaussian Mixture

MOG2 (Mixture of Gaussians 2) learns a "normal value distribution" for each pixel by observing several hundred frames. Any pixel outside this learned distribution = foreground.

Intuition: we keep statistics for "what brightness does this pixel normally have?" When a vehicle arrives, that pixel's value deviates from the learned model — foreground. Slow changes like day-to-night transition adapt the model over time.

```python
import cv2
import numpy as np

cap = cv2.VideoCapture("traffic.mp4")

if not cap.isOpened():
    raise IOError("Cannot open video")

# history: how many frames back to look
# varThreshold: pixel foreground sensitivity (lower = more sensitive)
# detectShadows: mark shadows separately
mog2 = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=16,
    detectShadows=True
)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # apply: learns background and produces foreground mask
    fg_mask = mog2.apply(frame)

    # With detectShadows=True, shadows are marked 127 (gray) — filter them
    _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

    # Clean with morphology
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)   # small noise
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)  # object holes

    # Find contours and count objects
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter small contours as noise (area < 500 pixels)
    real_objects = [c for c in contours if cv2.contourArea(c) > 500]

    # Draw boxes
    result = frame.copy()
    cv2.drawContours(result, real_objects, -1, (0, 255, 0), 2)

    # Show object count
    cv2.putText(result, f"Objects: {len(real_objects)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    display = np.hstack([
        frame,
        cv2.cvtColor(fg_mask, cv2.COLOR_GRAY2BGR),
        result
    ])
    cv2.imshow("Camera | Mask | Detection", display)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

`mog2.apply(frame)` does double duty: learns the background and returns the foreground mask. You can tune update rate with `mog2.apply(frame, learningRate=0.005)` for slower adaptation.

> **💡 Tip:** MOG2 learns background in the first 100–200 frames — detections during this period aren't reliable. Skip early frames with `cap.set(cv2.CAP_PROP_POS_FRAMES, 200)`.

> **⚠️ Warning:** With `detectShadows=True`, shadows are marked 127 (gray). Filter with `cv2.threshold(fg_mask, 200, 255, ...)` to avoid counting shadows as foreground — otherwise every object's shadow becomes a fake second object.

### MOG2 Parameter Guide

| Parameter | Default | Effect |
|-----------|---------|--------|
| `history` | 500 | Frames to look back — longer = slower adaptation |
| `varThreshold` | 16 | Threshold value — lower = more foreground |
| `detectShadows` | True | Shadow detection — increases computation |

## KNN Subtractor

K-Nearest Neighbors-based background model. Instead of assuming Gaussian distribution, it directly stores pixel values from the last N frames and uses KNN distance for classification.

```python
import cv2
import numpy as np

cap = cv2.VideoCapture("traffic.mp4")

if not cap.isOpened():
    raise IOError("Cannot open video")

knn = cv2.createBackgroundSubtractorKNN(
    history=500,
    dist2Threshold=400.0,
    detectShadows=True
)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fg_mask = knn.apply(frame)

    # Clean shadows
    _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

    result = cv2.bitwise_and(frame, frame, mask=fg_mask)

    cv2.imshow("KNN Result", result)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

KNN performs more stably in busy scenes (crowds, heavy traffic) than MOG2. Trade-off: higher memory use because it stores pixel values directly.

## Comparison Table

| Method | Speed | Accuracy | Adaptation | When to Use |
|--------|-------|----------|-----------|-----------|
| Frame Diff | Very fast | Low | None | Quick prototype, minimal motion |
| MOG2 | Fast | High | Gradual | General purpose, lighting changes |
| KNN | Medium | Very high | Gradual | Busy scenes, complex background |

## Summary & Further Reading

- Frame differencing subtracts consecutive frames to detect motion — simple but blind to slow motion, sensitive to camera jitter.
- MOG2 learns a Gaussian mixture model for each pixel; adapts automatically to slow background changes.
- `detectShadows=True` marks shadows as 127 (gray) — filter with `threshold(fg_mask, 200, 255)` to avoid treating them as foreground.
- MOG2 learns in first 100–200 frames — detections during this period aren't reliable.
- Morphology (opening + closing) is the standard final step to clean MOG2 masks.
- KNN is more stable in busy scenes but uses more memory.
- Contour area filtering (`contourArea > threshold`) is mandatory to remove small noise contours.

**References**

- Zivkovic, Z. (2004). "Improved Adaptive Gaussian Mixture Model for Background Subtraction." *International Conference on Pattern Recognition (ICPR)*. [doi:10.1109/ICPR.2004.1333992](https://doi.org/10.1109/ICPR.2004.1333992)
- Zivkovic, Z. & van der Heijden, F. (2006). "Efficient Adaptive Density Estimation per Image Pixel for the Task of Background Subtraction." *Pattern Recognition Letters*, 27(7), 773–780.
