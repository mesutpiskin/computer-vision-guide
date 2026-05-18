[Türkçe](./8-goruntu-manipulasyonu.md) | English

# Image Manipulation and Geometric Transformations

Your browser app snapped a photo of a document, but the document is tilted. Or your object recognition model needs to work consistently from any angle, but the camera isn't fixed. Geometric transformations solve these problems: they move pixels in an image to new locations according to systematic rules. This chapter covers the fundamentals from resizing through perspective correction, plus drawing operations on images.

## Why Geometric Transformation?

Consider two practical scenarios: First, a scanned document photo — because the camera didn't look straight down, the document appears skewed and OCR quality drops. Second, quality control of products on a conveyor belt — the camera sees from different angles but your model needs to work angle-independently. In both cases, geometric transformation solves the problem by repositioning pixel coordinates into a new order.

## Basic Transformations

### Resizing

When you shrink an image, you lose information — that's unavoidable. But the quality of that loss is determined by the interpolation method.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

h, w = img.shape[:2]

# Resize by pixel dimensions
small = cv2.resize(img, (320, 240), interpolation=cv2.INTER_AREA)

# Resize by ratio (enlarge to 150%)
large = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

print(f"Original: {img.shape[:2]}, Small: {small.shape[:2]}, Large: {large.shape[:2]}")

cv2.imshow("Small", small)
cv2.imshow("Large", large)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`INTER_AREA` averages pixel blocks when shrinking — the cleanest reduction. `INTER_LINEAR` interpolates from 4 neighboring pixels when enlarging — fast and good enough. If quality matters, use `INTER_CUBIC` or `INTER_LANCZOS4`, though they're slower.

| Interpolation | Use Case | Speed |
|---------------|----------|-------|
| `INTER_NEAREST` | Pixel art, mask images | Fastest |
| `INTER_LINEAR` | General enlargement | Fast |
| `INTER_AREA` | Shrinking | Medium |
| `INTER_CUBIC` | Quality enlargement | Slow |
| `INTER_LANCZOS4` | Maximum quality | Slowest |

### Flipping

Mirror the image horizontally, vertically, or both:

```python
import cv2

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

flip_vertical = cv2.flip(img, 0)     # 0: vertical axis (up-down)
flip_horizontal = cv2.flip(img, 1)   # 1: horizontal axis (left-right mirror)
flip_both = cv2.flip(img, -1)        # -1: both axes

comparison = np.hstack([img, flip_horizontal, flip_vertical])
cv2.imshow("Original | Horizontal | Vertical", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

When three images sit side by side, the difference is immediately clear: horizontal flip is like looking in a mirror, vertical flip is looking upside down.

### Rotation

The idea behind rotation: take each pixel in the image and rotate it around a chosen center point by a specific angle. Mathematically:

$$[x', y'] = R \cdot [x, y]^T$$

Where $R$ is the rotation matrix. OpenCV uses an expanded form that includes center and scale parameters.

```python
import cv2

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

h, w = img.shape[:2]
center = (w // 2, h // 2)

# Center: image center, angle: 45°, scale: 1.0 (size unchanged)
M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(img, M, (w, h))

# Rotate without cropping — expand canvas
M2 = cv2.getRotationMatrix2D(center, 30, 1.0)
rotated2 = cv2.warpAffine(img, M2, (w, h), borderMode=cv2.BORDER_REPLICATE)

cv2.imshow("Rotated 45", rotated)
cv2.imshow("Rotated 30 Replicate", rotated2)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

The last two arguments to `warpAffine` are the output size. If you don't want the image corners clipped, you can use the diagonal length as canvas size: `int(np.sqrt(h**2 + w**2))`.

## Affine Transformation

Affine transformation guarantees that parallel lines in the input remain parallel in the output. Scaling, rotation, translation, and reflection are all affine transformations. The key point: 3 source points and their destinations are enough — 3 point pairs solve for 6 unknowns.

Intuition: imagine grabbing three points shaped like a triangle and pulling them. The rest of the image stretches and bends to follow, but parallel lines stay parallel.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

h, w = img.shape[:2]

# Source points: top-left, top-right, bottom-left
src_pts = np.float32([
    [0, 0],
    [w - 1, 0],
    [0, h - 1]
])

# Destination points: slight skewing effect
dst_pts = np.float32([
    [0, 0],
    [w - 1, 0],
    [50, h - 1]
])

M = cv2.getAffineTransform(src_pts, dst_pts)
affine_result = cv2.warpAffine(img, M, (w, h))

cv2.imshow("Original", img)
cv2.imshow("Affine", affine_result)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

We moved the bottom-left corner 50 pixels to the right — the image is skewed but the top edge remains straight. Notice: in affine transformation, parallel lines are preserved.

## Perspective Transformation (Homography)

Perspective transformation is a more powerful tool — it no longer guarantees that parallel lines stay parallel, but it lets you model real-world perspective. Smartphone document scanners do exactly this: detect the 4 corners of a document in a photo and "flatten" it.

Mathematically, a 3×3 homography matrix encodes the transformation between source and destination planes. 4 point pairs are enough to solve for 8 unknowns.

Scenario: straighten a tilted photo of a whiteboard. We know the 4 corners of the board.

```python
import cv2
import numpy as np

path = "whiteboard.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

# 4 corners in the original image (clockwise: top-left, top-right, bottom-right, bottom-left)
src_pts = np.float32([
    [120, 50],   # top-left
    [620, 80],   # top-right
    [580, 430],  # bottom-right
    [80, 400]    # bottom-left
])

# Target: a clean rectangle
output_w, output_h = 600, 400
dst_pts = np.float32([
    [0, 0],
    [output_w - 1, 0],
    [output_w - 1, output_h - 1],
    [0, output_h - 1]
])

M = cv2.getPerspectiveTransform(src_pts, dst_pts)
flattened = cv2.warpPerspective(img, M, (output_w, output_h))

cv2.imshow("Original (Tilted)", img)
cv2.imshow("Flattened", flattened)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`warpPerspective` takes a 3×3 homography matrix and transforms each source pixel to destination coordinates. You specify the output size yourself — if you know the document's actual aspect ratio, adjust accordingly.

> **💡 Tip:** In real applications, instead of entering corners manually, you can auto-detect document boundaries with `cv2.findContours`. A 4-sided contour with the largest area is the best document candidate.

> **⚠️ Warning:** Perspective transformation loses information — especially areas outside the corners. For document scanning applications, choose source coordinates as accurately as possible.

## Drawing on Images

In OpenCV, all drawing functions modify the image in-place. If you want to preserve the original, call `img.copy()` first.

```python
import cv2
import numpy as np

# Create an empty black canvas
canvas = np.zeros((500, 700, 3), dtype=np.uint8)

# Rectangle: top-left corner, bottom-right corner, color (BGR), thickness (-1 = filled)
cv2.rectangle(canvas, (50, 50), (300, 200), (0, 255, 0), 2)
cv2.rectangle(canvas, (350, 50), (650, 200), (255, 0, 0), -1)  # filled blue

# Circle: center, radius, color, thickness
cv2.circle(canvas, (150, 350), 80, (0, 0, 255), 3)
cv2.circle(canvas, (500, 350), 60, (0, 255, 255), -1)  # filled yellow

# Line: start, end, color, thickness
cv2.line(canvas, (0, 480), (700, 480), (200, 200, 200), 1)

# Text: text, position (bottom-left corner), font, scale, color, thickness
cv2.putText(
    canvas, "OpenCV Drawing", (50, 470),
    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2
)

cv2.imshow("Drawing Examples", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

The color argument is always a `(B, G, R)` tuple. `thickness=-1` fills the shape. The `cv2.putText` coordinate is the bottom-left corner of the text — not the top.

> **⚠️ Warning:** `cv2.putText` doesn't support Turkish characters (ş, ğ, ü, ç, ö, ı). Use the PIL/Pillow library for Turkish text.

### Drawing Functions Summary

| Function | Basic Parameters | Note |
|----------|------------------|------|
| `cv2.rectangle` | top-left, bottom-right, color, thickness | `-1` thickness = filled |
| `cv2.circle` | center, radius, color, thickness | `-1` thickness = filled |
| `cv2.line` | start, end, color, thickness | |
| `cv2.ellipse` | center, axes, angle, start, end | |
| `cv2.polylines` | point array, closed?, color, thickness | |
| `cv2.putText` | text, position, font, scale, color, thickness | ASCII characters only |

## ROI Cropping

ROI (Region of Interest) is the simplest way to extract a specific region from an image. It uses NumPy slicing.

```python
import cv2

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

# img[y1:y2, x1:x2] — vertical (rows) first, then horizontal (columns)
roi = img[80:280, 100:400].copy()

print(f"Original: {img.shape[:2]}, ROI: {roi.shape[:2]}")

# Show ROI boundary on original
display = img.copy()
cv2.rectangle(display, (100, 80), (400, 280), (0, 255, 0), 2)

cv2.imshow("ROI Display", display)
cv2.imshow("ROI", roi)
cv2.imwrite("cropped_region.jpg", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

ROI cropping uses lazy evaluation — no new memory is allocated until you call `.copy()`. It just opens a "window" into the original array. If you process an ROI and put it back into the pipeline, you can use this feature: `img[y1:y2, x1:x2] = processed_roi`.

## Summary & Further Reading

- Interpolation choice directly affects image quality: use `INTER_AREA` when shrinking, `INTER_LINEAR` or `INTER_CUBIC` when enlarging.
- Affine transformation preserves parallel lines — 3 point pairs are enough; use `cv2.getAffineTransform` + `cv2.warpAffine`.
- Perspective transformation (homography) doesn't preserve parallel lines but models plane-to-plane transformation with 4 corners — the foundation of document scanning apps.
- Use `cv2.warpPerspective` for perspective correction, `cv2.warpAffine` for affine/rotation/translation.
- Drawing functions modify images in-place; call `.copy()` first to preserve the original.
- ROI cropping uses `img[y1:y2, x1:x2]` — `.copy()` is mandatory for independent copies.
- `cv2.putText` is ASCII-only; use PIL/Pillow for Turkish characters.

**References**

- Bradski, G. & Kaehler, A. (2017). *Learning OpenCV 3*. O'Reilly Media.
- OpenCV Geometric Transformations: [docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html)
