
**Video Analiz ve Nesne Takibi** 
--------------------------------

Video analizi oldukça dağılmış bir konudur fakat temel anlamıyla video üzerindeki nesneleri ve hareket eden objeleri tespit ederek bunları takip etmeyi kapsar. Bu kapsamda bu bölümde video üzerinde hareket eden objeleri yakalamayı ve bunları takip etmeyi ele alacağız. Arkaplan çıkarma algoritmaları da bu kapsamda ele alınabilir, diğer geliştirilmiş başlıca algoritmalara göz atmak gerekirse:

* Mean Shift
* Camshift
* Optik Akış

OpenCV Object Tracker altında yer alan bazı algoritmalar ise:

* GOTURN
* BOOSTING
* MIL
* KCF
* CSRT
* TLD
* MOSSE

**Ağırlıklı Ortalama Öteleme Algoritması (Mean Shift)**

Mean Shift farklı maalesef bir çok farklı şekilde Türkçeye çevriliyor, farklı akademik kaynaklara baktığımda “Ortalama Kaydırma”, “ Ağırlıklı Ortalama Kaydırma”vb. gibi bir çok farklı çevirisi var. TÜBA terimler sözlüğüne bakarak bende kendimce mantıklı olduğunu düşündüğüm “Ağırlıklı Ortalama Öteleme Algoritması” başlığını atmaya karar verdim.

Bu yazıda ele alacağımız konu hareketli bir nesnenin nasıl nakip edilebileceği olacak. Hareketli nesneleri takip etmek bilgisayarlı görü alanında çok sık karşılaşılan bir problemdir. Örneğin, kamera alanı içerisine giren bir canlı, bir alan içerisinde odaklanılması istenilen hedef, hareketinin analizine ihtiyaç duyulan bir nesne çok sıklıkla karşılaşılan örneklerindendir. Mean Shift algoritmasını kullanarak hareket halindeki bir “nesneyi” nasıl takip edebileceğimize bakmadan önce bu algoritmanın nasıl çalıştığına bir göz atalım.

Mean Shift Algoritması Nedir? Nasıl Çalışır?


Sanılanın aksine Mean Shift algoritması oldukça “eski”. Bu algoritmanın temelleri 1975 yılına kadar dayanıyor, fakat bu tarihde matematiksel olarak ifade edilsede kendisine bir yer bulamadı. Ta ki Dorin Comaniciu tarafından pratik olarak bir alanda kullanılıncaya dek.  İlgili makalesine buradan ulaşabilirsiniz http://www.comaniciu.net/Papers/MsRobustApproach.pdf.

Algoritmadaki mantık oldukça basitti, veri kümesi üzerindeki veri (bazı kaynaklarda nokta olarak geçer) dağılımının en yüksek olduğu yeri bulmayı sağlar. Yani elinizdeki bir görüntü ve devam edecek görüntü üzerinde (next frame) belirlenen bir alan içerisinde yer alan tepe noktaları belirlemesi sürecidir. Belirlenen tepe noktalar takip edilmek istenilen nesne olacaktır. Oldukça basit, hızlı ve işlevsel bir yöntemdir. Aşağıdaki görsellere bakalım, bu görsellerde görüntü üzerindeki nesneyi ve bu nesnenin piksellerinin kümelenmesini inceleyim.


![MeanShift](static/meanshift.png)

Yukarıdaki görselde yer aldığı gibi bazı noktaların kümelenişini görebilirsiniz. Algoritmanın yaptığıda bu tepe noktalardaki kümelenmeleri her görüntü üzerinde yeniden hesaplayarak, değişen görüntü üzerinde istenilen nokta kümelerinin bulunmasıdır. Mean Shift algoritmasını zora sokan durumlardan birisi parlaklık yani görüntüye düşen ışık üzerindeki değişikliklerdir. Eğer ışık dengesi çok fazla değişiyorsa farklı ön işlemlere tutarak bu durumu elimine etmek gerekebilir. Tam da bu konuda oldukça faydası olan histogram eşitleme konusuna göz atmakta fayda var. Histogram eşitleme üzerine de bir yazı yazacağım fakat o zaman kadar buradaki bağlantıyı kullanarak bu konuya göz atabilirsiniz. http://www.yildiz.edu.tr/~bayram/sgi/saygi.htm


Mean Shift algoritmasının iplementasyonlarını OpenCV 2.3 sürümünde gördüğümü hatırlıyorum fakat kesin olarak hangi sürüm ile birlikte geldiğine dair detaylı bir araştırma yapmak gerek. Neyseki çokta önemli değil en popüler dağıtımların hepsi bunu destekliyor. Örnek uygulamada OpenCV 3.4 kullanacağım.

Senaryomuz oldukça basit olacak, örnek videoda bir SU27 yer alıyor (bilmeyenler için bu bir savaş jeti) amacımız SU27’yi (evet SU27’yi seviyorum 🙂 ) kesintisiz olarak takip edebilmek. Sizden gelen talepler üzerine Python örneği ekleyeceğim, fakat talebiniz olursa Java, Android vs. olarak da ekleyebilirim.


*Python:*
```Python
videoCapture = cv2.VideoCapture("video.mp4")

ret, frame = videoCapture.read()
rows, cols = frame.shape[:2]

w = 100
h = 150
col = int((cols - w) / 2)
row = int((rows - h) / 2)

shiftWindow = (col, row, w, h)
```

Yukarıda; Öncelikli olarak video capture ile örnek video dosyası yüklenir. Video dosyası üzerine Mean Shift için bir alan belirlenir. Bu alan 100×150 olarak belirlenmiş ve ağırlıklı ortalaması belirlenecek olan dörtgen alanıdır. Bu alanın boyutlarıyla oynayın, eğer ki algoritma nesnenizi tam olarak takip edemiyorsa belirlediğiniz dörtgen alan da problem olabilir. shiftWindow nesnesi artık bu alanı tanımlamaktadır.

```Python
lowLimit = np.array((0., 60., 32.))
highLimit = np.array((180., 255., 255.))

mask = cv2.inRange(roiHsv, lowLimit, highLimit)

roiHist = cv2.calcHist([roiHsv], [0], mask, [180], [0, 180])
cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
```

Şimdi görüntü üzerindeki parlaklığı, renk dağılımlarını dengelemek için bir maskeleme alanı oluşturalım ve bu alan üzerinde histogram eşitleme yapalım. Algoritmanın doğru ağırlıkları hesaplayabilmesi için bu önemli bir noktadır.

```Python
terminationCriteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS , 15, 1)
```

Daha öncede sürekli yineleyen algoritmalar için gerekli bir parametre olan durdurma ölçütümüzü belirleyelim. Bu parametre algoritmanın kendi içerisinde kaydırma/hesaplama işlemini kaç defa yapacağını belirlemektedir. bu parametre değeri (15 olarak belirlediğim) size kalmıştır, bu parametre ile oynayın.

```Python
retVal , frame = videoCapture.read()
frameHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

backprojectedFrame = cv2.calcBackProject([frameHsv], [0], roiHist, [0, 180], 1)
```

Artık yukarıda da görebileceğiniz gibi video içerisinde öncelikli  HSV  renk uzayı üzerinde histogram alıp histogram back projection yapacağız ve tüm görüntü üzerinde istediğimiz yerin segmentlerini bulacağız.

```Python
mask = cv2.inRange(frameHsv, lowLimit, highLimit)
```

Algoritmanın sonucunu iyileştirmek için karanlık alanları maskeliyoruz.

```Python
ret, shiftWindow = cv2.meanShift(backprojectedFrame, shiftWindow, terminationCriteria)

col, row = shiftWindow[:2]
frame = cv2.rectangle(frame, (col, row), (col + w, row + h), 255, 2)
```
Daha önce belirlediğimiz dörtgen alanı kullanarak mean shift algoritmasını yine belirlediğimiz kriter ile başlatıyoruz, ve belirlediği alanı frame üzerine çiziyoruz.

Video:

[![Youtube Video](http://img.youtube.com/vi/9qzaBzmmL7s/0.jpg)](https://youtu.be/9qzaBzmmL7s)


**Camshift (Sürekli Mean Shift) Algoritması**

Eğer, MeanShift algoritmasının örnek projesini çalıştırdıysanız veya yukarıdaki videoyu izlediyseniz bir şeyi fark etmiş olabilirsiniz; sabit boyuttaki nesne alanı. Detaylandırmak gerekirse; MeanShift algoritması sürekli olarak , başlangıçta verdiğimiz boyutlarda bir kaydırma penceresi kullanır, bu durum takip edilmek istenilen alanın boyutunun sürekli olarak aynı kalmasına sebep olur çünkü MeanShift algoritmamız bir defa "initialize" edilmiş ve aynı pencereyi kullanarak çalışmaya devam etmiştir.

Bu sorun üzerine Gary Bradski (Learning OpenCV Kitabının Yazarı, Bilgisayar Bilimci) MeanShift algoritmasını her frame üzerinde sürekli olarak çalıştırarak, belirlenen kaydırma penceresini yeniden hesaplayarak boyutlandırmayı amaçlamış ve bunu başarmıştır. Yeni algoritma CamShift "Sürekli Uyarlanabilir Meanshift" algoritması olarak adlandırılmıştır.

Bu algoritmanın kullanımı, yukarıda anlatılan ve örnek projeler kısmında da bulabileceğiniz MeanShift algoritması ile benzer şekildedir.

```Python
   ret, shiftWindow = cv.CamShift(backprojectedFrame, shiftWindow, terminationCriteria)
 ```

**GOTURN Tracker Algoritması**

GOTURN derin öğrenme tabanlı CNN kullanan bir nesne takip algoritmasıdır. Bu algoritma "Learning to Track at 100 FPS with Deep
Regression Networks" http://davheld.github.io/GOTURN/GOTURN.pdf makalesi ile duyrulmuştur. Bu algoritma ile art arda gelen bir dizi frame yani video üzerinde tek bir nesnenin takibi yapılabilir. Yolda giden bir araç, yürüyen bir insan veya yuvarlanan bir top kısacası videonun başında takip edilmesini istediğiniz şeyi videonun sonuna kadar takip edilebilir. Bu algoritma eğitilmiş bir model ile kullanılır, opencv iplemantasyonu için eğitilmiş bir caffe modeli mevcuttur.


| ![GOTURN NESNE TAKİP ALGORİTMASI](static/goturn.png) | 
|:--:| 
|*Görsel Kaynağı: "Learning to Track at 100 FPS with Deep Regression Networks"* Makalesi Sayfa 2|
**BOOSTING Tracker Algoritması**

**MIL Tracker Algoritması**

**KCF Tracker Algoritması**

**CSRT Tracker Algoritması**

**TLD Tracker Algoritması**

**MOSSE Tracker Algoritması**

