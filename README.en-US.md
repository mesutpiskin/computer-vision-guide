English | [Türkçe](./README.md)

[![Chapters](https://img.shields.io/badge/chapters-31-brightgreen.svg)](#documentation)
[![Sponsor](https://img.shields.io/badge/sponsor-%E2%9D%A4-ff69b4.svg?logo=github)](https://github.com/sponsors/mesutpiskin)
[![Video](https://img.shields.io/badge/Video-@mesutpiskin-red.svg?logo=youtube&longCache=true&style=flat)](https://www.youtube.com/channel/UC_ko-bnDYXCVL1XJG0doRDg)

# Image Processing and Computer Vision Guide

A comprehensive, practical guide to building computer vision applications with OpenCV and modern deep learning frameworks.

<p align="center">
<img src="/other/banner-en.png"/>
</p>

This guide bridges theory and practice for both students and working developers. Each chapter opens with a real-world problem, builds intuition before introducing formulas, and delivers complete, copy-paste-ready Python examples. Students learn the concepts; developers ship the code.

**31 chapters** · Python 3.10+ · OpenCV 4.9+ · PyTorch · Ultralytics YOLOv8

---

## Table of Contents

- [Documentation](#documentation)
- [Getting Started](#getting-started)
- [Example Projects](#example-projects)
- [Contributing](#contributing)
- [Support the Project](#support-the-project)
- [Release History](#release-history)

---

## Documentation

Every chapter follows the same structure: **real-world problem** → intuitive explanation → formula (where needed) → complete working Python code → comparison table → summary and references.

| Chapter | Summary |
| ------- | ------- |
| [What is OpenCV?](/docs/1-introduction.en-US.md) | OpenCV history and architecture, module overview, comparison with alternative libraries, OpenCV 4.x/5.0 highlights. |
| [Development Environment](/docs/2-development-environments.en-US.md) | Setting up Python, VS Code, Jupyter Notebook, Google Colab, and Conda for computer vision development. |
| [OpenCV Wrappers](/docs/3-opencv-wrappers.en-US.md) | EmguCV, JavaCV, LiveCV, RubyCV — what they are and when to use them. |
| [Installation and Compilation](/docs/4-opencv-installation.en-US.md) | OpenCV installation for Windows, Linux, macOS, and Raspberry Pi. |
| [IDE Configuration](/docs/5-ide-Configuration.en-US.md) | Configuration for VS Code, PyCharm, Conda, Google Colab, and Android Studio. |
| [Introduction and Basic Concepts](/docs/6-image-processing-concepts.en-US.md) | Digital image as a matrix, BGR/RGB difference, reading from file and camera, pixel manipulation. |
| [Video Recorders and Codecs](/docs/7-video-recorder-codec.en-US.md) | Codec, FourCC, and video recording with `cv2.VideoWriter`. |
| [Image Manipulation](/docs/8-pixel-manipulation.en-US.md) | Resize, rotate, affine and perspective transforms; document scanner scenario. |
| [Color Spaces and Histogram](/docs/9-color-spaces.en-US.md) | BGR, HSV, Lab color spaces; color-mask object detection; histogram equalization and CLAHE. |
| [Morphological Image Processing](/docs/10-morphological-operators.en-US.en-US.md) | Erosion, dilation, opening, closing, morphological gradient; Otsu and adaptive thresholding. |
| [Filters and Edge Detection](/docs/11-filtering-and-edge-detection.en-US.md) | Convolution intuition, Gaussian/Median/Bilateral blur, Sobel, four-stage Canny pipeline. |
| [Background Subtraction](/docs/12-background-subtraction.en-US.md) | Frame differencing, MOG2 Gaussian mixture model, KNN subtractor; security camera scenario. |
| [Video Analysis and Object Tracking](/docs/13-object-tracking.en-US.md) | Optical flow constraint, Lucas-Kanade pyramidal LK, Farneback dense flow, CSRT and KCF trackers. |
| [Object Detection and Recognition](/docs/14-object-detection.en-US.md) | Haar Cascade, Template Matching, real-time YOLOv8 detection; IoU, Precision/Recall, mAP metrics. |
| [Camera Calibration and 3D Vision](/docs/15-image-distortion-and-camera-calibration.en-US.md) | Pinhole camera model, radial distortion correction, chessboard calibration, stereo depth map. |
| [Face Recognition](/docs/17-face-recognition.en-US.md) | Eigenfaces/LBPH, FaceNet embedding intuition, ArcFace angular margin, DeepFace integration. |
| [Optical Character Recognition (OCR)](/docs/18-optic-character-recognition.en-US.md) | OCR pipeline, image preprocessing, Tesseract PSM modes, EasyOCR, EAST text detection. |
| [Feature Extraction and Matching](/docs/19-feature-extraction.en-US.md) | SIFT DoG scale space, ORB, FLANN matching, Lowe ratio test, RANSAC homography; image stitching. |
| [GPU and Parallel Computing](/docs/20-gpu-paralel-hesaplama.md) | CUDA module, OpenVINO model acceleration, threading for parallel image processing. |
| [Pose Estimation](/docs/21-poz-tahmini.md) | 17 COCO keypoints, MediaPipe Pose skeleton detection, angle calculation, rep counter, YOLOv8-Pose. |
| [Segmentation](/docs/22-segmentasyon.md) | Semantic/instance/panoptic differences, Watershed, YOLOv8-seg, SAM (Segment Anything), IoU and mIoU. |
| [Edge Deployment](/docs/23-edge-deployment.md) | Model optimization with ONNX Runtime and TFLite, Raspberry Pi and mobile deployment. |
| [OpenCV Mobile](/docs/24-opencv-mobil.md) | OpenCV on Android and iOS, camera stream processing, TFLite integration. |
| [Augmented Reality](/docs/25-artirilmis-gerceklik.md) | ArUco marker detection, 3D axis projection, image overlay, MediaPipe face filter. |
| [Vision Transformers](/docs/26-vision-transformers.md) | Attention mechanism intuition, ViT patch embedding and CLS token, Swin shifted window, DETR, CNN vs ViT. |
| [Generative Models and Diffusion](/docs/27-generatif-modeller.md) | GAN minimax game intuition, VAE latent space, DDPM noise process, Stable Diffusion, ControlNet. |
| [3D Vision](/docs/28-3d-vision.md) | Stereo and monocular depth estimation, Open3D point cloud, PointNet permutation invariance, NeRF. |
| [Video Understanding and Action Recognition](/docs/29-video-siniflandirma.md) | Two-Stream, SlowFast dual-pathway architecture, VideoMAE tube masking, HuggingFace action classification. |
| [Model Training and Evaluation](/docs/30-model-egitimi-ve-degerlendirme.md) | Data preparation, augmentation, Mixup, ResNet50 fine-tuning, Cosine Annealing, confusion matrix. |
| [Vision-Language Models](/docs/31-vision-language-modeller.md) | CLIP contrastive loss, zero-shot classification, LLaVA, BLIP-2 Q-Former; visual question answering. |

---

## Getting Started

Install the core dependencies:

```bash
pip install opencv-python numpy matplotlib
```

For deep learning and modern chapters:

```bash
pip install torch torchvision ultralytics mediapipe easyocr deepface transformers diffusers open3d
```

All code examples require Python 3.10+ and OpenCV 4.9+. Sample source code is available in the [`/code`](/code/) directory.

---

## Example Projects

<table style="width: 100%;">
<tbody>
<tr>
<td><strong>Topic</strong></td>
<td><strong>Python</strong></td>
<td><strong>Java</strong></td>
<td><strong>C++</strong></td>
<td><strong>C#</strong></td>
<td><strong>JavaScript</strong></td>
</tr>
<tr>
<td>Video I/O</td>
<td>
<ul>
<li><a href="/code/kamera-io/python/video_io.py">Video and Camera I/O</a></li>
<li><a href="/code/kamera-io/python/video-kaydet.py">Video Recorder</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Image Manipulation</td>
<td>
<ul>
<li><a href="/code/goruntu-manipulasyonu/python/geometrik-sekiller.py">Geometric Shape Drawing</a></li>
<li><a href="/code/goruntu-manipulasyonu/python/goruntu-kirpma.py">Image Crop</a></li>
<li><a href="/code/goruntu-manipulasyonu/python/piksel-manupulasyonu.py">Pixel Manipulation</a></li>
<li><a href="/code/goruntu-manipulasyonu/python/yeniden-boyutlandirma.py">Image Resize</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Color Spaces</td>
<td>
<ul>
<li><a href="/code/renk-uzaylari/python/renk-uzayi-donusumu.py">Color Space Conversion</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Morphological Image Processing</td>
<td>
<ul>
<li><a href="/code/morfolojik-goruntu-isleme/python/acinim-opening.py">Opening</a></li>
<li><a href="/code/morfolojik-goruntu-isleme/python/kapanim-closing.py">Closing</a></li>
<li><a href="/code/morfolojik-goruntu-isleme/python/genisletme-dilation.py">Dilation</a></li>
<li><a href="/code/morfolojik-goruntu-isleme/python/gradient.py">Gradient</a></li>
<li><a href="/code/morfolojik-goruntu-isleme/python/asindirme-erozyon.py">Erosion</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Filters</td>
<td>
<ul>
<li><a href="/code/filtreleme/python/guasian.py">Gaussian</a></li>
<li><a href="/code/filtreleme/python/sobel.py">Sobel</a></li>
<li><a href="/code/filtreleme/python/laplacian-sobel.py">Laplacian &amp; Sobel</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Edge Detection</td>
<td>
<ul>
<li><a href="/code/kenar-belirleme/python/canny.py">Canny</a></li>
<li><a href="code/kenar-belirleme/python/kenar-belirleme-toplu.py">GaussianBlur &amp; Canny &amp; Sobel &amp; Prewitt</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>
<ul>
<li><a href="/code/kenar-belirleme/javascript/edge_detector.html">Canny</a></li>
</ul>
</td>
</tr>
<tr>
<td>Background Subtraction</td>
<td>
<ul>
<li><a href="/code/arkaplan-cikarma/python/absdif.py">Absdiff</a></li>
<li><a href="/code/arkaplan-cikarma/python/background-subtractor-gmg.py">MOG / MOG2 / GMG</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Video Analysis and Object Tracking</td>
<td>
<ul>
<li><a href="/code/video-analiz/python/meanshift.py">MeanShift</a></li>
<li><a href="/code/video-analiz/python/camshift.py">CamShift</a></li>
</ul>
</td>
<td>
<ul>
<li><a href="https://github.com/mesutpiskin/opencv-object-detection/tree/master/src/ColorBasedObjectTracker">Color-Based Object Tracking</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Object Detection and Recognition</td>
<td>
<ul>
<li><a href="/code/nesne-tespit-ve-tanima/python/template-matching.py">Template Matching</a></li>
<li><a href="/code/nesne-tespit-ve-tanima/python/derin_sinir_agi.py">Object Recognition with DNN</a></li>
<li><a href="/code/nesne-tespit-ve-tanima/python/haar-cascade.py">Face Detection with Haar Cascade</a></li>
</ul>
</td>
<td>
<ul>
<li><a href="/code/nesne-tespit-ve-tanima/java/TemplateMatching.java">Template Matching</a></li>
<li><a href="https://github.com/mesutpiskin/opencv-object-detection/tree/master/src/DeepNeuralNetwork">Object Recognition with DNN</a></li>
<li><a href="/code/nesne-tespit-ve-tanima/java/DetectFace.java">Face Detection with Haar Cascade</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Feature Extraction</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Camera Calibration and 3D Vision</td>
<td>
<ul>
<li><a href="/code/kamera-kalibrasyon-3d-goru/python/fisheye-lens-duzeltme.py">Fisheye Lens Correction</a></li>
<li><a href="/code/kamera-kalibrasyon-3d-goru/python/kamera-kalibrasyonu.py">Camera Calibration</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Machine Learning and Deep Learning</td>
<td>
<ul>
<li><a href="/code/yuz-tanima/python/dnn_yuz_tespiti/">Face Detection with DNN</a></li>
</ul>
</td>
<td>
<ul>
<li><a href="https://github.com/mesutpiskin/GenderClassification">Gender Classification with DNN</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Face Recognition</td>
<td>
<ul>
<li><a href="/code/yuz-tanima/python/facerecognition_kutuphanesi/">Face Recognition with face_recognition</a></li>
<li><a href="/code/yuz-tanima/python/facenet/">Face Recognition with FaceNet</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>
<ul>
<li><a href="https://github.com/mesutpiskin/face-detection-and-recognition">Face Recognition with Eigenfaces and Fisherfaces</a></li>
</ul>
</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Optical Character Recognition (OCR)</td>
<td>
<ul>
<li><a href="/code/optik-karakter-tanima-ocr/python/tesseract-python/">OCR with Tesseract</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Augmented Reality</td>
<td>
<ul>
<li><a href="/code/arttirilmis-gerceklik/python/sapka-filtresi/">Hat Filter — Face Detection and Hat Overlay</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
</tbody>
</table>

---

## Contributing

Contributions are welcome — bug reports, new chapter proposals, code corrections, or translations. See [CONTRIBUTING.en-US.md](/CONTRIBUTING.en-US.md) for guidelines.

Questions and discussions go in [Issues](https://github.com/mesutpiskin/computer-vision-guide/issues). For direct contact, reach out via <a href="http://mesutpiskin.com">the website</a> or <a href="mailto:mesutpiskin@outlook.com">email</a>.

---

## Support the Project

This guide is a free, open-source educational resource maintained entirely on a volunteer basis. If it has been useful to you and you'd like to support new chapters, updated examples, and the continued growth of the community, consider sponsoring via GitHub Sponsors.

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-%23ff69b4?logo=github-sponsors&logoColor=white)](https://github.com/sponsors/mesutpiskin)

Your support directly funds new content, code maintenance, and the broader Turkish computer vision community.

---

## Release History

### v3.0 — May 2026

The most comprehensive update since the repository's launch in 2018. Migration to a Python-first stack, eleven new chapters, and a ground-up rewrite of all existing chapters happened simultaneously. An O'Reilly-style pedagogical structure was adopted throughout: each topic opens with a real-world problem, intuition precedes formulas, and every code example is complete and runnable.

**Rewritten chapters (15):** 1, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 21, 22

**New chapters (11):**
- **Chapter 20:** [GPU and Parallel Computing](/docs/20-gpu-paralel-hesaplama.md) — CUDA, OpenVINO, Threading
- **Chapter 21:** [Pose Estimation](/docs/21-poz-tahmini.md) — MediaPipe Pose, YOLOv8-Pose, angle calculation
- **Chapter 22:** [Segmentation](/docs/22-segmentasyon.md) — YOLOv8-seg, SAM, DeepLab
- **Chapter 23:** [Edge Deployment](/docs/23-edge-deployment.md) — ONNX Runtime, TFLite, quantization
- **Chapter 24:** [OpenCV Mobile](/docs/24-opencv-mobil.md) — Android, iOS
- **Chapter 25:** [Augmented Reality](/docs/25-artirilmis-gerceklik.md) — ArUco, 3D Overlay, Face Filter
- **Chapter 26:** [Vision Transformers](/docs/26-vision-transformers.md) — ViT, Swin Transformer, DETR
- **Chapter 27:** [Generative Models and Diffusion](/docs/27-generatif-modeller.md) — GAN, VAE, DDPM, Stable Diffusion
- **Chapter 28:** [3D Vision](/docs/28-3d-vision.md) — PointNet, NeRF, Depth Estimation
- **Chapter 29:** [Video Understanding and Action Recognition](/docs/29-video-siniflandirma.md) — SlowFast, VideoMAE
- **Chapter 30:** [Model Training and Evaluation](/docs/30-model-egitimi-ve-degerlendirme.md) — Transfer Learning, Augmentation
- **Chapter 31:** [Vision-Language Models](/docs/31-vision-language-modeller.md) — CLIP, LLaVA, BLIP-2

---

### v1.0 — 2018–2020 · [`v1` tag](https://github.com/mesutpiskin/computer-vision-guide/tree/v1)

Initial release. Java, Python, and C++ examples with OpenCV 3.x/4.x. Fundamental image processing topics.
