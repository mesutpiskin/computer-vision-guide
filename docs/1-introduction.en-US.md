[Türkçe](./1-opencv-nedir.md) | English

# What is OpenCV?

If an autonomous vehicle needs to make a braking decision, a surgical robot must move with millimetric precision, or a security camera must identify a missing child in a crowd, the same question lies at the core: how will the machine understand what it sees? In this chapter, we'll explore what computer vision is and get to know OpenCV, the industry standard library that has dominated this field for 25 years. By the end, your development environment will be ready and you'll be able to read and process your first image.

## Computer Vision: Giving Machines the Ability to See

When the human eye looks at a scene, it processes color, depth, motion, and context simultaneously—this is the product of millions of years of evolutionary engineering. Computer vision is the discipline that attempts to transfer this ability to digital systems. Extracting meaning from raw pixel values: identifying an object in an image, measuring motion between frames, reconstructing the three-dimensional structure of a scene.

Applications have already entered everyone's daily life:

- **Autonomous vehicles:** Lane following, pedestrian-oriented object detection, traffic sign reading
- **Medical imaging:** Tumor segmentation in MRI images, skin cancer screening in dermatological images
- **Industrial quality control:** Defect detection at the micron level on production lines
- **Augmented reality:** Face filters, virtual furniture placement, navigation overlays

All of these applications share a common toolkit: OpenCV.

## What is OpenCV?

OpenCV (Open Source Computer Vision Library) is an open-source library containing over 2500 optimized algorithms for computer vision and machine learning. Initiated in 1999 by Gary Bradski while working at Intel, the project continues to grow today with contributions from Itseez, Google, Intel, and community developers.

The library's architecture is layered: a **C++ core** written for maximum performance; **Python, Java, and C#** wrappers make this core accessible. The speed required to manipulate pixels in real-time comes from C++'s efficient memory access; but a prototype developer doesn't need that—the Python interface provides an abstraction compatible with `numpy`.

The numbers tell the scale: over 3 million downloads per week, 47,000+ GitHub stars, active developer communities in over 90 countries. OpenCV is one of the rare libraries where you can move from academic prototype to production system with a single dependency.

## Why OpenCV?

OpenCV's prominence among many image processing libraries is no accident. Real-time applications don't permit sacrificing performance at the pixel level—and OpenCV distinguishes itself at this point from its competitors.

**Hardware acceleration:** Support for CUDA (NVIDIA GPU), OpenCL (general-purpose GPU), AVX/SSE (CPU vectorization), and NEON (ARM) means the same algorithm runs optimized from a desktop GPU to a Raspberry Pi. There can be a 10-50x speed difference between running a Gaussian blur operation on the CPU versus on CUDA.

**Ecosystem depth:** Not just image processing—video analysis, camera calibration, 3D reconstruction, machine learning, deep learning inference all under one roof. You can run PyTorch and TensorFlow models directly with the `cv2.dnn` module.

**Industry backing:** Google Lens, Intel RealSense SDK, Sony camera software, Microsoft HoloLens—all use OpenCV. The support and documentation you might need in a production system are already there.

> **📌 Note:** OpenCV's Python package `opencv-python` contains a compiled binary of the C++ core. That is, `pip install opencv-python` also installs high-performance C++ code—Python merely calls this code.

## When to Use Alternatives

OpenCV isn't a universal solution. Choosing the right tool directly impacts project success.

| Library | Strength | When to Use |
|---------|----------|------------|
| **OpenCV** | Classic CV algorithms, real-time processing, video | Camera streams, object detection, classic filters, production systems |
| **scikit-image** | Research quality, excellent documentation, NumPy compatibility | Academic work, rapid prototyping, signal processing research |
| **Pillow (PIL)** | Simple file I/O, basic transformations | Format conversion, resizing, web application thumbnails |
| **torchvision** | Tight PyTorch integration, data augmentation, model zoo | PyTorch model training, data preprocessing pipelines |
| **imageio** | Multi-format reading (TIFF stacks, DICOM, video) | Medical images, multi-page files, video file reading |

In practice, these libraries don't exclude each other—you can prototype with scikit-image and move to production with OpenCV in one project.

## OpenCV Modules

OpenCV is organized into modules by functionality. Knowing which module solves which problem makes finding the right function easier.

| Module | Name | What It Does |
|--------|------|--------------|
| `core` | Core | Basic data structures (Mat), arithmetic, memory management |
| `imgproc` | Image Processing | Filters, geometric transformations, color space conversions, morphology |
| `highgui` | High Level GUI | Open windows, display images/video, mouse/keyboard events |
| `videoio` | Video I/O | Camera and video file reading/writing, codec management |
| `video` | Video Analysis | Optical flow, background subtraction, object tracking |
| `calib3d` | Calibration and 3D | Camera calibration, stereo vision, perspective transformation |
| `features2d` | Feature Detectors | SIFT, ORB, AKAZE keypoint detection and descriptors |
| `dnn` | Deep Neural Networks | Load and run ONNX, TensorFlow, Caffe, PyTorch models |
| `ml` | Machine Learning | SVM, k-NN, decision trees, random forests |
| `objdetect` | Object Detection | Haar cascades, HOG+SVM detectors, QR/barcode |
| `photo` | Photo Processing | Denoising, HDR merging, color transfer |
| `stitching` | Panorama | Multi-image stitching, spherical projection |

> **💡 Tip:** Read the output of `cv2.getBuildInformation()`. Which modules are enabled, whether CUDA is supported, and which compiler it was built with all appear in this output—especially valuable when debugging environment issues.

## OpenCV 4.x / 5.0 Innovations

### G-API: Graph-Based Pipeline

Traditional OpenCV code runs line by line—each function call executes immediately. G-API (Graph API) instead defines operations as a computation graph first, then optimizes and executes it as a whole. This significantly reduces memory bandwidth usage, especially in multi-stage pipelines.

```python
import cv2 as cv

# Define pipeline with G-API
g_in = cv.GMat()
g_gray = cv.gapi.BGR2Gray(g_in)
g_blur = cv.gapi.gaussianBlur(g_gray, (5, 5), 1.5)
g_edges = cv.gapi.Canny(g_blur, 50, 150)
comp = cv.GComputation(g_in, g_edges)

# Run—the pipeline is optimized and executed in one pass
img = cv.imread("image.jpg")
result = comp.apply(img)
```

### Enhanced DNN Module

With OpenCV 4.7+ comes ONNX Runtime integration, significantly expanding model compatibility. `cv2.dnn.readNetFromONNX()` now supports up to `opset 17`; transformer-based models work.

### QR Code and Barcode Module

```python
import cv2
import numpy as np

img = cv2.imread("qr.jpg")
if img is None:
    raise FileNotFoundError("qr.jpg not found")

detector = cv2.QRCodeDetector()
data, points, _ = detector.detectAndDecode(img)

if data:
    print(f"QR content: {data}")
    # Visualize corner points
    if points is not None:
        pts = points.astype(int).reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

cv2.imshow("QR Code", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

With `cv2.barcode.BarcodeDetector`, 1D barcodes like EAN-13 and Code128 can also be read—no extra dependencies required.

## Installation and First Code

### Installation

```bash
# Basic installation—sufficient for most use cases
pip install opencv-python numpy

# Contrib modules (includes SIFT and additional algorithms)
pip install opencv-contrib-python numpy

# Headless server environment (no GUI window—smaller size)
pip install opencv-python-headless numpy
```

> **⚠️ Warning:** `opencv-python` and `opencv-contrib-python` cannot be installed together in the same environment—both provide the `cv2` module and conflict. Choose one and uninstall the other: `pip uninstall opencv-python`.

### Version and Build Information

```python
import cv2
import numpy as np

# Version information
print(f"OpenCV version : {cv2.__version__}")
print(f"NumPy version  : {np.__version__}")

# Build details—CUDA, OpenCL, optimization flags
build_info = cv2.getBuildInformation()

# Filter to relevant lines only
for line in build_info.splitlines():
    if any(kw in line for kw in ("CUDA", "OpenCL", "AVX", "NEON", "Python")):
        print(line.strip())
```

Typical output:
```
OpenCV version : 4.9.0
NumPy version  : 1.26.4
  CUDA:                      YES (ver 12.2, CUFFT CUBLAS)
  OpenCL:                    YES (no extra features)
  AVX:                       YES
  Python 3:                  /usr/bin/python3 (ver 3.11.0)
```

### First Image: Read, Display, Save

```python
import cv2
import numpy as np

def process_image(input_path: str, output_path: str) -> None:
    """Read an image, display basic information, convert to grayscale, and save."""
    # Read
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"{input_path} not found")

    # Basic information
    height, width, num_channels = img.shape
    print(f"Size      : {width}x{height} pixels")
    print(f"Channels  : {num_channels}  (BGR order—OpenCV doesn't read RGB!)")
    print(f"Data type : {img.dtype}   (uint8 = 0-255 range)")
    print(f"Memory    : {img.nbytes / 1024:.1f} KB")

    # Color space conversion
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Display on screen
    cv2.imshow("Original", img)
    cv2.imshow("Grayscale", gray)
    cv2.waitKey(0)           # Close on any key press
    cv2.destroyAllWindows()

    # Save
    cv2.imwrite(output_path, gray)
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    process_image("test.jpg", "test_gray.jpg")
```

> **⚠️ Warning:** OpenCV reads images in **BGR** order, not RGB. When passing images to Matplotlib or PyTorch, convert with `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` —otherwise colors appear wrong.

### Real-Time Video from Camera

```python
import cv2

cap = cv2.VideoCapture(0)   # 0 = default camera; file path also works
if not cap.isOpened():
    raise RuntimeError("Camera could not be opened")

print(f"Resolution : {cap.get(cv2.CAP_PROP_FRAME_WIDTH):.0f}x"
      f"{cap.get(cv2.CAP_PROP_FRAME_HEIGHT):.0f}")
print(f"FPS        : {cap.get(cv2.CAP_PROP_FPS):.1f}")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Simple operation: horizontal flip
    mirrored = cv2.flip(frame, 1)
    cv2.imshow("Camera", mirrored)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

> **💡 Tip:** `cv2.waitKey(1)` waits one millisecond and returns the ASCII code of the pressed key. The `& 0xFF` mask works around an issue on some platforms where waitKey returns a 32-bit value. Always use this pattern in video loops.

## Summary & Further Reading

- OpenCV with 2500+ algorithms is the single destination for computer vision; its C++ core is accessed through a Python interface.
- Thanks to CUDA, OpenCL, and AVX support, the same code runs optimized from desktop to embedded systems.
- `opencv-python` and `opencv-contrib-python` cannot be installed together; choose one based on your needs.
- OpenCV reads in **BGR**—when passing to Matplotlib, PyTorch, or the web, RGB conversion must not be forgotten.
- G-API optimizes multi-stage pipelines in a single pass, eliminating unnecessary memory copies.
- `cap.release()` and `cv2.destroyAllWindows()` must be called on every exit path of video code—otherwise camera resources are not freed.
- `cv2.getBuildInformation()` is the first place to look when debugging environment issues.

### References

- Bradski, G. (2000). "The OpenCV Library." *Dr. Dobb's Journal of Software Tools.* — the original library paper
- OpenCV Documentation: https://docs.opencv.org/4.x/
- OpenCV GitHub: https://github.com/opencv/opencv
- Kaehler, A. & Bradski, G. (2016). *Learning OpenCV 3.* O'Reilly Media.
