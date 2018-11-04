OpenCV Nedir?
-------------



OpenCV (Open Source Computer Vision) açık kaynak kodlu görüntü işleme kütüphanesidir. 1999 yılında İntel tarafından geliştirilmeye başlanmış daha sonra Itseez, Willow, Nvidia, AMD,  Google gibi şirket ve toplulukların desteği ile gelişim süreci devam etmektedir. İlk sürüm olan OpenCV alfa 2000 yılında piyasaya çıkmıştır. İlk etapta C programlama dili ile geliştirilmeye başlanmış ve daha sonra birçok algoritması C++ dili ile geliştirilmiştir. Open source yani açık kaynak kodlu bir kütüphanedir ve BSD lisansı ile altında geliştirilmektedir. BSD lisansına sahip olması bu kütüphaneyi istediğiniz projede ücretsiz olarak kullanabileceğiniz anlamına gelmektedir.  OpenCV platform bağımsız bir kütüphanedir, bu sayede Windows, Linux, FreeBSD, Android, Mac OS ve iOS platformlarında çalışabilmektedir. C++, C, Python, Java, Matlab, EmguCV kütüphanesi aracılığıyla da Visual Basic Net, C# ve Visual C++ dilleri ile topluluklar tarafından geliştirilen farklı wrapperlar aracılığıyla Perl ve Ruby programlama dilleri ile kolaylıkla OpenCV uygulamaları geliştirilebilir.

Mayıs 2016 tarihinde, OpenCV geliştirici Itseez firması Intel tarafından satın alındı. OpenCV geliştirmesine Intel çatısı altından devam edeceğini duyurdu. Bugün itirabri ile de OpenCV 4.0 versiyonu release olmak üzere.

OpenCV kütüphanesi içerisinde görüntü işlemeye (image processing) ve makine öğrenmesine (machine learning) yönelik 2500’den fazla algoritma bulunmaktadır. Bu algoritmalar ile yüz tanıma, nesneleri ayırt etme, insan hareketlerini tespit edebilme, nesne sınıflandırma, plaka tanıma, üç boyutlu görüntü üzerinde işlem yapabilme, görüntü karşılaştırma, optik karakter tanımlama OCR (Optical Character Recognition) gibi işlemler rahatlıkla yapılabilmektedir.


![OpenCV Versiyon](http://mesutpiskin.com/blog/wp-content/uploads/2016/05/0-1.png "")


OpenCV logosu üçgen halinde O, C ve V harflerinin temsilidir. Logo, Açık Kaynak (Open Source) ve Bilgisayarlı Görü (Computer Vision) kelimelerini ifade eder. O, C, V harfleri, ünlü Kanizsa üçgen optik yanılsamasını anımsatır. harflerin renkleri ise RGB renk uzayını ifade eder .

![OpenCV Logo](https://opencv.org/assets/theme/logo.png "")

**OpenCV Bileşenleri**



OpenCV kütüphanesini daha iyi anlamak için mimarisinden ve OpenCV’yi oluşturan bileşenlerden bahsetmek istiyorum.

*   **Core:** OpenCV’nin temel fonksiyonları ve matris, point, size gibi veri yapılarını bulundurur. Ayrıca görüntü üzerine çizim yapabilmek için kullanılabilecek metotları ve XML işlemleri için gerekli bileşenleri barındırır.
*   **HighGui:** Resim görüntüleme, pencereleri yönetme ve grafiksel kullanıcı arabirimleri için gerekli olabilecek metotları barındırır. 3.0 öncesi sürümlerde dosya sistemi üzerinden resim dosyası okuma ve yazma işlemlerini yerine getiren metotları barındırmaktaydı.
*   **Imgproc:** Filtreleme operatörleri, kenar bulma, nesne belirleme, renk uzayı yönetimi, renk yönetimi ve eşikleme gibi neredeyse tüm fonksiyonları içine alan bir pakettir. 3 ve sonra sürümlerde bazı fonksiyonlar değişmiş olsada 2 ve 3 sürümünde de bir çok fonksiyon aynıdır.
*   **Imgcodecs:** Dosya sistemi üzerinden resim ve video okuma/yazma işlemlerini yerine getiren metotları barındırmaktadır.
*   **Videoio:** Kameralara ve video cihazlarına erişmek ve görüntü almak ve görüntü yazmak için gerekli metotları barındırır. OpenCV 3 sürümü öncesinde bu paketteki birçok metot video paketi içerisindeydi.

Tüm OpenCV modülleri için [http://docs.opencv.org/3.0-beta/modules/refman.html](http://docs.opencv.org/3.0-beta/modules/refman.html) adresine göz atabilirsiniz.

**Alternatif Görüntü İşleme Kütüphaneleri**



Görüntü işleme projelerinizde kullanacağınız kütüphaneyi amacınıza uygun olarak seçmeniz önemlidir. Bu seçimi yaparken ne yapmak istediğinize doğru karar vermelisiniz, örneğin sadece kameradan (usb, ip vs.) görüntü almak için projenize OpenCV entegre etmenize gerek olmayabilir. Bu gibi durumlar için ve OpenCV’nin neden iyi olduğunu anlayabilmek amacıyla alternatif olarak görüntü işleme kütüphanelerine de bakalım.

*   **MATLAB:** Matlab için bir görüntü işleme kütüphanesi olarak bahsetmek doğru değildir fakat içerisinde görüntü işlemeye yönelik temel algoritmaları barındırmaktadır.Dördüncü nesil ve çok amaçlı bir programlama dilidir. Akademik araştırmalarınızda, performansın önemli olmadığı durumlarda temel görüntü işlemleri için tercih edebilirsiniz.Matlab kullanarak OpenCV Kütüphanesi ile etkileşimli olarak da uygulamalarda geliştirmek mümkündür.
*   **Halcon:** Endüstriyel projeler için tercih edilen, kendi içerisinde geliştirme ortamının yanı sıra çeşitli programlama dilleri (C, C++, VS C++, C#, VB NET) için kütüphanesi bulunan, yapay görme (machine vision) odaklı ticari bir yazılımdır. İçerisinde birçok hazır fonksiyon bulundurur bu sayede hızlı uygulamalar geliştirilebilir. OpenCV açık kaynak kodlu, ücretsiz bir kütüphanedir ve computer vision odaklıdır.Bu yönleri ile Halcon’dan ayrılmaktadır.
*   **OpenFrameworks:** Açık kaynak olarak geliştirilen bu kütüphane C++ programlama dili için geliştirilen bu proje OS X, Linux, Embedded Linux (ARM), iOS, Android platformlarında çalışabilmektedir. OpenCV kütüphanesinin bir çok algoritmasını kullanır ve temel çıkış amacı kolay ve hızlı uygulama geliştirmektir. Örneğin OpenCV ile 2t sürede gerçekleştirdiğiniz bir işi 1t sürede gerçekleştirebilirsiniz, bunun temel sebebi ise bir çok fonksiyonu aracılığıyla standart hale getirilmiş olan işleri tek satır ile yapabilmesidir (Nesne tespiti,takibi renk belirleme, karşılaştırma vb.).
*   **CIMG:** Açık kaynak kodlu bir görüntü işleme kütüphanesidir. Windows, Linux ve OS X platformu üzerinde çalışmaktadır. Sadece C++ dili için desteği bulunmaktadır fakat yazılmış wrapperlar ile Java ve Python ile de uygulama geliştirilebilmektedir. Birçok algoritmayı barındırmaktadır fakat OpenCV kadar performanslı ve geniş bir algoritma altyapısına sahip değildir.
*   **Fiji:** Java platformu için geliştirilmiş açık kaynak kodlu GPL lisansına sahip bir görüntü işleme kütüphanesidir. Windows, Linux ve MAC OSX Intel 32-bit veya 64-bit üzerinde çalışır. Bilimsel görüntü analizi için geliştirilmiştir. Genetik, hücre biyolojisi, nöro-bilim gibi alanlar için özelleştirilmiş algoritmalara sahiptir.

Endrov, ImageJ, Lead tools, Pink, Image Magick, Boost ise görüntü işleme kütüphanelerinden bazılarıdır.  

**Neden OpenCV**

OpenCV görüntü işleme kütüphaneleri arasında en popüler ve en çok kullanılanıdır. 2016 verileri itibari ile OpenCV kütüphanesinin toplam indirme sayısı 7 milyonu geçmiştir. Yazılım geliştiriciler için bir kütüphanenin, teknolojinin popülerleşmesinin temel sebebi o teknoloji hakkındaki erişilebilecek kaynak çeşitliliğidir. OpenCV geniş bir kaynağa sahiptir, yapmak istediğiniz şeyle alakalı olarak size yardımcı olacak topluluklar ve bulabileceğiniz teknik dokumanlar oldukça fazladır. Bilişim sektöründe kullanım oranı fazla olan bütün programlama dillerine desteği bulunmaktadır, açık kaynak kodlu olması itibari ile de doğrudan desteği bulunmayan programlama dilleri için ara katmanlar yazılmış ve OpenCV bu dile entegre edilmiştir. Geniş işletim sistemi desteği bulunması itibariyle de geliştiriciler için, platformlar arası uygulama geçişini kolaylaştırmaktadır. Aktif olarak OpenCV kullanan bazı projelere göz atarsak neden en iyisi olduğunu daha iyi anlayabiliriz. Google tarafından cadde ve sokakları haritalamak amacıyla yürütülen street view projesi, NASA tarafından Marsa gönderilen keşif aracı (Curiosity) ile Mars yüzeyini görüntülemek, yorumlamak ve aracın bazı hareketlerini otonom olarak yapabilmek için OpenCV kullanılmıştır.

**OpenCV 2 ile OpenCV 3 Versiyonu Arasındaki Farklar**

Bu soru daha çok yeni başlayanlar veya projesinde hangi sürümü kullanmasına karar veremeyenler tarafından geliyor. Bu sürümleri kesin bir çizgiyle bir birinden ayırmamak gerekiyor, yani Python 2 ile Python 3 arasındaki ayrım gibi düşünülmemeli. Sürekli geliştirilen bir kütüphane ve yenilendikçe üzerine bir şeyler katıldıkça versiyonlama sisteminin doğası gereği major atlıyor. (Versiyonlama sistemlerinde x.x.x.x şeklinde giden numaralandırma Major, Minor, Build,Revision olarak adlandırılır.) Öğrenmek veya bir şeyler denemek için indiriyorsanız en güncel sürüm olan 3.1 i kullanmanızı öneririm veya iki sürümüde referans olarak ekleyip aynı projede kullanabilirsiniz bunun için bir engel bulunmuyor.

3.x sürümünde daha çok mobil (ios,android), Intel işlemciler ve ARM mimarisi (iOT kartlar, FPGI vb.) için iyileştirmeler yapıldı. Açık kaynak kod olması sebebiyle de bağımsız geliştiriciler tarafından bir çok yeni paket eklendi. Eski algoritmalar çıkartıldı ve yerlerine yenileri eklendi bu sebeple de paketlerde yeni bir düzenlemeye gidildi. Java geliştiricisi değilseniz paketlerdeki değişiklikler sizi çok ilgilendirmiyor olabilir :).

Eklenen bazı özellikler:

*   [Android] Android 5.x sürümleri için kamerada yaşanan sorunlar giderildi ve daha efektif kamera kullanımı sunuldu.
*   [Windows-MacOS] 3.1 sürümüyle Visual Studio 2015 ve Xcode7 desteği geldi.
*   [Intel] Intelin de desteğiyle Intel işlemcilerde performans artışı sağlayan Integrated Performance Primitives (Intel® IPP) entegre edildi. Bu sayede çekirdekler otomatik olarak optimize ediliyor.
*   [Intel] Intelin desteğiyle OpenCL tarafında iyileştirmeler yapıldı ve ek özellikler eklendi, bu sayede paralel komut işlemede performans artışı sağlandı.
*   [Genel] HAL (Hardware Acceleration Layer) yani donanım hızlandırma katmanı ek modül olarak sunuluyordu bu modül doğrudan OpenCV içerisine taşındı ve yeni aritmatik işlem fonksiyonları eklendi.
*   [Genel] ni-black thresholding algoritması eklendi.
*   [Genel] Fuzzy görüntü işleme modülü geliştirildi.
*   [Genel] Kernelized Correlation Filtresi ile gerçek zamanlı çok nesne izleme.
*   [Genel] RGBD Modülü geliştirildi.
*   [Genel] Matlab iyileştirmeleri yapıldı.
*   [Genel] CUDA için iyileştirmeler yapıldı.
yukarıdakiler sadece bazıları ve tabiki bir çok bug temizlendi. OpenCV belirli bir doygunluk seviyesine ulaşmıştı, bu sebeple performans iyileştirmeleri ve bug temizleme üzerine geliştirmeler yapılıyordu, paralel programlama ve derin öğrenmedeki gelişmeler ile birlikte 3.x sürümünde bu doğrultuda bir çok yeni modül ve algoritma entegre edildi.

**OpenCV 4 ile Bizi Neler Bekliyor**

OpenCV 4 versiyonu takviminin gerisinde kalmış olsada çok yakında release olacak. 4 versiyonu ile birlikte derin öğrenme ve GPU tarafında bir çok kolaylık ve yenilik olması bekleniyor. Bu versiyon release olduğunda bir çok sinir ağını OpenCV ile kolayca kullanabilmeyi ve daha hızlı sonuçlar alabilmeyi umuyoruz. Nvidia GPU ları için yürütülen parça bağımsız projelerde 4 ile birlikte OpenCV modülleri içerisindeki yerini alacak. Sürüm release olduğunda burayı tekrardan günceller ve gelen yeniliklere birlikte bakıyor oluruz.
