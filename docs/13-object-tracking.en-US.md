[Türkçe](./13-video-analiz.md) | English

# Video Analysis: Optical Flow and Object Tracking

You want a drone's camera to keep a target in view without losing it. Each frame isn't an isolated photo — it's connected to the previous one. Tools that model this relationship are optical flow and trackers. This chapter covers everything from tracking points across frames to full-resolution motion maps, from classic OpenCV trackers to modern multi-object algorithms.

## Optical Flow: Expressing Motion Numerically

Think of a leaf swept along by a river. The leaf changes position from one frame to the next. Optical flow expresses this displacement as a vector — imagine making the wind visible.

Core assumption: **brightness constancy** — a pixel on an object's surface has the same brightness across two frames:

$$I(x, y, t) = I(x + \Delta x, y + \Delta y, t + \Delta t)$$

This assumption isn't perfect — lighting changes or texture repetition can mislead — but works surprisingly well in practice.

## Lucas-Kanade: Sparse Optical Flow

Tracking every pixel is computationally expensive. Lucas-Kanade instead tracks selected keypoints: corners, sharp edges — features easy to distinguish. Fewer points, higher speed.

**Pyramidal LK** is an extension. It first computes flow on smaller image versions (pyramid layers), staying stable with large motions. Single-scale Lucas-Kanade can lose fast-moving objects; pyramidal structure fixes this.

```python
import cv2
import numpy as np

cap = cv2.VideoCapture(0)  # 0: default camera; provide path for video file

ret, prev_frame = cap.read()
if not ret:
    raise RuntimeError("Cannot open camera")

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Find good corners to track
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
prev_pts = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)

# Trajectory colors and drawing mask
colors = np.random.randint(0, 255, (100, 3))
mask = np.zeros_like(prev_frame)

lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Track points to next frame
    next_pts, status, _ = cv2.calcOpticalFlowPyrLK(
        prev_gray, gray, prev_pts, None, **lk_params
    )

    # Filter successfully tracked points
    if next_pts is not None:
        good_new = next_pts[status == 1]
        good_old = prev_pts[status == 1]

        # Draw trajectories
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel().astype(int)
            c, d = old.ravel().astype(int)
            mask = cv2.line(mask, (a, b), (c, d), colors[i % 100].tolist(), 2)
            frame = cv2.circle(frame, (a, b), 4, colors[i % 100].tolist(), -1)

    output = cv2.add(frame, mask)
    cv2.imshow("Lucas-Kanade Optical Flow", output)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

    prev_gray = gray.copy()
    prev_pts = good_new.reshape(-1, 1, 2) if next_pts is not None else prev_pts

cap.release()
cv2.destroyAllWindows()
```

Each colored line shows the path one point traces — like painting with the wind. If point count drops, refresh by calling `goodFeaturesToTrack` again.

> **📌 Note:** The `status == 1` filter removes points the optical flow algorithm couldn't track confidently. Always apply this filter, otherwise lost points produce spurious vectors.

## Farneback: Dense Optical Flow

While Lucas-Kanade watches selected points, Farneback computes flow for every pixel. The result: a motion map covering the entire image — ideal for video stabilization and motion density analysis.

Farneback approximates images with polynomial functions and derives motion from how those approximations change between frames. High computational cost, but the information is equally rich.

```python
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

ret, prev_frame = cap.read()
if not ret:
    raise RuntimeError("Cannot open camera")

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Compute dense optical flow
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, gray,
        None,
        pyr_scale=0.5,   # Pyramid shrinking ratio
        levels=3,        # Pyramid levels
        winsize=15,      # Averaging window size
        iterations=3,    # Iterations per level
        poly_n=5,        # Polynomial neighborhood size
        poly_sigma=1.2,  # Gaussian standard deviation
        flags=0,
    )

    # Visualize with HSV: Hue=direction, Value=magnitude
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv = np.zeros_like(prev_frame)
    hsv[..., 1] = 255                                        # Saturation max
    hsv[..., 0] = angle * 180 / np.pi / 2                   # Direction → hue
    hsv[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    bgr_flow = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    combined = np.hstack([frame, bgr_flow])
    cv2.imshow("Original | Farneback Flow", combined)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

    prev_gray = gray.copy()

cap.release()
cv2.destroyAllWindows()
```

Colors in the output represent direction, brightness represents speed: red = rightward, blue = leftward, green = upward motion. Stationary background stays black; moving objects shimmer in color.

> **💡 Tip:** In video stabilization, Farneback flow computes a global transformation matrix that estimated camera motion, then the image is shifted in the opposite direction — shaky video becomes steady.

## OpenCV Object Trackers

Optical flow models general motion between pixels. Trackers solve a different problem: a user marks an object, the tracker follows it through a film.

Workflow:
1. `tracker.init(frame, bbox)` in first frame — introduce the object
2. Every new frame: `tracker.update(frame)` — get new location
3. Interpret `(success, bbox)` pair

**CSRT** (Channel and Spatial Reliability Tracking): Uses channel reliability filters, resistant to partial occlusion and size changes. Slower but accurate.

**KCF** (Kernelized Correlation Filters): Frequency-domain correlation filtering, real-time speed. Fast but can lose track with large size changes.

```python
import cv2

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if not ret:
    raise RuntimeError("Cannot open camera")

# User selects ROI in first frame
# Mouse drag to draw, ENTER confirms, C cancels
bbox = cv2.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
cv2.destroyWindow("Select Object")

# Create tracker — choose CSRT or KCF
tracker = cv2.TrackerCSRT_create()
# tracker = cv2.TrackerKCF_create()  # Faster alternative

tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    success, bbox = tracker.update(frame)

    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Tracking", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Object Lost", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Object Tracking", frame)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

> **💡 Tip:** For single-object, CSRT prioritizes accuracy. For real-time multi-object, KCF is preferred. Lost objects can't be re-found by trackers themselves — you must reinitialize them.

> **⚠️ Warning:** Some trackers require `opencv-contrib-python` (OpenCV 4.5+). If `TrackerCSRT_create()` fails, install: `pip install opencv-contrib-python`.

## Modern Multi-Object Tracking

OpenCV trackers handle one object. Factory lines or crowded scenes require tracking dozens.

**DeepSORT**: A detector (like YOLO) finds objects each frame. DeepSORT matches detections to Kalman filter-predicted positions. Objects keep IDs even when momentarily hidden, and re-identification features assign consistent IDs.

**ByteTrack**: Simpler, faster than DeepSORT. It includes low-confidence detections in tracking, reducing missed objects. Outperforms DeepSORT in crowded scenes.

Both follow the same pipeline: detect → feature extraction → Kalman prediction → Hungarian algorithm matching → ID assignment.

## Method Comparison

| Method | Accuracy | Speed | Objects | Usage |
|--------|----------|-------|---------|--------|
| LK Sparse | Medium | Very fast | Many points | Camera motion, landmarks |
| Farneback Dense | High | Slow | All pixels | Stabilization, motion analysis |
| CSRT | High | ~25 FPS | 1 | Precise tracking, partial occlusion |
| KCF | Medium | ~100 FPS | 1 | Real-time, simple motion |
| DeepSORT/ByteTrack | Very high | GPU required | Many | Industrial multi-object |

## Summary

- Optical flow models pixel displacement between frames.
- Brightness constancy assumption underlies optical flow; sensitivity drops with lighting changes.
- Lucas-Kanade tracks sparse keypoints fast and reliably; pyramidal structure handles large motions.
- Farneback computes flow for every pixel; useful for stabilization and motion density maps.
- CSRT emphasizes accuracy, KCF emphasizes speed; both single-object only.
- Multi-object tracking with DeepSORT and ByteTrack are industry standards.
- `tracker.update()` each call returns `(success, bbox)`; `success=False` means object lost.

## Further Reading

- Bouguet, J.Y., "Pyramidal Implementation of the Lucas Kanade Feature Tracker" (2001) — original technical report on LK pyramid
- Farneback, G., "Two-Frame Motion Estimation Based on Polynomial Expansion" (SCIA 2003) — Farneback method paper
- Bewley et al., "Simple Online and Realtime Tracking" (ICIP 2016): https://arxiv.org/abs/1602.00763 — SORT algorithm, DeepSORT foundation
- Zhang et al., "ByteTrack" (ECCV 2022): https://arxiv.org/abs/2110.06864 — ByteTrack paper
