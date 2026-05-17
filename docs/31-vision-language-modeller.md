# Vision-Language Modeller: CLIP, LLaVA ve Multimodal AI

Vision-language modeller, görüntü ve metin modalitelerini birlikte işleyerek zero-shot sınıflandırma, görsel soru-cevap ve multimodal akıl yürütme gibi görevleri gerçekleştirir. Bu bölümde CLIP ve LLaVA mimarilerini inceleyeceğiz.

## Teorik Temel

**CLIP (Contrastive Language-Image Pre-training):**
Görüntü encoder $f$ ve metin encoder $g$ ile contrastive learning:
$$\mathcal{L}_{CLIP} = -\frac{1}{N}\sum_{i=1}^N \log \frac{\exp(\text{sim}(f(I_i), g(T_i))/\tau)}{\sum_{j=1}^N \exp(\text{sim}(f(I_i), g(T_j))/\tau)}$$
$\tau$: öğrenilebilir sıcaklık parametresi. 400M (görüntü, metin) çiftinde pre-training.

Zero-shot sınıflandırma: sınıf isimleri prompt olarak girilir, en yüksek cosine benzerliği seçilir.

**LLaVA (Large Language and Vision Assistant):**
Visual encoder (CLIP ViT-L/14) + lineer projeksiyon + LLM (Vicuna/LLaMA).
Görüntü patch'leri token'a dönüştürülüp metin token'larıyla birlikte LLM'e beslenir.
Multi-turn conversation destekler.

**BLIP-2 — Q-Former:**
Sabit image encoder ile LLM arasında öğrenilebilir köprü: 32 query token ile cross-attention.

**Referanslar:**
- Radford et al., "Learning Transferable Visual Models From Natural Language Supervision", ICML 2021 (https://arxiv.org/abs/2103.00020)
- Liu et al., "Visual Instruction Tuning (LLaVA)", NeurIPS 2023 (https://arxiv.org/abs/2304.08485)

## Pratik Uygulama

```python
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# CLIP ile zero-shot sınıflandırma
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
if model is None:
    raise RuntimeError("CLIP modeli yüklenemedi")
model.eval()

img = Image.open("resim.jpg").convert("RGB")

# Sınıf adlarını Türkçe prompt ile dene
siniflar = ["bir kedi", "bir köpek", "bir araba", "bir uçak", "bir insan"]

inputs = processor(text=siniflar, images=img, return_tensors="pt", padding=True)

with torch.no_grad():
    outputs = model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)

print("Zero-shot Sınıflandırma Sonuçları:")
for sinif, prob in zip(siniflar, probs[0]):
    print(f"  {sinif}: {prob.item():.4f}")

en_iyi = siniflar[probs.argmax().item()]
print(f"\nTahmin: {en_iyi}")


# CLIP ile semantik görüntü arama
def get_image_embedding(img_path, model, processor):
    img = Image.open(img_path).convert("RGB")
    if img is None:
        raise FileNotFoundError(f"{img_path} bulunamadı")
    inputs = processor(images=img, return_tensors="pt")
    with torch.no_grad():
        return model.get_image_features(**inputs).squeeze()


def get_text_embedding(text, model, processor):
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    with torch.no_grad():
        return model.get_text_features(**inputs).squeeze()


def cosine_similarity(a, b):
    return torch.dot(a, b) / (a.norm() * b.norm() + 1e-8)


# Kullanım örneği
query_emb = get_text_embedding("bir köpek parkta koşuyor", model, processor)
# img_emb = get_image_embedding("foto.jpg", model, processor)
# benzerlik = cosine_similarity(query_emb, img_emb)
print(f"\nQuery embedding boyutu: {query_emb.shape}")
print("Cosine similarity ile görüntü arama yapılabilir")
```

## Özet & İleri Okuma

- CLIP görüntü-metin çiftlerini contrastive loss ile birlikte eğitir; zero-shot transfer sağlar
- Zero-shot: sınıf listesi prompt olarak verilir, en yüksek cosine benzerliği seçilir
- LLaVA görüntü feature'larını token'a çevirerek LLM'e besler; multimodal chat mümkün
- BLIP-2 Q-Former ile frozen modelleri birleştirerek eğitim maliyetini azaltır
- Sıcaklık parametresi $\tau$ dağılımın keskinliğini kontrol eder; çok küçük → overconfident
- Referans: CLIP (https://arxiv.org/abs/2103.00020), LLaVA (https://arxiv.org/abs/2304.08485)
