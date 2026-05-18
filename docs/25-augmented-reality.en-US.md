[Türkçe](./25-artirilmis-gerceklik.md) | English

# Augmented Reality

Augmented Reality (AR) overlays digital objects or information onto real-world images. With OpenCV, you can develop marker-based AR applications, face filters, and 3D object projection.

## AR with ArUco Markers

ArUco is a square marker system built into OpenCV. It's used to compute the camera's position relative to the marker (camera pose).

### Create Marker

```python
import cv2
import numpy as np

# Select ArUco dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# Create marker (id=42, 200x200 pixels)
marker_img = np.zeros((200, 200), dtype=np.uint8)
marker_img = cv2.aruco.generateImageMarker(aruco_dict, 42, 200)

cv2.imwrite("aruco_marker_42.png", marker_img)
cv2.imshow("ArUco Marker", marker_img)
cv2.waitKey(0)
```

### Detect Marker

```python
import cv2
import numpy as np

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
detector_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, detector_params)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    corners, ids, rejected = detector.detectMarkers(frame)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        print(f"Detected marker IDs: {ids.flatten()}")

    cv2.imshow("ArUco Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Camera Calibration

For AR, you need to know the camera's intrinsic parameters. If calibration was done previously, `camera_matrix` and `dist_coeffs` should be saved. For a rough estimate:

```python
import numpy as np

# Camera matrix estimation (if uncalibrated)
h, w = 480, 640
focal_length = w  # estimate
camera_matrix = np.array([
    [focal_length, 0, w / 2],
    [0, focal_length, h / 2],
    [0, 0, 1]
], dtype=np.float64)

dist_coeffs = np.zeros((5, 1))
```

For proper calibration, refer to the camera calibration chapter.

### 3D Axes Drawing (Pose Estimation)

```python
import cv2
import numpy as np

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
detector = cv2.aruco.ArucoDetector(aruco_dict, cv2.aruco.DetectorParameters())

marker_size = 0.05  # 5 cm

h, w = 480, 640
camera_matrix = np.array([[w, 0, w/2], [0, w, h/2], [0, 0, 1]], dtype=np.float64)
dist_coeffs = np.zeros((5, 1))

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    corners, ids, _ = detector.detectMarkers(frame)

    if ids is not None:
        for i, corner in enumerate(corners):
            rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
                corner, marker_size, camera_matrix, dist_coeffs
            )
            # Draw 3D axes
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs,
                              rvec, tvec, marker_size * 0.5)

    cv2.imshow("AR Pose", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### 2D Image Overlay (Image Overlay)

Overlay an image onto a marker using homography:

```python
import cv2
import numpy as np

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
detector = cv2.aruco.ArucoDetector(aruco_dict, cv2.aruco.DetectorParameters())

overlay_img = cv2.imread("logo.png")

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    corners, ids, _ = detector.detectMarkers(frame)

    if ids is not None and 42 in ids:
        idx = np.where(ids == 42)[0][0]
        c = corners[idx][0]  # 4 corner points

        h, w = overlay_img.shape[:2]
        src_pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        dst_pts = c.astype(np.float32)

        H, _ = cv2.findHomography(src_pts, dst_pts)
        warped = cv2.warpPerspective(overlay_img, H,
                                     (frame.shape[1], frame.shape[0]))

        mask = cv2.warpPerspective(
            np.ones((h, w), dtype=np.uint8) * 255, H,
            (frame.shape[1], frame.shape[0])
        )
        frame[mask > 0] = warped[mask > 0]

    cv2.imshow("AR Overlay", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Face Filter with MediaPipe

```python
import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

def overlay_image_alpha(background, overlay, x, y):
    """Overlay image with alpha channel onto background."""
    if overlay.shape[2] < 4:
        overlay = cv2.cvtColor(overlay, cv2.COLOR_BGR2BGRA)
    oy, ox = overlay.shape[:2]
    if x < 0 or y < 0 or x + ox > background.shape[1] or y + oy > background.shape[0]:
        return background
    alpha = overlay[:, :, 3] / 255.0
    for c in range(3):
        background[y:y+oy, x:x+ox, c] = (
            alpha * overlay[:, :, c] +
            (1 - alpha) * background[y:y+oy, x:x+ox, c]
        )
    return background

# Overlay image like a hat or mustache (BGRA format)
hat = cv2.imread("hat.png", cv2.IMREAD_UNCHANGED)

cap = cv2.VideoCapture(0)
with mp_face_mesh.FaceMesh(refine_landmarks=True) as face_mesh:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks and hat is not None:
            h, w = frame.shape[:2]
            lm = results.multi_face_landmarks[0].landmark
            # Forehead point (landmark 10)
            forehead = lm[10]
            fx, fy = int(forehead.x * w), int(forehead.y * h)

            hat_w = int(abs(lm[234].x - lm[454].x) * w * 1.3)
            hat_h = int(hat_w * hat.shape[0] / hat.shape[1])
            hat_resized = cv2.resize(hat, (hat_w, hat_h))

            x = fx - hat_w // 2
            y = fy - hat_h
            frame = overlay_image_alpha(frame, hat_resized, x, y)

        cv2.imshow("Face Filter AR", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
```

---

## Recommended Resources

* [OpenCV ArUco Documentation](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)
* [MediaPipe Face Mesh](https://mediapipe.readthedocs.io/en/latest/solutions/face_mesh.html)
