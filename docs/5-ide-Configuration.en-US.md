[Türkçe](./5-ide-yapilandirmasi.md) | English

**IDE Configuration**
----------------------

This chapter explains step-by-step how to set up an OpenCV Python project in the most commonly used development environments.

## Visual Studio Code with Python + OpenCV Setup

### 1. Install Required Extensions

From the VS Code Extensions panel (Ctrl+Shift+X), install these extensions:

* `ms-python.python` — Python language support
* `ms-python.pylance` — Type checking and autocompletion
* `ms-toolsai.jupyter` — Notebook support

### 2. Create Virtual Environment and Select Interpreter

```bash
# Create virtual environment in project folder
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Install dependencies
pip install opencv-python opencv-contrib-python numpy matplotlib
```

To select the interpreter in VS Code: `Ctrl+Shift+P` → "Python: Select Interpreter" → Select Python from `.venv`.

### 3. First Project: Read and Display an Image

Create a `main.py` file:

```python
import cv2

img = cv2.imread("test.jpg")
if img is None:
    raise FileNotFoundError("Image file not found")

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

Run with `F5` or in the terminal with `python main.py`.

### 4. Debug Configuration with launch.json

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

### 5. Linter Configuration with settings.json

`.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

---

## Anaconda / Conda Installation

Conda is a popular package manager for scientific Python projects that prevents package conflicts.

```bash
# Create new conda environment
conda create -n cv-env python=3.11
conda activate cv-env

# Install OpenCV from conda-forge channel
conda install -c conda-forge opencv

# Or via pip
pip install opencv-python opencv-contrib-python
```

To select the conda environment in VS Code: `Ctrl+Shift+P` → "Python: Select Interpreter" → Select the conda environment.

---

## PyCharm Setup

1. Open PyCharm, "New Project" → "Pure Python"
2. Interpreter: "New environment using Virtualenv"
3. In Terminal: `pip install opencv-python numpy`
4. Packages can be added via `Settings > Project > Python Interpreter > +`

---

## Google Colab (No Installation Required)

To start directly in your browser, go to [colab.research.google.com](https://colab.research.google.com) and create a new notebook.

```python
# OpenCV is already installed in Colab
import cv2
import numpy as np
from google.colab.patches import cv2_imshow  # Use this instead of imshow

# Example: create and display an image
img = np.zeros((300, 400, 3), dtype=np.uint8)
cv2.putText(img, "Hello OpenCV!", (50, 150),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv2_imshow(img)
```

Note: `cv2.imshow()` doesn't work in Colab; use `cv2_imshow` or Matplotlib instead.

---

## Android Studio with Android OpenCV Setup

To use OpenCV in Android applications:

1. Download the "Android" package from [opencv.org/releases](https://opencv.org/releases/)
2. In Android Studio: `File > New > Import Module` → Select the `sdk/java` folder inside the downloaded zip
3. Add module dependency in `app/build.gradle`:

```groovy
dependencies {
    implementation project(':sdk')
}
```

4. Load OpenCV in your Java file:

```java
static {
    if (!OpenCVLoader.initDebug()) {
        Log.e("OpenCV", "Failed to load");
    }
}
```
