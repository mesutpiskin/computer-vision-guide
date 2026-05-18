# Bölüm 31: Vision-Language Modeller

Bir e-ticaret sitesinde kullanıcı "kırmızı spor ayakkabı" yazar ve sistem binlerce ürün fotoğrafından eşleşenleri getirir — ama hiçbir fotoğrafa "kırmızı spor ayakkabı" etiketi elle girilmemiştir. Ya da görme engelli bir kullanıcı için yüklenen her fotoğraf otomatik olarak Türkçe açıklanır. Bu görevler tek başına ne görüntü ne de dil modeliyle çözülebilir. Bu bölümde her iki modaliteyi birleştiren modelleri inceleyeceğiz.

## Neden Multimodal?

Görüntü modeli görseli anlar ama "bu nedir?" sorusunu metin olarak cevaplayamaz. Dil modeli metni anlar ama bir fotoğrafa bakamaz. Vision-Language modeller iki modaliteyi aynı vektör uzayına yerleştirerek "bu görüntü bu metinle ne kadar uyuşuyor?" sorusunu cevaplayabilir hale gelir.

Bu yetenek şaşırtıcı bir kapı aralar: hiç görmediği sınıfları, sadece metin açıklamasıyla tanıyabilir — **zero-shot** (sıfır örnek) sınıflandırma.

## CLIP (Contrastive Language-Image Pre-Training)

400 milyon görüntü-metin çiftiyle eğitilmiş. Model, "kedi fotoğrafı" yazısıyla gerçek kedi fotoğrafını aynı vektör uzayında yakın noktalara yerleştirmeyi öğrendi. Alakasız çiftler uzak noktalara gider.

**Çift kule mimarisi (dual encoder):**
- **Görüntü encoder (ViT):** Görüntüyü sabit boyutlu vektöre dönüştürür → $f_I$
- **Metin encoder (Transformer):** Metni sabit boyutlu vektöre dönüştürür → $f_T$
- Her iki encoder bağımsız çalışır, aynı boyutlu çıktı üretir

**Benzerlik ölçümü:**

$$\text{sim}(I, T) = \frac{f_I \cdot f_T}{\|f_I\| \cdot \|f_T\|}$$

Bu kosinüs benzerliğidir — iki vektörün açısını ölçer. 1 = mükemmel eşleşme, 0 = ilgisiz.

**Eğitim:** Bir batch'te N görüntü-metin çifti var. Doğru eşleşmelerin benzerliği yükselsin, yanlış eşleşmeler düşsün. Bu **contrastive loss** ile sağlanır.

**Zero-shot sınıflandırma:** Eğitim gerekmez — sınıf isimlerini metne çevir, görüntüye en yakın metni bul.

```python
# Gereksinimler: pip install transformers Pillow torch requests
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import requests

model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)
model.eval()

# Test görüntüsü
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

# Sınıf adayları — bunları hiç eğitmeden sınıflandırabiliriz
candidate_labels = [
    "a photo of a dog",
    "a photo of a cat",
    "a photo of a car",
    "a photo of a bird",
    "a photo of a person"
]

inputs = processor(
    text=candidate_labels,
    images=image,
    return_tensors="pt",
    padding=True
)

with torch.no_grad():
    outputs = model(**inputs)

# Logit'ler görüntü-metin benzerlik puanları
logits = outputs.logits_per_image  # (1, num_labels)
probs = torch.softmax(logits, dim=-1)[0]

print("Zero-shot sınıflandırma sonuçları:")
for label, prob in sorted(zip(candidate_labels, probs), key=lambda x: x[1], reverse=True):
    print(f"  {label}: {prob.item()*100:.1f}%")
```

> **💡 İpucu:** `"A photo of a {label}"` şablonu, doğrudan etiket adından daha iyi çalışır. "Labrador" yerine "a photo of a Labrador dog" daha yüksek doğruluk sağlar. Bu prompt engineering denen ince bir sanattır.

**Anlamsal görüntü arama (semantic search):**

```python
# Gereksinimler: pip install transformers Pillow torch numpy
import numpy as np
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model.eval()

def encode_image(image: Image.Image) -> np.ndarray:
    """Görüntüyü CLIP özellik vektörüne dönüştür."""
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        features = model.get_image_features(**inputs)
    features = features / features.norm(dim=-1, keepdim=True)
    return features.cpu().numpy()[0]

def encode_text(text: str) -> np.ndarray:
    """Metni CLIP özellik vektörüne dönüştür."""
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    with torch.no_grad():
        features = model.get_text_features(**inputs)
    features = features / features.norm(dim=-1, keepdim=True)
    return features.cpu().numpy()[0]

# Kullanım: görüntü veritabanını encode et, sorgu ile kosinüs benzerliği hesapla
query = "a red sports car"
query_vec = encode_text(query)
# image_vectors = [encode_image(img) for img in image_database]
# similarities = [np.dot(query_vec, iv) for iv in image_vectors]
# En yüksek benzerlikli görüntüleri getir

print(f"Sorgu vektörü boyutu: {query_vec.shape}")
print("Sorgu encode edildi. Görüntü veritabanıyla benzerlik hesaplanabilir.")
```

## LLaVA (Large Language and Vision Assistant)

CLIP görüntü ile metni aynı uzaya koyuyor ama yalnızca kısa metin embedding üretebiliyor — uzun, çok adımlı yanıtlar veremez. LLaVA şu soruyu soruyor: CLIP'in görsel özelliklerini bir büyük dil modeline (Llama, Vicuna) bağlasak ne olur?

**Mimari:**
1. CLIP görüntü encoder → görsel özellik vektörleri
2. Doğrusal projeksiyon katmanı (lineer adapter) → dil modeli boyutuna hizala
3. Büyük dil modeli (Llama/Vicuna) → görsel + metin tokenlerini birlikte işle → metin üret

Sonuç: Görüntü hakkında konuşabilen, soru cevaplayabilen, açıklama yazabilen bir model.

```python
# Gereksinimler: pip install transformers Pillow torch requests
# Not: llava-1.5-7b-hf ~14GB RAM gerektirir. GPU önerilir.
from transformers import LlavaForConditionalGeneration, AutoProcessor
from PIL import Image
import torch
import requests

model_id = "llava-hf/llava-1.5-7b-hf"

# Bellek kısıtı varsa 4-bit quantization
try:
    from transformers import BitsAndBytesConfig
    quantization_config = BitsAndBytesConfig(load_in_4bit=True)
    model = LlavaForConditionalGeneration.from_pretrained(
        model_id, quantization_config=quantization_config
    )
except Exception:
    # 4-bit yoksa float16
    model = LlavaForConditionalGeneration.from_pretrained(
        model_id, torch_dtype=torch.float16
    )

processor = AutoProcessor.from_pretrained(model_id)

# Görüntü ve soru
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

# LLaVA konuşma formatı
conversation = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "Bu görüntüde ne görüyorsun? Köpeğin ırkını ve ruh halini açıkla."}
        ]
    }
]

prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
inputs = processor(images=image, text=prompt, return_tensors="pt")

with torch.no_grad():
    output = model.generate(**inputs, max_new_tokens=200, do_sample=False)

response = processor.decode(output[0], skip_special_tokens=True)
# Sadece asistan yanıtını çıkar
answer = response.split("ASSISTANT:")[-1].strip()
print(f"LLaVA yanıtı:\n{answer}")
```

> **⚠️ Dikkat:** LLaVA-7B modeli yaklaşık 14GB GPU belleği gerektirir. Küçük GPU için `llava-hf/llava-1.5-7b-hf` ile 4-bit quantization, ya da bulut servisleri (HuggingFace Inference API) kullan.

## BLIP-2

LLaVA doğrudan projeksiyon katmanı kullanırken, BLIP-2 daha sofistike bir köprü kurar: **Q-Former (Querying Transformer)**.

Q-Former, öğrenilebilir sorgu tokenleri ile görüntü özelliklerinden en önemli bilgiyi süzerek dil modeline iletir. Bu "bilgi damıtma" katmanı sayesinde BLIP-2 farklı dil modelleri (OPT, FlanT5) ile kolayca birleştirilebilir.

```python
# Gereksinimler: pip install transformers Pillow torch requests
from transformers import Blip2ForConditionalGeneration, Blip2Processor
from PIL import Image
import torch
import requests

model_name = "Salesforce/blip2-opt-2.7b"
device = "cuda" if torch.cuda.is_available() else "cpu"

processor = Blip2Processor.from_pretrained(model_name)
model = Blip2ForConditionalGeneration.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)
model.eval()

url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

# Görüntü açıklaması üret (caption)
inputs = processor(images=image, return_tensors="pt").to(device, torch.float16
         if device == "cuda" else torch.float32)

with torch.no_grad():
    generated_ids = model.generate(**inputs, max_new_tokens=50)

caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
print(f"BLIP-2 açıklama: {caption}")

# Görsel soru cevaplama
question = "What breed is the dog?"
inputs_vqa = processor(images=image, text=question, return_tensors="pt").to(
    device, torch.float16 if device == "cuda" else torch.float32
)

with torch.no_grad():
    generated_ids = model.generate(**inputs_vqa, max_new_tokens=30)

answer = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
print(f"Soru: {question}")
print(f"BLIP-2 yanıtı: {answer}")
```

> **📌 Not:** BLIP-2 görüntü açıklaması (captioning) ve kısa yanıtlı soru-cevap (VQA) için güçlüdür. Uzun diyalog ve çok adımlı akıl yürütme için LLaVA daha uygundur.

## Kullanım Senaryoları

**Görüntüyle arama:** Binlerce ürün fotoğrafını CLIP ile encode et, kullanıcı sorgusunu metin olarak encode et, en yakın görüntüleri getir. Etiket gerektirmez.

**Erişilebilirlik:** Görme engelli kullanıcılar için BLIP-2 veya LLaVA ile yüklenen her fotoğrafa otomatik açıklama üret.

**Tıbbi görüntü raporlama:** Radyoloji görüntüsünü alan ve birincil bulgular için taslak rapor üreten asistan sistemler (son karar her zaman uzman hekime bırakılmalıdır).

**İçerik moderasyonu:** CLIP ile "şiddet içerikli görüntü", "uygunsuz içerik" gibi kategorilerle zero-shot sınıflandırma.

**E-ticaret:** Ürün fotoğrafından otomatik başlık, kategori, özellik listesi üretimi.

## Yöntem Karşılaştırması

| Model | Birincil Görev | GPU Belleği | Hız | Güçlü Yön |
|-------|---------------|-------------|-----|-----------|
| **CLIP ViT-B/32** | Zero-shot sınıflama, arama | ~1 GB | Çok hızlı | Büyük ölçekli arama, sınıflandırma |
| **CLIP ViT-L/14** | Zero-shot (yüksek doğruluk) | ~3 GB | Hızlı | Daha iyi doğruluk |
| **BLIP-2 (2.7B)** | Caption, VQA | ~6 GB | Orta | Kısa yanıt, açıklama |
| **LLaVA-1.5-7B** | Çok dönüşlü sohbet, VQA | ~14 GB | Yavaş | Uzun açıklama, diyalog |

## Özet & İleri Okuma

- **CLIP**, 400 milyon görüntü-metin çiftiyle contrastive learning ile eğitilmiştir; görüntü ve metin aynı vektör uzayına yerleştirilir.
- **Zero-shot sınıflandırma**, sınıf isimlerini metin şablonuna sokarak eğitimsiz sınıflandırmayı mümkün kılar — "A photo of a {label}" şablonu güçlü sonuç verir.
- **Kosinüs benzerliği** ile görüntü-metin eşleşme skoru hesaplanır; semantik görüntü aramanın temelidir.
- **LLaVA**, CLIP görsel özelliklerini büyük dil modeline bağlayarak uzun metin yanıtları ve çok dönüşlü diyalogu mümkün kılar.
- **BLIP-2** Q-Former köprüsüyle görüntü açıklaması ve kısa VQA görevlerinde güçlü performans gösterir.
- Vision-language modeller erişilebilirlik, e-ticaret, tıbbi raporlama ve içerik moderasyonu alanlarında pratik değer üretir.
- Bu alandaki gelişmeler hız kesmeden devam ediyor: GPT-4o, Gemini, Claude gibi modeller görüntü anlama yeteneklerini doğrudan temel modele entegre ediyor.

### Referanslar

- Radford et al., "Learning Transferable Visual Models From Natural Language Supervision" (ICML 2021): [https://arxiv.org/abs/2103.00020](https://arxiv.org/abs/2103.00020)
- Liu et al., "Visual Instruction Tuning" / LLaVA (NeurIPS 2023): [https://arxiv.org/abs/2304.08485](https://arxiv.org/abs/2304.08485)
- Li et al., "BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models" (ICML 2023): [https://arxiv.org/abs/2301.12597](https://arxiv.org/abs/2301.12597)
