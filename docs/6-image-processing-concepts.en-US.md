[Türkçe](./6-giris-temel-kavramlar.md) | English

# Digital Image Fundamentals

Have you ever wondered how a computer "sees" a security camera recording? That beautiful photo on your screen is actually a table of tens of millions of numbers to the computer. In this chapter, we'll understand the mathematical structure of digital images, read and display images with OpenCV, and establish real-time data flow from a camera.

## What is a Digital Image?

Imagine a black-and-white photograph printed on paper as a grid of squares. Each square carries a single number representing the brightness at that point. The finer the grid, the sharper the image. In a color photograph, each square carries not one but three numbers: red, green, and blue components.

Mathematically, we write: $f(x, y) \to [0, 255]$ — a function that assigns a color value to a coordinate. A grayscale image is a two-dimensional matrix of size H×W; a color image is a three-dimensional tensor of size H×W×3.

**Why the 0–255 range?** Because each pixel is represented by 8 bits: $2^8 = 256$ different values. 0 is pure black, 255 is pure white. Since 8-bit images are the most common format, OpenCV uses the `uint8` data type by default.

> **📌 Note:** 16-bit and 32-bit images also exist — medical imaging (MRI, CT) and HDR photography use these formats. In 32-bit float images, the value range is 0.0–1.0.

## BGR and RGB: OpenCV's Color Order

A color pixel consists of three channels. But in what order? Most applications and libraries use RGB (Red-Green-Blue) order. OpenCV, however, uses BGR (Blue-Green-Red) order for historical reasons: the Windows bitmap format during development preferred this order, and it became standard.

In practice, the only difference is: in an image array returned by OpenCV, `img[:, :, 0]` gives the blue channel, while `img[:, :, 2]` gives the red channel.

> **⚠️ Warning:** If you don't perform the `COLOR_BGR2RGB` conversion when displaying an image in Matplotlib, colors will be wrong — red objects appear blue and blue objects appear red.

## Reading and Displaying Images

OpenCV's most basic operation: read an image from disk, display it on screen, and save it. The following code reads an image, prints its size and data type, displays it on screen, and saves it to a new file.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

# Basic image information
print(f"Size (H×W×C): {img.shape}")   # e.g., (480, 640, 3)
print(f"Data type: {img.dtype}")         # uint8
print(f"Min/Max value: {img.min()}, {img.max()}")

cv2.imshow("Original Image", img)
cv2.waitKey(0)               # Wait until any key is pressed
cv2.destroyAllWindows()

# Save to disk
cv2.imwrite("output.jpg", img)
print("Image saved: output.jpg")
```

`img.shape` gives three numbers: (height, width, number of channels). Height comes first because matrix indexing follows row-column order. In grayscale images, shape is `(H, W)` with no third dimension.

> **💡 Tip:** When `cv2.imread` fails, it returns `None` without raising an error. This is why the `if img is None` check is critical after every read.

### `cv2.imread` Flags

| Flag | Value | Description |
|--------|-------|----------|
| `cv2.IMREAD_COLOR` | 1 (default) | Read color, discard alpha channel |
| `cv2.IMREAD_GRAYSCALE` | 0 | Read as grayscale |
| `cv2.IMREAD_UNCHANGED` | -1 | Read PNG with alpha channel |

## Real-Time Image Reading from Camera

After static images, it's time for live video streams. In OpenCV, camera and video are opened with the same `VideoCapture` interface; the only difference is the argument.

`cv2.VideoCapture(0)` opens the first camera on your operating system (usually the built-in webcam). If you have multiple cameras, try indices `1`, `2`, etc.

```python
import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Camera could not be opened")

# Camera properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Camera: {width}×{height} @ {fps:.1f} FPS")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Camera", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

`cap.read()` returns two values: `ret` (success flag) and `frame` (image). `cv2.waitKey(1)` waits approximately 1 ms — the smaller this value, the higher the frame rate, but if you set it to 0, it will display the first frame and stop.

> **💡 Tip:** The `& 0xFF` mask prevents problems caused by upper bits of key codes on some systems. It's a safe habit to always use it.

### Adjusting Camera Properties

You can change resolution and FPS with `cap.set()`:

```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)
```

> **📌 Note:** If the camera hardware doesn't support the requested value, it will fall back to the nearest supported value. After setting, check the actual value with `cap.get()`.

## Video Files and IP Cameras

The same `VideoCapture` structure opens video files like MP4, AVI, and network streams.

```python
import cv2

# Video file
cap = cv2.VideoCapture("traffic.mp4")

# IP camera RTSP stream — uncomment and modify the URL for your camera
# cap = cv2.VideoCapture("rtsp://192.168.1.100:554/stream")

# HTTP MJPEG stream
# cap = cv2.VideoCapture("http://192.168.1.100:8080/video")

if not cap.isOpened():
    raise IOError("Video source could not be opened")

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Total frames: {total_frames}, FPS: {fps:.1f}")
print(f"Estimated duration: {total_frames / fps:.1f} seconds")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Video", frame)

    # Calculate wait time based on FPS
    wait_time = max(1, int(1000 / fps))
    if cv2.waitKey(wait_time) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

For video files, calculate the wait time based on FPS: for 30 FPS, `1000/30 ≈ 33 ms`; for 25 FPS, `40 ms`. Without this, the video plays much faster than real speed.

> **📌 Note:** IP Camera URL Formats
>
> - RTSP (most common): `rtsp://user:password@192.168.1.100:554/live`
> - HTTP MJPEG: `http://192.168.1.100:8080/video`
> - GStreamer pipeline (Linux): `"v4l2src ! videoconvert ! appsink"`
>
> For RTSP connection issues, try the flag `cv2.VideoCapture("rtsp://...", cv2.CAP_FFMPEG)`.

## Pixel Manipulation

In an OpenCV image, which is a NumPy array, single pixel and region access is done with direct array indexing.

The coordinate system requires attention: `img[y, x]` has row (vertical position = y) first, then column (horizontal = x). This is the standard matrix indexing order.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

# Read single pixel — img[row, column] i.e., img[y, x]
pixel = img[100, 200]
print(f"Pixel at (200, 100) in BGR: {pixel}")

# Write pixel — paint that point red
img_copy = img.copy()
img_copy[100, 200] = [0, 0, 255]   # BGR: red

# ROI (Region of Interest) cropping
# img[y_start:y_end, x_start:x_end]
roi = img[100:300, 150:400].copy()
print(f"ROI size: {roi.shape}")

# Save ROI
cv2.imwrite("roi_output.jpg", roi)

# Highlight ROI — draw rectangle on original
img_highlighted = img.copy()
cv2.rectangle(img_highlighted, (150, 100), (400, 300), (0, 255, 0), 2)

cv2.imshow("ROI Highlighted", img_highlighted)
cv2.imshow("ROI", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

NumPy slicing returns a view — changes to `roi = img[100:300, 150:400]` also affect the original `img`. If you want to work independently, `.copy()` is required.

> **⚠️ Warning:** In the expression `img[100, 200]`, 100 comes first (100 rows = y=100), then 200 columns (x=200). This is the point at Cartesian coordinates (x=200, y=100). Mixing up this order causes annoying bugs — especially when OpenCV functions like `cv2.circle(img, (x, y), ...)` use Cartesian order while NumPy indexing uses matrix order.

## Summary & Further Reading

- A digital image is a discrete sampling of the function $f(x,y) \to [0,255]$; a grayscale image is an H×W matrix, a color image is an H×W×3 tensor.
- OpenCV uses BGR order; the `cv2.COLOR_BGR2RGB` conversion is mandatory before displaying with matplotlib.
- `cv2.imread` returns `None` on failure — always check `if img is None` after every read.
- `cv2.VideoCapture` provides the same interface for camera, video file, and IP camera; arguments are `0`, `"file.mp4"`, or RTSP URL respectively.
- Every video loop must have `if not ret: break` at the end and `cap.release(); cv2.destroyAllWindows()` after the loop.
- Pixel access is `img[y, x]` — row (y) first, then column (x).
- ROI cropping is done with NumPy slicing `img[y1:y2, x1:x2]`; add `.copy()` for independent copies.

**References**

- Bradski, G. & Kaehler, A. (2017). *Learning OpenCV 3*. O'Reilly Media.
- OpenCV Documentation: [docs.opencv.org/4.x](https://docs.opencv.org/4.x/)
