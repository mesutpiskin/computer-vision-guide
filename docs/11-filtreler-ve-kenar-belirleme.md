**Filtreleme ve Kenar Belirleme Algoritmaları** 
-----------------------------------------------

### Teorik Temel

**Gaussian Filtresi:**
$$G(x,y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}$$
$\sigma$ (standart sapma) bulanıklık derecesini belirler. Büyük $\sigma$ → güçlü gürültü bastırma.

**Sobel Operatörü — Gradyan:**
$$G_x = \begin{bmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{bmatrix} * I, \quad G_y = \begin{bmatrix}-1&-2&-1\\0&0&0\\1&2&1\end{bmatrix} * I$$
$$|\nabla I| = \sqrt{G_x^2 + G_y^2}, \quad \theta = \arctan\left(\frac{G_y}{G_x}\right)$$

**Canny Kenar Belirleme (4 Aşama):**
1. Gaussian ile gürültü bastırma
2. Sobel ile gradyan büyüklük/yönü
3. Non-maximum suppression — gradyan yönünde yerel olmayan maksimumları sıfırla
4. Double thresholding: güçlü kenar $>T_h$, zayıf kenar $T_l < \cdot < T_h$

Referans: Canny, J. "A Computational Approach to Edge Detection", IEEE TPAMI 1986 (https://doi.org/10.1109/TPAMI.1986.4767851)

### Pratik Uygulama

```python
import cv2
import numpy as np

img = cv2.imread("resim.jpg")
if img is None:
    raise FileNotFoundError("resim.jpg bulunamadı")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Gaussian bulanıklaştırma
blurred = cv2.GaussianBlur(gray, (5, 5), sigmaX=1.4)

# Sobel gradyanları
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
magnitude = np.sqrt(sobelx**2 + sobely**2).astype(np.uint8)

# Laplacian
laplacian = cv2.Laplacian(gray, cv2.CV_64F)
laplacian_abs = np.uint8(np.absolute(laplacian))

# Canny — T_low=50, T_high=150 (2:3 oranı önerilir)
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

# Otomatik eşik (medyan tabanlı)
v = np.median(gray)
sigma = 0.33
lower = int(max(0, (1.0 - sigma) * v))
upper = int(min(255, (1.0 + sigma) * v))
auto_edges = cv2.Canny(gray, lower, upper)

cv2.imshow("Sobel Magnitude", magnitude)
cv2.imshow("Canny", edges)
cv2.imshow("Auto Canny", auto_edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Özet & İleri Okuma
- Gaussian filtresi σ parametresiyle bulanıklık derecesi ayarlanır
- Sobel birinci türev, Laplacian ikinci türev tabanlı kenar belirleyicilerdir
- Canny 4 aşamalı pipeline'ı ile en gürbüz kenar belirleyicidir
- T_low:T_high oranı yaklaşık 1:2 veya 1:3 olarak seçilmesi önerilir
- Medyan tabanlı otomatik eşik, farklı görüntülere adapte olur
- Referans: Canny 1986 — https://doi.org/10.1109/TPAMI.1986.4767851

---

Bu bölümde görüntü üzerindeki gürültüleri temizlemek, görüntü üzerindeki nesnelerin kenarlarını tespit etmek veya görüntüyü ön işlem ile analiz etmek için kullanılabilecek algroritmaların OpenCV kütüphanesi ile nasıl kullanılabileceğine bakacağız.

 ## Filtreleme

Filtre konusuna geçmeden önce öncelikli olarak gürültü kavramına bakmakta fayda var. Gürültü; hareket veya atmosferik kararsızlık nedeniyle meydana gelen bulanıklaşma veya resmi çekerken yanlış ışık etkisinden dolayı focus bulanıklaşması, kusursuz olmayan lenslerden kaynaklanan geometrik bozulma ve elektronik kaynaklardan gelen hatalar olarak verilebilir. Bu konuyu daha detaylı öğrenmek isterseniz olarak ele aldığım görüntü bozulmaları ve kamera kalibrasyonu konusuna bakabilirsiniz.

Filtreler genellikle ön işlem veya gürültü temizleme için kullanılırlar. Temel olarak görüntüyü bir fx fonksiyonuna sokararak filtre sabitini kullanır bu sayede görüntü üzerinde yer alan piksel değerlerinde bazı değişiklikler meydana gelir, sonuç olarak görüntü değişime uğrar. Instegram, mobil fotoğraf düzenleme uygulamaları veya profesyonel görüntü düzenleme programlarında filtrelere rastlamışsınızdır. Bundan önceki ilk iki konuda ele alınan örneklere dikkat ederseniz çıktı olarak oluşturulan görsellerde bazı piksellerin kaydığını, silik çıktığını veya tam olarak temizlenemediğini görürsünüz. Farklı görseller ile bu örnekleri yaptıysanız benzer sonuçlarla karşılaşmışsınızdır. Bunun nedeni kaynak olarak alınan görüntünün gürültülü olması veya ışık dengesinin bozuk olması gibi birçok durumdur. Bu sorunları aşmak için kaynak görüntüye öncelikle bir filtre uygulanır ve görüntünün işleme için en verimli hale getirilmesi sağlanır ve bu durum ön işleme olarak adlandırılır.

![Lena](static/lena.png)

**Blur**

Blur filtresi görüntüyü bulanıklaştırmak için kullanılır. Uygulamak için ise blur() metodu kullanılır. Bu metot parametre olarak kaynak görüntü mat nesnesi tipinde, mat tipinde bir sonuç ve Size tipinde uygulanacak olan bulanıklık değerini almaktadır.(çekirdek boyutu olarak da adlandırılır).

*Java:*

``` Java
Imgproc.blur(kaynakGoruntu, hedefGoruntu, new Size(50,50));
```

*Python:*
```Python
hedefGoruntu = cv2.blur(kaynakGoruntu,(50,50))
```

**GaussianBlur**

GaussianBlur filtresi görüntü üzerinde düzleştirme işlemi uygular. Uygulamak için GaussianBlur() metodu kullanılır. Bu metot parametre olarak kaynak görüntü mat nesnesi tipinde, mat tipinde bir sonuç ve Size tipinde uygulanacak olan bulanıklık değerini (çekirdek boyutu olarak da adlandırılır) ve SigmaX olarak adlandırılan çekirdek standart sapmasıdır almaktadır.

*Java:*

``` Java
Imgproc.GaussianBlur(kaynakGoruntu, hedefGoruntu, new Size(100,100),0);
```

*Python:*
```Python
hedefGoruntu = cv2.GaussianBlur(kaynakGoruntu,(100,100),0)
```

**Laplace**

Görüntü üzerinde nesnelerin sınır çizgilerini belirlemek için kullanılır. Piksellerin renk farklılıklarından yararlanır ve bu sayede nesnelerin sınır çizgileri tespit edilmiş olur. Uygulamak için Laplacian() metodu kullanılır. Bu metot parametre olarak kaynak görüntü mat nesnesi tipinde, mat tipinde bir sonuç ve int tipinde derinlik değeri almaktadır.

*Java:*

``` Java
Imgproc.Laplacian(kaynakGoruntu, hedefGoruntu,20);
```

*Python:*
```Python
hedefGoruntu = cv2.Laplacian(kaynakGoruntu,cv2.CV_64F)
```

**Sobel**

Görüntü üzerindeki kenarları elde etmek için kullanılır. Görüntü üzerindeki nesneleri kenarları belirleyerek ayrıştırmak istendiğinde bu filtreden yararlanılır.  Uygulamak için Sobel() metodu kullanılır. Bu metot parametre olarak kaynak görüntü mat nesnesi tipinde, mat tipinde bir sonuç, int olarak çıkış görüntü nesnesi için derinlik ve int tipinde türev olarak adlandırılan x, y değeri.

*Java:*

``` Java
Imgproc.Sobel(girisGoruntu, cikisGoruntu, ddepth, dx, dy);
```

*Python:*
```Python
cikisGoruntu = cv2.Sobel(girisGoruntu,cv2.CV_8U,1,0,ksize=5)
```


Diğer OpenCV içerisinde bulunan filtreleri ise aşağıda yer almaktadır.

* pyrMeanShiftFiltering()
* boxFilter()
* filter2D()
* Scharr()
* pyrUp()
* pyrDown()
* sepFilter2D()
* buildPyramid()

![Filtered](static/filtered.png)

 ## Kenar Belirleme

 Görüntü üzerinde kenar tespiti yapmak; o görüntüdeki nesneleri tespit etmek, saymak ve özelliklerini belirlemek amacıyla kullanılabilir. Kenar belirleme algoritmaları en temel anlatımıyla, görüntü üzerindeki piksellerin renk değerlerinin bir birlerinden farklılaşması ile belirlenir.


![Kenar](static/kenar-1.png)

 Yukarıdaki görsele baktığınızda farklılaşmanın nereden başladığını tahmin edebilir misiniz? Gördüğünüz üzere 4 ve 152 numaralı matris elemanları arasında keskin bir renk geçişi olmuş, bu renk geçişi (gürültü olmadığı taktirde) iki farklı nesnenin başlangıç ve bitiş çizgilerini ifade edebilir. İşte bu geçişler bizim için kenar çizgilerini ifade etmektedir. Örnek matrisimiz görüldüğü üzere gri (Gray) renk uzayına sahip bu renk uzayında matris elemanları yani pikseller 0-255 arasında renk değerlerine sahipti eğer görüntümüzü siyah-beyaz renk uzayına çevirir ve 0-1 aralığında renk kodları alması işimizi kolaylaştırmaz mı? İşte bu noktada kenar çıkarımı yapmadan Thresholding (Eşikleme) yapmamız işe yarayabilir. Bu uygulama şeklinde her algoritma kendisine has çıkarımlar yaparak tespit edebilir, bu yüzden görüntümüz de hangisinin daha iyi sonuç verdiğini deneyerek göreceğiz. Aşağıdaki görselde kenar çıkarma algoritması uygulanmış bir görüntü görmektesiniz. Bu görüntü üzerinde geçen kolileri saymak için ideal bir yöntem olabilir mi?

 ![Kenar](static/kenar-2.jpg)


 Kenar belirlemek için geliştirilmiş bir çok algoritma vardır ve bu algoritmaların neredeyse tamamına yakını OpenCV içerisinde mevcuttur.

Başlıca kenar belirleme algoritmaları:
* Canny
* Sobel
* Prewitt
* Lablacian
* Zero-Cross

Bu algoritmalar içerisinden Canny algoritması verdiği başarılı sonuçlar neticesinde en sık kullanılandır.

Canny:

*Java:*

``` Java
Imgproc.Canny(input_mat, detected_edges_mat, lowThreshold, maxThreshold, kernel_size );
```

input mat kenar tespiti yapacağımız matrisimiz, detected_edges_mat işlem sonucu kenarları tespit edilmiş mat nesnemiz, eşikleme yani thresholding yapacağımız için istediğimiz minimum değeri , maxThreshold ise eşikleme için kullanılmasını istediğimiz maksimum eşik değeri, kernel_size  parametresi ise çekirdek matrisi tanımlamaktadır bu rada önerilen matris değerlerini kullanabilir özel matris oluşturabilir istersek de boş bırakarak varsayılan çekirdek matrisin kullanılmasını sağlayabiliriz.

*Java:*

``` Java
 public static void main(String args[]) {
        String NATIVALIBRARYx64 = "res//lib//x64//opencv_java310";
        System.loadLibrary(NATIVALIBRARYx64);
        Mat imageInMat = Imgcodecs.imread("mevlana.jpg");
        Mat canny = new Mat();
        Imgproc.Canny(imageInMat, canny, 50, 150);
        Imgcodecs.imwrite("mevlana_canny.jpg", canny);
    }
```

*Python:*

``` Python
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('mevlana.jpg',0)
edges = cv2.Canny(img,50,150)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Orjinal'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Canny'), plt.xticks([]), plt.yticks([])

plt.show()
```

![Kenar](static/canny_edge.png)