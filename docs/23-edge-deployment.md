**ONNX ve TFLite ile Edge Deployment**
----------------------------------------

Derin öğrenme modellerini Raspberry Pi, Jetson Nano, mobil cihazlar veya mikrodenetleyiciler gibi kaynak kısıtlı donanımlarda çalıştırmak için modelleri optimize etmek ve dönüştürmek gerekir. Bu bölümde ONNX ve TensorFlow Lite formatlarını ele alacağız.

## ONNX (Open Neural Network Exchange)

ONNX, farklı derin öğrenme çerçeveleri arasında model transferini sağlayan açık format standardıdır. PyTorch'tan ONNX'e ve ardından OpenCV/ONNXRuntime'a geçiş için kullanılır.

### PyTorch Modelini ONNX'e Dönüştür

```python
import torch
import torchvision.models as models

model = models.resnet18(pretrained=True)
model.eval()

dummy_input = torch.randn(1, 3, 224, 224)

torch.onnx.export(
    model,
    dummy_input,
    "resnet18.onnx",
    opset_version=12,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}}
)
print("ONNX dosyası oluşturuldu: resnet18.onnx")
```

### YOLOv8 → ONNX

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.export(format="onnx", imgsz=640, simplify=True)
# yolov8n.onnx oluşturulur
```

### ONNX Runtime ile Çıkarım

```bash
pip install onnxruntime  # CPU
pip install onnxruntime-gpu  # CUDA GPU
```

```python
import onnxruntime as ort
import numpy as np
import cv2

# Oturum oluştur
providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
session = ort.InferenceSession("resnet18.onnx", providers=providers)

# Giriş adı ve şekli
input_name = session.get_inputs()[0].name
print(f"Model girişi: {input_name}, şekil: {session.get_inputs()[0].shape}")

# Görüntüyü hazırla
img = cv2.imread("test.jpg")
img = cv2.resize(img, (224, 224))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = img.astype(np.float32) / 255.0
img = (img - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]  # ImageNet normalize
blob = np.transpose(img, (2, 0, 1))[np.newaxis, ...]

# Çıkarım
outputs = session.run(None, {input_name: blob})
pred = np.argmax(outputs[0])
print(f"Tahmin edilen sınıf: {pred}")
```

### ONNX Modelini OpenCV ile Kullan

```python
import cv2
import numpy as np

net = cv2.dnn.readNetFromONNX("yolov8n.onnx")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

img = cv2.imread("test.jpg")
blob = cv2.dnn.blobFromImage(img, 1/255.0, (640, 640), swapRB=True)
net.setInput(blob)
outputs = net.forward()
print(f"Çıktı şekli: {outputs.shape}")
```

---

## TensorFlow Lite (TFLite)

TFLite, Android ve iOS cihazlar ile Raspberry Pi için optimize edilmiş hafif çıkarım motorudur.

### Keras Modelini TFLite'e Dönüştür

```python
import tensorflow as tf

# Mevcut Keras modelini yükle
model = tf.keras.applications.MobileNetV2(weights="imagenet")

# TFLite'e dönüştür
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Opsiyonel: FP16 ya da INT8 quantization
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]  # FP16

tflite_model = converter.convert()
with open("mobilenetv2.tflite", "wb") as f:
    f.write(tflite_model)
print(f"Model boyutu: {len(tflite_model) / 1024:.1f} KB")
```

### INT8 Quantization (Daha Küçük, Daha Hızlı)

```python
import tensorflow as tf
import numpy as np

def representative_dataset():
    for _ in range(100):
        img = np.random.randint(0, 256, (1, 224, 224, 3), dtype=np.uint8)
        yield [img.astype(np.float32) / 255.0]

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

tflite_model = converter.convert()
with open("mobilenetv2_int8.tflite", "wb") as f:
    f.write(tflite_model)
```

### TFLite ile Çıkarım (Python)

```python
import tensorflow as tf
import numpy as np
import cv2

interpreter = tf.lite.Interpreter(model_path="mobilenetv2.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

img = cv2.imread("test.jpg")
img = cv2.resize(img, (224, 224))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
input_data = np.expand_dims(img.astype(np.float32) / 255.0, axis=0)

interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()

output = interpreter.get_tensor(output_details[0]['index'])
pred = np.argmax(output[0])
print(f"Tahmin: {pred}")
```

### TFLite ile Raspberry Pi Deployment

```bash
# Raspberry Pi 4 üzerinde
pip install tflite-runtime
```

```python
import tflite_runtime.interpreter as tflite
import numpy as np
import cv2

interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
# Aynı API, sadece import değişti
```

---

## Model Boyutu ve Hız Karşılaştırması

MobileNetV2 örneği, Raspberry Pi 4:

| Format | Boyut | Çıkarım Süresi |
|--------|-------|---------------|
| Keras FP32 | 14 MB | ~800 ms |
| TFLite FP32 | 14 MB | ~300 ms |
| TFLite FP16 | 7 MB | ~280 ms |
| TFLite INT8 | 3.5 MB | ~150 ms |

---

## ONNX vs TFLite Seçim Rehberi

* **ONNX:** PyTorch kaynaklı modeller, masaüstü/sunucu deployment, OpenCV entegrasyonu
* **TFLite:** Android/iOS/Raspberry Pi, TensorFlow/Keras kaynaklı modeller, minimum footprint
