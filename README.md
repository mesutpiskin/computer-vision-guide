[English](./README.en-US.md) | Türkçe

[![Bölüm](https://img.shields.io/badge/bölüm-31-brightgreen.svg)](#dokümantasyon)
[![Sponsor](https://img.shields.io/badge/sponsor-%E2%9D%A4-ff69b4.svg?logo=github)](https://github.com/sponsors/mesutpiskin)
[![Video](https://img.shields.io/badge/Video-@mesutpiskin-red.svg?logo=youtube&longCache=true&style=flat)](https://www.youtube.com/channel/UC_ko-bnDYXCVL1XJG0doRDg)

# Görüntü İşleme ve Bilgisayarlı Görü Kılavuzu

OpenCV ve modern derin öğrenme framework'leriyle bilgisayarlı görü uygulamaları geliştirmeye yönelik kapsamlı Türkçe kaynak.

<p align="center">
<img src="/other/banner.png"/>
</p>

Bu kılavuz, üniversite öğrencisinden yazılım geliştiriciye her seviyeye hitap eder. Her konu gerçek dünya problemiyle açılır, formüller sezgiyle desteklenir, kod örnekleri kopyala-çalıştır kalitesindedir. Öğrenciler kavramı öğrenir, geliştiriciler doğrudan üretime taşır.

**31 bölüm** · Python 3.10+ · OpenCV 4.9+ · PyTorch · Ultralytics YOLOv8

---

## İçindekiler

- [Dokümantasyon](#dokümantasyon)
- [Başlarken](#başlarken)
- [Örnek Projeler](#örnek-projeler)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Projeyi Destekle](#projeyi-destekle)
- [Sürüm Geçmişi](#sürüm-geçmişi)

---

## Dokümantasyon

Her bölüm şu yapıyı izler: **gerçek dünya problemi** → sezgisel açıklama → formül (gerekirse) → tam çalışan Python kodu → karşılaştırma tablosu → özet ve kaynaklar.

Kullanılan İngilizce terimlerin Türkçe karşılıkları için [terimler sözlüğüne](/docs/terimler.md), önerilen ek kaynaklar için [tavsiye içerikler](/other/tavsiye-icerikler.md) sayfasına bakabilirsiniz.

| Bölüm | Özet |
| ----- | ---- |
| [OpenCV Nedir?](/docs/1-opencv-nedir.md) | OpenCV tarihi ve mimarisi, modüller, alternatif kütüphaneler karşılaştırması, OpenCV 4.x/5.0 yenilikleri. |
| [Geliştirme Ortamı ve Platformlar](/docs/2-gelistirme-ortamlari.md) | Python, VS Code, Jupyter Notebook, Google Colab ve Conda ile geliştirme ortamı kurulumu. |
| [OpenCV Wrappers](/docs/3-opencv-wrappers.md) | EmguCV, JavaCV, LiveCV, RubyCV ve wrapper'lar arası farklar. |
| [Kurulum ve Derleme](/docs/4-opencv-kurulumlar.md) | Windows, Linux, macOS ve Raspberry Pi için OpenCV kurulumu ve derleme seçenekleri. |
| [IDE Yapılandırması](/docs/5-ide-yapilandirmasi.md) | VS Code, PyCharm, Conda, Google Colab ve Android Studio yapılandırması. |
| [Giriş ve Temel Kavramlar](/docs/6-giris-temel-kavramlar.md) | Dijital görüntünün matris temsili, BGR/RGB farkı, dosyadan ve kameradan görüntü okuma, piksel manipülasyonu. |
| [Video Kaydediciler ve Kod Çözücüler](/docs/7-video-kaydediciler-codec.md) | Codec, FourCC ve `cv2.VideoWriter` ile video kaydetme. |
| [Görüntü Manipülasyonu](/docs/8-goruntu-manipulasyonu.md) | Yeniden boyutlandırma, döndürme, affine ve perspektif dönüşümleri; belge tarayıcı uygulaması senaryosu. |
| [Renk Uzayları ve Histogram](/docs/9-renk-uzaylari.md) | BGR, HSV, Lab renk uzayları; renk maskesiyle nesne tespiti; histogram eşitleme ve CLAHE. |
| [Morfolojik Görüntü İşleme](/docs/10-morfolojik-goruntu-isleme.md) | Erosion, dilation, opening, closing, morfolojik gradient; Otsu ve adaptif eşikleme. |
| [Filtreler ve Kenar Belirleme](/docs/11-filtreler-ve-kenar-belirleme.md) | Konvolüsyon sezgisi, Gaussian/Median/Bilateral blur, Sobel, Canny dört aşamalı boru hattı. |
| [Arkaplan Çıkarma](/docs/12-arka-plan-cikarma.md) | Frame differencing, MOG2 Gaussian karışım modeli, KNN subtractor; güvenlik kamerası senaryosu. |
| [Video Analiz ve Nesne Takibi](/docs/13-video-analiz.md) | Optik akış kısıtı, Lucas-Kanade piramidal LK, Farneback dense flow, CSRT ve KCF tracker. |
| [Nesne Tespiti ve Tanıma](/docs/14-nesne-tespiti.md) | Haar Cascade, Template Matching, YOLOv8 gerçek zamanlı tespit; IoU, Precision/Recall ve mAP metrikleri. |
| [Kamera Kalibrasyonu ve 3D Görü](/docs/15-kamera-kalibrasyonu-ve-3d-goru.md) | Pinhole kamera modeli, radyal bozulma düzeltme, satranç tahtası kalibrasyonu, stereo derinlik haritası. |
| [Yüz Tanıma](/docs/17-yuz-tanima.md) | Eigenfaces/LBPH, FaceNet embedding sezgisi, ArcFace açısal margin, DeepFace ile hazır entegrasyon. |
| [Optik Karakter Tanıma (OCR)](/docs/18-optik-karakter-tanima.md) | OCR boru hattı, görüntü önişleme, Tesseract PSM modları, EasyOCR, EAST metin tespiti. |
| [Öznitelik Çıkarımı](/docs/19-oznitelik-cikarimi.md) | SIFT DoG ölçek uzayı, ORB, FLANN eşleştirme, Lowe oran testi, RANSAC homoğrafi; panorama dikişleme. |
| [GPU ve Paralel Hesaplama](/docs/20-gpu-paralel-hesaplama.md) | CUDA modülü, OpenVINO ile model hızlandırma, threading ile paralel görüntü işleme. |
| [Poz Tahmini](/docs/21-poz-tahmini.md) | 17 COCO keypoint, MediaPipe Pose ile iskelet tespiti, açı hesaplama fonksiyonu, squat sayacı, YOLOv8-Pose. |
| [Segmentasyon](/docs/22-segmentasyon.md) | Semantik/instance/panoptik farkı, Watershed, YOLOv8-seg, SAM (Segment Anything), IoU ve mIoU. |
| [Edge Deployment](/docs/23-edge-deployment.md) | ONNX Runtime ve TFLite ile model optimizasyonu, Raspberry Pi ve mobil platform deployment. |
| [OpenCV Mobil](/docs/24-opencv-mobil.md) | Android ve iOS'ta OpenCV, kamera akışı işleme, TFLite entegrasyonu. |
| [Artırılmış Gerçeklik](/docs/25-artirilmis-gerceklik.md) | ArUco marker tespiti, 3D eksen projeksiyonu, görüntü giydirme, MediaPipe yüz filtresi. |
| [Vision Transformers](/docs/26-vision-transformers.md) | Attention mekanizması sezgisi, ViT patch embedding ve CLS token, Swin kaydırmalı pencere, DETR, CNN vs ViT. |
| [Generatif Modeller ve Diffusion](/docs/27-generatif-modeller.md) | GAN minimax oyun sezgisi, VAE latent space, DDPM gürültü süreci, Stable Diffusion, ControlNet. |
| [3D Vision](/docs/28-3d-vision.md) | Stereo ve monoküler derinlik tahmini, Open3D nokta bulutu, PointNet permutation invariance, NeRF. |
| [Video Anlama ve Eylem Tanıma](/docs/29-video-siniflandirma.md) | Two-Stream, SlowFast çift yol mimarisi, VideoMAE tüp maskeleme, HuggingFace ile eylem sınıflandırma. |
| [Model Eğitimi ve Değerlendirme](/docs/30-model-egitimi-ve-degerlendirme.md) | Veri hazırlama, augmentation, Mixup, ResNet50 fine-tuning, Cosine Annealing, confusion matrix. |
| [Vision-Language Modeller](/docs/31-vision-language-modeller.md) | CLIP contrastive loss, zero-shot sınıflandırma, LLaVA, BLIP-2 Q-Former; görsel soru-cevap. |

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
<td><strong>Konu</strong></td>
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
<td>Kenar Belirleme</td>
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
<td>Arkaplan Çıkarma</td>
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

## Katkıda Bulunma

Katkıda bulunmak için [CONTRIBUTING.md](/CONTRIBUTING.md) dosyasına göz atabilirsiniz. Hata bildirimi, yeni bölüm önerisi veya kod düzeltmesi — her türlü katkı memnuniyetle karşılanır.

Sorularınızı [Issues](https://github.com/mesutpiskin/computer-vision-guide/issues) bölümünü kullanarak iletebilirsiniz. Genel konular için <a href="http://mesutpiskin.com">web sitesi</a> veya <a href="mailto:mesutpiskin@outlook.com">e-posta</a> üzerinden ulaşabilirsiniz.

---

## Projeyi Destekle

Bu kılavuz, tamamen gönüllü emekle hazırlanmış ücretsiz ve açık kaynaklı bir eğitim kaynağıdır. Yeni bölümler eklenmesine, mevcut içeriğin güncellenmesine ve topluluğun büyümesine katkıda bulunmak istiyorsanız GitHub Sponsors üzerinden destek olabilirsiniz.

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-%23ff69b4?logo=github-sponsors&logoColor=white)](https://github.com/sponsors/mesutpiskin)

Desteğiniz; yeni bölümlerin yazılmasına, örnek kodların güncellenmesine ve Türkçe bilgisayarlı görü ekosisteminin gelişmesine doğrudan katkı sağlar.

---

## Sürüm Geçmişi

### v3.0 — Mayıs 2026

Reponun 2020'den bu yana en kapsamlı güncellemesi. Python-first altyapıya geçiş, 11 yeni bölüm ve tüm mevcut bölümlerin sıfırdan yeniden yazımı aynı anda gerçekleştirildi. O'Reilly tarzı pedagojik yapı benimsendi: her konu gerçek dünya problemiyle açılır, formüller sezgiyle desteklenir, kod örnekleri kopyala-çalıştır kalitesindedir.

**Yeniden yazılan bölümler (15 bölüm):** 1, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 21, 22

**Yeni eklenen bölümler (11 bölüm):**
- **Bölüm 20:** [GPU ve Paralel Hesaplama](/docs/20-gpu-paralel-hesaplama.md) — CUDA, OpenVINO, Threading
- **Bölüm 21:** [Poz Tahmini](/docs/21-poz-tahmini.md) — MediaPipe Pose, YOLOv8-Pose, açı hesaplama
- **Bölüm 22:** [Segmentasyon](/docs/22-segmentasyon.md) — YOLOv8-seg, SAM, DeepLab
- **Bölüm 23:** [Edge Deployment](/docs/23-edge-deployment.md) — ONNX Runtime, TFLite, niceleme
- **Bölüm 24:** [OpenCV Mobil](/docs/24-opencv-mobil.md) — Android, iOS
- **Bölüm 25:** [Artırılmış Gerçeklik](/docs/25-artirilmis-gerceklik.md) — ArUco, 3D Overlay, Yüz Filtresi
- **Bölüm 26:** [Vision Transformers](/docs/26-vision-transformers.md) — ViT, Swin Transformer, DETR
- **Bölüm 27:** [Generatif Modeller ve Diffusion](/docs/27-generatif-modeller.md) — GAN, VAE, DDPM, Stable Diffusion
- **Bölüm 28:** [3D Vision](/docs/28-3d-vision.md) — PointNet, NeRF, Derinlik Tahmini
- **Bölüm 29:** [Video Anlama ve Eylem Tanıma](/docs/29-video-siniflandirma.md) — SlowFast, VideoMAE
- **Bölüm 30:** [Model Eğitimi ve Değerlendirme](/docs/30-model-egitimi-ve-degerlendirme.md) — Transfer Learning, Augmentation
- **Bölüm 31:** [Vision-Language Modeller](/docs/31-vision-language-modeller.md) — CLIP, LLaVA, BLIP-2

---

### v1.0 — 2018–2020 · [`v1` etiketi](https://github.com/mesutpiskin/computer-vision-guide/tree/v1)

İlk yayın. OpenCV 3.x/4.x ile Java, Python ve C++ örnekleri. Temel görüntü işleme konuları.
