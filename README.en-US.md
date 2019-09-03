English | [Türkçe](./README.md)


[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/opencv-turkish-tutorial) [![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](#)
[![Video](https://img.shields.io/badge/Video-@mesutpiskin-red.svg?logo=youtube&longCache=true&style=flat)](https://www.youtube.com/channel/UC_ko-bnDYXCVL1XJG0doRDg)
[![Patreon](https://img.shields.io/badge/Patreon-donate_with_patreon-green.svg?logo=patreon&longCache=true&style=flat)](https://www.patreon.com/mesutpiskin)

- [Documentation](#documentation)
- [Example Projects](#example-projects)
- [Contribute](#contribute)
- [Question & Answer](#-question--answer)
- [License](#-license)

This guide to help you understand the basics of computerized view and to develop computer vision vision with OpenCV. Python, Java, JavaScript, C # and C ++ are supported with examples.

# Image Processing and Computer Vision Guide

 You will learn the image processing and machine learning algorithms.  We will develop example applications using **Python** , **C++**,  **JavaScript (OpenCV.JS)**, **MATLAB** and **C# (EmguCV)**  programming languages. This guide is intended to help you understand the basics of computerized view and develop OpenCV and computer vision applications. This document has been prepared to address those who have not previously been engaged in image processing, who are not familiar with the subject matter, and who, on the contrary, are knowledgeable about this subject and who want to develop themselves on different topics. Sample projects can be found in  <a href="/code/">code</a> and documents in <a href="/docs/">docs</a> directory.

<p align="center">

<img src="/other/banner-en.png"/>
</p>

---


<center>

 ★★ If you want to donate to projects, you can do this through <a href="https://www.patreon.com/mesutpiskin">Patreon</a> ★★

</center>

<center>


 ★★★ If you want to contribute the project; You can look at the contribute section.Feel free to contact us if you have a request or suggestion. To contact <a href="https://gitter.im/opencv-turkish-tutorial">Gitter</a> or <a href="mailto:mesutpiskin@outlook.com">email</a>. Much obliged! ★★★
 
</center>

---


## Documentation

| Lecture |Abstract|
|----------|--------|
| [What is OpenCV?](/docs/1-introduction.en-US.md)|OpenCV history and components, alternative image processing libraries,  OpenCV 2 vs OpenCV 3 vs OpenCV 4 and OpenCV 4 future.|
| [Development Environment and Platforms](/docs/2-development-environments.en-US.md) |Which platform and development environment should be selected, why Java, C ++ and Python are used for image processing.|
| [OpenCV Wrappers](/docs/3-opencv-wrappers.en-US.md) |What is Wrapper? What is EmguCV, JavaCV, LiveCV, Ruby CV, and what are the differences between wrappers?|
| [Installation and Compilation](/docs/4-opencv-installation.en-US.md) |OpenCV installation for Windows, Linux, macOS and Raspberry Pi.|
| [IDE Configuration](/docs/5-ide-Configuration.en-US.md) |Configuration settings for Eclipse, Netbeans, Android Studio and Intellij IDEA.|
| [Introduction and Basic Concepts](/docs/6-image-processing-concepts.en-US.md) |Image processing concepts. From the file, from the camera, reading the image from the IP camera. Changing camera parameters.|
| [Video Recorders and Decoders](/docs/7-video-recorder-codec.en-US.md) |Codec, FourCC and video recorder.|
| [Image Manipulation](/docs/8-pixel-manipulation.en-US.md) |Pixel manipulation, geometric objects and geometric transformations.|
| [Color Spaces and Histogram](/docs/9-color-spaces.en-US.md) |Color spaces, color spaces conversion. Histogram concept and histogram matching.|
| [Morphological Image Processing](/docs/10-morphological-operators.en-US.en-US.md) |Morphological operators and thresholding: Erosion, dilation, closing, gradyan, thresholding etc.
| [Filters and Edge Detection](/docs/11-filtering-and-edge-detection.en-US.md) |Filtering and edge detection algorithms: Blur, Sobel, Laplace, Canny etc.|
| [Background Subtraction](/docs/12-background-subtraction.en-US.md) | OpenCV background subtractor: Absdiff, MOG, MOG2 and GMG.|
| [Object Detection and Object Recognition](/docs/14-object-detection.en-US.md) |Object detection processes and algorithms. HaarCascade, TemplateMatching, DNN, CNN, SVM Machine Learning and Deep Learning Algorithms etc.
 [Feature and Feature Extraction](/docs/19-feature-extraction.en-US.md) |Feature , feature extraction for object detection, and feature matching. Brute-Force, FLANN, SURF, SIFT, BRIEF, ORB, FAST algorithms etc. 
| [Video Analysis and Object Tracking](/docs/13-object-tracking.en-US.md) |Mean Shift, Camshift, Optical flow, GOTURN, BOOSTING, MIL, CNN etc. Object or area tracking on video. |
| [Image Distortion and Stereo Vision](/docs/15-image-distortion-and-camera-calibration.en-US.md) | Image distortion and camera calibration, 3D images, depth estimation, stereoscopic vision and stereo image processing.|
| [Face Recognition](/docs/17-face-recognition.en-US.md) | What is face recognition? Face recognition with Eigenfaces, Fisherfaces, LBPH and machine learning algorithms. Different library integrations (dlib, tensorflow and face_recognition). |
| [Optical Character Recognition OCR ](/docs/18-optic-character-recognition.en-US.md)| Detecting text on the image. OCR processes, algorithms and libraries. Tesseract, textocr etc.
| GPU and Parallel Computing | Development of parallelized computerized vision applications on Nvidia GPU with Cuda module.|
| OpenCV Mobile  |Computerized view and image processing on mobile devices with Android and iOS operating system.|
| Augmented Reality | 3D models have been acquired through the camera, dressed on real-world image. OpenCV and OpenGL integration. Interactive computer vision application development.|





## Example Projects

<table style="width: 100%;">
<tbody>
<tr>
<td><strong>&nbsp;Topic</strong></td>
<td><strong>&nbsp;Python</strong></td>
<td><strong>&nbsp;Java</strong></td>
<td><strong>&nbsp;C++</strong></td>
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
<td>&nbsp;Filters</td>
<td>
<ul>
<li><a href="/code/filtreleme/python/guasian.py">Guassian</a></li>
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
<td>&nbsp;Edge Detection</td>
<td>
<ul>
<li><a href="/code/kenar-belirleme/python/canny.py">Canny</a></li>
<li><a href="code/kenar-belirleme/python/kenar-belirleme-toplu.py">GaussianBlur &amp; Canny &amp; Sobel &amp;&nbsp;Prewitt</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
  <td><ul>
<li><a href="/code/kenar-belirleme/javascript/edge_detector.html">Canny</a></li>
</ul></td>
</tr>
<tr>
<td>Background Subtraction</td>
<td>
<ul>
<li><a href="/code/arkaplan-cikarma/python/absdif.py">Absdiff</a></li>
<li><a href="/code/arkaplan-cikarma/python/background-subtractor-gmg.py">BackgroundSubtractorMOG - MOG2 - GMG</a></li>
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
<td>Object Detection and Object Recognition</td>
<td>
<ul>
<li><a href="/code/nesne-tespit-ve-tanima/python/template-matching.py">Template Matching</a></li>
<li><a href="/code/nesne-tespit-ve-tanima/python/derin_sinir_agi.py">Object Recognition with Deep Neural Network DNN</a></li>
<li><a href="/code/nesne-tespit-ve-tanima/python/haar-cascade.py">Face Detection with Haar Cascade Classifier</a></li>
</ul>
</td>
<td>

<ul>
<li><a href="/code/nesne-tespit-ve-tanima/java/TemplateMatching.java">Object Recognition with Template Matching</a></li>
<li><a href="https://github.com/mesutpiskin/opencv-object-detection/tree/master/src/DeepNeuralNetwork">Object Recognition with Deep Neural Network DNN</a></li>
<li><a href="/code/nesne-tespit-ve-tanima/java/DetectFace.java">Face Detection with Haar Cascade Classifier</a></li>

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
<li><a href="/code/kamera-kalibrasyon-3d-goru/python/fisheye-lens-duzeltme.py">Fisheye Image Correction</a></li>
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
<li><a href="/code/yuz-tanima/python/dnn_yuz_tespiti/">Face Detection with Deep Neural Network (DNN)</a></li>
</ul>


</td>
<td>
<ul>
<li><a href="https://github.com/mesutpiskin/GenderClassification">Gender Detection with Deep Neural Network (DNN)</a></li>
</ul>

</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Face recognition</td>
<td>
<ul>
<li><a href="/code/yuz-tanima/python/facerecognition_kutuphanesi/">Face Recognition with "FaceRecognition Lib"</a></li>
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
<td>Optical Character Recognition OCR</td>
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
<td>GPU and Parallel Computing</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>OpenCV MobilE</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
 <td>&nbsp;</td>
</tr>
<tr>
<td>Augmented Reality and Image Blending</td>
<td>
<ul>
<li><a href="/code/arttirilmis-gerceklik/python/sapka-filtresi/">Hat Filter - Face Detection and Hat Adding</a></li>
</ul>


</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
</tbody>
</table>


## Contribute

It's really nice to think about contributing, so you can look at the [Contribute](/CONTRIBUTING.en-US.md) link.


## 💬 Question & Answer
You can ask questions, source codes or any other questions by using the **issues** section (new issues). You can also use this section if you want to answer a question or check out the previous ones.

## 📄 License
Documents and source codes contained in this project are licensed  [MIT License](/LICENSE.en-US.md).
