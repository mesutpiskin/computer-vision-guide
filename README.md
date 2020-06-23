[English](./README.en-US.md) | Türkçe

[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/opencv-turkish-tutorial) [![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](#) 
[![Video](https://img.shields.io/badge/Video-@mesutpiskin-red.svg?logo=youtube&longCache=true&style=flat)](https://www.youtube.com/channel/UC_ko-bnDYXCVL1XJG0doRDg)

- [Görüntü İşleme ve Bilgisayarlı Görü Kılavuzu](#görüntü-i̇şleme-ve-bilgisayarlı-görü-kılavuzu)
  - [Dokümantasyon](#dokümantasyon)
  - [Örnek Projeler](#örnek-projeler)
  - [Destek](#destek)
  - [Soru & Cevap](#soru--cevap)
  - [Lisans](#lisans)

Bu eğitim, bilgisayarlı görünün temellerini anlayabilmenizi ve OpenCV ile bilgisayarlı görü uygulamaları geliştirebilmenizi amaçlamaktadır. Python, Java, JavaScript, C# ve C++ örnekleri ile desteklenmektedir. Talep veya öneriniz varsa iletişime geçmekten çekinmeyin. İletişime geçmek için <a href="http://meesutpiskin.com">web sitem</a> veya <a href="mailto:mesutpiskin@outlook.com">e-posta</a> bilgilerini kullanabilirsiniz. Teşekkürler!




# Görüntü İşleme ve Bilgisayarlı Görü Kılavuzu

OpenCV ile bilgisayarlı görü ve görüntü işleme eğitim dokümanı ile birlikte, görüntü işleme algoritmalarını öğrenecek, yeri geldiğinde ise **Java**, **Python** , **C++**, **JavaScript (OpenCV.JS)**, **MATLAB** ve **C# (EmguCV)** programlama dilleri kullanarak örnek uygulamalar geliştireceğiz. Bu eğitim, bilgisayarlı görünün temellerini anlayabilmenizi ve OpenCV ile bilgisayarlı görü uygulamaları geliştirebilmenizi amaçlamaktadır. Python, Java ve C++ örnekleri ile desteklenmektedir. Bu doküman, daha önce görüntü işleme ile uğraşmamış, bu konuda bilgisi olmayanlara ve tam aksine bu konuda bilgili, kendinisini farklı konularda geliştirmek isteyen herkese hitap edecek şekilde hazırlanmıştır. Temel tanımlardan başlanarak birçok kavram ve algoritma ele alınmıştır. Örnek projelere <a href="/code/">code</a> dizininden, eğitim konularına ise <a href="/docs/">docs</a> dizini altından ulaşabilirsiniz, ayrıca dokümantasyon içerisinde kullanılan İngilizce terimlerin Türkçe karşılıklarının yer aldığı <a href="/docs/terimler.md">terimler</a> sayfasına, konu ile alakalı önerilen tavsiye içeriklere ise <a href="/other/tavsiye-icerikler.md">tavsiye icerik</a> sayfasından ulaşabilirsiniz.

<p align="center">

<img src="/other/banner.png"/>
</p>


## Dokümantasyon

| Bölüm                                                                            | Özet                                                                                                                                                                       |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [OpenCV Nedir?](/docs/1-opencv-nedir.md)                                         | OpenCV'nin tarihi ve bileşenleri, alternatif görüntü işleme kütüphaneleri, neden OpenCV, OpenCV 2 vs OpenCV 3 ve OpenCV 4 ile gelecek yenilikler.                          |
| [Geliştirme Ortamı ve Platformlar](/docs/2-gelistirme-ortamlari.md)              | Hangi platform ve geliştirme ortamı seçilmeli, görüntü işleme için neden Java, C++ ve Python kullanılıyor.                                                                 |
| [OpenCV Wrappers](/docs/3-opencv-wrappers.md)                                    | Wrapper nedir? EmguCV, JavaCV, LiveCV, RubyCV nedir ve wrapperlar arası farklar nelerdir.                                                                                  |
| [Kurulum ve Derleme](/docs/4-opencv-kurulumlar.md)                               | Windows, Linux, macOS ve Raspberry Pi için OpenCV kurulumu.                                                                                                                |
| [IDE Yapılandırması](/docs/5-ide-yapilandirmasi.md)                              | Eclipse, Netbeans, Android Studio ve Intelij IDEA için yapılandırma ayarları.                                                                                              |
| [Giriş ve Temel Kavramlar](/docs/6-giris-temel-kavramlar.md)                     | Görüntü işleme kavramları. Dosyadan, kameradan, IP kameradan görüntü okuma. Kamera parametrelerini değiştirme.                                                             |
| [Video Kaydediciler ve Kod Çözücüler](/docs/7-video-kaydediciler-codec.md)       | Codec, FourCC ve video kaydetme.                                                                                                                                           |
| [Görüntü Manipülasyonu](/docs/8-goruntu-manipulasyonu.md)                        | Piksel manüpülasyonu, geometrik çizimler ve geometrik dönüşümler.                                                                                                          |
| [Renk Uzayları ve Histogram](/docs/9-renk-uzaylari.md)                           | Temel renk uzayları, renk uzayları arası dönüşüm. Histogram kavramı ve histogram eşitleme.                                                                                 |
| [Morfolojik Görüntü işleme](/docs/10-morfolojik-goruntu-isleme.md)               | Morfolojik operatörler ve eşikleme: Erosion, dilation, closing, gradyan, thresholding ...                                                                                  |
| [Filtreler ve Kenar Belirleme](/docs/11-filtreler-ve-kenar-belirleme.md)         | Filtreleme ve kenar belirleme algoritmaları: Blur, Sobel, Laplace, Canny ...                                                                                               |
| [Arkaplan Çıkarma](/docs/12-arka-plan-cikarma.md)                                | Absdiff, MOG, MOG2 ve GMG algoritmaları kullanarak, 2D görüntü arkaplan çıkarımı.                                                                                          |
| [Nesne Tespiti ve Nesne Tanıma](/docs/14-nesne-tespiti.md)                       | Nesne tespit süreçleri ve algoritmaları. HaarCascade, TemplateMatching, DNN, CNN, SVM Makine Öğrenmesi ve Derin Öğrenme algoritmaları ...                                  |
| [Öznitelik ve Öznitelik Çıkarımı](/docs/19-oznitelik-cikarimi.md)                | Öznitelik tanımı, nesne tespiti için öznitelik çıkarmı ve öznitelik eşleştirme. Brute-Force, FLANN, SURF, SIFT, BRIEF, ORB, FAST algoritmaları ...                         |
| [Video Analiz ve Nesne Takibi](/docs/13-video-analiz.md)                         | Mean Shift, Cam Shift, Optik akış, GOTURN, BOOSTING, MIL, CNN vb. algoritmalar ile video üzerinde nesne veya alan takibi.                                                  |
| [Görüntü Bozulmaları ve Stereo Görü](/docs/15-kamera-kalibrasyonu-ve-3d-goru.md) | Görüntü bozulmaları ve kamera kalibrasyonu, 3D görüntüler, derinlik kestirimi, stereoscopic vision ve stereo görüntü işleme.                                               |
| [Yüz Tanıma](/docs/17-yuz-tanima.md)                                             | Yüz tanıma nedir? Eigenfaces, Fisherfaces, LBPH ve makine öğrenmesi algoritmaları ile yüz tanıma. Farklı kütüphane entegrasyonları (dlib, tensorflow ve face recognition). |
| [Optik Karakter Tanıma OCR ](/docs/18-optik-karakter-tanima.md)                  | Görüntü üzerindeki metnin tespit edilmesi. OCR süreçleri, algoritmalar ve kütüphaneler. Tesseract, textocr...                                                              |
| GPU ve Paralel Hesaplama                                                         | Cuda modülü ile Nvidia GPU üzerinde paralelleştirilmiş bilgisayarlı görü uygulamaları geliştirme.                                                                          |
| OpenCV Mobil                                                                     | Android ve iOS işletim sistemine sahip mobil cihazlar üzerinde bilgisayarlı görü ve görüntü işleme.                                                                        |
| Artırılmış Gerçeklik                                                             | 3D modelleri kamera aracılığıyla elde edilmiş gerçek dünya görüntüsü üzerine giydirme. OpenCV ve OpenGL entegrasyonu. İnteraktif bilgisayarlı görü uygulaması geliştirme.  |

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
<li><a href="/code/goruntu-manipulasyonu/python/geometrik-sekiller.py">Geometrik Şekil çizme</a></li>
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
<td>Morfolojik G&ouml;rüntü İşleme</td>
<td>
<ul>
<li><a href="/code/morfolojik-goruntu-isleme/python/acinim-opening.py">Açınım (Opening)</a></li>
<li><a href="/code/morfolojik-goruntu-isleme/python/kapanim-closing.py">Kapanım (Closing)</a></li>
<li><a href="/code/morfolojik-goruntu-isleme/python/genisletme-dilation.py">Genisletme (Dilation)</a></li>
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
<td>&nbsp;Filtreler</td>
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
<td>&nbsp;Kenar Çıkarma</td>
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
<td>Arka Plan Çıkarma</td>
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
<td>Nesne Tespiti ve Nesne Tanıma</td>
<td>
<ul>
<li><a href="/code/nesne-tespit-ve-tanima/python/template-matching.py">Template Matching</a></li>
<li><a href="/code/nesne-tespit-ve-tanima/python/derin_sinir_agi.py">Derin Sinir Ağı DNN ile Nesne Tanıma</a></li>
<li><a href="/code/nesne-tespit-ve-tanima/python/haar-cascade.py">HaarCascade Classifier ile Yüz Tespiti</a></li>
</ul>
</td>
<td>

<ul>
<li><a href="/code/nesne-tespit-ve-tanima/java/TemplateMatching.java">Template Matching ile Nesne Tanıma</a></li>
<li><a href="https://github.com/mesutpiskin/opencv-object-detection/tree/master/src/DeepNeuralNetwork">Derin Sinir Ağı DNN ile Nesne Tanıma</a></li>
<li><a href="/code/nesne-tespit-ve-tanima/java/DetectFace.java">HaarCascade Classifier ile Yüz Tespiti</a></li>

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
<li><a href="/code/kamera-kalibrasyon-3d-goru/python/fisheye-lens-duzeltme.py">Balık Gözü (Fisheye) Görüntü Düzeltme</a></li>
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
<li><a href="/code/yuz-tanima/python/dnn_yuz_tespiti/">Derin Sinir Ağı (DNN) ile Yüz Tespiti</a></li>
</ul>

</td>
<td>
<ul>
<li><a href="https://github.com/mesutpiskin/GenderClassification">Derin Sinir Ağı (DNN) ile Cinsiyet Tespiti</a></li>
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
<li><a href="/code/yuz-tanima/python/facerecognition_kutuphanesi/">"FaceRecognition" kullanarak Yüz Tanıma</a></li>
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
<td>Optik Karakter Tanıma OCR</td>
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
<td>Arttırılmış Gerçeklik ve Görüntü Harmanlama</td>
<td>
<ul>
<li><a href="/code/arttirilmis-gerceklik/python/sapka-filtresi/">Şapka Filtresi - Yüz Tespiti ve Şapka Giydirme</a></li>
</ul>

</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
</tr>
</tbody>
</table>

## Destek

Katkıda bulunmayı düşünmeniz gerçekten çok güzel bir haber, bunun için [DESTEK](/CONTRIBUTING.md) bağlantısına göz atabilirsiniz.

## Soru & Cevap

Dokümanlar, kaynak kodlar veya her hangi bir konuda ki sorularınızı **issues** bölümünü kullanarak sorabilirsiniz (new issues). Soru cevaplamak veya daha öncekilere göz atmak isterseniz yine bu bölümü kullanabilirsiniz.

**Nasıl Soru Sorulur?**

Öncelikle [issues](https://github.com/mesutpiskin/opencv-tutorial/issues) bölümüne gidiniz. Sayfanın sağında yer alan **new issues** butonuna tıklayın. Açılan ilgili bölüme sorunuzu veya talebinizi açıklayıcı bir şekilde yazarak **Submit new issues** butonu aracılığıyla kaydedin.

## Lisans

Bu proje içerisinde yer alan doküman ve kaynak kodlar [MIT Lisansı](/LICENSE) ile lisanslanmıştır. İçeriğin **kaynak gösterilmeden** kullanılması durumunda bu kişiler/kurumlar [bu bölümde](/other/blacklist.md) paylaşılacaktır.
