# Video Anlama ve Eylem Tanıma

Video anlama, görüntü sınıflandırmasının zamansal boyuta genişletilmesidir. Bu bölümde SlowFast ve VideoMAE gibi modern video mimarilerini ve HuggingFace ile eylem tanıma uygulamasını inceleyeceğiz.

## Teorik Temel

**3D Konvolüsyon (C3D):**
2D $k\times k$ çekirdek yerine $k\times k\times k$ 3D çekirdek ile hem uzamsal hem zamansal bilgi birlikte işlenir:
$$\text{out}(t,x,y) = \sum_{\tau=0}^{k-1}\sum_{i=0}^{k-1}\sum_{j=0}^{k-1} \text{in}(t-\tau, x-i, y-j) \cdot W(\tau,i,j)$$

**SlowFast Network:**
İki paralel pathway:
- Slow pathway: düşük FPS ($\alpha \times$ az kare), yüksek kanal ($\beta \times$ fazla kanal) → görünüş
- Fast pathway: yüksek FPS (tam kare sayısı), düşük kanal → hareket
Lateral bağlantılar Fast → Slow bilgi aktarır.

**VideoMAE (Masked Autoencoder):**
Rastgele tube maskeleme: video voxel'larının %90'ı maskelenir.
Encoder maskelenmemiş patch'leri, decoder tüm video'yu reconstruct eder.
Self-supervised pre-training → downstream fine-tuning.

**Referanslar:**
- Feichtenhofer et al., "SlowFast Networks for Video Recognition", ICCV 2019 (https://arxiv.org/abs/1812.03982)
- Tong et al., "VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training", NeurIPS 2022 (https://arxiv.org/abs/2203.12602)

## Pratik Uygulama

```python
import cv2
import torch
import numpy as np
from transformers import VideoMAEForVideoClassification, VideoMAEImageProcessor

# VideoMAE ile eylem tanıma
processor = VideoMAEImageProcessor.from_pretrained(
    "MCG-NJU/videomae-base-finetuned-kinetics"
)
model = VideoMAEForVideoClassification.from_pretrained(
    "MCG-NJU/videomae-base-finetuned-kinetics"
)
if model is None:
    raise RuntimeError("VideoMAE modeli yüklenemedi")
model.eval()


def load_video_frames(path, num_frames=16, target_size=(224, 224)):
    """Videodan eşit aralıklı num_frames kare yükle."""
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise RuntimeError(f"Video açılamadı: {path}")

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total == 0:
        cap.release()
        raise ValueError("Video boş veya okunamıyor")

    indices = np.linspace(0, total - 1, num_frames, dtype=int)
    frames = []

    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, target_size)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)

    cap.release()

    if len(frames) < num_frames:
        raise ValueError(f"Yeterli kare yüklenemedi: {len(frames)}/{num_frames}")

    return frames


frames = load_video_frames("video.mp4", num_frames=16)

inputs = processor(frames, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits

predicted = logits.argmax(-1).item()
print(f"Tahmin edilen eylem: {model.config.id2label[predicted]}")

# Top-5
top5_probs, top5_indices = torch.softmax(logits, dim=-1).topk(5)
print("\nTop-5 Eylemler:")
for prob, idx in zip(top5_probs[0], top5_indices[0]):
    label = model.config.id2label[idx.item()]
    print(f"  {label}: {prob.item():.4f}")
```

## Özet & İleri Okuma

- Two-stream: spatial (RGB) ve temporal (optik akış) akışları ayrı CNN ile işler
- 3D konvolüsyon uzamsal ve zamansal bilgiyi tek geçişte yakalar; ancak hesaplama maliyeti yüksek
- SlowFast çift hız yoluyla görünüş ve hareketi ayrı kodlar; lateral bağlantılar bilgi alışverişi sağlar
- VideoMAE %90 maskeleme ile güçlü self-supervised pre-training öğrenir
- Kinetics-400/600 eylem tanıma alanının standart benchmark veri setleridir
- Referans: SlowFast (https://arxiv.org/abs/1812.03982), VideoMAE (https://arxiv.org/abs/2203.12602)
