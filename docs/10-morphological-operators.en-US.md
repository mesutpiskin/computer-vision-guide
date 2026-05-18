[Türkçe](./10-morfolojik-goruntu-isleme.md) | English

# Morphological Image Processing

You performed thresholding and got a binary image — but there are small noise spots and holes inside detected objects. These two problems are precisely where morphological operations excel. Morphology cleans shapes in binary images by shrinking, expanding, merging, and separating them. This chapter covers thresholding methods and fundamental morphological operators.

## Why Morphology?

Real scenario: a factory conveyor counts passing parts using a camera. You thresholded to separate objects from background. But now you face problems:

1. Small noise pixels around the object — each one gets counted as a fake object.
2. Holes inside the object — the object looks like two separate pieces.

Erosion solves the first problem, Dilation the second. Their combinations — Opening and Closing — handle both at once.

## Thresholding — Moving to Binary Image

Morphology works on binary (black and white) images. Three main ways to convert grayscale to binary:

**Simple thresholding:** Pixels below your chosen threshold become 0, above become 255.

```python
import cv2
import numpy as np

path = "object.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Fixed threshold
_, simple = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Otsu: automatically compute threshold (ideal for bimodal histogram)
_, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Adaptive: each region gets its own threshold (for varying illumination)
adaptive = cv2.adaptiveThreshold(
    gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    blockSize=11,    # neighborhood size (odd, >1)
    C=2              # constant subtracted from mean
)

comparison = np.hstack([simple, otsu, adaptive])
cv2.imshow("Fixed | Otsu | Adaptive", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

The Otsu algorithm analyzes the histogram and finds the threshold that maximizes variance between two classes — instead of guessing, just add the `THRESH_OTSU` flag. Adaptive thresholding works much better on shadowed or unevenly lit images (handwriting, book pages).

| Method | When to Use |
|--------|------------|
| Fixed threshold | Controlled studio lighting, simple tests |
| Otsu | Uniform background, bimodal histogram |
| Adaptive | Varying illumination, shadows, natural scenes |

## Structuring Element

The "brush" of morphology operations is the structuring element. Its size and shape determine how the operation behaves.

Intuition: a large brush erases small details, a fine brush does precision work. Circular shapes work well for round objects, rectangular shapes for sharp corners.

```python
import cv2

# Rectangular kernel 5×5
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Ellipse kernel 5×5 — for round objects
ellipse_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Cross/plus kernel
cross_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))

print("Rectangular kernel:\n", rect_kernel)
print("Ellipse kernel:\n", ellipse_kernel)
```

The ellipse kernel clips the corners of a rectangle — it produces more natural results on round objects.

## Erosion (Shrinking)

Shrinks objects: the kernel is white only where it lies entirely over the object. Otherwise it turns black. The object erodes from inside out, shrinking.

Intuition: press a hard brush around an object and smear black paint wherever the brush doesn't fit entirely inside. The object shrinks, thin connections break, small noise vanishes completely.

```python
import cv2
import numpy as np

path = "binary_image.jpg"
binary = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if binary is None:
    raise FileNotFoundError(f"{path} not found")

_, binary = cv2.threshold(binary, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

eroded = cv2.erode(binary, kernel, iterations=1)

cv2.imshow("Original | Eroded", np.hstack([binary, eroded]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

The `iterations` parameter specifies how many times to repeat. 2 iterations is equivalent to applying erosion twice in a row.

## Dilation (Expansion)

The opposite of erosion: the kernel is white wherever it touches the object at any point. The object expands outward.

Intuition: stamp the brush at every object point. The object inflates, holes close, nearby objects merge.

```python
import cv2
import numpy as np

path = "binary_image.jpg"
binary = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if binary is None:
    raise FileNotFoundError(f"{path} not found")

_, binary = cv2.threshold(binary, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

dilated = cv2.dilate(binary, kernel, iterations=1)

cv2.imshow("Original | Dilated", np.hstack([binary, dilated]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Opening = Erosion → Dilation

First shrink, then expand. Together they remove small noise but keep large objects. Erosion eliminates noise, then Dilation restores the large object roughly to original size.

Intuition: imagine a small pebble and a large block. Erosion shrinks both — but the pebble vanishes entirely, the block only slightly. Dilation then restores the block; the pebble is gone.

```python
import cv2
import numpy as np

path = "binary_image.jpg"
binary = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if binary is None:
    raise FileNotFoundError(f"{path} not found")

_, binary = cv2.threshold(binary, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

cv2.imshow("Original | Opening", np.hstack([binary, opened]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Closing = Dilation → Erosion

First expand, then shrink. Closes holes inside objects but preserves object size. Dilation fills holes, then Erosion returns the object to original boundaries.

Intuition: first inflate the object — holes close. Then shrink — the object returns to its old size but now without holes.

```python
import cv2
import numpy as np

path = "binary_image.jpg"
binary = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if binary is None:
    raise FileNotFoundError(f"{path} not found")

_, binary = cv2.threshold(binary, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

cv2.imshow("Original | Closing", np.hstack([binary, closed]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Morphological Gradient

The difference between Dilation and Erosion: the object's boundary — its edge.

Mathematically: $\text{Gradient} = \text{Dilation}(A) - \text{Erosion}(A)$

The result shows the outer boundary of the object. Unlike gradient-based edge detectors like Canny, morphology works on binary images and typically produces thicker but less noisy edges.

```python
import cv2
import numpy as np

path = "binary_image.jpg"
binary = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if binary is None:
    raise FileNotFoundError(f"{path} not found")

_, binary = cv2.threshold(binary, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

cv2.imshow("Binary | Gradient", np.hstack([binary, gradient]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## Comparison Table

| Operation | Formula | Purpose | When to Use |
|-----------|---------|---------|------------|
| Erosion | $E = A \ominus B$ | Shrink object, erase noise | Small noise pixels |
| Dilation | $D = A \oplus B$ | Grow object, close holes | Fragmented objects |
| Opening | Erosion → Dilation | Remove noise, preserve object | Noise around object |
| Closing | Dilation → Erosion | Close holes, preserve object | Holes inside object |
| Gradient | Dilation - Erosion | Extract object boundary | Edge/contour detection |

## All Operations: Single Example

This code applies all 6 operations to one image and displays them side by side:

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if img is None:
    raise FileNotFoundError(f"{path} not found")

_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

eroded   = cv2.erode(binary, kernel, iterations=1)
dilated  = cv2.dilate(binary, kernel, iterations=1)
opened   = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
closed   = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

# Add labels
def add_label(image, text):
    copy = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.putText(copy, text, (5, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return copy

row1 = np.hstack([
    add_label(binary, "Binary"),
    add_label(eroded, "Erosion"),
    add_label(dilated, "Dilation"),
])
row2 = np.hstack([
    add_label(opened, "Opening"),
    add_label(closed, "Closing"),
    add_label(gradient, "Gradient"),
])

result = np.vstack([row1, row2])
cv2.imshow("Morphological Operations", result)
cv2.imwrite("morphology_comparison.jpg", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Six frames in one window. First row: Binary, Erosion, Dilation. Second row: Opening, Closing, Gradient. Seeing each operation's effect side by side is the fastest way to cement understanding.

> **⚠️ Warning:** Morphological operations require the image to be binary (0 or 255). They technically work on grayscale too, but the results are interpreted differently — gray morphology is a separate topic.

## Summary & Further Reading

- Thresholding converts grayscale to binary. Otsu finds threshold automatically; Adaptive handles varying illumination.
- Structuring element (kernel) is the morphology operation's brush — size and shape affect the result.
- Erosion shrinks objects and removes small noise; Dilation expands objects and closes holes.
- Opening = Erosion + Dilation: cleans noise around objects.
- Closing = Dilation + Erosion: closes holes inside objects.
- Gradient = Dilation - Erosion: extracts object boundary.
- `cv2.morphologyEx` provides Opening, Closing, and Gradient in one function.

**References**

- Serra, J. (1982). *Image Analysis and Mathematical Morphology*. Academic Press.
- OpenCV Morphological Transformations: [docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
