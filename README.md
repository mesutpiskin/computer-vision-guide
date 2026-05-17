[English](./README.en-US.md) | Türkçe

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](#lisans)
[![Bölüm](https://img.shields.io/badge/bölüm-31-brightgreen.svg)](#dokümantasyon)
[![Video](https://img.shields.io/badge/Video-@mesutpiskin-red.svg?logo=youtube&longCache=true&style=flat)](https://www.youtube.com/channel/UC_ko-bnDYXCVL1XJG0doRDg)

# Görüntü İşleme ve Bilgisayarlı Görü Kılavuzu

OpenCV ve modern derin öğrenme framework'leriyle bilgisayarlı görü uygulamaları geliştirmeye yönelik kapsamlı Türkçe kaynak. Her bölüm teorik temel, matematiksel formüller ve tam çalışan Python kodu içerir.

<p align="center">
<img src="/other/banner.png"/>
</p>

**31 bölüm** · Python 3.10+ · OpenCV 4.9+ · PyTorch · Ultralytics YOLOv8

---

## İçindekiler

- [Dokümantasyon](#dokümantasyon)
- [Örnek Projeler](#örnek-projeler)
- [Başlarken](#başlarken)
- [Katkıda Bulunma](#destek)
- [Soru & Cevap](#soru--cevap)
- [Sürüm Notları](#sürüm-notları)
- [Lisans](#lisans)

---

## Dokümantasyon

Her bölüm şu yapıyı izler: **Teorik Temel** (formüller + akademik referanslar) → **Pratik Uygulama** (tam çalışan Python kodu) → **Özet & İleri Okuma**. Kullanılan İngilizce terimlerin Türkçe karşılıkları için [terimler sözlüğüne](/docs/terimler.md), önerilen ek kaynaklar için [tavsiye içerikler](/other/tavsiye-icerikler.md) sayfasına bakabilirsiniz.

| Bölüm | Özet |
| ----- | ---- |
| [OpenCV Nedir?](/docs/1-opencv-nedir.md) | OpenCV tarihi ve bileşenleri, alternatif kütüphaneler karşılaştırması, OpenCV 4.x/5.0 yenilikleri. |
| [Geliştirme Ortamı ve Platformlar](/docs/2-gelistirme-ortamlari.md) | Python, VS Code, Jupyter Notebook, Google Colab ve Conda ile geliştirme ortamı kurulumu. |
| [OpenCV Wrappers](/docs/3-opencv-wrappers.md) | EmguCV, JavaCV, LiveCV, RubyCV ve wrapper'lar arası farklar. |
| [Kurulum ve Derleme](/docs/4-opencv-kurulumlar.md) | Windows, Linux, macOS ve Raspberry Pi için OpenCV kurulumu. |
| [IDE Yapılandırması](/docs/5-ide-yapilandirmasi.md) | VS Code, PyCharm, Conda, Google Colab ve Android Studio yapılandırması. |
| [Giriş ve Temel Kavramlar](/docs/6-giris-temel-kavramlar.md) | Görüntü fonksiyonu $f:\mathbb{Z}^2\to\mathbb{Z}^k$, piksel/matris teorisi, dosyadan/kameradan/IP kameradan görüntü okuma. |
| [Video Kaydediciler ve Kod Çözücüler](/docs/7-video-kaydediciler-codec.md) | Codec, FourCC ve video kaydetme. |
| [Görüntü Manipülasyonu](/docs/8-goruntu-manipulasyonu.md) | Affine/perspektif dönüşüm matrisleri, interpolasyon teorisi, geometrik çizimler. |
| [Renk Uzayları ve Histogram](/docs/9-renk-uzaylari.md) | ITU-R BT.601 parlaklık denklemi, HSV/Lab dönüşüm formülleri, histogram eşitleme (CDF). |
| [Morfolojik Görüntü İşleme](/docs/10-morfolojik-goruntu-isleme.md) | Minkowski toplamı/farkı (dilation/erosion), opening/closing/gradient, structuring element seçimi. |
| [Filtreler ve Kenar Belirleme](/docs/11-filtreler-ve-kenar-belirleme.md) | Gaussian filtre, Sobel gradyanı, Laplace, Canny 4-aşamalı boru hattı. |
| [Arkaplan Çıkarma](/docs/12-arka-plan-cikarma.md) | GMM istatistiksel modeli $P(x)=\sum w_k\mathcal{N}$, MOG2 online güncelleme, Zivkovic ICPR 2004. |
| [Video Analiz ve Nesne Takibi](/docs/13-video-analiz.md) | Optik akış kısıtı, Lucas-Kanade en küçük kareler, piramidal LK, nesne takibi. |
| [Nesne Tespiti ve Tanıma](/docs/14-nesne-tespiti.md) | IoU/mAP/Precision-Recall, YOLO kayıp fonksiyonu, YOLOv8 ile gerçek zamanlı tespit. |
| [Kamera Kalibrasyonu ve 3D Görü](/docs/15-kamera-kalibrasyonu-ve-3d-goru.md) | Pinhole kamera modeli, radyal bozulma, DLT algoritması, stereo görü. |
| [Yüz Tanıma](/docs/17-yuz-tanima.md) | PCA/Eigenfaces, FaceNet triplet loss, ArcFace açısal margin, DeepFace entegrasyonu. |
| [Optik Karakter Tanıma (OCR)](/docs/18-optik-karakter-tanima.md) | CTC kayıp türetimi, CRNN mimarisi (CNN+BiLSTM+CTC), EasyOCR ve Tesseract. |
| [Öznitelik Çıkarımı](/docs/19-oznitelik-cikarimi.md) | SIFT DoG ölçek uzayı, 128-boyutlu descriptor, Lowe oran testi, FLANN+RANSAC homoğrafi. |
| [GPU ve Paralel Hesaplama](/docs/20-gpu-paralel-hesaplama.md) | CUDA modülü, OpenVINO ve threading ile paralel görüntü işleme. |
| [Poz Tahmini](/docs/21-poz-tahmini.md) | Keypoint Gaussian ısı haritası, OKS metriği, MediaPipe Pose ile iskelet tespiti ve açı hesaplama. |
| [Segmentasyon](/docs/22-segmentasyon.md) | mIoU formülü, Mask R-CNN pipeline, SAM mimarisi, YOLOv8-seg ile örnek segmentasyonu. |
| [Edge Deployment](/docs/23-edge-deployment.md) | ONNX Runtime ve TFLite ile model optimizasyonu, Raspberry Pi/mobil deployment. |
| [OpenCV Mobil](/docs/24-opencv-mobil.md) | Android ve iOS platformlarında OpenCV, kamera akışı işleme ve TFLite entegrasyonu. |
| [Artırılmış Gerçeklik](/docs/25-artirilmis-gerceklik.md) | ArUco marker tespiti, 3D eksen projeksiyonu, görüntü giydirme, MediaPipe yüz filtresi. |
| [Vision Transformers](/docs/26-vision-transformers.md) | ViT patch embedding, multi-head self-attention $\text{softmax}(QK^T/\sqrt{d_k})V$, DETR, Swin Transformer. |
| [Generatif Modeller ve Diffusion](/docs/27-generatif-modeller.md) | GAN minimax, VAE ELBO, DDPM ileri/geri yayılım, Stable Diffusion ve ControlNet. |
| [3D Vision](/docs/28-3d-vision.md) | PointNet simetrik fonksiyon, NeRF hacimsel render $C(\mathbf{r})=\int T(t)\sigma\mathbf{c}\,dt$, monoküler derinlik tahmini. |
| [Video Anlama ve Eylem Tanıma](/docs/29-video-siniflandirma.md) | SlowFast çift-yol mimarisi, VideoMAE tüp maskeleme, HuggingFace ile eylem tanıma. |
| [Model Eğitimi ve Değerlendirme](/docs/30-model-egitimi-ve-degerlendirme.md) | Transfer learning, Mixup augmentation, Cosine Annealing, Precision/Recall/F1/mAP. |
| [Vision-Language Modeller](/docs/31-vision-language-modeller.md) | CLIP contrastive loss, LLaVA görsel talimat ayarı, BLIP-2 Q-Former, zero-shot sınıflandırma. |

---

## Başlarken

Temel bağımlılıkları kurmak için:

```bash
pip install opencv-python numpy matplotlib
```

Derin öğrenme ve modern bölümler için:

```bash
pip install torch torchvision ultralytics mediapipe easyocr deepface transformers diffusers open3d
```

Kod örnekleri Python 3.10+ ve OpenCV 4.9+ gerektirir. Örnek kaynak kodlara [`/code`](/code/) dizininden ulaşabilirsiniz.

---

## Örnek Projeler

<table style="width: 100%;">
<tbody>
<tr>
<td><strong>&nbsp;Konu</strong></td>
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
<li><a href="/code/kamera-io/python/video_io.py">Video ve Kamera Giriş Çıkış</a></li>
<li><a href="/code/kamera-io/python/video-kaydet.py">Video Kaydetme</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Görüntü Manipülasyonu</td>
<td>
<ul>
<li><a href="/code/goruntu-manipulasyonu/python/geometrik-sekiller.py">Geometrik Şekil Çizme</a></li>
<li><a href="/code/goruntu-manipulasyonu/python/goruntu-kirpma.py">Görüntü Kırpma</a></li>
<li><a href="/code/goruntu-manipulasyonu/python/piksel-manupulasyonu.py">Piksel Manipülasyonu</a></li>
<li><a href="/code/goruntu-manipulasyonu/python/yeniden-boyutlandirma.py">Görüntü Boyutlandırma</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Renk Uzayları</td>
<td>
<ul>
<li><a href="/code/renk-uzaylari/python/renk-uzayi-donusumu.py">Renk Uzayı Dönüşümü</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Morfolojik Görüntü İşleme</td>
<td>
<ul>
<li><a href="/code/morfolojik-goruntu-isleme/python/acinim-opening.py">Açınım (Opening)</a></li>
<li><a href="/code/morfolojik-goruntu-isleme/python/kapanim-closing.py">Kapanım (Closing)</a></li>
<li><a href="/code/morfolojik-goruntu-isleme/python/genisletme-dilation.py">Genişletme (Dilation)</a></li>
<li><a href="/code/morfolojik-goruntu-isleme/python/gradient.py">Gradyan (Gradient)</a></li>
<li><a href="/code/morfolojik-goruntu-isleme/python/asindirme-erozyon.py">Aşındırma (Erosion)</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Filtreler</td>
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
<td>Kenar Çıkarma</td>
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
<td>Arka Plan Çıkarma</td>
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
<td>Video Analiz ve Nesne Takibi</td>
<td>
<ul>
<li><a href="/code/video-analiz/python/meanshift.py">MeanShift</a></li>
<li><a href="/code/video-analiz/python/camshift.py">CamShift</a></li>
</ul>
</td>
<td>
<ul>
<li><a href="https://github.com/mesutpiskin/opencv-object-detection/tree/master/src/ColorBasedObjectTracker">Renk Tabanlı Nesne Takibi</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Nesne Tespiti ve Tanıma</td>
<td>
<ul>
<li><a href="/code/nesne-tespit-ve-tanima/python/template-matching.py">Template Matching</a></li>
<li><a href="/code/nesne-tespit-ve-tanima/python/derin_sinir_agi.py">DNN ile Nesne Tanıma</a></li>
<li><a href="/code/nesne-tespit-ve-tanima/python/haar-cascade.py">HaarCascade ile Yüz Tespiti</a></li>
</ul>
</td>
<td>
<ul>
<li><a href="/code/nesne-tespit-ve-tanima/java/TemplateMatching.java">Template Matching</a></li>
<li><a href="https://github.com/mesutpiskin/opencv-object-detection/tree/master/src/DeepNeuralNetwork">DNN ile Nesne Tanıma</a></li>
<li><a href="/code/nesne-tespit-ve-tanima/java/DetectFace.java">HaarCascade ile Yüz Tespiti</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Öznitelik Çıkarımı</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Kamera Kalibrasyonu ve 3D Görü</td>
<td>
<ul>
<li><a href="/code/kamera-kalibrasyon-3d-goru/python/fisheye-lens-duzeltme.py">Balık Gözü Görüntü Düzeltme</a></li>
<li><a href="/code/kamera-kalibrasyon-3d-goru/python/kamera-kalibrasyonu.py">Kamera Kalibrasyonu</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Makine Öğrenmesi ve Derin Öğrenme</td>
<td>
<ul>
<li><a href="/code/yuz-tanima/python/dnn_yuz_tespiti/">DNN ile Yüz Tespiti</a></li>
</ul>
</td>
<td>
<ul>
<li><a href="https://github.com/mesutpiskin/GenderClassification">DNN ile Cinsiyet Tespiti</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Yüz Tanıma</td>
<td>
<ul>
<li><a href="/code/yuz-tanima/python/facerecognition_kutuphanesi/">FaceRecognition ile Yüz Tanıma</a></li>
<li><a href="/code/yuz-tanima/python/facenet/">FaceNet ile Yüz Tanıma</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>
<ul>
<li><a href="https://github.com/mesutpiskin/face-detection-and-recognition">Eigenfaces ve Fisherfaces ile Yüz Tanıma</a></li>
</ul>
</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Optik Karakter Tanıma (OCR)</td>
<td>
<ul>
<li><a href="/code/optik-karakter-tanima-ocr/python/tesseract-python/">Tesseract ile OCR</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>GPU ve Paralel Hesaplama</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>OpenCV Mobil</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
<tr>
<td>Artırılmış Gerçeklik</td>
<td>
<ul>
<li><a href="/code/arttirilmis-gerceklik/python/sapka-filtresi/">Şapka Filtresi — Yüz Tespiti ve Şapka Giydirme</a></li>
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

## Destek

Katkıda bulunmak için [CONTRIBUTING.md](/CONTRIBUTING.md) dosyasına göz atabilirsiniz. Hata bildirimi, yeni bölüm önerisi veya kod düzeltmesi her türlü katkı memnuniyetle karşılanır.

---

## Soru & Cevap

Dokümanlar, kaynak kodlar veya herhangi bir konudaki sorularınızı [issues](https://github.com/mesutpiskin/computer-vision-guide/issues) bölümünü kullanarak sorabilirsiniz. Soru sormak için **New Issue** butonuna tıklayın, sorunuzu açıklayıcı biçimde yazın ve gönderin.

Genel sorularınız veya tartışmalar için iletişime geçmek isterseniz <a href="http://mesutpiskin.com">web sitem</a> veya <a href="mailto:mesutpiskin@outlook.com">e-posta</a> üzerinden ulaşabilirsiniz.

---

## Sürüm Notları

### v3.0 — Mayıs 2026 (Akademik Genişletme)

**Revize Edilen Bölümler (15 bölüm):**
Tüm temel bölümler LaTeX formüller, arXiv/DOI akademik referanslar ve tam çalışan Python kodlarıyla (OpenCV 4.9+, PyTorch, Ultralytics) zenginleştirildi. Kod kalitesi standartları uygulandı: `None` kontrolü, `ret` kontrolü, kaynak yönetimi.

**Yeni Bölümler (6 bölüm):**
- **Bölüm 26:** [Vision Transformers](/docs/26-vision-transformers.md) — ViT, DETR, Swin Transformer
- **Bölüm 27:** [Generatif Modeller ve Diffusion](/docs/27-generatif-modeller.md) — GAN, VAE, DDPM, Stable Diffusion
- **Bölüm 28:** [3D Vision](/docs/28-3d-vision.md) — PointNet, NeRF, Derinlik Tahmini
- **Bölüm 29:** [Video Anlama ve Eylem Tanıma](/docs/29-video-siniflandirma.md) — SlowFast, VideoMAE
- **Bölüm 30:** [Model Eğitimi ve Değerlendirme](/docs/30-model-egitimi-ve-degerlendirme.md)
- **Bölüm 31:** [Vision-Language Modeller](/docs/31-vision-language-modeller.md) — CLIP, LLaVA, BLIP-2

---

### v2.0 — Mayıs 2026 (Modernizasyon) · [`v2.0` etiketi](https://github.com/mesutpiskin/computer-vision-guide/tree/v2.0)

Reponun 2020'den bu yana ilk büyük güncellemesi. Tüm içerik Python-first ve güncel kütüphanelere göre yeniden düzenlendi.

**Güncellenen Bölümler:**
- **Bölüm 1:** OpenCV 4.9/5.0 yenilikleri (DNN, CUDA, QR Kod, G-API)
- **Bölüm 2:** Java/Eclipse odaklı içerik → Python + VS Code + Jupyter + Colab
- **Bölüm 5:** Eclipse/Netbeans → VS Code, PyCharm, Conda, Android Studio
- **Bölüm 13:** GOTURN/Boosting deprecated; DaSiamRPN, NanoTrack, ByteTrack eklendi
- **Bölüm 14:** YOLOv8/v9 (Ultralytics API, özel eğitim, ONNX export)
- **Bölüm 17:** DeepFace, InsightFace, MediaPipe Face Mesh eklendi
- **Bölüm 18:** EasyOCR, PaddleOCR, TrOCR eklendi
- **Bölüm 19:** ORB, SIFT, FLANN, Homografi Python kod örnekleri eklendi

**Yeni Bölümler:**
- **Bölüm 20:** [GPU ve Paralel Hesaplama](/docs/20-gpu-paralel-hesaplama.md) — CUDA, OpenVINO, Threading
- **Bölüm 21:** [Poz Tahmini](/docs/21-poz-tahmini.md) — MediaPipe Pose, YOLOv8-Pose
- **Bölüm 22:** [Segmentasyon](/docs/22-segmentasyon.md) — YOLOv8-seg, SAM/SAM2, DeepLab
- **Bölüm 23:** [Edge Deployment](/docs/23-edge-deployment.md) — ONNX Runtime, TFLite, Quantization
- **Bölüm 24:** [OpenCV Mobil](/docs/24-opencv-mobil.md) — Android, iOS
- **Bölüm 25:** [Artırılmış Gerçeklik](/docs/25-artirilmis-gerceklik.md) — ArUco, 3D Overlay, Yüz Filtresi

---

### v1.0 — 2018–2020 · [`v1` etiketi](https://github.com/mesutpiskin/computer-vision-guide/tree/v1)

İlk yayın. OpenCV 3.x/4.x ile Java, Python ve C++ örnekleri. Temel görüntü işleme konuları.

---

## Lisans

Bu proje [MIT Lisansı](/LICENSE) ile lisanslanmıştır. İçeriğin **kaynak gösterilmeden** kullanılması durumunda ilgili kişiler/kurumlar [bu bölümde](/other/blacklist.md) paylaşılacaktır.
