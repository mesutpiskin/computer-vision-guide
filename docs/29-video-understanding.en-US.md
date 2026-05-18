[Türkçe](./29-video-siniflandirma.md) | English

# Chapter 29: Video Understanding

You want a security camera to detect only "falling" actions. The obvious approach: classify each frame independently. But a single frame can't answer "is someone falling or just sitting?" Action unfolds over time — across multiple frames. This chapter covers processing video with the temporal dimension.

## Why Video Is a Separate Problem

Image classification takes single H×W×3 frame. Video has T sequential frames: T×H×W×3. This dimensional growth isn't minor — it's fundamental.

Classifying each frame independently gives "person" but not "throwing a pass, shooting, standing?" Time carries the answer. Moreover, humans naturally think in temporal patterns — "door opening," "car braking," "hand waving" all depend on time.

## 3D Convolution (C3D)

2D convolution applies filters to H×W spatial area — learns "is there an edge here?" 3D convolution extends to T×H×W: applies filter in both space and time — learns "how did this object move across 8 frames?"

```
2D: filter size k×k     → spatial patterns
3D: filter size k×k×k   → spatial + temporal patterns
```

**Limitation:** Parameters scale with ~k factor compared to 2D. Single C3D training can take days, memory extremely high.

## Two-Stream Networks

Two-stream networks draw from neuroscience: brain has two separate visual pathways — "what" and "how it moves." Two-stream networks make same distinction.

- **First stream (Spatial/RGB):** Processes video frames — "what" (objects, colors, textures)
- **Second stream (Temporal/Optical flow):** Processes pixel motion between frames (optical flow images) — "how it moves"

Two streams' predictions merge in late fusion. One encodes appearance, the other motion, together they perform better.

**Disadvantage:** Optical flow computation is expensive and requires separate storage.

## SlowFast Networks

Brain processes at different frequencies. Slow processes (object recognition, scene understanding) change at millisecond scales. Fast processes (hand clapping, ball movement) happen much quicker. SlowFast embeds this observation directly into architecture.

**Slow pathway:**
- Sample few frames (e.g., 32 frames → 4 frames = every 8th frame)
- High spatial resolution
- Learns object appearance, context
- High capacity, many channels

**Fast pathway:**
- Many frames (32 frames → 32 frames = every frame)
- Low spatial resolution, few channels (1/8 of Slow pathway)
- Learns motion, temporal change
- Low computation cost

Two paths share information via **lateral connections** — Fast path's motion enriches Slow path's object representation.

```python
# Requirements: pip install torch torchvision
import torch

# Ready SlowFast model from PyTorch Hub
# (For real video inference, need torchvision>=0.13)
try:
    model = torch.hub.load("facebookresearch/pytorchvideo",
                            "slowfast_r50", pretrained=True)
    model.eval()
    print("SlowFast-R50 loaded.")
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")

    # SlowFast input format: [slow_clip, fast_clip]
    # slow_clip: (B, C, T_slow, H, W) — e.g., (1, 3, 4, 224, 224)
    # fast_clip: (B, C, T_fast, H, W) — e.g., (1, 3, 32, 224, 224)
    slow_clip = torch.randn(1, 3, 4, 224, 224)
    fast_clip = torch.randn(1, 3, 32, 224, 224)

    with torch.no_grad():
        output = model([slow_clip, fast_clip])
    print(f"Output shape: {output.shape}")  # (1, 400) — Kinetics-400 classes

except Exception as e:
    print(f"Model loading error: {e}")
    print("For manual install: pip install pytorchvideo")
```

## VideoMAE

BERT masks 15% of words, model learns to predict masked words from context. VideoMAE applies the same idea to video — but masks 90%, very high ratio.

Why so high? Video frames are temporally very similar — mask 15% and model just copies from neighbors. Mask 90% forces network to truly understand scene structure.

**Temporal tube masking:** Same spatial location stays masked across consecutive frames. Prevents "temporal interpolation" cheating.

Learns strong representation with limited labels (self-supervised pre-training), then fine-tunable with few labels.

```python
# Requirements: pip install transformers torch av numpy
from transformers import VideoMAEForVideoClassification, VideoMAEImageProcessor
import torch
import numpy as np

model_name = "MCG-NJU/videomae-base-finetuned-kinetics"
processor = VideoMAEImageProcessor.from_pretrained(model_name)
model = VideoMAEForVideoClassification.from_pretrained(model_name)
model.eval()

# VideoMAE expects 16 frames
# In real use, sample frames from video file
# Here we simulate video
num_frames = 16
height, width = 224, 224

# (num_frames, H, W, C) format random video
video_frames = [
    np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    for _ in range(num_frames)
]

# Process and predict
inputs = processor(video_frames, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# Top 3 predictions
probs = torch.softmax(outputs.logits, dim=-1)[0]
top3 = torch.topk(probs, k=3)

print("VideoMAE — Top 3 action predictions:")
for prob, idx in zip(top3.values, top3.indices):
    label = model.config.id2label[idx.item()]
    print(f"  {label}: {prob.item()*100:.1f}%")
```

> **💡 Tip:** To sample frames from video file, use `av` (PyAV): `pip install av`. Open video with `av.open("video.mp4")`, select 16 equally-spaced frames.

> **📌 Note:** Kinetics-400 contains 400 daily action classes. Model is fine-tuned on these. To adapt to your dataset, replace final layer and fine-tune.

## Method Comparison

| Method | Parameters | Kinetics Accuracy | Training | When to Use |
|--------|-----------|-------------------|----------|------------|
| **C3D** | ~78M | ~82% Top-1 | Expensive | Simple action, small data |
| **Two-Stream** | ~2×22M | ~88% Top-1 | Medium | If optical flow available |
| **SlowFast-R50** | ~34M | ~77.9% Top-1 (Kinetics-400) | Medium | Speed/accuracy balance |
| **VideoMAE-B** | ~87M | ~80.9% Top-1 (Kinetics-400) | Long (pre-train) | Limited labels, transfer |

> **⚠️ Warning:** Video models consume far more memory than image models. Start batch size 1, reduce frames/resolution on OOM.

## Summary & Further Reading

- Single frame classification can't capture temporal events like "falling" — temporal dimension is essential.
- **3D Convolution** filters space and time simultaneously; high parameter cost.
- **Two-Stream networks** process RGB (appearance) and optical flow (motion) separately, merge results.
- **SlowFast Networks** mimic brain's dual-frequency processing: slow path for objects, fast path for motion.
- **VideoMAE** uses 90% masking for self-supervised pre-training; produces strong representations with limited labels.
- Video model training/inference needs significantly more GPU memory than image models.
- Kinetics-400/600/700 are standard benchmarks for action recognition.

### References

- Tran et al., "Learning Spatiotemporal Features with 3D Convolutional Networks" (ICCV 2015): [https://arxiv.org/abs/1412.0767](https://arxiv.org/abs/1412.0767)
- Simonyan & Zisserman, "Two-Stream Convolutional Networks for Action Recognition in Videos" (NeurIPS 2014): [https://arxiv.org/abs/1406.2199](https://arxiv.org/abs/1406.2199)
- Feichtenhofer et al., "SlowFast Networks for Video Recognition" (ICCV 2019): [https://arxiv.org/abs/1812.01548](https://arxiv.org/abs/1812.01548)
- Tong et al., "VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training" (NeurIPS 2022): [https://arxiv.org/abs/2203.12602](https://arxiv.org/abs/2203.12602)
