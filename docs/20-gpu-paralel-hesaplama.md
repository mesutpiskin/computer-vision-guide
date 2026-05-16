**GPU ve Paralel Hesaplama**
----------------------------

Görüntü işleme ve derin öğrenme uygulamaları CPU üzerinde yavaş çalışabilir. GPU paralelleştirmesi ile işlem süreleri dramatik biçimde düşürülebilir. Bu bölümde OpenCV'nin CUDA modülü ve Intel OpenVINO ile GPU/NPU hızlandırmasını ele alacağız.

## OpenCV ile CUDA

OpenCV'nin CUDA modülü, Nvidia GPU'ları üzerinde temel görüntü işleme operasyonlarını paralel olarak çalıştırır. CUDA destekli OpenCV kullanmak için kaynak koddan derleme veya hazır CUDA-enabled wheel gerekmektedir.

### CUDA Desteğini Kontrol Et

```python
import cv2

cuda_count = cv2.cuda.getCudaEnabledDeviceCount()
print(f"CUDA destekli cihaz sayısı: {cuda_count}")

if cuda_count > 0:
    cv2.cuda.printCudaDeviceInfo(0)
```

### CUDA ile Görüntü İşleme

```python
import cv2
import numpy as np
import time

img = cv2.imread("buyuk_goruntu.jpg")

# CPU benchmark
t = time.time()
for _ in range(100):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
print(f"CPU: {(time.time() - t)*10:.1f} ms/kare")

# GPU ile aynı işlem
gpu_img = cv2.cuda_GpuMat()
gpu_img.upload(img)

t = time.time()
for _ in range(100):
    gpu_gray = cv2.cuda.cvtColor(gpu_img, cv2.COLOR_BGR2GRAY)
    gpu_blur = cv2.cuda.createGaussianFilter(
        cv2.CV_8UC1, cv2.CV_8UC1, (15, 15), 0
    ).apply(gpu_gray)
result = gpu_blur.download()
print(f"GPU: {(time.time() - t)*10:.1f} ms/kare")
```

### CUDA ile DNN Çıkarımı

```python
import cv2

net = cv2.dnn.readNetFromONNX("model.onnx")

# CUDA backend ayarla
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)  # veya DNN_TARGET_CUDA_FP16

img = cv2.imread("test.jpg")
blob = cv2.dnn.blobFromImage(img, 1/255.0, (640, 640), swapRB=True)
net.setInput(blob)
outputs = net.forward()
```

### CUDA Kurulum Notları

CUDA destekli OpenCV kurmak için iki yol vardır:

**Yol 1: pip wheel (kolay ama sürüm sınırlı)**
```bash
pip install opencv-python-headless  # önce kaldır
pip install opencv-contrib-python   # veya
# CUDA wheel için: https://github.com/cudawarper/opencv-cuda-wheels
```

**Yol 2: Kaynak koddan derleme (önerilen)**
```bash
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D WITH_CUDA=ON \
      -D CUDA_ARCH_BIN="8.6" \
      -D WITH_CUDNN=ON \
      -D OPENCV_DNN_CUDA=ON \
      -D ENABLE_FAST_MATH=1 \
      ..
make -j$(nproc)
sudo make install
```

---

## Intel OpenVINO ile Hızlandırma

OpenVINO (Open Visual Inference and Neural network Optimization), Intel CPU, GPU, VPU ve NPU üzerinde derin öğrenme modellerini optimize eder. CPU üzerinde bile CUDA'ya yakın performans sağlayabilir.

```bash
pip install openvino
```

### ONNX Modelini OpenVINO ile Çalıştır

```python
from openvino.runtime import Core
import numpy as np
import cv2

ie = Core()
model = ie.read_model("model.onnx")
compiled = ie.compile_model(model, "CPU")  # veya "GPU", "AUTO"

infer_request = compiled.create_infer_request()

img = cv2.imread("test.jpg")
blob = cv2.dnn.blobFromImage(img, 1/255.0, (640, 640), swapRB=True)

infer_request.infer({0: blob})
output = infer_request.get_output_tensor(0).data
print(f"Çıktı şekli: {output.shape}")
```

### OpenCV DNN ile OpenVINO Backend

```python
import cv2

net = cv2.dnn.readNetFromONNX("model.onnx")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
```

---

## Çoklu İş Parçacığı (Threading) ile Paralel İşleme

Python'da kamera akışını ayrı bir thread'de çalıştırmak kare bırakmayı önler:

```python
import cv2
import threading
import queue

class KameraThread:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.frame_queue = queue.Queue(maxsize=2)
        self.running = True
        threading.Thread(target=self._read_loop, daemon=True).start()

    def _read_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                if self.frame_queue.full():
                    self.frame_queue.get_nowait()
                self.frame_queue.put(frame)

    def read(self):
        return self.frame_queue.get(timeout=1)

    def stop(self):
        self.running = False
        self.cap.release()


cam = KameraThread(0)
while True:
    frame = cam.read()
    cv2.imshow("Thread Kamera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.stop()
cv2.destroyAllWindows()
```
