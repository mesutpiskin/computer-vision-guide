English | [Türkçe](./README.md)


[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/opencv-turkish-tutorial) [![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](#) ![%20](http://progressed.io/bar/20?title=Completed "General Completion 20%")
[![Video](https://img.shields.io/badge/Video-@mesutpiskin-red.svg?logo=youtube&longCache=true&style=flat)](https://www.youtube.com/channel/UC_ko-bnDYXCVL1XJG0doRDg)
[![Patreon](https://img.shields.io/badge/Patreon-donate_with_patreon-green.svg?logo=patreon&longCache=true&style=flat)](https://www.patreon.com/mesutpiskin)

- [Documentation](#dokümantasyon)
- [Example Projects](#örnek-projeler)
- [Contribute](#destek)
- [Question & Answer](#-soru--cevap)
- [License](#-lisans)

This guide to help you understand the basics of computerized view and to develop computer vision vision with OpenCV. Python, Java, JavaScript, C # and C ++ are supported with examples.

# Image Processing and Computer Vision Guide

OpenCV ile bilgisayarlı görü ve görüntü işleme eğitim dokümanı ile birlikte, görüntü işleme algoritmalarını öğrenecek, yeri geldiğinde ise **Java**, **Python** , **C++**,  **JavaScript (OpenCV.JS)**, **MATLAB** ve **C# (EmguCV)** programlama dilleri kullanarak örnek uygulamalar geliştireceğiz. Bu eğitim, bilgisayarlı görünün temellerini anlayabilmenizi ve OpenCV ile bilgisayarlı görü uygulamaları geliştirebilmenizi amaçlamaktadır. Python, Java ve C++ örnekleri ile desteklenmektedir. Bu doküman, daha önce görüntü işleme ile uğraşmamış, bu konuda bilgisi olmayanlara ve tam aksine bu konuda bilgili, kendinisini farklı konularda geliştirmek  isteyen herkese hitap edecek şekilde hazırlanmıştır. Temel tanımlardan başlanarak birçok kavram ve algoritma ele alınmıştır. Örnek projelere  <a href="/code/">code</a> dizininden, eğitim konularına ise <a href="/docs/">docs</a> dizini altından ulaşabilirsiniz.

<p align="center">

<img src="/banner/banner-en.png"/>
</p>

---


<p align="center">
 ★★ Projelere finansal destek olmak isterseniz <a href="https://www.patreon.com/mesutpiskin">Patreon</a> üzerinden bunu yapabilirsiniz. Destek olmayı düşünmüyorsanız bile göz atamınızdan memnun olurum. ★★
</p>

<p align="center">


 ★★★ Projeye destek olmak isterseniz; patreon destek kısmına göz atabilirsiniz. Talep veya öneriniz varsa iletişime geçmekten çekinmeyin. İletişime geçmek için <a href="https://gitter.im/opencv-turkish-tutorial">Gitter</a> veya <a href="https://github.com/mesutpiskin">buradaki</a> e-posta adresini kullanabilirsiniz. Teşekkürler! ★★★
</p>

---


## Documentation

| Lecture |Abstract|
|----------|--------|
| [What is OpenCV?](/docs/1-opencv-nedir.md)|OpenCV'nin tarihi ve bileşenleri, alternatif görüntü işleme kütüphaneleri, neden OpenCV, OpenCV 2 vs OpenCV 3 ve OpenCV 4 ile gelecek yenilikler.|
| [Development Environment and Platforms](/docs/2-gelistirme-ortamlari.md) |Hangi platform ve geliştirme ortamı seçilmeli, görüntü işleme için neden Java, C++ ve Python kullanılıyor.|
| [OpenCV Wrappers](/docs/3-opencv-wrappers.md) |Wrapper nedir? EmguCV, JavaCV, LiveCV, RubyCV nedir ve wrapperlar arası farklar nelerdir.|
| [Installation and Compilation](/docs/4-opencv-kurulumlar.md) |Windows, Linux, macOS ve Raspberry Pi için OpenCV kurulumu.|
| [IDE Configuration](/docs/5-ide-yapilandirmasi.md) |Eclipse, Netbeans, Android Studio ve Intelij IDEA için yapılandırma ayarları.|
| [Introduction and Basic Concepts](/docs/6-giris-temel-kavramlar.md) |Görüntü işleme kavramları. Dosyadan, kameradan, IP kameradan görüntü okuma. Kamera parametrelerini değiştirme.|
| [Video Recorders and Decoders](/docs/7-video-kaydediciler-codec.md) |Codec, FourCC ve video kaydetme.|
| [Image Manipulation](/docs/8-goruntu-manipulasyonu.md) |Piksel manüpülasyonu, geometrik çizimler ve geometrik dönüşümler.|
| [Color Spaces and Histogram](/docs/9-renk-uzaylari.md) |Temel renk uzayları, renk uzayları arası dönüşüm. Histogram kavramı ve histogram eşitleme.|
| [Morphological Image Processing](/docs/10-morfolojik-goruntu-isleme.md) |Morfolojik operatörler ve eşikleme: Erosion, dilation, closing, gradyan, thresholding ...|
| [Filters and Edge Detection](/docs/11-filtreler-ve-kenar-belirleme.md) |Filtreleme ve kenar belirleme algoritmaları: Blur, Sobel, Laplace, Canny ...|
| [Background Subtraction](/docs/12-arka-plan-cikarma.md) | Absdiff, MOG, MOG2 ve GMG algoritmaları kullanarak, 2D görüntü arkaplan çıkarımı.|
| [Object Detection and Object Recognition](/docs/14-nesne-tespiti.md) |Nesne tespit süreçleri ve algoritmaları. HaarCascade, TemplateMatching, DNN, CNN, SVM Makine Öğrenmesi ve Derin Öğrenme algoritmaları ...|
 [Feature and Feature Extraction](/docs/19-oznitelik-cikarimi.md) |Öznitelik tanımı, nesne tespiti için öznitelik çıkarmı ve öznitelik eşleştirme. Brute-Force, FLANN, SURF, SIFT, BRIEF, ORB, FAST algoritmaları ...|
| [Video Analysis and Object Tracking](/docs/13-video-analiz.md) |Mean Shift, Cam Shift, Optik akış, GOTURN, BOOSTING, MIL, CNN vb. algoritmalar ile video üzerinde nesne veya alan takibi. |
| [Image Distortion and Stereo Vision](/docs/15-kamera-kalibrasyonu-ve-3d-goru.md) | Görüntü bozulmaları ve kamera kalibrasyonu, 3D görüntüler, derinlik kestirimi, stereoscopic vision ve stereo görüntü işleme.|
| [Face Recognition](/docs/17-yuz-tanima.md) | Yüz tanıma nedir? Eigenfaces, Fisherfaces, LBPH ve makine öğrenmesi algoritmaları ile yüz tanıma. Farklı kütüphane entegrasyonları (dlib, tensorflow ve face recognition). |
| [Optical Character Recognition OCR ](/docs/18-optik-karakter-tanima.md)| Görüntü üzerindeki metnin tespit edilmesi. OCR süreçleri, algoritmalar ve kütüphaneler. Tesseract, textocr...|
| GPU and Parallel Computing | Cuda modülü ile Nvidia GPU üzerinde paralelleştirilmiş bilgisayarlı görü uygulamaları geliştirme.|
| OpenCV Mobile  | Android ve iOS işletim sistemine sahip mobil cihazlar üzerinde bilgisayarlı görü ve görüntü işleme.|
| Arttırılmış Gerçeklik| 3D modelleri kamera aracılığıyla elde edilmiş gerçek dünya görüntüsü üzerine giydirme. OpenCV ve OpenGL entegrasyonu. İnteraktif bilgisayarlı görü uygulaması geliştirme.|





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
 <td>&nbsp;</td>
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

It's really nice to think about contributing, so you can look at the [SUPPORT] (/CONTRIBUTING.md) link.


## 💬 Question & Answer
You can ask questions, source codes or any other questions by using the **issues** section (new issues). You can also use this section if you want to answer a question or check out the previous ones.

**How to Ask a Question?**

Öncelikle [issues](https://github.com/mesutpiskin/opencv-tutorial/issues) bölümüne gidiniz. Sayfanın sağında yer alan **new issues** butonuna tıklayın. Açılan ilgili bölüme sorunuzu veya talebinizi açıklayıcı bir şekilde yazarak **Submit new issues** butonu aracılığıyla kaydedin.


## 📄 License
Documents and source codes contained in this project are licensed  [MIT License] (/LICENSE-EN).
