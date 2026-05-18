[Türkçe](./19-oznitelik-cikarimi.md) | English

# Feature Extraction and Matching

You want to turn photos of the same building taken from different angles into a panorama. To do this, the computer must find the same points in both images — the building's corner, a window sill, a door handle — and align them. But if you compare pixel by pixel, a difference in light or a slight angle change ruins the match. In this section, you'll examine feature detectors and descriptors that solve this problem; then we'll go all the way to actually aligning two images.

## What Is a Feature?

Features are the "eye-catching" regions of an image — corners, blobs, distinctive edges. A good feature must be recognizable even if the viewpoint changes, the object is scaled up or down, or the lighting is brighter or dimmer. These three forms of robustness are called **rotation invariance**, **scale invariance**, and **lighting invariance**, respectively.

Why corners? Imagine a straight edge: if you slide along it, nothing changes — the image stays the same. A corner, though, carries information in two directions; it pins you to exactly that spot. It's an unforgeable, repeatable reference point.

> **📌 Note:** A detector tells you *where* to find a point of interest; a descriptor turns what's *around* that point into a numerical vector. They work together.

## SIFT: Scale Invariance

Imagine examining an image with a magnifying glass, scanning at different magnification levels. Points that stand out at every scale are true features — the algorithm that finds them is SIFT (Scale-Invariant Feature Transform).

**How it works, in brief:**

1. Blur the image with different sigma values using Gaussian blur.
2. Take the difference between consecutive Gaussians — these are DoG (Difference of Gaussians) images.
3. Mark local maxima and minima in the DoG pyramid as interest points.
4. Divide the 16×16 neighborhood around each point into 4×4 cells; compute a gradient histogram with 8 directions in each cell. Result: a 128-dimensional vector — the point's fingerprint.

This 128-dimensional vector is robust to rotation and scale changes because it's both normalized to the dominant direction and localized in scale space.

> **📌 Note:** From OpenCV 4.4 onwards, SIFT patent protection has expired and it's available in the main `opencv-python` package; you no longer need `opencv-contrib-python`.

```python
import cv2
import numpy as np

def sift_features(image_path: str) -> None:
    """Detect and visualize SIFT features."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"{image_path} not found")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create(nfeatures=500)
    keypoints, descriptors = sift.detectAndCompute(gray, None)

    print(f"Keypoints found    : {len(keypoints)}")
    print(f"Descriptor matrix shape : {descriptors.shape}")  # (N, 128)

    # Visualize keypoints
    img_kp = cv2.drawKeypoints(
        img, keypoints, None,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )
    cv2.imshow("SIFT Keypoints", img_kp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sift_features("building.jpg")
```

The `DRAW_RICH_KEYPOINTS` flag also draws each point's scale (circle diameter) and dominant direction (line) — useful for seeing what scale it was detected at and its orientation.

## ORB: Speed and Patent Freedom

SIFT works well, but computing 128 floats per pixel is slow on mobile or embedded systems. ORB (Oriented FAST + Rotated BRIEF) solves this differently: it finds keypoints with the FAST corner detector and generates the descriptor as **binary** (a bit string of 0s and 1s) instead of floats.

Comparing two binary descriptors is easy: XOR them, count the 1-bits. This operation is Hamming distance and runs extremely fast on CPU. ORB is roughly 100 times faster than SIFT.

```python
import cv2
import numpy as np

def orb_features(image_path: str) -> None:
    """Detect and visualize ORB features."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"{image_path} not found")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(nfeatures=500)
    keypoints, descriptors = orb.detectAndCompute(gray, None)

    print(f"Keypoints found    : {len(keypoints)}")
    print(f"Descriptor matrix shape : {descriptors.shape}")  # (N, 32) — 256 bits

    img_kp = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0))
    cv2.imshow("ORB Keypoints", img_kp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    orb_features("building.jpg")
```

The ORB descriptor is 32 bytes (256 bits) long — far below SIFT's 512 bytes. On memory-constrained platforms, this difference is critical.

## Feature Matching

We have descriptors extracted from two images. The question is: which point matches which?

### Brute Force Matcher (BFMatcher)

Compares every descriptor with every other descriptor — slow but gives the most accurate match.

- For float descriptors like SIFT: use `cv2.NORM_L2` (Euclidean distance)
- For binary descriptors like ORB: use `cv2.NORM_HAMMING`

### FLANN Matcher

FLANN (Fast Library for Approximate Nearest Neighbors) is far faster than brute force on large descriptor sets. It performs approximate nearest neighbor search — trading a small accuracy loss for large speed gains.

### Lowe's Ratio Test

Raw matching output is noisy — it contains many false matches. David Lowe's SIFT paper proposed a **ratio test** to filter these out:

For each descriptor, find the two closest matches. If the closest is much nearer than the second-closest, the match is reliable. As a formula:

$$\text{match is valid} \iff d_1 < 0.75 \cdot d_2$$

The intuition: a good match should be unrivaled. If the second candidate is nearly as close, we can't be confident in the first.

> **⚠️ Warning:** Don't use raw matches directly without applying the ratio test — false matches will ruin homography estimation.

```python
import cv2
import numpy as np

def match_features(path1: str, path2: str) -> tuple:
    """Match two images using SIFT + FLANN + Lowe ratio test."""
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    if img1 is None:
        raise FileNotFoundError(f"{path1} not found")
    if img2 is None:
        raise FileNotFoundError(f"{path2} not found")

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Extract SIFT features
    sift = cv2.SIFT_create()
    kp1, desc1 = sift.detectAndCompute(gray1, None)
    kp2, desc2 = sift.detectAndCompute(gray2, None)

    # FLANN parameters (for SIFT)
    index_params = dict(algorithm=1, trees=5)   # FLANN_INDEX_KDTREE = 1
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # k=2: find 2 closest matches for each point
    matches = flann.knnMatch(desc1, desc2, k=2)

    # Lowe ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    print(f"Total matches  : {len(matches)}")
    print(f"After ratio test : {len(good_matches)}")

    return img1, img2, kp1, kp2, good_matches
```

## Image Alignment with Homography and RANSAC

We have reliable matches. Now we need to find the **perspective transformation** between the two images — called a homography. A homography is a 3×3 matrix that maps every point from one plane to the correct location on another.

The problem: some matches may still be wrong (outliers). RANSAC (Random Sample Consensus) handles this: it randomly selects 4 point pairs, estimates a homography, and checks how many other points fit this model. The model that explains the most points wins.

```python
import cv2
import numpy as np

def align_images(path1: str, path2: str) -> None:
    """Align two images using SIFT + FLANN + Lowe + Homography."""
    img1, img2, kp1, kp2, good_matches = match_features(path1, path2)

    if len(good_matches) < 10:
        print("Not enough matches found.")
        return

    # Convert matched point coordinates to numpy arrays
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Find homography using RANSAC
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, ransacReprojThreshold=5.0)
    inlier_count = int(mask.sum())
    print(f"RANSAC inlier count: {inlier_count} / {len(good_matches)}")

    # Warp img1 to img2's perspective
    h2, w2 = img2.shape[:2]
    warped = cv2.warpPerspective(img1, H, (w2, h2))

    # Visualize matches (inliers only)
    matchesMask = mask.ravel().tolist()
    draw_params = dict(
        matchColor=(0, 255, 0),
        singlePointColor=None,
        matchesMask=matchesMask,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, **draw_params)

    cv2.imshow("Matches (RANSAC inliers)", img_matches)
    cv2.imshow("Aligned Image", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("matches.jpg", img_matches)
    cv2.imwrite("aligned.jpg", warped)
    print("matches.jpg and aligned.jpg saved.")

def match_features(path1: str, path2: str) -> tuple:
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    if img1 is None:
        raise FileNotFoundError(f"{path1} not found")
    if img2 is None:
        raise FileNotFoundError(f"{path2} not found")

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    kp1, desc1 = sift.detectAndCompute(gray1, None)
    kp2, desc2 = sift.detectAndCompute(gray2, None)

    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(desc1, desc2, k=2)

    good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

    return img1, img2, kp1, kp2, good_matches

if __name__ == "__main__":
    align_images("building_left.jpg", "building_right.jpg")
```

This produces two files: `matches.jpg` shows both images side-by-side with match lines drawn, and `aligned.jpg` is the first image warped to the second's perspective.

> **💡 Tip:** The `ransacReprojThreshold=5.0` parameter is the tolerance in pixels for reprojection error. For high-resolution images, 5-10 pixels is reasonable; for low-resolution, try 2-3.

## Method Comparison

| Method | Accuracy | Speed | Patent | Best Use |
|--------|----------|-------|--------|----------|
| **SIFT** | High | Slow | Free (4.4+) | Panorama, 3D reconstruction, research |
| **ORB** | Medium | Very fast | Free | Mobile app, embedded system, real-time AR |
| **AKAZE** | High | Medium | Free | Texture-rich scenes, rotation invariance critical |

> **📌 Note:** If precision isn't critical and device resources are constrained, ORB is often enough. For research-quality results, prefer SIFT or AKAZE.

## Summary & Further Reading

- A feature detector finds points of interest in an image; a descriptor converts what's around that point into a numerical vector.
- SIFT uses a DoG pyramid to achieve scale invariance and produces a 128-dimensional float descriptor; it's free from patents in OpenCV 4.4+.
- ORB uses binary descriptors, comparing them via Hamming distance, making it ~100× faster than SIFT.
- FLANN is far faster than brute force on large descriptor sets, trading small accuracy for big speed gains.
- Lowe's ratio test (`d1 < 0.75 * d2`) effectively eliminates false matches — always apply it.
- Homography describes the perspective transformation between two images; RANSAC finds the correct one despite outliers.
- The `cv2.findHomography` + `cv2.warpPerspective` pair forms the foundation of panorama and image alignment pipelines.

### References

- Lowe, D.G. (2004). "Distinctive Image Features from Scale-Invariant Keypoints." *IJCV*: https://doi.org/10.1023/B:VISI.0000029664.99615.94
- Rublee, E. et al. (2011). "ORB: An efficient alternative to SIFT or SURF." *ICCV 2011.*
- Alcantarilla, P. et al. (2012). "KAZE Features." *ECCV 2012.*
- Fischler, M. & Bolles, R. (1981). "Random Sample Consensus." *CACM*: https://doi.org/10.1145/358669.358692
