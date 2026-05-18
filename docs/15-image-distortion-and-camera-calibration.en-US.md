[Türkçe](./15-kamera-kalibrasyonu-ve-3d-goru.md) | English

# Camera Calibration and 3D Vision

Your action camera's photos show curved lines where they should be straight. A robot arm's camera miscalculates distance, and the arm reaches the wrong place. Both problems stem from the same source: without knowing the camera model, pixel coordinates can't be converted to real-world coordinates. Calibration learns this model; stereo vision then extracts depth from two calibrated cameras.

## Pinhole Camera Model

Drill a small hole in a dark room wall — the outside world appears inverted and vivid on the opposite wall. This principle, known as camera obscura, underlies the modern camera model.

Focal length (f) in this analogy is the hole's distance from the wall: large f gives narrow angle (telephoto), small f gives wide angle (fisheye). A real-world point (X, Y, Z) relates to image pixel (u, v) by:

$$\begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = K \cdot \begin{bmatrix} X/Z \\ Y/Z \\ 1 \end{bmatrix}$$

Where **K is the camera intrinsic matrix**:

$$K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}$$

$f_x, f_y$: focal length in pixels (depends on sensor size and pixel scale); $c_x, c_y$: image center. Without knowing K, you can't convert "150 units in pixels" to an actual distance.

## Lens Distortions

Real lenses aren't perfect pinholes. Two main types:

**Radial distortion:** Errors grow with distance from image center.
- *Barrel (pincushion):* Edges bulge outward. Action cameras' characteristic fisheye look.
- *Pincushion (cushion):* Edges curve inward. Common in old telephoto lenses.

**Tangential distortion:** Lens and sensor aren't perfectly parallel; image warps in one direction.

Correction formula for radial: $x_{corrected} = x(1 + k_1 r^2 + k_2 r^4 + k_3 r^6)$

Coefficients $k_1, k_2, k_3$ are learned via calibration. Add tangential coefficients $p_1, p_2$ to form distortion vector: `dist = [k1, k2, p1, p2, k3]`.

## Chessboard Calibration

Why chessboard? Corners can be found mathematically with precision — corners are exactly where two black and two white squares meet. 15–20 photos from different angles and distances reliably constrain camera parameters.

```python
import cv2
import numpy as np
import glob

# Interior chessboard corners (6x9 board has 5x8 interior corners)
BOARD_W, BOARD_H = 9, 6
SQUARE_SIZE = 25.0  # in mm

# 3D world coordinates — Z=0 plane
objp = np.zeros((BOARD_H * BOARD_W, 3), np.float32)
objp[:, :2] = np.mgrid[0:BOARD_W, 0:BOARD_H].T.reshape(-1, 2) * SQUARE_SIZE

obj_points = []  # 3D real-world points
img_points = []  # 2D image points
img_size = None

images = glob.glob("calibration/*.jpg")
if not images:
    raise FileNotFoundError("No images in calibration/ folder")

for path in images:
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_size = gray.shape[::-1]  # (width, height)

    ret, corners = cv2.findChessboardCorners(gray, (BOARD_W, BOARD_H), None)

    if ret:
        # Refine corner positions to sub-pixel accuracy
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        obj_points.append(objp)
        img_points.append(corners_refined)

print(f"Used {len(obj_points)} calibration images")

# Compute camera matrix and distortion coefficients
rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    obj_points, img_points, img_size, None, None
)

print(f"RMS reprojection error: {rms:.4f} pixels")
print("Camera matrix K:\n", K)
print("Distortion coefficients:", dist.ravel())

# Save calibration
np.save("camera_matrix.npy", K)
np.save("dist_coeffs.npy", dist)

# Apply undistort to sample image
test_img = cv2.imread(images[0])
undistorted = cv2.undistort(test_img, K, dist)

comparison = np.hstack([test_img, undistorted])
cv2.imshow("Original | Undistorted", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

RMS error < 0.5 pixels indicates good calibration. Above 1.0, add more images from varied angles.

> **⚠️ Warning:** Collect calibration photos at the same focal length. If you zoomed or changed camera settings, recalibrate — K matrix is lens-dependent.

> **💡 Tip:** `cv2.getOptimalNewCameraMatrix()` computes a wider area that compensates for edge loss after undistortion. Use this if image edges matter.

## Stereo Vision and Depth

Close your right eye and look at a pen. Switch eyes — the pen appears shifted. This parallax effect is how your brain computes depth from two eyes.

Two cameras apply the same principle: the image coordinate difference (disparity) of the same point in left and right cameras gives depth:

$$Z = \frac{f \cdot B}{d}$$

Where $f$ is focal length, $B$ is distance between cameras (baseline), and $d$ is disparity. Large disparity = near object; small disparity = far.

```python
import cv2
import numpy as np

# Load stereo images
left_img = cv2.imread("stereo_left.jpg")
right_img = cv2.imread("stereo_right.jpg")
if left_img is None or right_img is None:
    raise FileNotFoundError("Stereo image files not found")

left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

# Semi-Global Block Matching — SGBM
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=128,   # Must be multiple of 16
    blockSize=11,
    P1=8 * 3 * 11**2,    # Penalty for small disparity change
    P2=32 * 3 * 11**2,   # Penalty for large disparity change
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32,
)

disparity = stereo.compute(left_gray, right_gray).astype(np.float32) / 16.0

# Normalize and colorize
disp_normalized = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
disp_color = cv2.applyColorMap(disp_normalized, cv2.COLORMAP_JET)

cv2.imshow("Left Image", left_img)
cv2.imshow("Depth Map", disp_color)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

The depth map's warm colors (red) represent near objects, cool colors (blue) represent far. Computation is challenging on flat surfaces and edges.

> **📌 Note:** For reliable stereo depth, both cameras must be rectified — left and right images aligned to the same horizontal epipolar line. `cv2.stereoRectify()` and `cv2.initUndistortRectifyMap()` do this.

## Practice: Pixel Size to Real Size

After calibration, you can measure real size of objects in photos. Method: include a reference object of known size in the frame, compute pixel-to-mm scale.

```python
import cv2
import numpy as np

# Reference object: known width
W_mm = 85.6  # Credit card width (mm)

img = cv2.imread("measurement.jpg")
if img is None:
    raise FileNotFoundError("measurement.jpg not found")

# Load calibration
K = np.load("camera_matrix.npy")
dist = np.load("dist_coeffs.npy")

# Undistort
img = cv2.undistort(img, K, dist)

# Measure reference object's pixel width manually or auto
ref_pixel_width = 320  # Measured pixel width
focal_length_px = K[0, 0]  # f_x

# Estimate object distance (depth)
# In real use, get from stereo or known distance
Z_mm = 500.0  # Object 500mm away

# Pixel/mm conversion
px_per_mm = ref_pixel_width / W_mm

print(f"Scale: {px_per_mm:.2f} pixels/mm")
print(f"1 pixel ≈ {1/px_per_mm:.3f} mm at this distance")
```

## Method Comparison

| Topic | Method | When to Use |
|-------|--------|-----------|
| Remove lens distortion | `cv2.undistort()` | Always after calibration |
| Monocular depth | Monocular depth (DPT, MiDaS) | No stereo camera available |
| Stereo depth | StereoSGBM | High accuracy, controlled environment |
| 3D point cloud | `cv2.reprojectImageTo3D()` | After stereo, for 3D reconstruction |

## Summary

- Camera intrinsic matrix K relates pixel coordinates to real-world coordinates.
- Radial distortion bulges (barrel) or curves (pincushion) edges; tangential distortion warps in one direction.
- Chessboard calibration with 15–20 images learns K matrix and distortion coefficients reliably.
- RMS reprojection error < 0.5 pixels signals good calibration quality.
- Stereo vision: disparity from left-right coordinate difference yields depth via Z = f·B/d.
- SGBM stereo matching is directly usable in OpenCV; rectification is mandatory.
- After calibration, pixel measurements can be converted to millimeters.

## Further Reading

- Hartley & Zisserman, "Multiple View Geometry in Computer Vision" (2nd ed., 2004) — foundational textbook
- Zhang, Z., "A Flexible New Technique for Camera Calibration" (IEEE TPAMI 2000) — mathematical foundation of chessboard calibration
- OpenCV Camera Calibration Documentation: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
