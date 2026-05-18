[Türkçe](./23-edge-deployment.md) | English

# Edge Deployment with ONNX and TFLite

Deploying deep learning models on resource-constrained hardware like Raspberry Pi, Jetson Nano, mobile devices, or microcontrollers requires optimizing and converting models to run efficiently. This chapter covers the ONNX and TensorFlow Lite formats.

## ONNX (Open Neural Network Exchange)

ONNX is an open standard format that enables model transfer between different deep learning frameworks. It provides a bridge from PyTorch to ONNX and then to OpenCV or ONNX Runtime.

### Convert PyTorch Model to ONNX

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
print("ONNX file created: resnet18.onnx")
```

### YOLOv8 → ONNX

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.export(format="onnx", imgsz=640, simplify=True)
# Creates yolov8n.onnx
```

### Inference with ONNX Runtime

```bash
pip install onnxruntime  # CPU
pip install onnxruntime-gpu  # CUDA GPU
```

```python
import onnxruntime as ort
import numpy as np
import cv2

# Create session
providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
session = ort.InferenceSession("resnet18.onnx", providers=providers)

# Get input name and shape
input_name = session.get_inputs()[0].name
print(f"Model input: {input_name}, shape: {session.get_inputs()[0].shape}")

# Prepare image
img = cv2.imread("test.jpg")
img = cv2.resize(img, (224, 224))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = img.astype(np.float32) / 255.0
img = (img - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]  # ImageNet normalize
blob = np.transpose(img, (2, 0, 1))[np.newaxis, ...]

# Inference
outputs = session.run(None, {input_name: blob})
pred = np.argmax(outputs[0])
print(f"Predicted class: {pred}")
```

### Use ONNX Model with OpenCV

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
print(f"Output shape: {outputs.shape}")
```

---

## TensorFlow Lite (TFLite)

TFLite is a lightweight inference engine optimized for Android, iOS devices, and Raspberry Pi.

### Convert Keras Model to TFLite

```python
import tensorflow as tf

# Load an existing Keras model
model = tf.keras.applications.MobileNetV2(weights="imagenet")

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Optional: FP16 or INT8 quantization
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]  # FP16

tflite_model = converter.convert()
with open("mobilenetv2.tflite", "wb") as f:
    f.write(tflite_model)
print(f"Model size: {len(tflite_model) / 1024:.1f} KB")
```

### INT8 Quantization (Smaller, Faster)

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

### TFLite Inference (Python)

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
print(f"Prediction: {pred}")
```

### TFLite with Raspberry Pi Deployment

```bash
# On Raspberry Pi 4
pip install tflite-runtime
```

```python
import tflite_runtime.interpreter as tflite
import numpy as np
import cv2

interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
# Same API, only import changed
```

---

## Model Size and Speed Comparison

MobileNetV2 example on Raspberry Pi 4:

| Format | Size | Inference Time |
|--------|------|----------------|
| Keras FP32 | 14 MB | ~800 ms |
| TFLite FP32 | 14 MB | ~300 ms |
| TFLite FP16 | 7 MB | ~280 ms |
| TFLite INT8 | 3.5 MB | ~150 ms |

---

## ONNX vs TFLite Selection Guide

* **ONNX:** PyTorch-sourced models, desktop/server deployment, OpenCV integration
* **TFLite:** Android/iOS/Raspberry Pi, TensorFlow/Keras-sourced models, minimal footprint
