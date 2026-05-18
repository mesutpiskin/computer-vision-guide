[Türkçe](./21-poz-tahmini.md) | English

# Pose Estimation

You want to measure a person's knee angle in real time as they do squats at the gym: when the angle drops below 90°, increment the counter; when it rises above 160°, you're back to standing and ready for the next rep. Or in a physical therapy clinic, automatically assess a patient's shoulder alignment and lower back angle. Both scenarios ask the same fundamental question: where are the joint points in the person's body? In this chapter, we'll learn tools that answer this question in real time.

## What Is Pose Estimation?

Detecting the coordinates of anatomical keypoints in the human body and building a skeletal structure from these points is the definition of pose estimation.

The **COCO dataset standard** defines 17 keypoints: nose, left/right eye, left/right ear, left/right shoulder, left/right elbow, left/right wrist, left/right hip, left/right knee, left/right ankle. The model outputs three values for each: pixel coordinates `(x, y)` and a confidence score `visibility`.

The confidence score ranges from 0 to 1 — it indicates whether the point exists in the image and how sure the model is. Body parts outside the camera's view or hidden behind other objects are marked with low confidence.

> **📌 Note:** Pose estimation is different from object detection. Object detection says "a person is here"; pose estimation says "this person's knee point is there." They usually work sequentially.

## MediaPipe Pose

Google's MediaPipe library offers a lightweight, real-time solution for pose estimation. Running at 30+ FPS on desktop and staying smooth on mobile, it defines **33 landmarks** that extend COCO's 17 points to include finger and face points.

```bash
pip install mediapipe opencv-python numpy
```

```python
import cv2
import mediapipe as mp
import numpy as np

def camera_pose_detection() -> None:
    """Real-time skeleton detection from camera with MediaPipe Pose."""
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Camera could not be opened")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # MediaPipe expects RGB — convert from BGR
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            # Draw skeleton
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            # Get left shoulder coordinates
            landmarks = results.pose_landmarks.landmark
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]

            if left_shoulder.visibility > 0.5:
                h, w = frame.shape[:2]
                cx = int(left_shoulder.x * w)
                cy = int(left_shoulder.y * h)
                cv2.circle(frame, (cx, cy), 8, (0, 255, 255), -1)
                cv2.putText(frame, "Left Shoulder", (cx + 10, cy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        cv2.imshow("MediaPipe Pose", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    pose.close()

if __name__ == "__main__":
    camera_pose_detection()
```

> **⚠️ Warning:** Don't include points with visibility (`visibility`) below 0.5 in calculations — that point may be outside the camera or hidden behind another object. Low-confidence point coordinates can be meaningless.

MediaPipe landmark coordinates arrive **normalized**: `x` and `y` are in the 0-1 range, divided by image width/height. To convert to pixel coordinates, use `int(landmark.x * width)`.

## Angle Calculation

We have skeleton points; now we'll measure joint angles. Given three points: A (shoulder), B (elbow), C (wrist) — calculate the angle at the elbow.

We define two vectors: **BA** (from elbow to shoulder) and **BC** (from elbow to wrist). The angle between these vectors is the joint angle.

The `np.arccos` approach suffers from numerical instability at large angles. `np.arctan2` processes the two components separately, remaining stable across all angles and avoiding sign ambiguity.

```python
import numpy as np

def calculate_angle(a: list, b: list, c: list) -> float:
    """
    Calculate angle at B given three points.
    a, b, c: [x, y] coordinate lists
    """
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    # Vectors centered at b
    ba = a - b
    bc = c - b

    # Stable angle calculation using arctan2
    # np.cross → z-component of cross product (proportional to sin θ)
    # np.dot   → dot product (proportional to cos θ)
    angle = np.degrees(
        np.arctan2(np.cross(ba, bc), np.dot(ba, bc))
    )

    return abs(float(angle))

# Test
print(calculate_angle([0, 2], [0, 0], [2, 0]))   # Expected: 90.0
print(calculate_angle([0, 1], [0, 0], [1, 0]))   # Expected: 90.0
```

## Display Elbow Angle in Real Time

```python
import cv2
import mediapipe as mp
import numpy as np

def calculate_angle(a, b, c) -> float:
    a, b, c = np.array(a, float), np.array(b, float), np.array(c, float)
    ba, bc = a - b, c - b
    return abs(np.degrees(np.arctan2(np.cross(ba, bc), np.dot(ba, bc))))

def show_elbow_angle() -> None:
    """Display left elbow angle in real time from camera."""
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Camera could not be opened")

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

            left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = lm[mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = lm[mp_pose.PoseLandmark.LEFT_WRIST]

            if all(p.visibility > 0.5 for p in [left_shoulder, left_elbow, left_wrist]):
                a = [left_shoulder.x * w, left_shoulder.y * h]
                b = [left_elbow.x * w, left_elbow.y * h]
                c = [left_wrist.x * w, left_wrist.y * h]

                angle = calculate_angle(a, b, c)

                # Draw angle at elbow
                bx, by = int(b[0]), int(b[1])
                cv2.putText(frame, f"{angle:.1f}",
                            (bx - 30, by - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        cv2.imshow("Elbow Angle", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    pose.close()

if __name__ == "__main__":
    show_elbow_angle()
```

## Squat Counter

We can create a counter by connecting angle calculation to a state machine. When knee angle drops below 90°, switch to "down" state; when it rises above 160° while in "down" state, switch to "up" and increment the counter.

```python
import cv2
import mediapipe as mp
import numpy as np

def calculate_angle(a, b, c) -> float:
    a, b, c = np.array(a, float), np.array(b, float), np.array(c, float)
    ba, bc = a - b, c - b
    return abs(np.degrees(np.arctan2(np.cross(ba, bc), np.dot(ba, bc))))

def squat_counter() -> None:
    """Squat rep counter based on left knee angle."""
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Camera could not be opened")

    counter = 0
    stage = None   # "down" or "up"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            hip = lm[mp_pose.PoseLandmark.LEFT_HIP]
            knee = lm[mp_pose.PoseLandmark.LEFT_KNEE]
            ankle = lm[mp_pose.PoseLandmark.LEFT_ANKLE]

            if all(p.visibility > 0.5 for p in [hip, knee, ankle]):
                a = [hip.x * w, hip.y * h]
                b = [knee.x * w, knee.y * h]
                c = [ankle.x * w, ankle.y * h]
                angle = calculate_angle(a, b, c)

                # State machine
                if angle < 90:
                    stage = "down"
                if angle > 160 and stage == "down":
                    stage = "up"
                    counter += 1

                # HUD
                cv2.rectangle(frame, (0, 0), (200, 80), (0, 0, 0), -1)
                cv2.putText(frame, f"Reps: {counter}", (10, 35),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
                cv2.putText(frame, str(stage or "-"), (10, 65),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Angle: {angle:.1f}", (10, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 0), 1)

        cv2.imshow("Squat Counter", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    pose.close()

if __name__ == "__main__":
    squat_counter()
```

> **💡 Tip:** Angle thresholds (90° and 160°) vary person to person. In a real application, consider user calibration or adjustable thresholds.

## YOLOv8-Pose: Multi-Person Scenarios

MediaPipe is designed for one person — if multiple people are in the frame, it only processes the most prominent one. For multi-person scenarios, use YOLOv8-Pose: it finds each person in a separate detection box and extracts a skeleton for each.

```bash
pip install ultralytics
```

```python
import cv2
import numpy as np
from ultralytics import YOLO

def yolov8_pose_detection(video_path: str) -> None:
    """Multi-person pose detection with YOLOv8-Pose."""
    model = YOLO("yolov8n-pose.pt")   # Lightweight model; yolov8x-pose.pt is more accurate

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"{video_path} not found")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)
        annotated = results[0].plot()   # Draw skeletons and boxes

        # Access raw keypoint coordinates
        if results[0].keypoints is not None:
            kp_xy = results[0].keypoints.xy    # (N_people, 17, 2) tensor
            kp_conf = results[0].keypoints.conf  # (N_people, 17) confidence scores
            person_count = kp_xy.shape[0]
            print(f"Detected {person_count} people", end="\r")

        cv2.imshow("YOLOv8-Pose", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    yolov8_pose_detection("gym.mp4")
```

`results[0].keypoints.xy` is a PyTorch tensor; convert it to a NumPy array with `.cpu().numpy()`. Keypoint order follows the COCO standard.

> **⚠️ Warning:** `yolov8n-pose.pt` (nano) is fast but less accurate. For measurement-critical applications (physical therapy, sports analysis), use `yolov8m-pose.pt` or `yolov8x-pose.pt`.

## Method Comparison

| Method | Person Count | Speed (CPU) | Accuracy | Platform |
|--------|-------------|-----------|----------|----------|
| **MediaPipe Pose** | 1 (by default) | ~30 FPS | High | Mobile, desktop, web |
| **YOLOv8n-Pose** | Multi-person | ~20 FPS | Medium | Desktop, server |
| **YOLOv8x-Pose** | Multi-person | ~5 FPS | Very high | GPU required |

> **📌 Note:** On desktop with GPU, YOLOv8 has a better speed/accuracy trade-off. For mobile or browser targets, MediaPipe is preferred.

## Summary & Further Reading

- Pose estimation detects anatomical body points as `(x, y, visibility)` triples.
- MediaPipe Pose runs real-time with 33 landmarks; it stays smooth even on mobile.
- Landmark coordinates come normalized (0-1); multiply by image dimensions to get pixel coordinates.
- Points with visibility below 0.5 should be excluded from calculations.
- The vector method using `np.arctan2` for joint angles is more stable than `arccos`.
- In counter applications, a state machine ("down" / "up" stages) prevents false counts from jitter.
- YOLOv8-Pose outperforms MediaPipe on multi-person scenarios.

### References

- Cao, Z. et al. (2021). "OpenPose: Realtime Multi-Person 2D Pose Estimation." *IEEE TPAMI*: https://arxiv.org/abs/1812.08008
- Lugaresi, C. et al. (2019). "MediaPipe: A Framework for Building Perception Pipelines." https://arxiv.org/abs/1906.08172
- Jocher, G. et al. (2023). "Ultralytics YOLOv8." https://github.com/ultralytics/ultralytics
- MediaPipe Pose Documentation: https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
