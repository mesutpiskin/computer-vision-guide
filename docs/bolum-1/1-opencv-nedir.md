OpenCV Nedir?
-------------



OpenCV (Open Source Computer Vision) açık kaynak kodlu görüntü işleme kütüphanesidir. 1999 yılında İntel tarafından geliştirilmeye başlanmış daha sonra Itseez, Willow, Nvidia, AMD,  Google gibi şirket ve toplulukların desteği ile gelişim süreci devam etmektedir. İlk sürüm olan OpenCV alfa 2000 yılında piyasaya çıkmıştır. İlk etapta C programlama dili ile geliştirilmeye başlanmış ve daha sonra birçok algoritması C++ dili ile geliştirilmiştir. Open source yani açık kaynak kodlu bir kütüphanedir ve BSD lisansı ile altında geliştirilmektedir. BSD lisansına sahip olması bu kütüphaneyi istediğiniz projede ücretsiz olarak kullanabileceğiniz anlamına gelmektedir.  OpenCV platform bağımsız bir kütüphanedir, bu sayede Windows, Linux, FreeBSD, Android, Mac OS ve iOS platformlarında çalışabilmektedir. C++, C, Python, Java, Matlab, EmguCV kütüphanesi aracılığıyla da Visual Basic Net, C# ve Visual C++ dilleri ile topluluklar tarafından geliştirilen farklı wrapperlar aracılığıyla Perl ve Ruby programlama dilleri ile kolaylıkla OpenCV uygulamaları geliştirilebilir.

Mayıs 2016 tarihinde, OpenCV geliştirici Itseez firması Intel tarafından satın alındı. OpenCV geliştirmesine Intel çatısı altından devam edeceğini duyurdu. Bugün itirabri ile de OpenCV 4.0 versiyonu release olmak üzere.

OpenCV kütüphanesi içerisinde görüntü işlemeye (image processing) ve makine öğrenmesine (machine learning) yönelik 2500’den fazla algoritma bulunmaktadır. Bu algoritmalar ile yüz tanıma, nesneleri ayırt etme, insan hareketlerini tespit edebilme, nesne sınıflandırma, plaka tanıma, üç boyutlu görüntü üzerinde işlem yapabilme, görüntü karşılaştırma, optik karakter tanımlama OCR (Optical Character Recognition) gibi işlemler rahatlıkla yapılabilmektedir.


![OpenCV Versiyon](http://mesutpiskin.com/blog/wp-content/uploads/2016/05/0-1.png "")

OpenCV Bileşenleri
------------------


OpenCV kütüphanesini daha iyi anlamak için mimarisinden ve OpenCV’yi oluşturan bileşenlerden bahsetmek istiyorum.

*   **Core:** OpenCV’nin temel fonksiyonları ve matris, point, size gibi veri yapılarını bulundurur. Ayrıca görüntü üzerine çizim yapabilmek için kullanılabilecek metotları ve XML işlemleri için gerekli bileşenleri barındırır.
*   **HighGui:** Resim görüntüleme, pencereleri yönetme ve grafiksel kullanıcı arabirimleri için gerekli olabilecek metotları barındırır. 3.0 öncesi sürümlerde dosya sistemi üzerinden resim dosyası okuma ve yazma işlemlerini yerine getiren metotları barındırmaktaydı.
*   **Imgproc:** Filtreleme operatörleri, kenar bulma, nesne belirleme, renk uzayı yönetimi, renk yönetimi ve eşikleme gibi neredeyse tüm fonksiyonları içine alan bir pakettir. 3 ve sonra sürümlerde bazı fonksiyonlar değişmiş olsada 2 ve 3 sürümünde de bir çok fonksiyon aynıdır.
*   **Imgcodecs:** Dosya sistemi üzerinden resim ve video okuma/yazma işlemlerini yerine getiren metotları barındırmaktadır.
*   **Videoio:** Kameralara ve video cihazlarına erişmek ve görüntü almak ve görüntü yazmak için gerekli metotları barındırır. OpenCV 3 sürümü öncesinde bu paketteki birçok metot video paketi içerisindeydi.

Tüm OpenCV modülleri için [http://docs.opencv.org/3.0-beta/modules/refman.html](http://docs.opencv.org/3.0-beta/modules/refman.html) adresine göz atabilirsiniz.

**Alternatif Görüntü İşleme Kütüphaneleri**
-------------------------------------------


Görüntü işleme projelerinizde kullanacağınız kütüphaneyi amacınıza uygun olarak seçmeniz önemlidir. Bu seçimi yaparken ne yapmak istediğinize doğru karar vermelisiniz, örneğin sadece kameradan (usb, ip vs.) görüntü almak için projenize OpenCV entegre etmenize gerek olmayabilir. Bu gibi durumlar için ve OpenCV’nin neden iyi olduğunu anlayabilmek amacıyla alternatif olarak görüntü işleme kütüphanelerine de bakalım.

*   **MATLAB:** Matlab için bir görüntü işleme kütüphanesi olarak bahsetmek doğru değildir fakat içerisinde görüntü işlemeye yönelik temel algoritmaları barındırmaktadır.Dördüncü nesil ve çok amaçlı bir programlama dilidir. Akademik araştırmalarınızda, performansın önemli olmadığı durumlarda temel görüntü işlemleri için tercih edebilirsiniz.Matlab kullanarak OpenCV Kütüphanesi ile etkileşimli olarak da uygulamalarda geliştirmek mümkündür.
*   **Halcon:** Endüstriyel projeler için tercih edilen, kendi içerisinde geliştirme ortamının yanı sıra çeşitli programlama dilleri (C, C++, VS C++, C#, VB NET) için kütüphanesi bulunan, yapay görme (machine vision) odaklı ticari bir yazılımdır. İçerisinde birçok hazır fonksiyon bulundurur bu sayede hızlı uygulamalar geliştirilebilir. OpenCV açık kaynak kodlu, ücretsiz bir kütüphanedir ve computer vision odaklıdır.Bu yönleri ile Halcon’dan ayrılmaktadır.
*   **OpenFrameworks: **Açık kaynak olarak geliştirilen bu kütüphane C++ programlama dili için geliştirilen bu proje OS X, Linux, Embedded Linux (ARM), iOS, Android platformlarında çalışabilmektedir. OpenCV kütüphanesinin bir çok algoritmasını kullanır ve temel çıkış amacı kolay ve hızlı uygulama geliştirmektir. Örneğin OpenCV ile 2t sürede gerçekleştirdiğiniz bir işi 1t sürede gerçekleştirebilirsiniz, bunun temel sebebi ise bir çok fonksiyonu aracılığıyla standart hale getirilmiş olan işleri tek satır ile yapabilmesidir (Nesne tespiti,takibi renk belirleme, karşılaştırma vb.).
*   **CIMG:** Açık kaynak kodlu bir görüntü işleme kütüphanesidir. Windows, Linux ve OS X platformu üzerinde çalışmaktadır. Sadece C++ dili için desteği bulunmaktadır fakat yazılmış wrapperlar ile Java ve Python ile de uygulama geliştirilebilmektedir. Birçok algoritmayı barındırmaktadır fakat OpenCV kadar performanslı ve geniş bir algoritma altyapısına sahip değildir.
*   **Fiji:** Java platformu için geliştirilmiş açık kaynak kodlu GPL lisansına sahip bir görüntü işleme kütüphanesidir. Windows, Linux ve MAC OSX Intel 32-bit veya 64-bit üzerinde çalışır. Bilimsel görüntü analizi için geliştirilmiştir. Genetik, hücre biyolojisi, nöro-bilim gibi alanlar için özelleştirilmiş algoritmalara sahiptir.

Endrov, ImageJ, Lead tools, Pink, Image Magick, Boost ise görüntü işleme kütüphanelerinden bazılarıdır.  
