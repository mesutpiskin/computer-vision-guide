# English Translation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Translate all 30 Turkish documentation chapters into English, producing complete `.en-US.md` files that mirror the O'Reilly-style pedagogical structure of the Turkish originals.

**Architecture:** Each task reads a Turkish source file, produces an English translation that preserves structure and code exactly, and commits the result. All 30 tasks are fully independent and can run in parallel as 4 groups.

**Tech Stack:** Markdown, Python (code blocks kept as-is), git

---

## Translation Rules (Apply to Every Task)

These rules are mandatory for every agent working on this plan:

1. **Translate all prose** into natural, fluent English — not word-for-word, but idiomatic English that carries the same meaning and pedagogical tone.
2. **Keep all Python code blocks unchanged** — do not modify variable names, function calls, or logic.
3. **Translate inline code comments** — e.g., `# renkli görüntüyü oku` → `# read the color image`
4. **Translate callout box labels:**
   - `> **💡 İpucu:**` → `> **💡 Tip:**`
   - `> **⚠️ Dikkat:**` → `> **⚠️ Warning:**`
   - `> **📌 Not:**` → `> **📌 Note:**`
5. **Add language switcher at the very top** of each file (before the title):
   ```
   [Türkçe](./TURKISH-FILENAME.md) | English
   ```
6. **Preserve all section headings, structure, and formatting** — same heading hierarchy, same table structure, same callout placement.
7. **Keep technical terms in English** — they are already standard English in the Turkish source (e.g., `cv2.imread`, `YOLO`, `Softmax`, `Attention`).
8. **Translate comparison table content** — keep the table structure, translate all cell text.
9. **Tone:** Same O'Reilly teaching voice — a knowledgeable instructor explaining to a smart student. Confident, clear, not dry.

---

## File Map

| # | Turkish Source | English Target | Action |
|---|---------------|----------------|--------|
| 1 | `docs/1-opencv-nedir.md` | `docs/1-introduction.en-US.md` | Overwrite (empty) |
| 2 | `docs/2-gelistirme-ortamlari.md` | `docs/2-development-environments.en-US.md` | Overwrite (empty) |
| 3 | `docs/3-opencv-wrappers.md` | `docs/3-opencv-wrappers.en-US.md` | Overwrite (empty) |
| 4 | `docs/4-opencv-kurulumlar.md` | `docs/4-opencv-installation.en-US.md` | Overwrite (empty) |
| 5 | `docs/5-ide-yapilandirmasi.md` | `docs/5-ide-Configuration.en-US.md` | Overwrite (empty) |
| 6 | `docs/6-giris-temel-kavramlar.md` | `docs/6-image-processing-concepts.en-US.md` | Overwrite (empty) |
| 7 | `docs/7-video-kaydediciler-codec.md` | `docs/7-video-recorder-codec.en-US.md` | Overwrite (empty) |
| 8 | `docs/8-goruntu-manipulasyonu.md` | `docs/8-pixel-manipulation.en-US.md` | Overwrite (empty) |
| 9 | `docs/9-renk-uzaylari.md` | `docs/9-color-spaces.en-US.md` | Overwrite (empty) |
| 10 | `docs/10-morfolojik-goruntu-isleme.md` | `docs/10-morphological-operators.en-US.md` | Create new (fix double extension) |
| 11 | `docs/11-filtreler-ve-kenar-belirleme.md` | `docs/11-filtering-and-edge-detection.en-US.md` | Overwrite (empty) |
| 12 | `docs/12-arka-plan-cikarma.md` | `docs/12-background-subtraction.en-US.md` | Overwrite (empty) |
| 13 | `docs/13-video-analiz.md` | `docs/13-object-tracking.en-US.md` | Overwrite (empty) |
| 14 | `docs/14-nesne-tespiti.md` | `docs/14-object-detection.en-US.md` | Overwrite (empty) |
| 15 | `docs/15-kamera-kalibrasyonu-ve-3d-goru.md` | `docs/15-image-distortion-and-camera-calibration.en-US.md` | Overwrite (empty) |
| 17 | `docs/17-yuz-tanima.md` | `docs/17-face-recognition.en-US.md` | Overwrite (empty) |
| 18 | `docs/18-optik-karakter-tanima.md` | `docs/18-optic-character-recognition.en-US.md` | Overwrite (empty) |
| 19 | `docs/19-oznitelik-cikarimi.md` | `docs/19-feature-extraction.en-US.md` | Overwrite (empty) |
| 20 | `docs/20-gpu-paralel-hesaplama.md` | `docs/20-gpu-parallel-computing.en-US.md` | Create new |
| 21 | `docs/21-poz-tahmini.md` | `docs/21-pose-estimation.en-US.md` | Create new |
| 22 | `docs/22-segmentasyon.md` | `docs/22-segmentation.en-US.md` | Create new |
| 23 | `docs/23-edge-deployment.md` | `docs/23-edge-deployment.en-US.md` | Create new |
| 24 | `docs/24-opencv-mobil.md` | `docs/24-opencv-mobile.en-US.md` | Create new |
| 25 | `docs/25-artirilmis-gerceklik.md` | `docs/25-augmented-reality.en-US.md` | Create new |
| 26 | `docs/26-vision-transformers.md` | `docs/26-vision-transformers.en-US.md` | Create new |
| 27 | `docs/27-generatif-modeller.md` | `docs/27-generative-models.en-US.md` | Create new |
| 28 | `docs/28-3d-vision.md` | `docs/28-3d-vision.en-US.md` | Create new |
| 29 | `docs/29-video-siniflandirma.md` | `docs/29-video-understanding.en-US.md` | Create new |
| 30 | `docs/30-model-egitimi-ve-degerlendirme.md` | `docs/30-model-training.en-US.md` | Create new |
| 31 | `docs/31-vision-language-modeller.md` | `docs/31-vision-language-models.en-US.md` | Create new |

---

## GRUP A — Setup & Introduction (Tasks 1–7)

All 7 tasks in this group are independent and can run in parallel.

---

### Task 1: Chapter 1 — What is OpenCV?

**Files:**
- Read: `docs/1-opencv-nedir.md` (256 lines)
- Write: `docs/1-introduction.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/1-opencv-nedir.md
```

- [ ] **Step 2: Write the English translation**

Apply all Translation Rules above. The file starts with the language switcher:
```
[Türkçe](./1-opencv-nedir.md) | English
```

Then translate the full content. The chapter covers: what computer vision is, OpenCV history (Gary Bradski, Intel 1999), why OpenCV (C++ core, Python interface, CUDA/OpenCL support), module overview table (core, imgproc, highgui, video, calib3d, features2d, dnn), comparison table with scikit-image / Pillow / PyTorch Vision, OpenCV 4.9/5.0 highlights, and the first code example checking the installed version.

Write to: `docs/1-introduction.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/1-introduction.en-US.md
head -3 docs/1-introduction.en-US.md
```

Expected: 200+ lines, first line is the language switcher.

- [ ] **Step 4: Commit**

```bash
git add docs/1-introduction.en-US.md
git commit -m "docs: ch1 translate to English - what is OpenCV, modules, alternatives"
```

---

### Task 2: Chapter 2 — Development Environment

**Files:**
- Read: `docs/2-gelistirme-ortamlari.md` (124 lines)
- Write: `docs/2-development-environments.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/2-gelistirme-ortamlari.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./2-gelistirme-ortamlari.md) | English`

Content: Python setup, VS Code, Jupyter Notebook, Google Colab, Conda environment creation.

Write to: `docs/2-development-environments.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/2-development-environments.en-US.md
head -3 docs/2-development-environments.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/2-development-environments.en-US.md
git commit -m "docs: ch2 translate to English - development environment setup"
```

---

### Task 3: Chapter 3 — OpenCV Wrappers

**Files:**
- Read: `docs/3-opencv-wrappers.md` (94 lines)
- Write: `docs/3-opencv-wrappers.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/3-opencv-wrappers.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./3-opencv-wrappers.md) | English`

Content: EmguCV, JavaCV, LiveCV, RubyCV — what they are and differences between wrappers.

Write to: `docs/3-opencv-wrappers.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/3-opencv-wrappers.en-US.md && head -3 docs/3-opencv-wrappers.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/3-opencv-wrappers.en-US.md
git commit -m "docs: ch3 translate to English - OpenCV wrappers"
```

---

### Task 4: Chapter 4 — Installation and Compilation

**Files:**
- Read: `docs/4-opencv-kurulumlar.md` (176 lines)
- Write: `docs/4-opencv-installation.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/4-opencv-kurulumlar.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./4-opencv-kurulumlar.md) | English`

Content: OpenCV installation for Windows, Linux, macOS, Raspberry Pi. pip install vs source compilation.

Write to: `docs/4-opencv-installation.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/4-opencv-installation.en-US.md && head -3 docs/4-opencv-installation.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/4-opencv-installation.en-US.md
git commit -m "docs: ch4 translate to English - installation and compilation"
```

---

### Task 5: Chapter 5 — IDE Configuration

**Files:**
- Read: `docs/5-ide-yapilandirmasi.md` (160 lines)
- Write: `docs/5-ide-Configuration.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/5-ide-yapilandirmasi.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./5-ide-yapilandirmasi.md) | English`

Content: VS Code, PyCharm, Conda, Google Colab, Android Studio configuration.

Write to: `docs/5-ide-Configuration.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/5-ide-Configuration.en-US.md && head -3 docs/5-ide-Configuration.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/5-ide-Configuration.en-US.md
git commit -m "docs: ch5 translate to English - IDE configuration"
```

---

### Task 6: Chapter 6 — Introduction and Basic Concepts

**Files:**
- Read: `docs/6-giris-temel-kavramlar.md` (223 lines)
- Write: `docs/6-image-processing-concepts.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/6-giris-temel-kavramlar.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./6-giris-temel-kavramlar.md) | English`

Content: digital image as a number grid, matrix representation (2D grayscale, 3D color), BGR vs RGB explanation (with ⚠️ Warning callout about matplotlib), `cv2.imread` / `cv2.imshow` / `cv2.waitKey`, `img.shape` and `img.dtype`, webcam capture loop (`cv2.VideoCapture(0)`), video file and IP camera, pixel read/write, ROI cropping.

Write to: `docs/6-image-processing-concepts.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/6-image-processing-concepts.en-US.md && head -3 docs/6-image-processing-concepts.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/6-image-processing-concepts.en-US.md
git commit -m "docs: ch6 translate to English - digital image basics, camera capture"
```

---

### Task 7: Chapter 7 — Video Recorders and Codecs

**Files:**
- Read: `docs/7-video-kaydediciler-codec.md` (94 lines)
- Write: `docs/7-video-recorder-codec.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/7-video-kaydediciler-codec.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./7-video-kaydediciler-codec.md) | English`

Content: codecs, FourCC, `cv2.VideoWriter`, recording video from camera.

Write to: `docs/7-video-recorder-codec.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/7-video-recorder-codec.en-US.md && head -3 docs/7-video-recorder-codec.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/7-video-recorder-codec.en-US.md
git commit -m "docs: ch7 translate to English - video codecs and recording"
```

---

## GRUP B — Core OpenCV (Tasks 8–15)

All 8 tasks are independent and can run in parallel.

---

### Task 8: Chapter 8 — Image Manipulation

**Files:**
- Read: `docs/8-goruntu-manipulasyonu.md` (297 lines)
- Write: `docs/8-pixel-manipulation.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/8-goruntu-manipulasyonu.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./8-goruntu-manipulasyonu.md) | English`

Content: why geometric transforms are needed (straightening scanned documents), resize with interpolation choices (`INTER_AREA` for shrink, `INTER_LINEAR` for enlarge), flip, rotate with `getRotationMatrix2D`, affine transform (3-point), perspective transform for document scanner scenario, drawing functions (`rectangle`, `circle`, `line`, `putText`), ROI cropping with NumPy slicing.

Write to: `docs/8-pixel-manipulation.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/8-pixel-manipulation.en-US.md && head -3 docs/8-pixel-manipulation.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/8-pixel-manipulation.en-US.md
git commit -m "docs: ch8 translate to English - image manipulation, perspective transform"
```

---

### Task 9: Chapter 9 — Color Spaces and Histogram

**Files:**
- Read: `docs/9-renk-uzaylari.md` (293 lines)
- Write: `docs/9-color-spaces.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/9-renk-uzaylari.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./9-renk-uzaylari.md) | English`

Content: why color spaces matter (detecting red objects in RGB vs HSV), BGR channel splitting, grayscale conversion, HSV (Hue 0-179°, Saturation, Value), `cv2.inRange` color mask for object detection, Lab color space for face detection, histogram with `cv2.calcHist`, histogram equalization with `cv2.equalizeHist` and CLAHE.

Write to: `docs/9-color-spaces.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/9-color-spaces.en-US.md && head -3 docs/9-color-spaces.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/9-color-spaces.en-US.md
git commit -m "docs: ch9 translate to English - color spaces, HSV mask, histogram"
```

---

### Task 10: Chapter 10 — Morphological Image Processing

**Files:**
- Read: `docs/10-morfolojik-goruntu-isleme.md` (297 lines)
- Write: `docs/10-morphological-operators.en-US.md` ← **new correct path**
- Delete: `docs/10-morphological-operators.en-US.en-US.md` ← **remove double-extension file**

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/10-morfolojik-goruntu-isleme.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./10-morfolojik-goruntu-isleme.md) | English`

Content: why morphological ops (noise removal after thresholding), structuring element (think of it as a brush), erosion (shrinks, removes noise specks), dilation (expands, fills holes), opening = erosion then dilation (removes small noise), closing = dilation then erosion (fills gaps), morphological gradient, thresholding (global `cv2.threshold`, `cv2.THRESH_OTSU`, `cv2.adaptiveThreshold`).

Write to: `docs/10-morphological-operators.en-US.md`

- [ ] **Step 3: Remove the double-extension file and verify**

```bash
git rm docs/10-morphological-operators.en-US.en-US.md
wc -l docs/10-morphological-operators.en-US.md && head -3 docs/10-morphological-operators.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/10-morphological-operators.en-US.md
git commit -m "docs: ch10 translate to English - morphology, erosion/dilation, thresholding; fix double extension"
```

---

### Task 11: Chapter 11 — Filters and Edge Detection

**Files:**
- Read: `docs/11-filtreler-ve-kenar-belirleme.md` (335 lines)
- Write: `docs/11-filtering-and-edge-detection.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/11-filtreler-ve-kenar-belirleme.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./11-filtreler-ve-kenar-belirleme.md) | English`

Content: why filtering (camera noise before edge detection), convolution intuition (sliding window, kernel × neighborhood = output), average/Gaussian/Median/Bilateral blur comparison table, edge detection intuition (edge = rapid intensity change), Sobel (horizontal and vertical gradients), Canny 4-stage pipeline (noise reduction → gradient → non-maximum suppression → double threshold), automatic threshold selection (median-based), Laplacian.

Write to: `docs/11-filtering-and-edge-detection.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/11-filtering-and-edge-detection.en-US.md && head -3 docs/11-filtering-and-edge-detection.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/11-filtering-and-edge-detection.en-US.md
git commit -m "docs: ch11 translate to English - filters, Canny edge detection"
```

---

### Task 12: Chapter 12 — Background Subtraction

**Files:**
- Read: `docs/12-arka-plan-cikarma.md` (215 lines)
- Write: `docs/12-background-subtraction.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/12-arka-plan-cikarma.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./12-arka-plan-cikarma.md) | English`

Content: parking lot security camera scenario, frame differencing with `cv2.absdiff`, MOG2 Gaussian mixture model (learns each pixel's "normal" value), `cv2.createBackgroundSubtractorMOG2` parameters, KNN subtractor, comparison table (absdiff vs MOG2 vs KNN).

Write to: `docs/12-background-subtraction.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/12-background-subtraction.en-US.md && head -3 docs/12-background-subtraction.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/12-background-subtraction.en-US.md
git commit -m "docs: ch12 translate to English - background subtraction, MOG2"
```

---

### Task 13: Chapter 13 — Video Analysis and Object Tracking

**Files:**
- Read: `docs/13-video-analiz.md` (247 lines)
- Write: `docs/13-object-tracking.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/13-video-analiz.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./13-video-analiz.md) | English`

Content: optical flow intuition (making wind visible — predicting where each pixel goes in the next frame), Lucas-Kanade sparse optical flow with `cv2.goodFeaturesToTrack` and `cv2.calcOpticalFlowPyrLK`, Farneback dense flow with HSV visualization, OpenCV trackers CSRT and KCF (CSRT accurate, KCF fast), ByteTrack/DeepSORT brief mention.

Write to: `docs/13-object-tracking.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/13-object-tracking.en-US.md && head -3 docs/13-object-tracking.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/13-object-tracking.en-US.md
git commit -m "docs: ch13 translate to English - optical flow, Lucas-Kanade, object tracking"
```

---

### Task 14: Chapter 14 — Object Detection and Recognition

**Files:**
- Read: `docs/14-nesne-tespiti.md` (197 lines)
- Write: `docs/14-object-detection.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/14-nesne-tespiti.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./14-nesne-tespiti.md) | English`

Content: factory defect detection scenario, classification vs detection difference, Haar Cascade with `cv2.CascadeClassifier`, Template Matching with `cv2.matchTemplate`, YOLOv8 single-shot intuition, Ultralytics API (`YOLO("yolov8n.pt").predict(img)`), evaluation metrics (IoU intuition: intersection/union, Precision/Recall, mAP).

Write to: `docs/14-object-detection.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/14-object-detection.en-US.md && head -3 docs/14-object-detection.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/14-object-detection.en-US.md
git commit -m "docs: ch14 translate to English - object detection, Haar, YOLOv8, mAP"
```

---

### Task 15: Chapter 15 — Camera Calibration and 3D Vision

**Files:**
- Read: `docs/15-kamera-kalibrasyonu-ve-3d-goru.md` (217 lines)
- Write: `docs/15-image-distortion-and-camera-calibration.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/15-kamera-kalibrasyonu-ve-3d-goru.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./15-kamera-kalibrasyonu-ve-3d-goru.md) | English`

Content: wide-angle lens distortion problem, pinhole camera model (dark room with a small hole — camera works the same way), focal length and principal point, lens distortion types (radial barrel/pincushion, tangential), chessboard calibration with `cv2.calibrateCamera`, `cv2.undistort`, stereo vision depth estimation (pencil-in-front-of-nose parallax analogy), `cv2.StereoSGBM_create`.

Write to: `docs/15-image-distortion-and-camera-calibration.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/15-image-distortion-and-camera-calibration.en-US.md && head -3 docs/15-image-distortion-and-camera-calibration.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/15-image-distortion-and-camera-calibration.en-US.md
git commit -m "docs: ch15 translate to English - camera calibration, pinhole model, stereo vision"
```

---

## GRUP C — Machine Learning & Detection (Tasks 16–21)

All 6 tasks are independent and can run in parallel.

---

### Task 16: Chapter 17 — Face Recognition

**Files:**
- Read: `docs/17-yuz-tanima.md` (279 lines)
- Write: `docs/17-face-recognition.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/17-yuz-tanima.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./17-yuz-tanima.md) | English`

Content: detection vs recognition difference, Haar Cascade face detection, DNN-based detection, Eigenfaces (PCA intuition), LBPH with `cv2.face.LBPHFaceRecognizer_create`, FaceNet embedding (same person = nearby points in 128-D space), ArcFace angular margin, DeepFace API (`DeepFace.verify`, `DeepFace.analyze`), comparison table.

Write to: `docs/17-face-recognition.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/17-face-recognition.en-US.md && head -3 docs/17-face-recognition.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/17-face-recognition.en-US.md
git commit -m "docs: ch17 translate to English - face recognition, LBPH, DeepFace, ArcFace"
```

---

### Task 17: Chapter 18 — Optical Character Recognition

**Files:**
- Read: `docs/18-optik-karakter-tanima.md` (251 lines)
- Write: `docs/18-optic-character-recognition.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/18-optik-karakter-tanima.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./18-optik-karakter-tanima.md) | English`

Content: license plate / invoice / book digitization scenarios, OCR pipeline (preprocessing → text detection → text recognition), preprocessing techniques (grayscale → threshold → deskew), Tesseract with `pytesseract`, PSM modes, Turkish language pack, EasyOCR with 80+ language support, EAST text detection with DNN, comparison table.

Write to: `docs/18-optic-character-recognition.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/18-optic-character-recognition.en-US.md && head -3 docs/18-optic-character-recognition.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/18-optic-character-recognition.en-US.md
git commit -m "docs: ch18 translate to English - OCR, Tesseract, EasyOCR, text detection"
```

---

### Task 18: Chapter 19 — Feature Extraction and Matching

**Files:**
- Read: `docs/19-oznitelik-cikarimi.md` (272 lines)
- Write: `docs/19-feature-extraction.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/19-oznitelik-cikarimi.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./19-oznitelik-cikarimi.md) | English`

Content: panorama stitching scenario (matching same building from two angles), what makes a good feature (scale/rotation/lighting invariant), SIFT DoG scale space (magnifying glass analogy), 128-D orientation histogram descriptor, ORB (100x faster than SIFT, patent-free), brute-force vs FLANN matching, Lowe ratio test (`m.distance < 0.7 * n.distance`), homography with RANSAC (`cv2.findHomography`).

Write to: `docs/19-feature-extraction.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/19-feature-extraction.en-US.md && head -3 docs/19-feature-extraction.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/19-feature-extraction.en-US.md
git commit -m "docs: ch19 translate to English - SIFT, ORB, feature matching, homography"
```

---

### Task 19: Chapter 20 — GPU and Parallel Computing

**Files:**
- Read: `docs/20-gpu-paralel-hesaplama.md` (177 lines)
- Create: `docs/20-gpu-parallel-computing.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/20-gpu-paralel-hesaplama.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./20-gpu-paralel-hesaplama.md) | English`

Content: CUDA module for GPU-accelerated OpenCV operations, OpenVINO for model acceleration on Intel hardware, Python threading for parallel image processing pipelines.

Write to: `docs/20-gpu-parallel-computing.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/20-gpu-parallel-computing.en-US.md && head -3 docs/20-gpu-parallel-computing.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/20-gpu-parallel-computing.en-US.md
git commit -m "docs: ch20 translate to English - GPU computing, CUDA, OpenVINO"
```

---

### Task 20: Chapter 21 — Pose Estimation

**Files:**
- Read: `docs/21-poz-tahmini.md` (342 lines)
- Create: `docs/21-pose-estimation.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/21-poz-tahmini.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./21-poz-tahmini.md) | English`

Content: fitness coach app scenario (measuring elbow angle during pull-ups), 17 COCO keypoints, MediaPipe Pose (`mp.solutions.pose`), landmark list and visibility score, `calculate_angle(a, b, c)` function (angle between vectors), real-time elbow angle display, squat rep counter (knee angle < 90°), YOLOv8-Pose for multi-person scenarios, comparison table.

Write to: `docs/21-pose-estimation.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/21-pose-estimation.en-US.md && head -3 docs/21-pose-estimation.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/21-pose-estimation.en-US.md
git commit -m "docs: ch21 translate to English - pose estimation, MediaPipe, angle calculation"
```

---

### Task 21: Chapter 22 — Segmentation

**Files:**
- Read: `docs/22-segmentasyon.md` (289 lines)
- Create: `docs/22-segmentation.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/22-segmentasyon.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./22-segmentasyon.md) | English`

Content: tumor pixel-labeling in medical imaging scenario, segmentation types (semantic / instance / panoptic), Watershed algorithm (watershed analogy — each object is a basin, boundaries are dividing lines), YOLOv8-seg with mask overlay, SAM (Segment Anything — select with point, box, or text), IoU and mIoU evaluation, comparison table.

Write to: `docs/22-segmentation.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/22-segmentation.en-US.md && head -3 docs/22-segmentation.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/22-segmentation.en-US.md
git commit -m "docs: ch22 translate to English - segmentation, YOLOv8-seg, SAM"
```

---

## GRUP D — Advanced Topics (Tasks 22–30)

All 9 tasks are independent and can run in parallel.

---

### Task 22: Chapter 23 — Edge Deployment

**Files:**
- Read: `docs/23-edge-deployment.md` (205 lines)
- Create: `docs/23-edge-deployment.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/23-edge-deployment.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./23-edge-deployment.md) | English`

Content: ONNX Runtime for cross-platform model serving, TFLite for mobile/embedded deployment, model quantization (INT8), Raspberry Pi deployment.

Write to: `docs/23-edge-deployment.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/23-edge-deployment.en-US.md && head -3 docs/23-edge-deployment.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/23-edge-deployment.en-US.md
git commit -m "docs: ch23 translate to English - edge deployment, ONNX, TFLite"
```

---

### Task 23: Chapter 24 — OpenCV Mobile

**Files:**
- Read: `docs/24-opencv-mobil.md` (204 lines)
- Create: `docs/24-opencv-mobile.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/24-opencv-mobil.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./24-opencv-mobil.md) | English`

Content: Android (Java/Kotlin) and iOS (Swift/Objective-C) OpenCV integration, camera stream processing, TFLite model integration on mobile.

Write to: `docs/24-opencv-mobile.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/24-opencv-mobile.en-US.md && head -3 docs/24-opencv-mobile.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/24-opencv-mobile.en-US.md
git commit -m "docs: ch24 translate to English - OpenCV mobile, Android, iOS"
```

---

### Task 24: Chapter 25 — Augmented Reality

**Files:**
- Read: `docs/25-artirilmis-gerceklik.md` (233 lines)
- Create: `docs/25-augmented-reality.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/25-artirilmis-gerceklik.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./25-artirilmis-gerceklik.md) | English`

Content: ArUco marker detection and pose estimation, 3D axis projection onto real world, image overlay (virtual object on physical surface), MediaPipe face filter (hat filter scenario).

Write to: `docs/25-augmented-reality.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/25-augmented-reality.en-US.md && head -3 docs/25-augmented-reality.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/25-augmented-reality.en-US.md
git commit -m "docs: ch25 translate to English - augmented reality, ArUco, face filter"
```

---

### Task 25: Chapter 26 — Vision Transformers

**Files:**
- Read: `docs/26-vision-transformers.md` (189 lines)
- Create: `docs/26-vision-transformers.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/26-vision-transformers.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./26-vision-transformers.md) | English`

Content: CNNs miss long-range pixel relationships problem, attention mechanism (eyes focus on important words while reading), self-attention (each element measures relationship to all others), ViT (split image into 16×16 patches → tokens → [CLS] token for classification), Swin Transformer (local window attention + shifted window), DETR (detection as sequence-to-sequence — no NMS, no anchors), CNN vs ViT comparison table.

Write to: `docs/26-vision-transformers.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/26-vision-transformers.en-US.md && head -3 docs/26-vision-transformers.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/26-vision-transformers.en-US.md
git commit -m "docs: ch26 translate to English - Vision Transformers, ViT, Swin, DETR"
```

---

### Task 26: Chapter 27 — Generative Models and Diffusion

**Files:**
- Read: `docs/27-generatif-modeller.md` (242 lines)
- Create: `docs/27-generative-models.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/27-generatif-modeller.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./27-generatif-modeller.md) | English`

Content: synthetic data generation scenario, GAN (counterfeiter vs police analogy — generator improves until fake money is perfect), VAE (compress to meaning space → sample new images from that space), DDPM (add noise step by step → reverse the process to generate from noise), Stable Diffusion with `diffusers` library, text-to-image / img2img / inpainting.

Write to: `docs/27-generative-models.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/27-generative-models.en-US.md && head -3 docs/27-generative-models.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/27-generative-models.en-US.md
git commit -m "docs: ch27 translate to English - GAN, VAE, Diffusion, Stable Diffusion"
```

---

### Task 27: Chapter 28 — 3D Vision

**Files:**
- Read: `docs/28-3d-vision.md` (308 lines)
- Create: `docs/28-3d-vision.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/28-3d-vision.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./28-3d-vision.md) | English`

Content: robotics/autonomous vehicles need 3D problem, stereo depth estimation, monocular depth with DPT (`Intel/dpt-large`), point cloud with Open3D, RGBD camera depth maps, PointNet (permutation invariance — no order in a point cloud, use symmetric max pooling), NeRF (learn 3D scene from photos taken at different angles, render from new viewpoints).

Write to: `docs/28-3d-vision.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/28-3d-vision.en-US.md && head -3 docs/28-3d-vision.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/28-3d-vision.en-US.md
git commit -m "docs: ch28 translate to English - 3D vision, depth estimation, PointNet, NeRF"
```

---

### Task 28: Chapter 29 — Video Understanding and Action Recognition

**Files:**
- Read: `docs/29-video-siniflandirma.md` (157 lines)
- Create: `docs/29-video-understanding.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/29-video-siniflandirma.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./29-video-siniflandirma.md) | English`

Content: security camera fight detection scenario, video = image sequence + time dimension (why per-frame CNN is insufficient), 3D convolution, Two-Stream networks (one for RGB frames, one for optical flow), SlowFast (slow pathway: high-res low-fps for appearance; fast pathway: low-res high-fps for motion), VideoMAE (mask 90% of tubes → reconstruct from 10%).

Write to: `docs/29-video-understanding.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/29-video-understanding.en-US.md && head -3 docs/29-video-understanding.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/29-video-understanding.en-US.md
git commit -m "docs: ch29 translate to English - video understanding, SlowFast, VideoMAE"
```

---

### Task 29: Chapter 30 — Model Training and Evaluation

**Files:**
- Read: `docs/30-model-egitimi-ve-degerlendirme.md` (324 lines)
- Create: `docs/30-model-training.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/30-model-egitimi-ve-degerlendirme.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./30-model-egitimi-ve-degerlendirme.md) | English`

Content: train custom object detector with your own photos scenario, dataset folder structure (`train/`, `val/`, `test/`), `ImageFolder` with PyTorch DataLoader, labeling tools (LabelImg, Roboflow), data augmentation (why: multiply small dataset + generalize), `torchvision.transforms` pipeline, Mixup, transfer learning (take ImageNet-trained feature extractor → replace final layer), ResNet50 fine-tuning (full train loop + eval loop), Cosine Annealing LR, early stopping, confusion matrix, `classification_report`.

Write to: `docs/30-model-training.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/30-model-training.en-US.md && head -3 docs/30-model-training.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/30-model-training.en-US.md
git commit -m "docs: ch30 translate to English - model training, transfer learning, evaluation"
```

---

### Task 30: Chapter 31 — Vision-Language Models

**Files:**
- Read: `docs/31-vision-language-modeller.md` (268 lines)
- Create: `docs/31-vision-language-models.en-US.md`

- [ ] **Step 1: Read the Turkish source**

```bash
cat docs/31-vision-language-modeller.md
```

- [ ] **Step 2: Write the English translation**

Language switcher: `[Türkçe](./31-vision-language-modeller.md) | English`

Content: "find the red car in the photo" text-image search scenario, multimodal learning (image + text together), CLIP (trained on 400M image-text pairs — "cat photo" text and cat photo are nearby points, zero-shot classification with label list), `openai/clip-vit-base-patch32` via HuggingFace, LLaVA (connect CLIP visual features to a large language model — describe image, answer questions, do OCR), BLIP-2 Q-Former (query-based feature extraction → text generation), use cases (e-commerce image search, medical image-to-text, accessibility).

Write to: `docs/31-vision-language-models.en-US.md`

- [ ] **Step 3: Verify**

```bash
wc -l docs/31-vision-language-models.en-US.md && head -3 docs/31-vision-language-models.en-US.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/31-vision-language-models.en-US.md
git commit -m "docs: ch31 translate to English - CLIP, LLaVA, BLIP-2, zero-shot classification"
```

---

## Execution Order

All 4 groups are fully independent and can run in parallel:

```
GRUP A (Tasks 1–7)   ─┐
GRUP B (Tasks 8–15)  ─┤── All parallel
GRUP C (Tasks 16–21) ─┤
GRUP D (Tasks 22–30) ─┘
```

---

## Self-Review Notes

- **Spec coverage:** All 30 chapters covered (chapters 1–15, 17–31; chapter 16 does not exist in this repository).
- **No placeholders:** Every task specifies exact source path, target path, content summary, verification command, and commit message.
- **Double extension fix:** Task 10 explicitly removes `docs/10-morphological-operators.en-US.en-US.md` and creates the correctly named `docs/10-morphological-operators.en-US.md`.
- **README.en-US.md:** The link for chapter 10 in `README.en-US.md` already points to the wrong double-extension path — this should be fixed as part of Task 10:
  ```bash
  # In Task 10, also run:
  sed -i '' 's|10-morphological-operators.en-US.en-US.md|10-morphological-operators.en-US.md|g' README.en-US.md
  git add README.en-US.md
  ```
