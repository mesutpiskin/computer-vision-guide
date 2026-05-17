# Vision Transformers: ViT, Swin ve DETR

Vision Transformer (ViT), 2020 yılında Dosovitskiy ve ark. tarafından görüntü sınıflandırmaya transformer mimarisini uygulayarak tanıtıldı ve kısa sürede bilgisayarlı görünün baskın paradigması haline geldi. Bu bölümde ViT, Swin Transformer ve DETR mimarilerini teorik temelleri ve uygulamalarıyla inceleyeceğiz.

## Teorik Temel

**Patch Embedding:**
Görüntü $H \times W \times C$ boyutunda. $P \times P$ patch'lere bölünür:
$$N = \frac{HW}{P^2}$$
$N$: patch sayısı. ViT-Base/16 için $P=16$, $224\times224$ görüntüde $N=196$.

Her patch düzleştirilip lineer projeksiyon ile $D$ boyutlu embedding'e dönüştürülür:
$$z_0 = [x_{cls}; x_p^1 E; x_p^2 E; \ldots; x_p^N E] + E_{pos}$$
$E \in \mathbb{R}^{(P^2 C) \times D}$: embedding matrisi, $E_{pos}$: öğrenilebilir pozisyon kodlaması.

**Multi-Head Self-Attention (MHSA):**
$$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
$Q = XW_Q$, $K = XW_K$, $V = XW_V$. $d_k = D/h$ ($h$: kafa sayısı).

Hesaplama karmaşıklığı: $O(N^2 D)$ — büyük görüntülerde yavaş. Swin bunu $O(N w^2 D)$'ye indirir ($w$: pencere boyutu).

**DETR (Detection Transformer):**
CNN backbone + Transformer encoder-decoder + bipartite matching loss.
Macar algoritması ile NMS gerektirmeden set prediction yapar.

**Referanslar:**
- Dosovitskiy et al., "An Image is Worth 16x16 Words", ICLR 2021 (https://arxiv.org/abs/2010.11929)
- Liu et al., "Swin Transformer", ICCV 2021 (https://arxiv.org/abs/2103.14030)
- Carion et al., "End-to-End Object Detection with Transformers (DETR)", ECCV 2020 (https://arxiv.org/abs/2005.12872)

## Pratik Uygulama

```python
import torch
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image

# HuggingFace ViT ile görüntü sınıflandırma
processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")
model.eval()

img = Image.open("resim.jpg").convert("RGB")
if img is None:
    raise FileNotFoundError("resim.jpg bulunamadı")

inputs = processor(images=img, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits

predicted_class = logits.argmax(-1).item()
label = model.config.id2label[predicted_class]
confidence = torch.softmax(logits, dim=-1).max().item()
print(f"Tahmin: {label} ({confidence:.3f})")

# Top-5 tahminler
top5_probs, top5_indices = torch.softmax(logits, dim=-1).topk(5)
print("\nTop-5 Tahminler:")
for prob, idx in zip(top5_probs[0], top5_indices[0]):
    print(f"  {model.config.id2label[idx.item()]}: {prob.item():.4f}")

# Swin Transformer ile transfer learning (özel veri seti için)
from transformers import SwinForImageClassification

# Özel sınıf sayısına göre uyarla
swin = SwinForImageClassification.from_pretrained(
    "microsoft/swin-tiny-patch4-window7-224",
    num_labels=10,
    ignore_mismatched_sizes=True
)
if swin is None:
    raise RuntimeError("Swin modeli yüklenemedi")

print(f"Swin parametre sayısı: {sum(p.numel() for p in swin.parameters()):,}")
```

## Özet & İleri Okuma

- ViT görüntüyü sabit boyutlu patch'lere bölerek NLP transformer'ını görüntüye uygular
- Self-attention global bağlam yakalar; CNN'in lokal önyargısından farklı
- Swin Transformer shifted window ile $O(N^2)$'den $O(N)$'e karmaşıklığı düşürür
- DETR nesne tespitini NMS gerektirmeyen set prediction problemine çevirir
- ViT büyük veri setiyle pre-training gerektirir; küçük veri için Swin tercih edilmeli
- HuggingFace `transformers` kütüphanesi ViT/Swin/DETR modellerini hazır sunar

**İleri Okuma:**
- https://arxiv.org/abs/2010.11929 (ViT)
- https://arxiv.org/abs/2103.14030 (Swin)
- https://huggingface.co/docs/transformers/model_doc/vit
