[Türkçe](./28-3d-vision.md) | English

# Chapter 28: 3D Vision

An autonomous vehicle's camera must know how many meters away an obstacle is. A robot arm must understand the exact dimensions and position of a box. In medical imaging, organ volume needs to be measured. A 2D image alone cannot directly answer these questions — pixel coordinates carry no depth information. This chapter covers methods for understanding 3D world from 2D cameras.

## Depth Estimation

### Stereo Camera Depth

Hold your finger in front of your eyes. Close one eye, then the other — your finger appears to shift relative to the background. This **parallax** (disparity) effect lets you estimate distance. Two eyes separated by a known distance can measure finger distance using the shift amount.

Stereo cameras apply the same principle: two cameras are placed at a known distance ($B$ = baseline). The horizontal shift of the same point between left and right images is called **disparity** ($d$). Depth is calculated as:

$$Z = \frac{f \cdot B}{d}$$

Where $f$ is focal length, $B$ is baseline, $d$ is disparity (in pixels).

```python
# Requirements: pip install opencv-python numpy matplotlib
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load stereo images (or use your own)
# For this example, we simulate two grayscale images with artificial shift
left_img = cv2.imread("left.png", cv2.IMREAD_GRAYSCALE)
right_img = cv2.imread("right.png", cv2.IMREAD_GRAYSCALE)

# If no test images, create schematic
if left_img is None:
    left_img = np.random.randint(0, 255, (480, 640), dtype=np.uint8)
    # Right image is left's shifted version (real stereo simulation)
    right_img = np.roll(left_img, -20, axis=1)

# Compute disparity map with Semi-Global Block Matching
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=64,    # Must be multiple of 16
    blockSize=11,
    P1=8 * 3 * 11 ** 2,  # Neighbor disparity smoothing
    P2=32 * 3 * 11 ** 2,
    disp12MaxDiff=1,
    uniquenessRatio=15,
    speckleWindowSize=100,
    speckleRange=32
)

disparity = stereo.compute(left_img, right_img).astype(np.float32) / 16.0

# Calculate depth (f and B vary by camera)
focal_length = 700    # focal length in pixels
baseline = 0.1        # baseline distance in meters
depth = (focal_length * baseline) / (disparity + 1e-6)  # meters

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1); plt.imshow(left_img, cmap="gray"); plt.title("Left image"); plt.axis("off")
plt.subplot(1, 3, 2); plt.imshow(disparity, cmap="plasma"); plt.title("Disparity map"); plt.colorbar()
plt.subplot(1, 3, 3); plt.imshow(np.clip(depth, 0, 10), cmap="viridis"); plt.title("Depth (meters)"); plt.colorbar()
plt.tight_layout(); plt.savefig("stereo_depth.png", dpi=150); plt.show()
print("Depth map saved to stereo_depth.png.")
```

### Monocular Depth Estimation

Extracting depth from a single camera is geometrically ambiguous (scale ambiguity) — the same image could be a small object nearby or large object far away. But human brains can do it using perspective, shadows, texture cues. Deep learning learns these same cues.

**DPT (Dense Prediction Transformer)** uses ViT backbone to estimate relative depth for every pixel. Not absolute metric values (how many meters), but relative values (what's closer) — sufficient for many applications.

```python
# Requirements: pip install transformers Pillow torch requests matplotlib
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

# Test image
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Street_scene_in_Ghent_at_dusk.jpg/640px-Street_scene_in_Ghent_at_dusk.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
orig_size = image.size

inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
    predicted_depth = outputs.predicted_depth  # (1, H, W)

# Resize to original dimensions
depth = predicted_depth.squeeze().cpu().numpy()
depth_resized = np.array(
    Image.fromarray(depth).resize(orig_size, Image.BICUBIC)
)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(image); axes[0].set_title("Original"); axes[0].axis("off")
im = axes[1].imshow(depth_resized, cmap="plasma")
axes[1].set_title("Depth map (relative)"); axes[1].axis("off")
plt.colorbar(im, ax=axes[1], label="Relative depth (near = dark)")
plt.tight_layout(); plt.savefig("monocular_depth.png", dpi=150); plt.show()
print("Depth map saved to monocular_depth.png.")
```

In the depth map, nearby objects appear dark (low values), distant objects bright. Visually shows the scene's 3D structure intuitively.

> **📌 Note:** DPT produces relative depth. For true metric measurement (how many meters), use stereo camera, LiDAR, or Time-of-Flight (ToF) camera.

## Point Cloud

A set of (x, y, z) coordinates in 3D space is called a point cloud. Each point can include additional color (r, g, b) or intensity information. Millions of points represent a scene's 3D skeleton.

**RGBD camera** (Intel RealSense, Microsoft Kinect) produces both color and depth for each pixel. Combining these creates a colored point cloud.

> **💡 Tip:** `pip install open3d` — powerful 3D visualization library. Supports point clouds, meshes, and voxels.

```python
# Requirements: pip install open3d numpy
import open3d as o3d
import numpy as np

# Create random test point cloud (real data comes from RGBD camera)
np.random.seed(42)
n_points = 5000

# Points on sphere surface
theta = np.random.uniform(0, np.pi, n_points)
phi = np.random.uniform(0, 2 * np.pi, n_points)
r = 1.0 + 0.1 * np.random.randn(n_points)  # slight noise

x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)
points = np.stack([x, y, z], axis=1)

# Assign color (based on height)
z_norm = (z - z.min()) / (z.max() - z.min())

# Create Open3D point cloud
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# Color: z-based blue-red gradient
colors_rgb = np.zeros((n_points, 3))
colors_rgb[:, 0] = z_norm          # red channel
colors_rgb[:, 2] = 1 - z_norm      # blue channel
pcd.colors = o3d.utility.Vector3dVector(colors_rgb)

# Statistics
print(f"Number of points: {len(pcd.points)}")
print(f"Bounding box: {pcd.get_axis_aligned_bounding_box()}")

# Visualize (window opens)
o3d.visualization.draw_geometries([pcd],
                                   window_name="Point Cloud",
                                   width=800, height=600)

# Save to file
o3d.io.write_point_cloud("point_cloud.ply", pcd)
print("Saved to point_cloud.ply.")
```

> **⚠️ Warning:** The above example omits `plt_colormap` import — either remove that line or add `import matplotlib.pyplot as plt; plt_colormap = plt.cm.viridis`.

## PointNet

A critical problem with deep learning on point clouds: points are unordered. Feed 5000 points in different order, yet classify the same object. This requires **permutation invariance** (order independence).

PointNet's insight: process each point independently (via shared MLP), then combine all with **global max pooling**. Regardless of input order, max pooling gives same result. The point set's "essence" is this global feature vector.

**Why max pooling?** Each dimension captures the strongest signal, representing important object features (corners, edges, surfaces).

```python
# Requirements: pip install torch numpy
import torch
import torch.nn as nn

class PointNet(nn.Module):
    """Simplified PointNet classifier."""
    def __init__(self, num_classes=40):
        super().__init__()
        # Shared MLP — applied independently to each point
        self.mlp1 = nn.Sequential(
            nn.Conv1d(3, 64, 1), nn.BatchNorm1d(64), nn.ReLU(),
            nn.Conv1d(64, 128, 1), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Conv1d(128, 1024, 1), nn.BatchNorm1d(1024), nn.ReLU()
        )
        # Global max pooling → order-independent feature
        # Classification head
        self.classifier = nn.Sequential(
            nn.Linear(1024, 512), nn.BatchNorm1d(512), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(512, 256), nn.BatchNorm1d(256), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        # x: (B, 3, N) — B batch, 3 coordinates, N points
        features = self.mlp1(x)           # (B, 1024, N)
        global_feat = features.max(dim=2).values  # (B, 1024) — global max pooling
        return self.classifier(global_feat)

# Test
model = PointNet(num_classes=40)
batch_size, num_points = 4, 1024
x = torch.randn(batch_size, 3, num_points)  # 4 examples, 1024 points each
logits = model(x)
print(f"Input: {x.shape}")
print(f"Output (logits): {logits.shape}")  # (4, 40)
print(f"Number of parameters: {sum(p.numel() for p in model.parameters()):,}")
```

> **📌 Note:** Original PointNet includes a T-Net (Transformation Network) to align input points and features. This simplified version shows core idea; use original implementation for full performance.

## NeRF (Neural Radiance Field)

You photograph a statue from 100 different angles. NeRF learns 3D representation from these photos — now you can synthesize realistic images from angles never photographed. Revolutionary for museum exhibits, film effects, archaeological documentation.

**How it works?** A neural network learns each point's and viewing direction's color and intensity:

$$f_\theta(x, y, z, \theta, \phi) \to (R, G, B, \sigma)$$

- $(x, y, z)$: 3D position
- $(\theta, \phi)$: viewing direction (azimuth, elevation)
- $(R, G, B)$: color at that point
- $\sigma$: density (opaque or transparent?)

**Volume rendering:** Advance a camera ray through 3D space, sample color and density at each point, combine to compute pixel color. Do this for all pixels → view synthesis.

**Training:** Compare rendered images with actual photos, backpropagate MSE loss. Scene-specific training — each scene trained from scratch.

**Limitations:**
- Hours of training for single scene (original NeRF: ~8 hours)
- Struggles with dynamic scenes (moving objects)
- Artifacts with large viewing angle gaps

**Instant-NGP:** Hash encoding initializes weights with hashed grid values. Training drops from hours to minutes — makes practical use possible.

```python
# Full NeRF training requires special data and GPU.
# This is pseudo-code showing the core concept.

import torch
import torch.nn as nn

class NeRF(nn.Module):
    """Minimal NeRF network — position + direction → color + density."""
    def __init__(self, pos_dim=60, dir_dim=24, hidden=256):
        # Positional encoding: sine/cosine frequency components instead of raw coords
        # pos_dim = 3 * 2 * L_pos (for L_pos=10, pos_dim=60), dir_dim similar
        super().__init__()
        self.density_net = nn.Sequential(
            nn.Linear(pos_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
        )
        self.density_head = nn.Linear(hidden, 1)   # σ (density)
        self.color_net = nn.Sequential(
            nn.Linear(hidden + dir_dim, hidden // 2), nn.ReLU(),
            nn.Linear(hidden // 2, 3), nn.Sigmoid()  # RGB [0,1]
        )

    def forward(self, pos_enc, dir_enc):
        feat = self.density_net(pos_enc)
        sigma = torch.relu(self.density_head(feat))   # Density ≥ 0
        rgb = self.color_net(torch.cat([feat, dir_enc], dim=-1))
        return rgb, sigma

# Usage:
# nerf = NeRF()
# rgb, sigma = nerf(pos_encoded, dir_encoded)
# Integrate color along ray using volume rendering
print("NeRF model defined.")
print("For full implementation: https://github.com/bmild/nerf")
```

> **💡 Tip:** For practical NeRF use, try `nerfstudio`: `pip install nerfstudio`. Train on 10-20 photos of your scene, get results in minutes with Instant-NGP.

## Method Comparison

| Method | Input | Output | Strength | Limitation |
|--------|-------|--------|----------|-----------|
| **Stereo camera** | Two synced cameras | Metric depth | Real-time, metric | Requires setup |
| **Monocular (DPT)** | Single image | Relative depth | Easy setup | No metric scale |
| **RGBD camera** | Color + depth sensor | Point cloud | Easy integration | Indoor, short range |
| **PointNet** | Point cloud | Class / segment | Permutation invariant | Needs raw point cloud |
| **NeRF** | Multiple photos | Novel view | High-quality synthesis | Long training, static |
| **Instant-NGP** | Multiple photos | Novel view | Fast training | Still needs GPU |

## Summary & Further Reading

- **Stereo camera** uses parallax to produce metric depth; standard for real-time applications.
- **Monocular depth estimation** (DPT) produces relative depth from single image; practical for apps not requiring metric scale.
- **Point cloud** is 3D coordinate set; directly produced by LiDAR and RGBD cameras.
- **PointNet** enables 3D object recognition via permutation invariance and global max pooling.
- **NeRF** learns 3D scene representation from multi-view photos; synthesizes realistic images from novel viewpoints.
- **Instant-NGP** accelerates NeRF training from hours to minutes via hash encoding — enables practical use.
- 3D vision is foundation of robotics, autonomous vehicles, medical imaging, and AR applications.

### References

- Qi et al., "PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation" (CVPR 2017): [https://arxiv.org/abs/1612.00593](https://arxiv.org/abs/1612.00593)
- Mildenhall et al., "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis" (ECCV 2020): [https://arxiv.org/abs/2003.08934](https://arxiv.org/abs/2003.08934)
- Müller et al., "Instant Neural Graphics Primitives" (SIGGRAPH 2022): [https://arxiv.org/abs/2201.05989](https://arxiv.org/abs/2201.05989)
