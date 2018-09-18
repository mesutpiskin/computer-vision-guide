
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/opencv-turkish-tutorial) [![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](#) ![%60](http://progressed.io/bar/60?title=Tamamlanan "Genel Tamamlanma %60")

# Görüntü İşleme ve Bilgisayarlı Görü

OpenCV ile bilgisayarlı görü ve görüntü işleme eğitim dokümanı ile birlikte, görüntü işleme algoritmalarını öğrenecek, yeri geldiğinde ise **Java**, **Python** , **C++**, **MATLAB** ve **C# (EmguCV)** programlama dilleri kullanarak örnek uygulamalar geliştireceğiz. Bu eğitim, bilgisayarlı görünün temellerini anlayabilmenizi ve OpenCV ile bilgisayarlı görü uygulamaları geliştirebilmenizi amaçlamaktadır. Python, Java ve C++ örnekleri ile desteklenmektedir. Bu doküman, daha önce görüntü işleme ile uğraşmamış, bu konuda bilgisi olmayanlara ve tam aksine bu konuda bilgili, kendinisini farklı konularda geliştirmek  isteyen herkese hitap edecek şekilde hazırlanmıştır. Temel tanımlardan başlanarak birçok kavram ve algoritma ele alınmıştır. Örnek projelere **code** dizininden, eğitim konularına ise **docs** dizini altından ulaşabilirsiniz, **yararlı olması dileğiyle.**
<p align="center">

<img src="https://opencv.org/assets/theme/logo.png">
</p>

---

<p align="center">


 ★★★ Projeye destek olmak isterseniz; destek kısmına göz atabilirsiniz. Talep veya öneriniz varsa iletişime geçmekten çekinmeyin. İletişime geçmek için <a href="https://gitter.im/opencv-turkish-tutorial">Gitter</a> veya  <a href="https://github.com/mesutpiskin">profilimdeki</a> eposta adresini kullanabilirsiniz. Teşekkürler! ★★★
</p>

---

## İçerik

**Doküman**

| Bölüm |Özet|
|----------|:--------|
| [OpenCV Nedir?](/docs/1-opencv-nedir.md)|OpenCV'nin tarihi ve bileşenleri, alternatif görüntü işleme kütüphaneleri, neden OpenCV, OpenCV 2 vs OpenCV 3 ve OpenCV 4 ile gelecek yenilikler.|
| [Geliştirme Ortamlar](/docs/2-gelistirme-ortamlari.md) |Hangi platform ve geliştirme ortamı seçimilmei, görüntü işleme için neden Java ve Python.|
| [OpenCV Wrappers](/docs/3-opencv-wrappers.md) |Wrapper nedir? EmguCV, JavaCV, LiveCV, RubyCV ve wrapperlar arası farklar nelerdir.|
| [Kurulum ve Derleme](/docs/4-opencv-kurulumlar.md) |Windows, Linux, macOS ve Raspberry Pi için OpenCV kurulumu.|
| [IDE Yapılandırması](/docs/5-ide-yapilandirmasi.md) |Eclipse, Netbeans, Android Studio ve Intelij IDEA için yapılandırma ayarları.|
| [Giriş ve Temel Kavramlar](/docs/6-giris-temel-kavramlar.md) |Görüntü işleme kavramları. Dosyadan, kameradan, IP kameradan görüntü okuma. Kamera parametrelerini değiştirme.|
| [Video Kaydediciler ve Kod Çözücüler](/docs/7-video-kaydediciler-codec.md) |Codec, FourCC ve video kaydetme.|
| [Görüntü Manipülasyonu](/docs/8-goruntu-manipulasyonu.md) |Piksel manüpülasyonu, geometrik çizimler ve geometrik dönüşümler.|
| [Renk Uzayları](/docs/9-renk-uzaylari.md) |Temel renk uzayları ve renk uzayları arası dönüşüm.|
| [Morfolojik Görüntü işleme](/docs/10-morfolojik-goruntu-isleme.md) |Morfolojik operatörler ve eşikleme: Erosion, dilation, closing, gradyan, thresholding ...|
| [Filtreler ve Kenar Belirleme](/docs/11-filtreler-ve-kenar-belirleme.md) |Filtreleme ve kenar belirleme algoritmaları: Blur, Sobel, Laplace, Canny ...|
| [Arkaplan Çıkarma](/docs/12-arka-plan-cikarma.md) | Absdiff, MOG, MOG2 ve GMG algoritmaları kullanarak, 2D görüntü arkaplan çıkarımı.|
| [Video Analiz](/docs/13-video-analiz.md) |Mean Shift, Cam Shift, Optik akış vb. algoritmalar ile video üzerinde nesne tespit ve takibi. |



**Kaynak Kod**

<table style="width: 100%;">
<tbody>
<tr>
<td style="text-align: center;"><strong>&nbsp;Konu</strong></td>
<td style="text-align: center;"><strong>&nbsp;Python</strong></td>
<td style="text-align: center;"><strong>&nbsp;Java</strong></td>
<td style="text-align: center;"><strong>&nbsp;C++</strong></td>
<td style="text-align: center;"><strong>C#</strong></td>
<td style="text-align: center;"><strong>MATLAB</strong></td>
 
</tr>
<tr>
<td>Kamera I/O</td>
<td>
<ul>
<li><a href="/code/kamera-io/python/webcamden-oku.py">Kameradan Video Stream</a></li>
<li><a href="/code/kamera-io/python/ip-kameradan-oku.py">IP Kameradan Video Stream</a></li>
<li><a href="/code/kamera-io/python/video-dosyasi-oku.py">Video Dosyasından Stream</a></li>
<li><a href="/code/kamera-io/python/resim-oku.py">G&ouml;r&uuml;nt&uuml; Okuma</a></li>
<li><a href="/code/kamera-io/python/video-kaydet.py">Video Kaydetme</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
 <td>&nbsp;</td>
</tr>
<tr>
<td>G&ouml;r&uuml;nt&uuml; Manip&uuml;lasyonu</td>
<td>
<ul>
<li><a href="/code/goruntu-manipulasyonu/python/geometrik-sekiller.py">Geometrik Şekil &Ccedil;izme</a></li>
<li><a href="/code/goruntu-manipulasyonu/python/goruntu-kirpma.py">G&ouml;r&uuml;nt&uuml; Kırpma</a></li>
<li><a href="/code/goruntu-manipulasyonu/python/piksel-manupulasyonu.py">Piksel Manip&uuml;lasyonu</a></li>
<li><a href="/code/goruntu-manipulasyonu/python/yeniden-boyutlandirma.py">G&ouml;r&uuml;nt&uuml; Boyutlandırma</a></li>
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
<li><a href="/code/renk-uzaylari/python/renk-uzayi-donusumu.py">Renk Uzayı D&ouml;n&uuml;ş&uuml;m&uuml;</a></li>
</ul>
</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
<td>&nbsp;</td>
 <td>&nbsp;</td>
</tr>
<tr>
<td>Morfolojik G&ouml;r&uuml;nt&uuml; İşleme</td>
<td>
<ul>
<li><a href="/code/morfolojik-goruntu-isleme/python/acinim-opening.py">A&ccedil;ınım (Opening)</a></li>
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
<td>&nbsp;Kenar &Ccedil;ıkarma</td>
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
<td>Arka Plan &Ccedil;ıkarma</td>
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
<td>Video Analizi</td>
<td>
<ul>
<li><a href="/code/video-analiz/python/meanshift.py">MeanShift</a></li>
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

Öncelikle katkıda bulunmayı düşünmeniz gerçekten güzel haber. Öncelikli olarak aşağıdaki yapılacaklar kısmına göz atabilirsin. Projeye  üç farklı şekilde destek olabilirsiniz;

* **Dokümantasyon:** Burada yer almayan veya eski olduğunu düşündüğünüz bir konu varsa bize gönderebilirsiniz. Bunun için öncelikli olarak yer aldığı kategoriyi docs dizini altından bulun ve buradaki yer alan doküman içerisine ekleyin. Yeni bir konu hakkında birşeyler eklemek istiyorsanız uygun bir başlık ile docs dizini altına konuyu oluşturup gönderebilirsiniz.
* **Örnek Kod:** code dizininde ilgili konu başlıkları altında programlama diline göre gruplanmış klasörler yer almaktadır. Öncelikli olarak hangi konuda örnek proje ekleyeceğinizi belirleyin ve uygun bir dizin olup olmadığını kontrol edin. Uygun bir dizin bulamaz iseniz oluşturabilirsiniz. Konu başlığı altında hangi dilde örnek kod ekleyecekseniz o klasör altında projede kullandığınız harici materyal (görüntü, video, model dosyası vb.) ile birlikte ekleyip gönderin.
* **İmla:** Türkçemizi daha düzgün kullanmak adına doküman içerisinde gördüğünüz anlatım bozukluğu, imla yanlışı gibi hataları düzelterek gönderebilirsiniz.


## Yapılacaklar, Ekim 2018

- [ ] KNN, K En Yakın Komşu
- [ ] SVM, Destek Vektör Makinesi
- [x] CamShift, MeanShift
- [ ] Optik Akış
- [ ] Derin Öğrenme ile Yüz Tanıma
- [ ] Java ve C++ Örnekleri

## Lisans
Bu proje içerisinde yer alan doküman ve kaynak kodlar [MIT Lisansı](/LICENSE) ile lisanslanmıştır.
