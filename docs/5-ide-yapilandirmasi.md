**IDE Yapılandırması**
----------------------

Bu bölümde en yaygın kullanılan geliştirme ortamlarında OpenCV Python projesi nasıl kurulur adım adım anlatılmaktadır.

## Visual Studio Code ile Python + OpenCV Kurulumu

### 1. Gerekli Eklentileri Kur

VS Code Extensions panelinden (Ctrl+Shift+X) şu eklentileri kur:

* `ms-python.python` — Python dil desteği
* `ms-python.pylance` — Tip kontrolü ve otomatik tamamlama
* `ms-toolsai.jupyter` — Notebook desteği

### 2. Sanal Ortam Oluştur ve Yorumlayıcıyı Seç

```bash
# Proje klasöründe sanal ortam oluştur
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Bağımlılıkları kur
pip install opencv-python opencv-contrib-python numpy matplotlib
```

VS Code'da yorumlayıcıyı seçmek için: `Ctrl+Shift+P` → "Python: Select Interpreter" → `.venv` içindeki Python'ı seç.

### 3. İlk Proje: Görüntü Oku ve Göster

`main.py` dosyası oluştur:

```python
import cv2

img = cv2.imread("test.jpg")
if img is None:
    raise FileNotFoundError("Görüntü dosyası bulunamadı")

cv2.imshow("Görüntü", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

`F5` ile çalıştır veya terminalde `python main.py`.

### 4. launch.json ile Debug Yapılandırması

`.vscode/launch.json` dosyasını oluştur:

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

### 5. settings.json ile Linter Yapılandırması

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

## Anaconda / Conda ile Kurulum

Conda, bilimsel Python projelerinde paket çakışmalarını önleyen popüler bir paket yöneticisidir.

```bash
# Yeni conda ortamı oluştur
conda create -n cv-env python=3.11
conda activate cv-env

# OpenCV conda-forge kanalından kur
conda install -c conda-forge opencv

# Veya pip ile
pip install opencv-python opencv-contrib-python
```

VS Code'da conda ortamını seçmek için: `Ctrl+Shift+P` → "Python: Select Interpreter" → conda ortamını seç.

---

## PyCharm ile Kurulum

1. PyCharm'ı aç, "New Project" → "Pure Python"
2. Interpreter: "New environment using Virtualenv"
3. Terminal'de: `pip install opencv-python numpy`
4. `Settings > Project > Python Interpreter > +` ile paket eklenebilir

---

## Google Colab (Kurulum Gerektirmez)

Tarayıcı üzerinden doğrudan başlamak için [colab.research.google.com](https://colab.research.google.com) adresine git ve yeni bir notebook oluştur.

```python
# OpenCV Colab'da zaten yüklüdür
import cv2
import numpy as np
from google.colab.patches import cv2_imshow  # imshow yerine bu kullanılır

# Örnek: görüntü üret ve göster
img = np.zeros((300, 400, 3), dtype=np.uint8)
cv2.putText(img, "Merhaba OpenCV!", (50, 150),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv2_imshow(img)
```

Not: Colab'da `cv2.imshow()` çalışmaz; bunun yerine `cv2_imshow` veya Matplotlib kullanın.

---

## Android Studio ile Android OpenCV Kurulumu

Android uygulamalarında OpenCV kullanmak için:

1. [opencv.org/releases](https://opencv.org/releases/) adresinden "Android" paketini indir
2. Android Studio'da: `File > New > Import Module` → indirilen zip içindeki `sdk/java` klasörünü seç
3. `app/build.gradle` içine modül bağımlılığı ekle:

```groovy
dependencies {
    implementation project(':sdk')
}
```

4. Java dosyasında OpenCV'yi yükle:

```java
static {
    if (!OpenCVLoader.initDebug()) {
        Log.e("OpenCV", "Yüklenemedi");
    }
}
```
