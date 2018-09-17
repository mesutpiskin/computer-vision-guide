**Video Kaydediciler ve Codec** 
-------------------------------

OpenCV ile video oluşturmak yani eldeki görüntü dizilerini kaydetmek için VideoWriter sınıfı kullanılmaktadır.  Kullanımına geçmeden önce bazı kavramlara bakmakta fayda var bu kavramlar codec yani kod çözücü ve FourCC (Four character code).

Codec (Kod Çözücü):

Ham ses ve görüntü dosyalarının boyutu oldukça büyüktür, bu sorunu çözmeni yolu ise bu verileri sıkıştırmaktır. Görüntü ve ses dosyalarını sıkıştırmak için bir çok farklı algoritma geliştirilmiştir, bu algoritmalar sıkıştırmak için  farklı yöntemler kullanmışlardır. Sıkıştırılan veriyi açmak için ise bu sıkıştırma algoritmasını anlayacak ve veriyi gösterecek bir çözücüye ihtiyaç duyulmaktadır, işte bu çözücüler codec olarak adlandırılmaktadır. Sık kullanılan sizinde aşina olduğunuzu düşündüğüm bazı codec’ler şunlardır; H261, MJPEG, MPEG vb.

FourCC:

“Four character code” yani  dört karakter kodu olarak adlandırılır.  FourCC nin amacı medya verilerindeki codec’leri dört karakter ile tanımlamaktır, yani standart bir tanımlama formatı oluşturmaktır.  FourCC kodunu tanımlarken  ASCI tablosunda olmayan bir karakter kullanılamaz. En çok bilinenleri DIVX, XVID, H264 vb. güncel listeye buradan bakabilirsiniz. Codec’leri indirmek için ise bu bağlantıyı kullanabilirsiniz.

FourCC formatı aşağıdaki gibidir,

__ – __ – __ – __

8   –  8   –   8   –   8      = 4byte – 32bit

OpenCV içerisinde codec tanımlamak veya kullanmak için FourCC kullanacağız.

 
VideoWriter

Videoyu yazmak için 5 adet parametreye ihtiyacı vardır, bu parametreler; videonun kaydedileceği dizin, codec,  frame boyutu (genişlik, yükseklik), fps değeri ve videonun renkli mi yoksa siyah beyaz mı kayıt edileceğini belirten boolean bir bayrak değişken.



*Java:*

```Java
VideoWriter videoWriter;
videoWriter = new VideoWriter(outputFile, VideoWriter.fourcc('X', 'V','I','D'),
                fps, frameSize, isRGB);
//fourcc ile codec olarak x264 kullanacağımızı belirttik
//Yazma işlemi için ise aşağıdaki metodu ekledik bu sayede parametre olarak verdiğimiz görüntüyü yazacak
 public void Write(Mat frame) {
        if(videoWriter.isOpened()==false){
            videoWriter.release();
            throw new IllegalArgumentException("Video Writer Exception: VideoWriter açılamadı,"
                    + "parametreleri kontrol edin.");        
        }
        //Yaz
        videoWriter.write(frame);
    }

//Örnek için VideoCapture ile kameradan görüntü okuyalım ve aynı videoyu yazalım

VideoCapture videoCapture = new VideoCapture(0);
Size frameSize = new Size((int) videoCapture.get(Videoio.CAP_PROP_FRAME_WIDTH), (int) videoCapture.get(Videoio.CAP_PROP_FRAME_HEIGHT));
VideoWriter videoWriter = new VideoWriter("test.avi", VideoWriter.fourcc('X', 'V','I','D'),
                videoCapture.get(Videoio.CAP_PROP_FPS), frameSize, true);
while (videoCapture.read(mat)) {
            videoWriter.write(mat);         
        }
        videoCapture.release();
        videoWriter.release();
```


*Python:*

```Python
import cv2

cap = cv2.VideoCapture(0)

# VideoWriter nesnesini oluştur
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('kayit.avi',fourcc, 10.0, (1024,768))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        # geçerli frame'i yaz
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

```


Bu işlem sonucunda muhtemel karşılaşacağınız sorunlardan bir tanesi yazılan video’nun açılmaması veya yazma işleminin başarısız olmasıdır. Bu sorunun nedeni muhtemelen sisteminizde codec paketinin eksik olmasından kaynaklanmaktadır, çözümü için https://ffmpeg.org/download.html  bağlantıdan ffmpeg indirebilir ve http://www.wikihow.com/Install-FFmpeg-on-Windows bağlantıdan nasıl kurulduğuna göz atabilirsiniz.

