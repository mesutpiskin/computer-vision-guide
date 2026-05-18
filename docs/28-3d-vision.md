# Bölüm 28: 3D Vision

Sürücüsüz bir araç kamerasından önündeki engelin kaç metre uzakta olduğunu bilmeli. Robot kolu kutunun tam boyutlarını ve konumunu anlamalı. Tıbbi görüntülemede organın hacmini ölçmek gerekiyor. 2D görüntü bu soruların hiçbirini doğrudan cevaplayamaz — piksel koordinatları derinlik bilgisi taşımaz. Bu bölümde 2D kameradan 3D dünyayı anlamanın yöntemlerini inceleyeceğiz.

## Derinlik Tahmini

### Stereo Kamera ile Derinlik

Gözünün önünde bir parmak tut. Önce sol gözünü kapat, sonra sağ gözünü — parmak arka plana göre yer değiştirmiş gibi görünür. Bu **parallax** (ışınım farkı) etkisidir. İki göz arasındaki mesafeyi ve kayma miktarını bilirsen parmağın ne kadar uzakta olduğunu hesaplayabilirsin.

Stereo kamera aynı ilkeyi kullanır: iki kamera bilinen bir mesafe ($B$ = baseline) ile yerleştirilir. Sol ve sağ görüntülerdeki aynı noktanın yatay kayması **disparity** ($d$) olarak ölçülür. Derinlik şöyle hesaplanır:

$$Z = \frac{f \cdot B}{d}$$

Burada $f$ odak uzaklığı, $B$ kameralar arası mesafe, $d$ disparity (piksel cinsinden).

```python
# Gereksinimler: pip install opencv-python numpy matplotlib
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Stereo görüntüler yükle (ya da kendi görüntülerini kullan)
# Bu örnek için iki aynı gri görüntü + yapay kayma simüle ediyoruz
left_img = cv2.imread("left.png", cv2.IMREAD_GRAYSCALE)
right_img = cv2.imread("right.png", cv2.IMREAD_GRAYSCALE)

# Eğer test görüntüsü yoksa şematik oluştur
if left_img is None:
    left_img = np.random.randint(0, 255, (480, 640), dtype=np.uint8)
    # Sağ görüntü solun kaydırılmış versiyonu (gerçek stereo simülasyonu)
    right_img = np.roll(left_img, -20, axis=1)

# Semi-Global Block Matching ile disparity haritası
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=64,    # 16'nın katı olmalı
    blockSize=11,
    P1=8 * 3 * 11 ** 2,  # Komşu disparity düzgünleştirme
    P2=32 * 3 * 11 ** 2,
    disp12MaxDiff=1,
    uniquenessRatio=15,
    speckleWindowSize=100,
    speckleRange=32
)

disparity = stereo.compute(left_img, right_img).astype(np.float32) / 16.0

# Derinlik hesapla (f ve B kameraya göre değişir)
focal_length = 700    # piksel cinsinden odak uzaklığı
baseline = 0.1        # metre cinsinden kamera arası mesafe
depth = (focal_length * baseline) / (disparity + 1e-6)  # metre

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1); plt.imshow(left_img, cmap="gray"); plt.title("Sol görüntü"); plt.axis("off")
plt.subplot(1, 3, 2); plt.imshow(disparity, cmap="plasma"); plt.title("Disparity haritası"); plt.colorbar()
plt.subplot(1, 3, 3); plt.imshow(np.clip(depth, 0, 10), cmap="viridis"); plt.title("Derinlik (metre)"); plt.colorbar()
plt.tight_layout(); plt.savefig("stereo_depth.png", dpi=150); plt.show()
print("Derinlik haritası stereo_depth.png'ye kaydedildi.")
```

### Monoküler Derinlik Tahmini

Tek kameradan derinlik ölçmek geometrik olarak belirsizdir (scale ambiguity) — aynı görüntü hem yakında küçük nesne hem uzakta büyük nesne olabilir. Ama insan beyni bunu yapabiliyor: perspektif, gölge, dokusal ipuçları kullanarak. Derin öğrenme de aynı ipuçlarını öğreniyor.

**DPT (Dense Prediction Transformer)** modeli, ViT backbone kullanarak her piksel için göreli derinlik tahmini yapar. Mutlak metrik değil (kaç metre), göreli değer (hangisi daha yakın) — ama birçok uygulama için yeterli.

```python
# Gereksinimler: pip install transformers Pillow torch requests matplotlib
from transformers import DPTForDepthEstimation, DPTImageProcessor
from PIL import Image
import torch
import numpy as np
import matplotlib.pyplot as plt
import requests

model_name = "Intel/dpt-large"
processor = DPTImageProcessor.from_pretrained(model_name)
model = DPTForDepthEstimation.from_pretrained(model_name)
model.eval()

# Test görüntüsü
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Street_scene_in_Ghent_at_dusk.jpg/640px-Street_scene_in_Ghent_at_dusk.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
orig_size = image.size

inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
    predicted_depth = outputs.predicted_depth  # (1, H, W)

# Orijinal boyuta yeniden örnekle
depth = predicted_depth.squeeze().cpu().numpy()
depth_resized = np.array(
    Image.fromarray(depth).resize(orig_size, Image.BICUBIC)
)

# Görselleştir
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(image); axes[0].set_title("Orijinal"); axes[0].axis("off")
im = axes[1].imshow(depth_resized, cmap="plasma")
axes[1].set_title("Derinlik haritası (göreli)"); axes[1].axis("off")
plt.colorbar(im, ax=axes[1], label="Göreli derinlik (yakın = koyu)")
plt.tight_layout(); plt.savefig("monocular_depth.png", dpi=150); plt.show()
print("Derinlik haritası monocular_depth.png'ye kaydedildi.")
```

Derinlik haritasında yakındaki nesneler koyu (düşük değer), uzaktakiler açık renk görünür. Görsel olarak izlenen sahnenin 3D yapısını sezgisel biçimde anlamayı sağlar.

> **📌 Not:** DPT göreli derinlik üretir. Gerçek metrik ölçüm (kaç metre) için stereo kamera, LiDAR veya zaman uçuş kamerası (ToF) gerekir.

## Nokta Bulutu (Point Cloud)

3D uzayda (x, y, z) koordinatlarının kümesine nokta bulutu denir. Her noktaya ek olarak renk (r, g, b) veya yoğunluk (intensity) bilgisi de eklenebilir. Milyonlarca noktadan oluşan nokta bulutu bir sahnenin 3D iskeletini temsil eder.

**RGBD kamera** (Intel RealSense, Microsoft Kinect) her piksel için hem renk hem derinlik değeri üretir. Bu iki bilgiyi birleştirerek renkli nokta bulutu elde edilir.

> **💡 İpucu:** `pip install open3d` — 3D görselleştirme için güçlü kütüphane. Nokta bulutu, mesh ve voksel işleme destekler.

```python
# Gereksinimler: pip install open3d numpy
import open3d as o3d
import numpy as np

# Rastgele test nokta bulutu oluştur (gerçekte RGBD kameradan gelir)
np.random.seed(42)
n_points = 5000

# Küre yüzeyi üzerinde noktalar
theta = np.random.uniform(0, np.pi, n_points)
phi = np.random.uniform(0, 2 * np.pi, n_points)
r = 1.0 + 0.1 * np.random.randn(n_points)  # biraz gürültü

x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)
points = np.stack([x, y, z], axis=1)

# Her noktaya renk ata (yüksekliğe göre)
z_norm = (z - z.min()) / (z.max() - z.min())
colors = plt_colormap(z_norm)  # Renkli görselleştirme için

# Open3D ile nokta bulutu oluştur
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# Renk: z koordinatına göre mavi-kırmızı gradyan
colors_rgb = np.zeros((n_points, 3))
colors_rgb[:, 0] = z_norm          # kırmızı kanal
colors_rgb[:, 2] = 1 - z_norm      # mavi kanal
pcd.colors = o3d.utility.Vector3dVector(colors_rgb)

# İstatistikler
print(f"Nokta sayısı: {len(pcd.points)}")
print(f"Sınır kutusu: {pcd.get_axis_aligned_bounding_box()}")

# Görselleştir (pencere açılır)
o3d.visualization.draw_geometries([pcd],
                                   window_name="Nokta Bulutu",
                                   width=800, height=600)

# Dosyaya kaydet
o3d.io.write_point_cloud("point_cloud.ply", pcd)
print("point_cloud.ply olarak kaydedildi.")
```

> **⚠️ Dikkat:** Yukarıdaki örnekte `plt_colormap` import edilmemiştir — görselleştirme kısmını ya kaldırın ya da `import matplotlib.pyplot as plt; plt_colormap = plt.cm.viridis` ekleyin.

## PointNet

Nokta bulutlarını derin öğrenme ile işlerken kritik bir sorun var: noktaların sırası rastgele. 5000 noktayı farklı sıralarda versen de aynı nesneyi tanımalı. Bu **permutation invariance** (sıra bağımsızlığı) gereksinimi.

PointNet'in sezgisi şu: Her noktayı bağımsız olarak işle (paylaşılan MLP ile), sonra hepsini **global max pooling** ile birleştir. Hangi sırayla gelirse gelsin, max pooling aynı sonucu verir. Nokta setinin "özü" bu global özellik vektörüdür.

**Neden max pooling?** Her boyutta en güçlü sinyali tutan nokta, nesnenin önemli özelliklerini (köşe, kenar, yüzey) temsil eder.

```python
# Gereksinimler: pip install torch numpy
import torch
import torch.nn as nn

class PointNet(nn.Module):
    """Basitleştirilmiş PointNet sınıflandırıcı."""
    def __init__(self, num_classes=40):
        super().__init__()
        # Paylaşılan MLP — her noktaya bağımsız uygulanır
        self.mlp1 = nn.Sequential(
            nn.Conv1d(3, 64, 1), nn.BatchNorm1d(64), nn.ReLU(),
            nn.Conv1d(64, 128, 1), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Conv1d(128, 1024, 1), nn.BatchNorm1d(1024), nn.ReLU()
        )
        # Global max pooling → sıra bağımsız özellik
        # Sınıflandırıcı head
        self.classifier = nn.Sequential(
            nn.Linear(1024, 512), nn.BatchNorm1d(512), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(512, 256), nn.BatchNorm1d(256), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        # x: (B, 3, N) — B batch, 3 koordinat, N nokta
        features = self.mlp1(x)           # (B, 1024, N)
        global_feat = features.max(dim=2).values  # (B, 1024) — global max pooling
        return self.classifier(global_feat)

# Test
model = PointNet(num_classes=40)
batch_size, num_points = 4, 1024
x = torch.randn(batch_size, 3, num_points)  # 4 örnek, her biri 1024 nokta
logits = model(x)
print(f"Giriş: {x.shape}")
print(f"Çıkış (logits): {logits.shape}")  # (4, 40)
print(f"Parametre sayısı: {sum(p.numel() for p in model.parameters()):,}")
```

> **📌 Not:** Orijinal PointNet bir T-Net (Transformation Network) ile giriş noktalarını ve feature'ları hizalar. Bu basitleştirilmiş versiyon temel fikri gösterir; tam performans için orijinal implementasyonu inceleyin.

## NeRF (Neural Radiance Field)

Bir heykeli 100 farklı açıdan fotoğrafladın. NeRF bu fotoğraflardan sahnenin 3D temsilini öğrenir — artık hiç çekmediğin yeni açılardan gerçekçi görüntüler sentezleyebilirsin. Müze sergileri, film efektleri, arkeolojik eser belgeleme için devrim niteliğinde.

**Nasıl çalışır?** Nöral ağ, 3D uzaydaki her noktanın ve bakış yönünün renk ve yoğunluğunu öğrenir:

$$f_\theta(x, y, z, \theta, \phi) \to (R, G, B, \sigma)$$

- $(x, y, z)$: 3D uzaydaki konum
- $(\theta, \phi)$: bakış yönü (azimuth, elevation)
- $(R, G, B)$: o noktanın rengi
- $\sigma$: yoğunluk (opak mı, saydam mı?)

**Hacimsel render:** Bir kamera ışınını 3D uzayda ilerletirken her noktadan renk ve yoğunluk örnekle, bunları birleştirerek pikselin rengini hesapla. Bunu tüm pikseller için yap → yeni açıdan görüntü elde et.

**Eğitim:** Mevcut fotoğrafları render ile karşılaştır, fark (MSE kaybı) ile geri yayılım. Sahneye özgü eğitim — her sahne için sıfırdan eğitim gerekir.

**Kısıtlamalar:**
- Tek sahne için saatler süren eğitim (orijinal NeRF: ~8 saat)
- Dinamik sahnelerde (hareket eden nesneler) zorlanır
- Büyük açı boşluklarında bozulma

**Instant-NGP:** Hash encoding ile ağırlıkları hashlenmiş ızgara değerleriyle başlat. Eğitim saniyelerden dakikalara düşer — pratik kullanımı mümkün kılar.

```python
# NeRF eğitimi tam olarak çalıştırmak için özel veri ve GPU gerekir.
# Bu örnek NeRF'in temel fikrinin pseudo-kodu niteliğindedir.

import torch
import torch.nn as nn

class NeRF(nn.Module):
    """Minimal NeRF ağı — pozisyon + yön → renk + yoğunluk."""
    def __init__(self, pos_dim=60, dir_dim=24, hidden=256):
        # Pozisyonel encoding: ham koordinat yerine sinüs/kosinüs frekans bileşenleri
        # pos_dim = 3 * 2 * L_pos (L_pos=10 için 60), dir_dim benzer şekilde
        super().__init__()
        self.density_net = nn.Sequential(
            nn.Linear(pos_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
        )
        self.density_head = nn.Linear(hidden, 1)   # σ (yoğunluk)
        self.color_net = nn.Sequential(
            nn.Linear(hidden + dir_dim, hidden // 2), nn.ReLU(),
            nn.Linear(hidden // 2, 3), nn.Sigmoid()  # RGB [0,1]
        )

    def forward(self, pos_enc, dir_enc):
        feat = self.density_net(pos_enc)
        sigma = torch.relu(self.density_head(feat))   # Yoğunluk ≥ 0
        rgb = self.color_net(torch.cat([feat, dir_enc], dim=-1))
        return rgb, sigma

# Kullanım:
# nerf = NeRF()
# rgb, sigma = nerf(pos_encoded, dir_encoded)
# Hacimsel render ile ışın boyunca renk bütünleştir
print("NeRF modeli tanımlandı.")
print("Tam uygulama için: https://github.com/bmild/nerf")
```

> **💡 İpucu:** Pratik NeRF için `nerfstudio` paketini dene: `pip install nerfstudio`. 10-20 fotoğrafla kendi sahneni eğitebilirsin ve Instant-NGP ile dakikalar içinde sonuç alırsın.

## Yöntem Karşılaştırması

| Yöntem | Giriş | Çıkış | Güçlü Yön | Kısıt |
|--------|-------|-------|-----------|-------|
| **Stereo kamera** | İki senkronize kamera | Metrikh derinlik | Gerçek zamanlı, metrik | Kamera kurulumu gerekir |
| **Monoküler (DPT)** | Tek görüntü | Göreli derinlik | Kolay kurulum | Metrik ölçüm yok |
| **RGBD kamera** | Renkli + derinlik sensörü | Nokta bulutu | Kolay entegrasyon | Kapalı mekan, kısa menzil |
| **PointNet** | Nokta bulutu | Sınıf / segment | Permutation invariant | Ham nokta bulutu gerekir |
| **NeRF** | Çoklu fotoğraf | Yeni görüş açısı | Yüksek kalite sentez | Uzun eğitim, statik sahne |
| **Instant-NGP** | Çoklu fotoğraf | Yeni görüş açısı | Hızlı eğitim | Hala GPU gerekir |

## Özet & İleri Okuma

- **Stereo kamera**, parallax etkisini kullanarak metrikh derinlik üretir; gerçek zamanlı uygulamalar için standart yöntemdir.
- **Monoküler derinlik tahmini** (DPT) tek görüntüden göreli derinlik üretir; metrik ölçüm gerektirmeyen uygulamalar için pratiktir.
- **Nokta bulutu**, 3D uzaydaki (x,y,z) koordinat kümesidir; LiDAR ve RGBD kameralar doğrudan üretir.
- **PointNet**, nokta sırasından bağımsız (permutation invariant) 3D nesne tanıma için global max pooling kullanır.
- **NeRF**, çoklu açıdan çekilen fotoğraflardan nöral ağ ile sahne temsilini öğrenir; hiç çekilmemiş açılardan gerçekçi görüntü sentezi yapabilir.
- **Instant-NGP**, hash encoding ile NeRF eğitimini saatlerden dakikalara indirgeyen pratik yenilik sunar.
- 3D vision alanı robotik, otonom araç, tıbbi görüntüleme ve artırılmış gerçeklik uygulamalarının temelini oluşturur.

### Referanslar

- Qi et al., "PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation" (CVPR 2017): [https://arxiv.org/abs/1612.00593](https://arxiv.org/abs/1612.00593)
- Mildenhall et al., "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis" (ECCV 2020): [https://arxiv.org/abs/2003.08934](https://arxiv.org/abs/2003.08934)
- Müller et al., "Instant Neural Graphics Primitives" (SIGGRAPH 2022): [https://arxiv.org/abs/2201.05989](https://arxiv.org/abs/2201.05989)
