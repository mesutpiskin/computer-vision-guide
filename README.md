[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](#)
# Görüntü İşleme ve Bilgisayarlı Görü


OpenCV ile bilgisayarlı görü ve görüntü işleme eğitim dokümanı ile birlikte, görüntü işleme algoritmalarını öğrenecek, yeri geldiğinde ise **Java**, **Python** ve **Csharp** programlama dilleri kullanarak örnek uygulamalar geliştireceğiz. Bu doküman, daha önce görüntü işleme ile uğraşmamış, bu konuda bilgisi olmayanlara ve tam aksine bu konuda bilgili, kendinisini farklı konularda geliştirmek  isteyen herkese hitap edecek şekilde hazırlanmıştır. Temel tanımlardan başlanarak birçok kavram ve algoritma ele alınmıştır. Örnek projelere **code** dizini altından ulaşabileceğiniz gibi, ilgi konu içerisindenden de ulaşabilirsiniz, **yararlı olması dileğiyle.**

---

<p align="center">
 ★★★ Dokumantasyonu beğendiyseniz ve destek olmak isterseniz; anlatım bozuklukları, kod değişikliği veya yeni bir örnek göndermekten çekinmeyin. Buradaki dokümantasyonun orijinaline <a href="http://mesutpiskin.com/blog">bu adresten</a> ulaşabilirsiniz. İletişime geçmek isterseniz  <a href="https://github.com/mesutpiskin">profilimdeki</a> eposta adresini kullanabilirsiniz. Teşekkürler! ★★★
</p>

## İçerik

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
| [ ](/docs/12-.md) | |
| [ ](/docs/12-.md) | |



## Nasıl Katkı Sağlanır

Öncelikle katkıda bulunmayı düşünmeniz gerçekten güzel haber. Üç farklı şekilde destek olabilirsiniz;

*  **Dokümantasyon:** Burada yer almayan veya eski olduğunu düşündüğünüz bir konu varsa bize gönderebilirsiniz. Bunun için öncelikli olarak yer aldığı kategoriyi docs dizini altından bulun ve buradaki yer alan doküman içerisine ekleyin. Yeni bir konu hakkında birşeyler eklemek istiyorsanız uygun bir başlık ile docs dizini altına konuyu oluşturup gönderebilirsiniz.
* **Örnek Kod:** code dizininde ilgili konu başlıkları altında programlama diline göre gruplanmış klasörler yer almaktadır. Öncelikli olarak hangi konuda örnek proje ekleyeceğinizi belirleyin ve uygun bir dizin olup olmadığını kontrol edin. Uygun bir dizin bulamaz iseniz oluşturabilirsiniz. Konu başlığı altında hangi dilde örnek kod ekleyecekseniz o klasör altında projede kullandığınız harici materyal (görüntü, video, model dosyası vb.) ile birlikte ekleyip gönderin.
* **İmla:** Türkçemizi daha düzgün kullanmak adına doküman içerisinde gördüğünüz anlatım bozukluğu, imla yanlışı gibi hataları düzelterek gönderebilirsiniz.


## Eklenmesi Planlananlar , Ekim 2018

- [ ] KNN, K En Yakın Komşu
- [ ] SVM, Destek Vektör Makinesi
- [ ] SURF
- [ ] SIFT
- [x] CamShift, MeanShift
- [ ] Optik Akış
- [ ] Derin Öğrenme ile Yüz Tanıma