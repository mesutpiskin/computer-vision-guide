**Platform ve Geliştirme Ortamı Seçimi**
----------------------------------------

OpenCV platform bağımsız bir kütüphanedir; Windows, Linux ve macOS üzerinde sorunsuz çalışır. Bu bölümde 2024 itibarıyla önerilen geliştirme ortamlarını ve dil tercihlerini ele alacağız.

## Programlama Dili Seçimi

### Python (Önerilen)

Bilgisayarlı görü ve görüntü işleme projelerinde Python günümüzde açık ara en yaygın tercih haline gelmiştir. Bunun başlıca nedenleri:

* **Ekosistem zenginliği:** NumPy, SciPy, scikit-learn, PyTorch, TensorFlow, Keras, Ultralytics, MediaPipe gibi kütüphanelerin tamamı Python için birinci sınıf destek sunmaktadır.
* **Hızlı prototipleme:** Jupyter Notebook veya Google Colab üzerinde satır satır deneme yapabilir, sonuçları görsel olarak inceleyebilirsiniz.
* **OpenCV dokümantasyonu:** OpenCV'nin resmi dokümantasyon örneklerinin büyük çoğunluğu Python ile yazılmaktadır.
* **Topluluk:** Stack Overflow, GitHub Issues ve Hugging Face üzerindeki örneklerin büyük çoğunluğu Python tabanlıdır.

Performans kritik prodüksiyon uygulamaları için Python'dan C++ veya ONNX/TFLite runtime'larına geçiş yaygın bir pratiktir. Ancak geliştirme ve araştırma için Python tercih edilmelidir.

### C++ (İleri Düzey / Prodüksiyon)

C++, OpenCV'nin ana dilidir. Gömülü sistemler, gerçek zamanlı video işleme ve düşük gecikme gerektiren uygulamalar için tercih edilir. Başlangıç için önerilmez.

### Java / Android

Android mobil uygulamaları geliştirmek isteyenler için Java veya Kotlin ile OpenCV kullanımı uygundur. Masaüstü Java uygulamaları için ise günümüzde neredeyse tercih edilmemektedir.

---

## Önerilen Geliştirme Ortamları

### 1. Visual Studio Code + Python (En Yaygın Tercih)

VS Code, hızlı, ücretsiz ve açık kaynak bir editördür. Python geliştirme için şu eklentileri kurmanız önerilir:

* **Python** (Microsoft)
* **Pylance** (tip kontrolü ve otomatik tamamlama)
* **Jupyter** (notebook desteği)

**Kurulum adımları:**

```bash
# 1. Python 3.10+ kurulu olduğunu doğrula
python --version

# 2. Sanal ortam oluştur
python -m venv cv-env

# 3. Sanal ortamı aktive et
# macOS/Linux:
source cv-env/bin/activate
# Windows:
cv-env\Scripts\activate

# 4. OpenCV kur
pip install opencv-python opencv-contrib-python numpy
```

Kurulumu doğrulamak için:

```python
import cv2
print(cv2.__version__)  # 4.9.x veya üstü bekleniyor
```

### 2. Jupyter Notebook / JupyterLab

Görüntü işleme algoritmalarını adım adım incelemek, ara sonuçları görselleştirmek için Jupyter ideal bir ortamdır.

```bash
pip install jupyterlab
jupyter lab
```

Jupyter içinde OpenCV görüntüsü göstermek için `cv2.imshow` yerine Matplotlib kullanın:

```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("goruntu.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.axis("off")
plt.show()
```

### 3. Google Colab (Bulut, Kurulum Gerektirmez)

Kendi bilgisayarınıza herhangi bir şey kurmak istemiyorsanız Google Colab ücretsiz GPU desteği ile tarayıcı üzerinden çalışır.

```python
# Colab'da OpenCV zaten yüklü gelir, ek bir şey gerekmez
import cv2
print(cv2.__version__)
```

Colab'da görüntü yüklemek için:

```python
from google.colab import files
uploaded = files.upload()  # Dosya yükle
```

veya Google Drive bağlantısı:

```python
from google.colab import drive
drive.mount('/content/drive')
img = cv2.imread('/content/drive/MyDrive/goruntu.jpg')
```

### 4. PyCharm (Büyük Projeler İçin)

Büyük ölçekli proje geliştiriyorsanız PyCharm Professional veya Community sürümü tercih edilebilir. Dahili debugger ve profiler özellikleri ile performans optimizasyonu kolaylaşır.

---

## İşletim Sistemi Seçimi

* **Linux (Ubuntu 22.04 önerilir):** CUDA, OpenVINO ve çoğu ML kütüphanesinin en iyi desteğini Linux üzerinde alırsınız. Sunucu ve üretim ortamları için standarttır.
* **macOS:** Apple Silicon (M1/M2/M3) çipleri için OpenCV ARM optimizasyonları mevcuttur. `pip install opencv-python` ile sorunsuz kurulum yapılabilir.
* **Windows:** WSL2 (Windows Subsystem for Linux) üzerinden Ubuntu kullanmak, doğrudan Windows'a göre daha az sorunla karşılaşmanızı sağlar.

**Gömülü Sistemler:** Raspberry Pi, Jetson Nano ve Jetson Orin gibi kartlar için Debian tabanlı Linux dağıtımları tercih edilmelidir.
