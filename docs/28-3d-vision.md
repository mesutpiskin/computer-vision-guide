# 3D Vision: Nokta Bulutu, NeRF ve Derinlik Tahmini

3D görü, 2D görüntülerden üç boyutlu yapıyı anlamayı ve yeniden oluşturmayı hedefler. Bu bölümde nokta bulutu işleme (PointNet), Neural Radiance Fields (NeRF) ve monoküler derinlik tahmini konularını inceleyeceğiz.

## Teorik Temel

**Nokta Bulutu (Point Cloud):**
$N$ adet 3D nokta kümesi: $\mathcal{P} = \{(x_i, y_i, z_i)\}_{i=1}^N$. Sırasız (unordered) veri — permutation invariant işlem zorunludur.

**PointNet — Simetrik Fonksiyon:**
$$f(\{x_1,...,x_N\}) \approx g(h(x_1),...,h(x_N))$$
$g$: max-pooling (permutation invariant), $h$: shared MLP. Her nokta bağımsız işlenir, sonra global özellik elde edilir.

**NeRF (Neural Radiance Field):**
Sahne, sürekli bir nöral fonksiyon olarak temsil edilir:
$$F_\theta: (\mathbf{x}, \mathbf{d}) \rightarrow (\mathbf{c}, \sigma)$$
$\mathbf{x}=(x,y,z)$: 3D konum, $\mathbf{d}=(\theta,\phi)$: görüş yönü, $\mathbf{c}=(r,g,b)$: renk, $\sigma$: yoğunluk.

Hacimsel rendering ile piksel rengi:
$$C(\mathbf{r}) = \int_{t_n}^{t_f} T(t)\,\sigma(\mathbf{r}(t))\,\mathbf{c}(\mathbf{r}(t),\mathbf{d})\,dt$$
$T(t) = \exp\!\left(-\int_{t_n}^t \sigma(\mathbf{r}(s))\,ds\right)$: transmittance (geçirgenlik).

**Referanslar:**
- Qi et al., "PointNet: Deep Learning on Point Sets", CVPR 2017 (https://arxiv.org/abs/1612.00593)
- Mildenhall et al., "NeRF: Representing Scenes as Neural Radiance Fields", ECCV 2020 (https://arxiv.org/abs/2003.08934)

## Pratik Uygulama

```python
import torch
import cv2
import numpy as np
from transformers import DPTForDepthEstimation, DPTImageProcessor
from PIL import Image

# DPT (Dense Prediction Transformer) ile monoküler derinlik tahmini
processor = DPTImageProcessor.from_pretrained("Intel/dpt-large")
model = DPTForDepthEstimation.from_pretrained("Intel/dpt-large")
if model is None:
    raise RuntimeError("DPT modeli yüklenemedi")
model.eval()

img_path = "resim.jpg"
img_cv = cv2.imread(img_path)
if img_cv is None:
    raise FileNotFoundError(f"{img_path} bulunamadı")

rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
pil_img = Image.fromarray(rgb)
inputs = processor(images=pil_img, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    depth = outputs.predicted_depth  # (1, H, W)

depth_np = depth.squeeze().numpy()
depth_norm = cv2.normalize(depth_np, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# Renk haritası ile görselleştir
depth_color = cv2.applyColorMap(depth_norm, cv2.COLORMAP_MAGMA)
combined = np.hstack([img_cv, depth_color])
cv2.imshow("Sol: Orijinal | Sag: Derinlik Haritasi", combined)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Derinlik istatistikleri
print(f"Min derinlik: {depth_np.min():.3f}")
print(f"Max derinlik: {depth_np.max():.3f}")
print(f"Ortalama derinlik: {depth_np.mean():.3f}")

# Open3D ile nokta bulutu oluşturma (isteğe bağlı)
try:
    import open3d as o3d
    depth_o3d = o3d.geometry.Image(depth_norm)
    color_o3d = o3d.geometry.Image(rgb)
    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color_o3d, depth_o3d, depth_scale=1000.0, convert_rgb_to_intensity=False
    )
    intrinsic = o3d.camera.PinholeCameraIntrinsic(
        width=img_cv.shape[1], height=img_cv.shape[0],
        fx=525.0, fy=525.0,
        cx=img_cv.shape[1] / 2.0, cy=img_cv.shape[0] / 2.0
    )
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, intrinsic)
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    o3d.visualization.draw_geometries([pcd], window_name="Nokta Bulutu")
except ImportError:
    print("Open3D kurulu değil: pip install open3d")
```

## Özet & İleri Okuma

- Nokta bulutu sırasız 3D veri; PointNet max-pooling ile permutation invariance sağlar
- NeRF sahneyi MLP ile sürekli radiance field olarak temsil eder; yeni açılardan render eder
- Monoküler derinlik tahmini tek kameradan göreli derinlik üretir (mutlak ölçek bilinmez)
- DPT transformer tabanlı encoder ile yüksek çözünürlüklü derinlik haritası üretir
- Open3D nokta bulutu işleme ve görselleştirme için standart Python kütüphanesidir
- Referans: PointNet (https://arxiv.org/abs/1612.00593), NeRF (https://arxiv.org/abs/2003.08934)
