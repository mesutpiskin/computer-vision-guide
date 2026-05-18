[Türkçe](./26-vision-transformers.md) | English

# Chapter 26: Vision Transformers

CNNs excel at learning local patterns like edges, textures, and shapes in an image. However, they struggle to capture global context, such as the distant relationship between a "dog's ear" and a "dog's tail." In this chapter, we'll examine how to adapt the Transformer architecture to images and what benefits it brings.

## Attention (Attention Mechanism)

When reading a paper, we don't pay equal attention to every word — when we encounter the word "bank," we look at the surrounding context to understand whether it means financial institution or riverbank. Transformers make this intuitive process mathematical: each element measures its relationship to all other elements and assigns higher weights to important ones.

In images, **self-attention** measures each image patch's relationship with all other patches. It can capture distant context like "if this patch is a dog's nose, then the dog's eye patch is also important."

**Mathematical formula:**

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Think of it this way: $Q$ (Query) asks "what am I looking at?", $K$ (Key) represents "what am I?", and $V$ (Value) represents "what is my content?". $QK^T$ measures the similarity of each query-key pair, dividing by $\sqrt{d_k}$ prevents gradient explosion, and softmax normalizes weights to 0-1 range.

> **📌 Note:** Multi-head attention performs this operation in parallel with multiple "heads" — each head can learn different types of relationships (one learning color similarity, another learning shape relationships).

## ViT (Vision Transformer)

BERT in NLP processes text by dividing it into subword pieces. ViT applies the same idea to images: divide the image into fixed-size patches (16×16) and feed each patch like a "word" to the Transformer.

**How it works:**
1. Divide image into 16×16 pixel patches (224×224 image → 196 patches)
2. Flatten each patch and convert to embedding vector via linear projection
3. Add special `[CLS]` token — a classification token that summarizes the entire image
4. Add positional encoding — so the network knows the patch's location
5. Pass through Transformer encoder blocks
6. Extract classification decision from `[CLS]` token output

> **📌 Note:** ViT outperforms CNNs on large datasets (JFT-300M, ImageNet-21k). On small datasets, CNN is better — ViT lacks the *inductive bias* (local connectivity, translation invariance) and thus needs more data to learn.

```python
# Requirements: pip install transformers Pillow torch torchvision requests
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import torch
import requests

# Load model and processor
model_name = "google/vit-base-patch16-224"
processor = ViTImageProcessor.from_pretrained(model_name)
model = ViTForImageClassification.from_pretrained(model_name)
model.eval()

# Download test image (or use your own)
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

# Process image and get prediction
inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# Print top 5 predictions
logits = outputs.logits
probs = torch.softmax(logits, dim=-1)[0]
top5 = torch.topk(probs, k=5)

print("Top 5 predictions:")
for prob, idx in zip(top5.values, top5.indices):
    label = model.config.id2label[idx.item()]
    print(f"  {label}: {prob.item():.4f} ({prob.item()*100:.1f}%)")
```

Output resembles:

```
Top 5 predictions:
  golden retriever: 0.8234 (82.3%)
  Labrador retriever: 0.0891 (8.9%)
  kuvasz: 0.0213 (2.1%)
  ...
```

The `[CLS]` token's Transformer output encodes relationships between all patches, allowing the model to evaluate global context when making decisions.

## Swin Transformer

ViT has a problem: for N patches, attention computation is $O(N^2)$ complexity. On a 224×224 image, there are 196 patches, manageable; but on a 1024×1024 image, there are 4096 patches and $4096^2 \approx 16.7\text{M}$ operations — computationally infeasible.

**Swin Transformer's solution:** Instead of computing attention over all patches, limit attention computation to small local *windows*. Patches within a window see each other, but not across windows. This reduces complexity to $O(N)$.

But how is information shared across windows? **Shifted window attention**: Between layers, windows are shifted by half a window — patches at boundaries in one layer fall within the same window in the next layer, allowing information to cross boundaries.

**Hierarchical structure:** Swin creates a feature pyramid like CNNs — in deeper layers, patches are merged, reducing resolution and increasing channels. This allows Swin to directly replace CNN backbones.

```python
# Requirements: pip install transformers Pillow torch requests
from transformers import SwinForImageClassification, AutoImageProcessor
from PIL import Image
import torch
import requests

model_name = "microsoft/swin-tiny-patch4-window7-224"
processor = AutoImageProcessor.from_pretrained(model_name)
model = SwinForImageClassification.from_pretrained(model_name)
model.eval()

url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

probs = torch.softmax(outputs.logits, dim=-1)[0]
top3 = torch.topk(probs, k=3)

print("Swin Transformer predictions:")
for prob, idx in zip(top3.values, top3.indices):
    label = model.config.id2label[idx.item()]
    print(f"  {label}: {prob.item()*100:.1f}%")
```

> **💡 Tip:** Swin-T (tiny) → Swin-S (small) → Swin-B (base) → Swin-L (large) variants exist. Start with Swin-T for production, upgrade if needed.

## DETR (Detection Transformer)

Classical object detection has two annoying components: *anchor box* design for generating object candidates and *Non-Maximum Suppression (NMS)* for removing overlapping boxes. DETR eliminates both.

DETR solves object detection as a **sequence-to-sequence** problem: give the image to a Transformer, get object boxes and class predictions directly. It matches "100 object queries" with the image using attention mechanism to produce predictions.

**Bipartite matching:** During training, predictions are matched to ground-truth boxes using the Hungarian algorithm. One-to-one matching — NMS is unnecessary.

```python
# Requirements: pip install transformers Pillow torch timm requests
from transformers import DetrForObjectDetection, DetrImageProcessor
from PIL import Image
import torch
import requests

model_name = "facebook/detr-resnet-50"
processor = DetrImageProcessor.from_pretrained(model_name)
model = DetrForObjectDetection.from_pretrained(model_name)
model.eval()

# Example image from COCO dataset
url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# Show detections above threshold
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(
    outputs, target_sizes=target_sizes, threshold=0.9
)[0]

print(f"Detected objects: {len(results['labels'])}")
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    label_name = model.config.id2label[label.item()]
    box_coords = [round(c, 1) for c in box.tolist()]
    print(f"  {label_name}: {score.item():.3f} — box: {box_coords}")
```

> **⚠️ Warning:** DETR converges slowly during training (may need 300 epochs) and lags behind classical detectors on small objects. Deformable DETR addresses these issues significantly.

## CNN vs ViT Comparison

| Feature | CNN | ViT | Swin |
|---------|-----|-----|------|
| **Data requirement** | Low-medium (1k+ examples) | High (100k+ recommended) | Medium (close to CNN) |
| **Inductive bias** | Strong (locality, translation invariance) | Weak (learned from data) | Medium (local windows) |
| **Training time** | Fast | Slow | Medium |
| **Global context** | Limited (deeper layers) | Full (every layer) | Semi-local |
| **Transfer learning** | Excellent (small data) | Excellent (large data) | Excellent (all scales) |
| **Computational complexity** | $O(N)$ | $O(N^2)$ | $O(N)$ |
| **Backbone usage** | Yes | Difficult | Yes |

> **📌 Note:** Practical recommendation: <10k images, start with ResNet/EfficientNet. Large dataset, try ViT or Swin. For object detection and segmentation, Swin backbone is an excellent choice.

## Summary & Further Reading

- **Self-attention** directly models distant relationships between patches — no need for CNN's layer-by-layer receptive field growth.
- **ViT** divides image into 16×16 patches and applies NLP Transformer directly to images; outperforms CNNs on large datasets.
- **[CLS] token** carries global representation of the entire image; classification decision comes from here.
- **Positional encoding** tells the network the patch's location in the image — without it, the Transformer doesn't know where patches are.
- **Swin Transformer** reduces $O(N^2)$ complexity to $O(N)$ via local window attention and can replace CNN backbones via hierarchical structure.
- **DETR** converts object detection to sequence-to-sequence, eliminating anchor boxes and NMS.
- CNN and ViT aren't mutual competitors — CNN better on small data, ViT/Swin better on large data; most modern systems combine both.

### References

- Dosovitskiy et al., "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale" (ICLR 2021): [https://arxiv.org/abs/2010.11929](https://arxiv.org/abs/2010.11929)
- Liu et al., "Swin Transformer: Hierarchical Vision Transformer using Shifted Windows" (ICCV 2021): [https://arxiv.org/abs/2103.14030](https://arxiv.org/abs/2103.14030)
- Carion et al., "End-to-End Object Detection with Transformers" (ECCV 2020): [https://arxiv.org/abs/2005.12872](https://arxiv.org/abs/2005.12872)
