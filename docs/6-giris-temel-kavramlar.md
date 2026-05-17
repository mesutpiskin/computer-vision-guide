

**Temel Kavramlar ve OpenCV'ye Giriş** 
--------------------------------------

Dijital görüntü işleme ile ilgili birçok kavrama aşina olabilirsiniz fakat bu kavramların çok iyi bir şekilde bilinmesi önem arz etmektedir. Bu nedenle bazı görüntü işleme kavramların ne olduğunu açıklamaya çalışacağım. Bu tanımlar ansiklopedik olarak değil, görüntü işlemede neyi ifade ettiklerine göre olacaktır.

Dijital Görüntü: Gerçek yaşamdaki analog bir verinin kamera gibi donanımlar kullanılarak dijital bir hale getirilmesiyle oluşmaktadır. Bu veri 1 ve 0 ile dijital olarak tanımlanıp, analog karşılığına denk gelmektedir. Dijital görüntü 2 boyutlu bir dizi yani satır ve sütun veya renk uzayına göre farklı boyutlara sahip matris olarak depolanabilmektedir.

Piksel: Dijital bir görüntünün satır ve sütun olarak barındırılabileceğini söylemiştik, bu dijital görüntüde satır ve sütunların kesiştiği noktalar piksel olarak atlandırılmaktadır yani her bir hücreye piksel denilmektedir. Bu durumda piksel dijital görüntüyü oluşturan en küçük birimdir.

![Piksel](static/temel-kavramlar.jpg)

Yukarıdaki görselde göründüğü üzere bir dijital görüntünün seçili bölgesinden kesit alınmış ve bu kesitin dijital olarak nasıl tutulduğu gösterilmiştir. Alınan kesit 8×8 boyutunda bir dizidir, bu dizinin her bir elamanının tuttuğu veri ise dijital görüntünün o pikselindeki renk bilgisine karşılık gelmektedir.

---

### Teorik Temel — Dijital Görüntü Matematiği

#### Dijital Görüntü Fonksiyonu

Matematiksel açıdan bir dijital görüntü, koordinat uzayından değer uzayına bir eşleme (fonksiyon) olarak tanımlanır:

$$f: \mathbb{Z}^2 \rightarrow \mathbb{Z}^k$$

Burada $(x, y)$ piksel koordinatını, $k$ ise kanal sayısını temsil eder. Sezgisel olarak: görüntü, her $(x, y)$ noktasına bir renk ya da yoğunluk değeri atayan bir ızgara fonksiyonudur.

| Görüntü Türü | Kanal Sayısı ($k$) | Örnek |
|---|---|---|
| Gri tonlamalı | $k = 1$ | Siyah-beyaz fotoğraf |
| RGB renkli | $k = 3$ | Standart dijital fotoğraf |
| RGBA (şeffaflıklı) | $k = 4$ | PNG saydamlık katmanı |

**Örnekleme (Sampling) ve Nicemleme (Quantization):**

Gerçek dünyadaki analog bir görüntü, dijitalleştirilirken iki temel adımdan geçer:

1. **Örnekleme:** Sürekli uzaydaki görüntü, ayrık (discrete) bir ızgaraya dönüştürülür. Bu ızgaranın yoğunluğu görüntünün çözünürlüğünü belirler (örneğin 1920×1080 piksel).
2. **Nicemleme:** Her pikselin yoğunluk değeri, sınırlı sayıda tam sayı seviyesine yuvarlanır.

**Bit Derinliği:**

Bit derinliği, her pikselin kaç farklı değer alabileceğini belirler:

- **8-bit:** $2^8 = 256$ seviye → değer aralığı $[0, 255]$ (en yaygın format)
- **16-bit:** $2^{16} = 65536$ seviye → değer aralığı $[0, 65535]$ (tıbbi ve bilimsel görüntüleme)
- **32-bit float:** Normalleştirilmiş aralık $[0.0, 1.0]$ (derin öğrenme modelleri)

> **Referans:** Gonzalez, R. C. & Woods, R. E. (2018). *Digital Image Processing* (4. baskı). Pearson. [imageprocessingplace.com](https://www.imageprocessingplace.com)

---

#### NumPy ile Görüntü Temsili

OpenCV, görüntüleri NumPy dizileri olarak temsil eder. Bir RGB görüntünün bellek düzeni şu şekildedir:

```
img.shape → (H, W, C)
           ↑   ↑   ↑
        Yükseklik  Genişlik  Kanal
```

**Önemli:** OpenCV varsayılan olarak **BGR** kanal sırası kullanır (RGB değil):

| Dizin | `img[:, :, 0]` | `img[:, :, 1]` | `img[:, :, 2]` |
|---|---|---|---|
| Kanal | Blue (Mavi) | Green (Yeşil) | Red (Kırmızı) |

Bu fark, görüntüleri matplotlib gibi RGB bekleyen kütüphanelere aktarırken dikkat edilmesi gereken kritik bir ayrıntıdır.

---

#### Konvolüsyon — Görüntü İşlemenin Matematiksel Temeli

Konvolüsyon, bulanıklaştırma, keskinleştirme ve kenar tespiti gibi pek çok görüntü işleme operasyonunun matematiksel temelidir. İki boyutlu ayrık konvolüsyon şu şekilde tanımlanır:

$$g(x,y) = f(x,y) * h(x,y) = \sum_{s}\sum_{t} f(s,t) \cdot h(x-s,\, y-t)$$

Değişkenlerin Türkçe açıklaması:
- $f(x, y)$: giriş görüntüsü — işlenmek istenen orijinal matris
- $h(x, y)$: çekirdek (kernel) — uygulanacak filtre maskesi (örneğin 3×3 Gaussian)
- $g(x, y)$: çıkış görüntüsü — filtrelenmiş sonuç
- $\sum_{s}\sum_{t}$: çekirdeğin tüm konumları üzerindeki toplam

**Sezgisel Açıklama:** Her çıkış pikseli $g(x, y)$, giriş görüntüsündeki komşu piksellerin çekirdek ağırlıklarına göre alınan ağırlıklı ortalamasıdır. Çekirdek büyüdükçe daha geniş bir komşuluk bölgesi dikkate alınır.

**Örnek Çekirdekler:**

- **Kimlik (Identity):** $h = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix}$ → görüntüyü değiştirmez
- **Ortalama Filtresi:** $h = \frac{1}{9}\begin{bmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{bmatrix}$ → bulanıklaştırır
- **Sobel (yatay kenar):** $h = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$ → dikey kenarları tespit eder

---

### Pratik Uygulama — Piksel Erişimi ve Görüntü Temsili

Aşağıdaki örnek, görüntünün matematiksel yapısını doğrudan NumPy dizisi üzerinde keşfeder ve gri tonlamaya dönüşüm formülünü gösterir:

```python
import cv2
import numpy as np

# Görüntü okuma ve temel bilgiler
img = cv2.imread("resim.jpg")
print(f"Shape: {img.shape}")        # (H, W, 3)
print(f"Dtype: {img.dtype}")        # uint8
print(f"Min/Max: {img.min()}/{img.max()}")

# Piksel erişimi
b, g, r = img[100, 200]            # (y=100, x=200) pikselinin BGR değerleri
print(f"B={b}, G={g}, R={r}")

# Gri tonlamaya dönüşüm: Y = 0.299R + 0.587G + 0.114B
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Görüntü istatistikleri
mean, std = cv2.meanStdDev(img)
print(f"Kanal ortalamaları (BGR): {mean.flatten()}")

# Kameradan görüntü okuma
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    cv2.imshow("Kamera", frame)
    cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
```

**Kod Notları:**
- `img.shape` → `(yükseklik, genişlik, kanal)` sırasını izler — matematikteki $(satır, sütun)$ konvansiyonuyla aynıdır
- `img.dtype` → genellikle `uint8` (8-bit işaretsiz tam sayı), değer aralığı $[0, 255]$
- Gri dönüşümde kullanılan $Y = 0.299R + 0.587G + 0.114B$ formülü ITU-R BT.601 standardından gelir; insan gözünün yeşile daha duyarlı olmasını yansıtır
- `cv2.meanStdDev()` her kanal için ortalama $\mu$ ve standart sapma $\sigma$ hesaplar

---

### Özet & İleri Okuma

- Dijital görüntü, $f(x,y)$ fonksiyonu olarak 2B/3B matris şeklinde temsil edilir
- 8-bit görüntüde her piksel $[0, 255]$ aralığında tam sayı değer taşır
- OpenCV **BGR** kanal sırası kullanır (RGB değil); matplotlib gibi araçlarla çalışırken dönüşüm gerekir
- NumPy shape → `(yükseklik, genişlik, kanal)` sırasını izler
- Konvolüsyon, görüntü işlemenin temel matematiksel operasyonudur; bulanıklaştırma, keskinleştirme ve kenar tespitinin hepsi konvolüsyon temeline dayanır
- `cv2.imread` varsayılan olarak BGR okur; `cv2.IMREAD_GRAYSCALE` bayrağı ile doğrudan gri ton yüklenebilir
- **Referans:** Gonzalez & Woods — *Digital Image Processing* → [imageprocessingplace.com](https://www.imageprocessingplace.com)

---

FPS (Frame Per Second): Saniyedeki çerçeve sayısı olarak tanımlanır. Video aygıtlarında ve grafik kartlarında ayırt edici bir kriterdir. Bu görüntüleme aygıtlarının bir saniyede ürettiği  görüntü sayısını ifade eder. Fps değeri ne kadar yüksek ise saniyede yakalanan görüntü sayısı artacak ve en küçük değişiklikler bile yakalanabilecektir. Görüntü işleme projelerinizde kullandığınız kameraların fps değerinin yüksek olması önemlidir. Şöyle örnekleyebiliriz: Bir fabrikada üretim bandından  saniyede 10 adet ürün üretilerek geçtiğini düşünelim, geliştirdiğimiz yazılım ise geçen bu ürünleri yakalayıp analiz edecek ve kalite kontrolü yapacak olsun. Seçtiğimiz kamera aygıtının fps değeri düşük olur ise geçen ilk 10 ürünü yakalasak bile ardından gelecek 10 ürünü kamera aygıtı kaçırabilir, çünkü üretim bandının hızı kamera aygıtının saniyede yakalayabildiği görüntü adetinden fazladır.

**Dosya Sisteminden Görüntü Okuma**

OpenCV ile dosya sisteminden görüntü dosyası okumak için Imgcodecs paketi içerisindeki imread metodu kullanılmaktadır. Bu konu öncesinde önemli bir sınıf olan Mat sınıfına göz atalım.

Mat tipi olarak da adlandırabileceğimiz bu sınıf, görüntü barındırma işlevine sahiptir. Okunan görüntü dosyaları OpenCV kütüphanesin de mat sınıfında tutulmaktadır. Alınan görüntü renk uzayına göre farklı boyutlarda olabilecek dizi haline getirilerek bu tip içerisinde tutulur.

Bir örnek yapalım ve dosya sisteminden görüntü okuyarak bunu mat tipi içerisinde tutalım.


*Java:*

```Java
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;
 
public class Giris {	
	public static void main(String[] args) {
		//sistem kütüphanesini yükleme
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
		//görüntüyü barındıracak nesne
		Mat imageArray;
		//görüntü dosyasını oku
		imageArray=Imgcodecs.imread("C:\\Users\\mesutpiskin\\resim.jpg");
		//mat nesnesinin satır ve sutun sayısı
		System.out.println(imageArray.rows());
		System.out.println(imageArray.cols());
	}
}
```

OpenCV kütüphanesini kullanmak için native kütüphaneyi yüklememiz gerekmekte, bunun için loadLibrary metotu ile bu işlemi yapıyoruz. Bir adet mat nesnesi tanımlıyoruz bu nesne ile okunacak olan görüntüyü üzerinde işlem yapmak için barındırabileceğiz. Imgcodecs.imread ile parametre olarak bulunduğu dosya adresi verilen resim.jpg resmini okuyoruz. Okunan bu resim dosyasını dijital olarak imageArray mat nesnesi tutmaktadır, artık bu nesne üzerinden o görüntüye ulaşabiliriz. Resim dosyası okunduğunda bu resmin eni ve boyu kadar mat nesnesi boyutlandırılır ve satır, sütün sayısını yazdırdığımızda resmin satır sütun sayısını elde edebiliriz, satır ve sütun çarpımı ise kaç adet piksele (hücreye) sahip olduğunu gösterecektir.


Yukarıdaki örneği OpenCV 3.x sürümü yerine OpenCV 2.x sürümü ile gerçekleştirecek olursak değişen tek şey imread metodunu çağırdığımız sınıf olacaktır. OpenCV 2.x sürümü görüntü okuma, yazma işlemleri Highgui ile yapılmaktaydı, 3.x sürümü ile birlikte bunlar Imgcodecs içerisine taşınmıştır.

```Java
import org.opencv.highgui.*;
...
imageArray=Highgui.imread("C:\\Users\\mesutpiskin\\resim.jpg");
...
```


*Python:*

imread() ile dosyadan okuduğumuz resmi imshow ile görüntüleyelim.

```python
import numpy as np
import cv2

img = cv2.imread('resim.jpg')
if img is None:
    raise FileNotFoundError("Görüntü dosyası bulunamadı: resim.jpg")

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

```


**Dosya Sisteminden Video Okuma**

Aynı yöntemle video dosyasını okumak  için aşağıdaki gibi bir örnek yapalım. Video okurken dikkat etmeniz gereken konu videonun codec’i dir.Aşağıdaki örnek gösterilen video dosyasındaki 100 frame i resim olarak dosya sistemine yazmaktadır.



``` Java
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.videoio.VideoCapture;

public class VideoDosyasiOkumaOrnegi{

	public static void main(String[] args){
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
		Mat frame = new Mat();
		VideoCapture videoCapture = new VideoCapture();
		// Video dosyasını aç
		videoCapture.open("C:\\Users\\mesutpiskin\\Documents\\videodosyasi.avi");
		int i = 0;
		// ağlantı açıldı ise
		if (videoCapture.isOpened()) {
			// Videodan 100 adet frame oku
			while (i < 100) {
				// Frame okunabildi ise
				if (videoCapture.read(frame)) {
					// Dosya sistemine yaz
					Imgcodecs.imwrite("C:\\Users\\mesutpiskin\\Desktop\\" + i + ".jpg", frame);
					System.out.println("İşlem tamamlandı." + i);
					i++;
				}

			}

		}
	}

}
```

*Python:*

```python
import cv2

# Video dosyasını aç
cap = cv2.VideoCapture("videodosyasi.avi")

while(True):
    # görüntü oku
    ret, frame = cap.read()
    if not ret:
        break

    # alınan görüntüyü göster
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# kamerayı kapat
cap.release()
cv2.destroyAllWindows()
```

**Video Kameradan Görüntü Okuma**

Usb kameradan, ip kameradan, video dosyasından veya bir video kaynağından kayıt almak için videoio paketi içerisindeki VideoCapture sınıfı kullanılmaktadır. Video Capture int tipinde kamera aygıtı numarası almaktadır. Vereceğiniz 0 parametres ise sistemde tanımlanan varsayılan kamera aygıtını ifade etmektedir. Yukarıdaki örneklere bu açıdan baktığımızda:

*Java:*

``` Java
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.videoio.VideoCapture;

public class Kamera {
	public static void main(String[] args) {
		// sistem kütüphanesini yükleme
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
		// görüntüyü barındıracak nesne
		Mat imageArray = new Mat();
		// video aygıtlarına erişim sağlar
		VideoCapture videoDevice = new VideoCapture();
		// varsayılan video aygıtını başlatır
		videoDevice.open(0);
		// video aygıtı bağlantısı yapıldı mı?
		if (videoDevice.isOpened()) {
		// video aygıtından bir kare oku ve mat nesnesine yerleştir
			videoDevice.read(imageArray);
			// alınan dijital görüntü bilgileri
			System.out.println(imageArray.toString());
			// video aygıtını setbest bırak
			videoDevice.release();
		} else {
			System.out.println("Video aygıtına bağlanılamadı.");
		}
	}
}
```

*Python:*

```python
import cv2

cap = cv2.VideoCapture(0)
#Kamera aygıtına bağlanılabildi mi?
while(cap.isOpened()):
#Görüntüyü oku ve görüntüle
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

VideoCapture sınıfından oluşturulan nesne, video aygıtını başlatmaktadır. Bu nesnenin open() metodu string ve int olarak parametre almaktadır. string olarak verilen parametre video dosyasının yolunu, örneğin C:\video.avi gibi veya yayın yapan bir ip kameranın adresini () alabilir.

int tipinde verilen parametreler ise örnekte de olduğu gibi sisteme takılı olan kameraların numaralarıdır. Parametre olarak 0 verildiğinde sistemdeki varsayılan video aygıtına bağlanır. Sistemdeki başka bir kameraya erişim sağlanılmak isteniyorsa int olarak 1, 2, 3 gibi numarası verilerek bağlanılabilinir. isOpen() metodu ile de bağlantı durumu kontrol edilebilir. VideoCapture sınıfından oluşturulan nesnenin read() metodu ile de aygıttan bir kayıt alınır ve mat nesnesi içerisinde barındırılır. Kamera bağlantısını kapatmak için ise release() metodu kullanılır, bu metot kullanılmaz ve video aygıtı bağlantısı kesilmez ile sürekli olarak bir görüntü akışı gerçekleştirilebilir. imageArray olarak adlandırılan mat nesnesinin toString() metodu ile satır, sütun veya adresi gibi temel bilgilerine erişilebilir. Video aygıtından alınan görüntü imageArray içerisine aktarılır ve bu nesneye ilişkin bilgiler ekranda gösterilir.


**IP Kameradan Görüntü Okuma**

IP kameralar sağladığı kullanım kolaylığı, sunucu üzerinde görüntü işlemek veya kamera sisteminin kurulduğu alan dışında görüntüleri yorumlamak amacıyla sıklıkla tercih edilirler. Bazı kamera aygıtları üzerinde kendi mikro işlemcisi olabilir ve görüntü aktarmaya ihityac duymadan burada işlenebilir. Bizim konumuz bu kameralar değil, yakaladığı görüntüyü üzerinde bulunan web sunucu aracılığıyla ağ üzerinde yayınlayabilen kameralar. Bu kameralar sabit ip adresi üzerinden yayın yaparlar. Benim kullandığım ip kamera 192.168.1.51 ip adresinden yayın yapıyor, bu adrese tarayıcı aracılığıyla bağlantığımızda 8080 veya sizin atadığınız varsayılanın dışında bir portt ile üzerindeki web sunucusuna erişiriz. Burada görüntü ayarları içerisinde format kısmını mjpg olarak değiştiriyoruz. Bir çok yüksek çözünürlüklü kamera farklı formatlarda yayın yapıyor ve bu formatları OpenCV aracılığıyla okumak zor olduğu için aygıtınız destekliyorsa mjpg yapmanızda fayda var. Kamera yayın için bir adres vercektir benim kameram adresinden yayın yapıyor. Bu kısımdan sonra bu görüntüyü dosya sisteminden okur gibi okuyabiliyoruz. Şimdi ip kameraya bağlanalım ve bir kare yakalayalım.

Bir IP kameranın yayın adresi nasıl bulunur?

İp kameranızın yayın adresini bulamıyorsanız bunun için iSpy yazılımını kullanabilirsiniz. iSpy açık kaynak ücretsiz bir yazılımdır. Bu yazılım ile bir çok kameranın yayın adreslerini bulabilir ve test edebilirsiniz, ayrıca buradaki https://www.ispyconnect.com/sources.aspx bağlantıdan da iSpy kamera bağlantı arşivine ulaşabilirsiniz. iSpy indirme bağlantısı: https://www.ispyconnect.com/download.aspx

*Java:*

``` Java
public static void main(String[] args) {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
		Mat imageArray = new Mat();
		VideoCapture videoDevice = new VideoCapture();
		// verilen adresteki yayını yakalar
		videoDevice.open("http://192.168.1.51/mjpg/stream.cgi");
                // Kullanıcı girişi gerektiren yayınlar için aşağıdaki gibi düzenlemeniz gerekmekte
		//videoDevice.open("http://<username:password>@<ip_address>/video.cgi?.mjpg")
		if (videoDevice.isOpened()) {
		// video aygıtından bir kare oku ve mat nesnesine yerleştir
			videoDevice.read(imageArray);
			videoDevice.release();
		} else {
			System.out.println("IP kamera aygıtına bağlanılamadı.");
		}
	}
```

*Python:*
```python
import cv2
cap = cv2.VideoCapture('http://admin:admin@192.168.1.51/cgi/stream.mjpg')

while True:
  ret, frame = cap.read()
  if not ret:
    break
  cv2.imshow('Video', frame)

  if cv2.waitKey(1) == 27:
    break

cap.release()
cv2.destroyAllWindows()
```

VideoCapture sınıfında bulunan set() metodu ile video aygıtları için bazı ayarları yapılandırabiliriz. int tipinde id ve paramtere değerini alır. get() metodu ile de değerleri görebilirsiniz. propId olarak tanımlanan int tipinde verilecek atanacak olan özelliğin id değeridir. Doğrudan int tipinde id değeri verilebileceği gibi 3.x öncesi sürümlerde Highgui 3.x sürümlerde ise Videoio içerisindeki int değişkenleride doğrudan kullanabilirsiniz. VideoCapture sınıfında kullanılabilecek bazı parametrelere göz atalım.

- **cv2.CAP_PROP_POS_MSEC:** Video dosyasından okuma yaparken mili saniye cinsinden o anki video zamanını yönetir.

- **cv2.CAP_PROP_FRAME_WIDTH:** Okunan görüntünün genişliğini yönetir. Görüntü genişliği değiştirilebilir yada okunan görüntünün genişliği öğrenilebilir.

- **cv2.CAP_PROP_FRAME_HEIGHT:** Okunan görüntünün yüksekliğini yönetir. Görüntü yüksekliği değiştirilebilir yada okunan görüntünün yüksekliği öğrenilebilir.

- **cv2.CAP_PROP_FPS:** Görüntünün saniyedeki kare hızını ifade eden FPS değeri değiştirilebilir.

- **cv2.CAP_PROP_FOURCC:** Codec değiştirilebilir. Kodek dört karakterlik kod ile ifade edilir.

- **cv2.CAP_PROP_FRAME_COUNT:** Görüntünün çerçeve (frame) sayısına erişilebilir.

- **cv2.CAP_PROP_FORMAT:** Mat nesnesinin formatı değiştirilebilir.

- **cv2.CAP_PROP_BRIGHTNESS:** Görüntünün parlaklık değeri değiştirilebilir. Bu parametre sadece kamera aygıtları için geçerlidir.

- **cv2.CAP_PROP_CONTRAST:** Görüntünün kontrast değeri değiştirilebilir. Bu parametre sadece kamera aygıtları için geçerlidir.

- **cv2.CAP_PROP_SATURATION:** Görüntünün doygunluk değeri değiştirilebilir. Bu parametre sadece kamera aygıtları için geçerlidir.

- **cv2.CAP_PROP_HUE:** Görüntünün renk tonu değiştirilebilir. Bu parametre sadece kamera aygıtları için geçerlidir.

- **cv2.CAP_PROP_CONVERT_RGB:** Görüntünün RGB renk uzayına dönüştürülmesi gerekiyor ise kullanılır.

- **cv2.CAP_PROP_WHITE_BALANCE_BLUE_U:** Görüntünün beyaz dengesi değiştirilebilir.

- **cv2.CAP_PROP_ISO_SPEED:** Kameranın ISO hızı değiştirilebilir. Tüm aygıtlar için desteklenmemektedir.

- **cv2.CAP_PROP_BUFFERSIZE:** Ara belleğe alınacak olan çerçeve (frame) miktarı değiştirilebilir. Bellek taşmaları için dikkatli olunmalıdır.

