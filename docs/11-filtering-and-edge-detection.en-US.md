[Türkçe](./11-filtreler-ve-kenar-belirleme.md) | English

# Filtering and Edge Detection

Every image from a camera sensor contains some noise — especially in low light, pixel values may deviate from what they should be. These random fluctuations cause serious problems for sensitive algorithms like edge detection: noise pixels look like "edges" too. This chapter covers filters that clean images and algorithms that then detect edges cleanly.

## Convolution Intuition

Convolution happens as a small window (kernel) slides across the image. At each position: pixel values in the window are multiplied by kernel coefficients, and the sum becomes the new pixel value. Different kernels create different effects — an averaging kernel blurs, a difference kernel highlights edges.

Mathematically (2D discrete convolution):

$$G[i, j] = \sum_{m} \sum_{n} I[i+m, j+n] \cdot K[m, n]$$

Where $I$ is the source image, $K$ is the kernel, and $G$ is the output. Border pixels need special handling (padding) — OpenCV uses mirroring by default.

## Blurring Filters

### Average Filter

Averages all pixel values in the kernel with equal weight. Fast but damages edges.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

# Kernel size 5×5 — must be odd and positive
average = cv2.blur(img, (5, 5))

cv2.imshow("Original | Average 5x5", np.hstack([img, average]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Gaussian Filter

Weights center pixels higher, distant pixels lower. Closer to how human vision blurs — visually more natural.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

# sigmaX=0: auto-compute from kernel size
gaussian = cv2.GaussianBlur(img, (5, 5), sigmaX=0)

cv2.imshow("Original | Gaussian 5x5", np.hstack([img, gaussian]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Gaussian sigma controls blur amount. When `sigmaX=0`, OpenCV calculates it by formula: $\sigma = 0.3 \cdot ((k-1) \cdot 0.5 - 1) + 0.8$.

### Median Filter

Sorts all pixel values in the neighborhood and takes the median. Excellent for salt-and-pepper noise because extreme values (0 or 255) are never the median.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

# Add synthetic salt-and-pepper noise
noisy = img.copy()
noise_mask = np.random.random(img.shape[:2])
noisy[noise_mask < 0.02] = 0      # 2% black pixels
noisy[noise_mask > 0.98] = 255    # 2% white pixels

# ksize must be odd and >= 3
median = cv2.medianBlur(noisy, 5)

cv2.imshow("Noisy | Median", np.hstack([noisy, median]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Median filtering is especially preferred for barcode readers and scanned documents where salt-and-pepper noise is common.

### Bilateral Filter

Removes noise while preserving edges. Beyond standard Gaussian filtering, it weights pixel intensity difference too: if a neighbor is both far away AND value-different (edge point), it gets low weight.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

# d=9: neighborhood diameter, sigmaColor=75: color difference tolerance, sigmaSpace=75: distance tolerance
bilateral = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

cv2.imshow("Original | Bilateral", np.hstack([img, bilateral]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Bilateral filtering's cost is performance — it's noticeably slower than others. Use carefully in real-time apps.

### Filter Comparison

| Filter | Noise Type | Edge Preservation | Speed | Usage |
|--------|-----------|-------------------|-------|--------|
| Average | General | Weak | Very fast | Quick prototype |
| Gaussian | Gaussian noise | Medium | Fast | General purpose, pre-Canny |
| Median | Salt-and-pepper | Good | Medium | Barcode, scanned docs |
| Bilateral | General | Excellent | Slow | Face processing, artistic effects |

### Four Filters Side by Side

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

average   = cv2.blur(img, (5, 5))
gaussian   = cv2.GaussianBlur(img, (5, 5), 0)
median     = cv2.medianBlur(img, 5)
bilateral  = cv2.bilateralFilter(img, 9, 75, 75)

def label(img, text):
    k = img.copy()
    cv2.putText(k, text, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return k

row1 = np.hstack([label(img, "Original"), label(average, "Average")])
row2 = np.hstack([label(gaussian, "Gaussian"), label(median, "Median")])
row3 = np.hstack([label(bilateral, "Bilateral"), np.zeros_like(img)])

result = np.vstack([row1, row2])
cv2.imshow("Filter Comparison", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Gaussian and Median compared with same kernel size show differences most clearly at edge regions.

## Edge Detection

Intuition: an edge is where brightness difference between neighboring pixels is large. We measure this difference by computing the image's derivative.

## Sobel Operator

Sobel computes horizontal and vertical gradients of the image. Horizontal gradient ($G_x$) detects vertical edges, vertical gradient ($G_y$) detects horizontal edges.

Gradient magnitude is:

$$|G| = \sqrt{G_x^2 + G_y^2}$$

This value shows how fast intensity changes at a pixel — high means edge point.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)  # reduce noise first

# CV_64F: use 64-bit float to capture negative gradients
sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)   # horizontal gradient
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)   # vertical gradient

# Compute magnitude, convert to uint8
magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
magnitude = np.uint8(np.clip(magnitude, 0, 255))

# For display, normalize
sobel_x_display = cv2.convertScaleAbs(sobel_x)
sobel_y_display = cv2.convertScaleAbs(sobel_y)

cv2.imshow("Sobel X | Y | Magnitude",
           np.hstack([sobel_x_display, sobel_y_display, magnitude]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Using `CV_64F` is important — with `uint8`, negative gradients clamp to zero and some edges vanish. After computing, use `convertScaleAbs` to return uint8 for display.

## Canny Edge Detector

Canny remains the most widely used edge detector today. Its four-stage pipeline produces clean, thin, connected edges:

1. **Gaussian noise reduction:** so small noise doesn't look like edges.
2. **Sobel gradient computation:** measure edge strength and direction at each pixel.
3. **Non-maximum suppression:** delete pixels that aren't local maxima along edge direction — edges become thin.
4. **Double thresholding (Hysteresis):** strong edges ($> t_{high}$) are kept; weak edges ($t_{low} < x < t_{high}$) connected to strong ones are kept; rest discarded.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Manual thresholds
canny_manual = cv2.Canny(gray, threshold1=50, threshold2=150)

# Auto threshold: based on median
sigma = 0.33
median = float(np.median(gray))
low = int(max(0, (1.0 - sigma) * median))
high = int(min(255, (1.0 + sigma) * median))
canny_auto = cv2.Canny(gray, low, high)

print(f"Auto thresholds — low: {low}, high: {high}")

cv2.imshow("Canny Manual | Auto",
           np.hstack([canny_manual, canny_auto]))
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Auto threshold formula: $t_{low} = (1-\sigma) \cdot \text{median}$ and $t_{high} = (1+\sigma) \cdot \text{median}$. With $\sigma = 0.33$, this works well for most images.

> **💡 Tip:** Auto threshold formula: `sigma=0.33`, `low=int((1.0-sigma)*median)`, `high=int((1.0+sigma)*median)`. This is a reliable starting point — fine-tune for your specific image.

> **⚠️ Warning:** Canny's input parameters matter — especially Gaussian sigma. Manual `GaussianBlur` before calling Canny gives you better control.

### Canny vs Sobel Comparison

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Sobel
sobel_x = cv2.Sobel(gray_blur, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray_blur, cv2.CV_64F, 0, 1, ksize=3)
sobel_mag = cv2.convertScaleAbs(np.sqrt(sobel_x**2 + sobel_y**2))

# Canny — auto threshold
median = float(np.median(gray_blur))
canny = cv2.Canny(gray_blur,
                  int(max(0, 0.67 * median)),
                  int(min(255, 1.33 * median)))

def label(image, text):
    k = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.putText(k, text, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return k

result = np.hstack([label(sobel_mag, "Sobel"), label(canny, "Canny")])
cv2.imshow("Sobel vs Canny", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Canny edges are far thinner and connected than Sobel — non-maximum suppression makes each edge one pixel thick. Sobel is raw gradient, faster but thicker.

## Laplacian Operator

While Sobel computes first derivative (gradient), Laplacian computes second derivative. It finds edges at zero-crossings — works in all directions at once.

Mathematically: $\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}$

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)

laplacian = cv2.Laplacian(gray, cv2.CV_64F)
laplacian_abs = cv2.convertScaleAbs(laplacian)

cv2.imshow("Laplacian", laplacian_abs)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Laplacian is very noise-sensitive — always apply Gaussian blurring first. In practice, it doesn't replace Canny but finds use in focus analysis (which region is sharper?).

## Summary & Further Reading

- Convolution: kernel slides across image; at each position, dot product of values and weights becomes the output.
- Gaussian filter is the best general-purpose noise reducer; standard pre-processing before edge detection.
- Median filter excels at salt-and-pepper noise — other filters just spread it around.
- Bilateral filter preserves edges while removing noise but is slow — use carefully in real-time apps.
- Sobel computes gradients separately; use `CV_64F` to avoid losing negative gradients.
- Canny's four-stage pipeline produces the cleanest edges; non-maximum suppression makes edges one pixel thick.
- Auto Canny threshold: `sigma=0.33`, `low=(1-sigma)*median`, `high=(1+sigma)*median`.
- Laplacian computes second derivative — very noise-sensitive; always blur first.

**References**

- Canny, J. (1986). "A Computational Approach to Edge Detection." *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 8(6), 679–698.
- Gonzalez, R. C. & Woods, R. E. (2017). *Digital Image Processing* (4th ed.). Pearson.
