[Türkçe](./9-renk-uzaylari.md) | English

# Color Spaces and Histograms

Imagine trying to detect a red ball by looking at its RGB color value. Indoors: (220, 40, 30). In bright sunlight: (255, 100, 80). Same ball, but completely different RGB values due to lighting. This problem illustrates why we need to learn color spaces. This chapter covers different representations of color, lighting-independent object detection, and analyzing an image's brightness distribution.

## Why Color Space Is Needed

In the RGB model, red, green, and blue components together encode both hue and brightness. When light changes, all three channels change — even if the hue stays the same. This makes color-based segmentation unstable.

In the HSV (Hue-Saturation-Value) model, hue (H) is separated from brightness. No matter what light a red ball is in, its hue channel gives a similar value; only value (brightness) changes. This separation makes object detection far more reliable.

## RGB/BGR Channels

An OpenCV image is a NumPy array using BGR order. We can examine channels separately with `cv2.split`.

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

# Split channels
b, g, r = cv2.split(img)

# Show each channel separately — zero out others
zero = np.zeros_like(b)

blue_display = cv2.merge([b, zero, zero])
green_display = cv2.merge([zero, g, zero])
red_display = cv2.merge([zero, zero, r])

comparison = np.hstack([img, blue_display, green_display, red_display])
cv2.imshow("Original | B | G | R", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Instead of showing each channel as grayscale alone, we use colored merge to display them — this helps you understand each channel's contribution more clearly.

> **💡 Tip:** `cv2.split` returns each channel as a separate copy — uses memory. If you only need one channel, `b = img[:, :, 0]` is more efficient.

## Grayscale

If color information isn't needed, converting to grayscale both reduces computation by a third and enables many algorithms.

```python
import cv2

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(f"Colored: {img.shape}, Gray: {gray.shape}")

cv2.imshow("Gray", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

OpenCV's grayscale formula is $G = 0.114B + 0.587G + 0.299R$ — it accounts for the human eye's greater sensitivity to green. It's a weighted blend, not a simple average.

When to use grayscale: edge detection, thresholding, template matching, optical flow — most algorithms expect single-channel input.

## HSV Color Space

HSV uses a cylindrical coordinate system:
- **H (Hue — tone):** 0–179° — the color itself. Red near 0°, green 60°, blue 120°.
- **S (Saturation — saturation):** 0–255 — color vibrancy. 0 = gray, 255 = fully saturated.
- **V (Value — brightness):** 0–255 — brightness. 0 = black, 255 = fully bright.

In OpenCV, hue ranges 0–179 instead of 0–360 (divided by 2 to fit in 8-bit).

```python
import cv2
import numpy as np

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Yellow color mask (HSV: H≈25-35, S>100, V>100)
lower_bound = np.array([20, 100, 100])
upper_bound = np.array([40, 255, 255])

mask = cv2.inRange(hsv, lower_bound, upper_bound)

# Apply mask to original image
result = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("Original", img)
cv2.imshow("Mask", mask)
cv2.imshow("Yellow Regions", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`cv2.inRange` produces a binary mask: 255 for pixels within bounds, 0 for others. `cv2.bitwise_and` applies this mask to the original image.

### Common Color HSV Ranges

| Color | H Low | H High | S Low | S High | V Low | V High |
|-------|-------|--------|-------|--------|-------|--------|
| Red (1) | 0 | 10 | 100 | 255 | 100 | 255 |
| Red (2) | 160 | 179 | 100 | 255 | 100 | 255 |
| Orange | 10 | 25 | 100 | 255 | 100 | 255 |
| Yellow | 20 | 40 | 100 | 255 | 100 | 255 |
| Green | 40 | 80 | 50 | 255 | 50 | 255 |
| Blue | 100 | 130 | 50 | 255 | 50 | 255 |
| Purple | 130 | 160 | 50 | 255 | 50 | 255 |

> **💡 Tip:** Red appears at 0° and 170° (two separate ranges: 0–10 and 160–179) because the hue circle closes at 0°/360°. Combine both masks with `cv2.bitwise_or(mask1, mask2)`.

### Real-Time Color Detection

Full example: detect yellow objects in live camera feed.

```python
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open camera")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Yellow color range
    lower = np.array([20, 100, 100])
    upper = np.array([40, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)

    # Clean noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Show side by side
    display = np.hstack([frame, result])
    cv2.imshow("Camera | Yellow Detection", display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

We applied morphological opening to the mask — this cleans small noise pixels. The next chapter covers morphology in detail.

## Lab Color Space

CIE L*a*b* (or Lab) models how the human eye perceives color:
- **L:** Brightness (0–100)
- **a:** Red-Green axis (negative = green, positive = red)
- **b:** Blue-Yellow axis (negative = blue, positive = yellow)

```python
import cv2

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
l, a, b = cv2.split(lab)

print(f"L channel mean: {l.mean():.1f}, a mean: {a.mean():.1f}, b mean: {b.mean():.1f}")
```

Lab's main advantage: color distances — the Euclidean distance between two colors better matches what the human eye perceives. It's preferred for skin tone detection, image segmentation, and color comparison.

## Histogram

A histogram shows how many pixels carry each brightness value. A dark photo has its histogram piled left (low values); an overexposed image piles right (high values). This "personality" of an image is revealed at a glance.

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

path = "test_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Gray histogram: [channel list], [mask], [bin count], [value range]
hist_gray = cv2.calcHist([gray], [0], None, [256], [0, 256])

# Color histogram: each channel separately
colors = ('b', 'g', 'r')
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
axes[0].set_title("Image")
axes[0].axis('off')

axes[1].plot(hist_gray, color='gray', label='Gray')
for ch_idx, color in enumerate(colors):
    hist = cv2.calcHist([img], [ch_idx], None, [256], [0, 256])
    axes[1].plot(hist, color=color, alpha=0.7)

axes[1].set_xlim([0, 256])
axes[1].set_title("Histogram")
axes[1].set_xlabel("Pixel Value")
axes[1].set_ylabel("Pixel Count")
plt.tight_layout()
plt.savefig("histogram.png", dpi=150)
plt.show()
```

Histograms are typically drawn as line plots, not bars — with 256 values, a line looks cleaner.

## Histogram Equalization

In a low-contrast image, most pixels squeeze into a narrow range — the histogram is narrow and tall. Equalization spreads this distribution across 0–255, boosting contrast.

Intuition: we aim for a histogram with equal frequencies across the range. Using the Cumulative Distribution Function (CDF), pixel values are remapped.

```python
import cv2
import numpy as np

path = "dark_image.jpg"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError(f"{path} not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Global histogram equalization
equalized = cv2.equalizeHist(gray)

# CLAHE: Contrast Limited Adaptive Histogram Equalization
# clipLimit: clips local peaks (prevents over-brightening)
# tileGridSize: how many pieces to divide image into
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe_result = clahe.apply(gray)

# Triple comparison
comparison = np.hstack([gray, equalized, clahe_result])
cv2.imshow("Original | equalizeHist | CLAHE", comparison)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Global equalization adjusts the entire image to one histogram — some regions may become over-bright. CLAHE divides the image into small blocks and equalizes each independently; `clipLimit` prevents local peaks. The result is much more balanced and natural.

> **💡 Tip:** In medical imaging (X-ray, MRI), satellite photos, and low-light conditions, CLAHE markedly outperforms global equalization. For color images, apply only to the brightness channel (L in Lab or V in HSV) — this prevents color distortion.

### Histogram Equalization Methods Comparison

| Method | Advantage | Disadvantage | When to Use |
|--------|-----------|--------------|------------|
| `equalizeHist` | Fast, simple | Excessive contrast, noise amplification | Uniform lighting |
| CLAHE | Balanced, natural | Slower, needs tuning | Medical imaging, satellite |

## Summary & Further Reading

- In RGB, hue and brightness are inseparable; when light changes, all channels change. HSV solves this.
- In HSV, Hue codes tone, Saturation saturation, Value brightness. OpenCV's H range is 0–179.
- Red spans two separate hue ranges (0–10 and 160–179); combine with `cv2.bitwise_or`.
- Color mask workflow: `cv2.inRange` + `cv2.bitwise_and` — the foundation of color-based segmentation.
- Lab color space measures distances closer to human perception — useful for skin detection and color comparison.
- Histogram summarizes image brightness distribution; computed with `cv2.calcHist`.
- `equalizeHist` is global, CLAHE is local contrast enhancement. For color images, apply only to brightness channel.

**References**

- OpenCV Color Conversions: [docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html](https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html)
- Zuiderveld, K. (1994). "Contrast Limited Adaptive Histogram Equalization." Graphics Gems IV, Academic Press.
