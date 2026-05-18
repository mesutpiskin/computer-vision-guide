[Türkçe](./20-gpu-paralel-hesaplama.md) | English

# GPU and Parallel Computing

Image processing and deep learning applications can run slowly on CPU. With GPU parallelization, processing times drop dramatically. In this chapter, we'll cover GPU acceleration with OpenCV's CUDA module and Intel OpenVINO.

## OpenCV with CUDA

OpenCV's CUDA module runs basic image processing operations in parallel on Nvidia GPUs. To use CUDA-enabled OpenCV, you need either source compilation or a pre-built CUDA wheel.

### Check for CUDA Support

```python
import cv2

cuda_count = cv2.cuda.getCudaEnabledDeviceCount()
print(f"CUDA-enabled devices: {cuda_count}")

if cuda_count > 0:
    cv2.cuda.printCudaDeviceInfo(0)
```

### Image Processing with CUDA

```python
import cv2
import numpy as np
import time

img = cv2.imread("large_image.jpg")

# CPU benchmark
t = time.time()
for _ in range(100):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
print(f"CPU: {(time.time() - t)*10:.1f} ms/frame")

# Same operation on GPU
gpu_img = cv2.cuda_GpuMat()
gpu_img.upload(img)

t = time.time()
for _ in range(100):
    gpu_gray = cv2.cuda.cvtColor(gpu_img, cv2.COLOR_BGR2GRAY)
    gpu_blur = cv2.cuda.createGaussianFilter(
        cv2.CV_8UC1, cv2.CV_8UC1, (15, 15), 0
    ).apply(gpu_gray)
result = gpu_blur.download()
print(f"GPU: {(time.time() - t)*10:.1f} ms/frame")
```

### DNN Inference with CUDA

```python
import cv2

net = cv2.dnn.readNetFromONNX("model.onnx")

# Set CUDA backend
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)  # or DNN_TARGET_CUDA_FP16

img = cv2.imread("test.jpg")
blob = cv2.dnn.blobFromImage(img, 1/255.0, (640, 640), swapRB=True)
net.setInput(blob)
outputs = net.forward()
```

### CUDA Installation Notes

There are two ways to install CUDA-enabled OpenCV:

**Option 1: pip wheel (easy but limited versions)**
```bash
pip install opencv-python-headless  # uninstall first
pip install opencv-contrib-python   # or
# For CUDA wheel: https://github.com/cudawarper/opencv-cuda-wheels
```

**Option 2: Build from source (recommended)**
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

## Acceleration with Intel OpenVINO

OpenVINO (Open Visual Inference and Neural network Optimization) optimizes deep learning models on Intel CPUs, GPUs, VPUs, and NPUs. Even on CPU alone, it can deliver CUDA-like performance.

```bash
pip install openvino
```

### Run an ONNX Model with OpenVINO

```python
from openvino.runtime import Core
import numpy as np
import cv2

ie = Core()
model = ie.read_model("model.onnx")
compiled = ie.compile_model(model, "CPU")  # or "GPU", "AUTO"

infer_request = compiled.create_infer_request()

img = cv2.imread("test.jpg")
blob = cv2.dnn.blobFromImage(img, 1/255.0, (640, 640), swapRB=True)

infer_request.infer({0: blob})
output = infer_request.get_output_tensor(0).data
print(f"Output shape: {output.shape}")
```

### OpenCV DNN with OpenVINO Backend

```python
import cv2

net = cv2.dnn.readNetFromONNX("model.onnx")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
```

---

## Parallel Processing with Threading

In Python, running camera capture in a separate thread prevents frame drops:

```python
import cv2
import threading
import queue

class CameraThread:
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


cam = CameraThread(0)
while True:
    frame = cam.read()
    cv2.imshow("Threaded Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.stop()
cv2.destroyAllWindows()
```
