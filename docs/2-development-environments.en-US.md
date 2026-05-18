[Türkçe](./2-gelistirme-ortamlari.md) | English

**Platform and Development Environment Selection**
----------------------------------------

OpenCV is a platform-independent library that runs smoothly on Windows, Linux, and macOS. In this chapter, we'll explore the recommended development environments and programming language choices as of 2024.

## Programming Language Selection

### Python (Recommended)

Python has become the overwhelmingly dominant choice in computer vision and image processing projects today. The main reasons include:

* **Rich ecosystem:** Libraries like NumPy, SciPy, scikit-learn, PyTorch, TensorFlow, Keras, Ultralytics, and MediaPipe all provide first-class support for Python.
* **Rapid prototyping:** You can experiment line-by-line in Jupyter Notebook or Google Colab, visually inspecting results immediately.
* **OpenCV documentation:** The vast majority of official OpenCV documentation examples are written in Python.
* **Community:** Most examples on Stack Overflow, GitHub Issues, and Hugging Face are Python-based.

For performance-critical production applications, it's common to transition from Python to C++ or ONNX/TFLite runtimes. However, for development and research, Python should be your first choice.

### C++ (Advanced / Production)

C++ is OpenCV's native language. It's preferred for embedded systems, real-time video processing, and low-latency applications. Not recommended for beginners.

### Java / Android

Java or Kotlin with OpenCV is appropriate for developers wanting to build Android mobile applications. For desktop Java applications, it's rarely used today.

---

## Recommended Development Environments

### 1. Visual Studio Code + Python (Most Common Choice)

VS Code is a fast, free, and open-source editor. For Python development, we recommend installing these extensions:

* **Python** (Microsoft)
* **Pylance** (type checking and autocompletion)
* **Jupyter** (notebook support)

**Installation steps:**

```bash
# 1. Verify Python 3.10+ is installed
python --version

# 2. Create a virtual environment
python -m venv cv-env

# 3. Activate the virtual environment
# macOS/Linux:
source cv-env/bin/activate
# Windows:
cv-env\Scripts\activate

# 4. Install OpenCV
pip install opencv-python opencv-contrib-python numpy
```

To verify the installation:

```python
import cv2
print(cv2.__version__)  # Expecting 4.9.x or higher
```

### 2. Jupyter Notebook / JupyterLab

Jupyter is an ideal environment for step-by-step examination of image processing algorithms and visual inspection of intermediate results.

```bash
pip install jupyterlab
jupyter lab
```

In Jupyter, use Matplotlib instead of `cv2.imshow` to display OpenCV images:

```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("image.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.axis("off")
plt.show()
```

### 3. Google Colab (Cloud, No Installation Required)

If you don't want to install anything on your computer, Google Colab runs in your browser with free GPU support.

```python
# OpenCV is already installed in Colab, no additional setup needed
import cv2
print(cv2.__version__)
```

To upload an image in Colab:

```python
from google.colab import files
uploaded = files.upload()  # Upload file
```

Or connect to Google Drive:

```python
from google.colab import drive
drive.mount('/content/drive')
img = cv2.imread('/content/drive/MyDrive/image.jpg')
```

### 4. PyCharm (For Large Projects)

If you're developing large-scale projects, PyCharm Professional or Community edition is a good choice. Built-in debugger and profiler features make performance optimization easier.

---

## Operating System Selection

* **Linux (Ubuntu 22.04 recommended):** You get the best support for CUDA, OpenVINO, and most ML libraries on Linux. It's the standard for server and production environments.
* **macOS:** Apple Silicon (M1/M2/M3) chips have ARM optimizations for OpenCV. You can install with `pip install opencv-python` without issues.
* **Windows:** Using Ubuntu through WSL2 (Windows Subsystem for Linux) results in fewer problems compared to native Windows.

**Embedded Systems:** For boards like Raspberry Pi, Jetson Nano, and Jetson Orin, Debian-based Linux distributions are preferred.
