# Bölüm 26: Vision Transformers

CNN'ler bir görüntüdeki kenar, doku ve şekil gibi yerel örüntüleri çok iyi öğrenir. Ancak "köpek kulağı" ile "köpek kuyruğu" arasındaki uzak bölge ilişkisi gibi global bağlamı yakalamakta zorlanırlar. Bu bölümde Transformer mimarisini görüntülere nasıl uyarlayabileceğimizi ve bunun bize ne kazandırdığını inceleyeceğiz.

## Attention (Dikkat) Mekanizması

Bir makale okurken her kelimeye eşit dikkat vermeyiz — "banka" kelimesini gördüğümüzde, cümlenin geri kalanına bakarak para mı yoksa nehir kenarı mı olduğunu anlarız. Transformer bu sezgisel süreci matematiksel hale getirir: her öğe, diğer tüm öğelerle ilişkisini ölçer ve önemli olanlara daha fazla ağırlık verir.

Görüntülerde **self-attention**, her görüntü yamasının diğer tüm yamalarla ilişkisini ölçer. "Bu yama köpek burnuysa, köpek gözü yaması da önemlidir" gibi uzak bağlamları yakalayabilir.

**Matematiksel formül:**

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Burada $Q$ (Query/Soru), $K$ (Key/Anahtar) ve $V$ (Value/Değer) matrislerini şöyle düşün: $Q$ "neye bakıyorum?", $K$ "ben neyim?", $V$ "benim içeriğim ne?" sorularını temsil eder. $QK^T$ her soru-anahtar çiftinin benzerliğini ölçer, $\sqrt{d_k}$ bölümü gradyanların patlamasını önler, softmax ağırlıkları 0-1 arasına normalize eder.

> **📌 Not:** Multi-head attention, bu işlemi paralel birden fazla "kafa" ile yapar — her kafa farklı tür ilişkileri öğrenebilir (biri renk benzerliğini, diğeri şekil ilişkisini).

## ViT (Vision Transformer)

NLP'deki BERT modeli, metni kelime parçalarına bölerek işler. ViT aynı fikri görüntülere uygular: görüntüyü sabit boyutlu yamalar (patch) halinde keser ve her yamayı bir "kelime" gibi Transformer'a besler.

**Nasıl çalışır:**
1. Görüntüyü 16×16 piksellik yamalara böl (224×224 görüntü → 196 yama)
2. Her yamayı düzleştir ve doğrusal projeksiyon ile embedding vektörüne dönüştür
3. Özel `[CLS]` tokeni ekle — tüm görüntüyü özetleyen sınıflandırma tokeni
4. Pozisyonel encoding ekle — ağ yamanın konumunu bilsin
5. Transformer encoder bloklarından geçir
6. `[CLS]` token çıktısından sınıflandırma yap

> **📌 Not:** ViT büyük veri setlerinde (JFT-300M, ImageNet-21k) CNN'leri geçiyor. Küçük veri setlerinde CNN daha iyi — ViT'in öğrenmesi gereken *inductive bias* yok (yerel bağlantı, öteleme değişmezliği), dolayısıyla daha fazla veriye ihtiyaç duyuyor.

```python
# Gereksinimler: pip install transformers Pillow torch torchvision requests
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import torch
import requests

# Model ve işlemciyi yükle
model_name = "google/vit-base-patch16-224"
processor = ViTImageProcessor.from_pretrained(model_name)
model = ViTForImageClassification.from_pretrained(model_name)
model.eval()

# Test görüntüsü indir (ya da kendi görüntünü kullan)
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

# Görüntüyü işle ve tahmin al
inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# İlk 5 tahmini yazdır
logits = outputs.logits
probs = torch.softmax(logits, dim=-1)[0]
top5 = torch.topk(probs, k=5)

print("İlk 5 tahmin:")
for prob, idx in zip(top5.values, top5.indices):
    label = model.config.id2label[idx.item()]
    print(f"  {label}: {prob.item():.4f} ({prob.item()*100:.1f}%)")
```

Çıktı şuna benzer:

```
İlk 5 tahmin:
  golden retriever: 0.8234 (82.3%)
  Labrador retriever: 0.0891 (8.9%)
  kuvasz: 0.0213 (2.1%)
  ...
```

`[CLS]` tokeninin Transformer çıktısı, tüm yamalar arasındaki ilişkileri kodladığından model global bağlamı değerlendirerek karar verir.

## Swin Transformer

ViT'in bir sorunu var: N yama için $O(N^2)$ karmaşıklıkta attention hesaplanır. 224×224 görüntüde 196 yama var, bu yönetilebilir; ama 1024×1024 görüntüde 4096 yama olur ve $4096^2 \approx 16.7\text{M}$ işlem gerekir — pratikte kullanılamaz hale gelir.

**Swin Transformer'ın çözümü:** Tüm yamalar yerine, attention hesaplamasını küçük yerel *pencerelere* (window) sınırla. Her pencere içindeki yamalar birbirini görür, pencereler arası değil. Bu $O(N)$ karmaşıklığa düşürür.

Peki pencereler arası bilgi nasıl aktarılır? **Shifted window attention**: Katmanlar arasında pencereler yarım pencere kaydırılır — önceki katmanda sınırda kalan yamalar, sonraki katmanda aynı pencereye düşer ve bilgi sınırı aşar.

**Hiyerarşik yapı:** Swin, CNN gibi özellik piramidi oluşturur — derin katmanlarda yamalar birleştirilerek çözünürlük düşer, kanal sayısı artar. Bu yapı Swin'i doğrudan CNN yerine backbone olarak kullanmayı mümkün kılar.

```python
# Gereksinimler: pip install transformers Pillow torch requests
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

print("Swin Transformer tahminleri:")
for prob, idx in zip(top3.values, top3.indices):
    label = model.config.id2label[idx.item()]
    print(f"  {label}: {prob.item()*100:.1f}%")
```

> **💡 İpucu:** Swin-T (tiny) → Swin-S (small) → Swin-B (base) → Swin-L (large) seçenekleri var. Prodüksiyona başlarken Swin-T ile başla, gerekirse büyük versiyona geç.

## DETR (Detection Transformer)

Klasik nesne tespitinde iki can sıkıcı bileşen var: nesne adayı üretmek için *anchor box* tasarımı ve örtüşen kutuları elemek için *Non-Maximum Suppression (NMS)*. DETR bunların ikisini de kaldırır.

DETR nesne tespitini bir **sequence-to-sequence** problemi olarak çözer: görüntüyü Transformer'a ver, doğrudan nesne kutusu ve sınıf tahminleri al. "100 nesne sorgusunu" attention mekanizması ile görüntüyle eşleştirerek tahminler üretir.

**Bipartite matching:** Eğitim sırasında tahminleri gerçek kutularla eşleştirmek için Macar algoritması kullanılır. "Tahmin 7 gerçek kutu 3'e en iyi uyuyor" gibi birebir eşleştirme yapar — NMS gerekmez.

```python
# Gereksinimler: pip install transformers Pillow torch timm requests
from transformers import DetrForObjectDetection, DetrImageProcessor
from PIL import Image
import torch
import requests

model_name = "facebook/detr-resnet-50"
processor = DetrImageProcessor.from_pretrained(model_name)
model = DetrForObjectDetection.from_pretrained(model_name)
model.eval()

# COCO veri setinden örnek görüntü
url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# Eşiği geç nesneleri göster
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(
    outputs, target_sizes=target_sizes, threshold=0.9
)[0]

print(f"Tespit edilen nesne sayısı: {len(results['labels'])}")
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    label_name = model.config.id2label[label.item()]
    box_coords = [round(c, 1) for c in box.tolist()]
    print(f"  {label_name}: {score.item():.3f} — kutu: {box_coords}")
```

> **⚠️ Dikkat:** DETR eğitim sürecinde yavaş yakınsıyor (300 epoch gerekebilir) ve küçük nesnelerde klasik dedektörlerin gerisinde kalıyor. Deformable DETR bu sorunları büyük ölçüde gidermiştir.

## CNN vs ViT Karşılaştırması

| Özellik | CNN | ViT | Swin |
|---------|-----|-----|------|
| **Veri ihtiyacı** | Az-orta (1k+ örnek) | Yüksek (100k+ önerilir) | Orta (CNN'e yakın) |
| **Inductive bias** | Güçlü (yerellik, öteleme değişmezliği) | Zayıf (veriden öğrenir) | Orta (yerel pencere) |
| **Eğitim süresi** | Hızlı | Yavaş | Orta |
| **Global bağlam** | Sınırlı (derin katmanlarda) | Tam (her katmanda) | Yarı-yerel |
| **Transfer learning** | Çok iyi (küçük veri) | Çok iyi (büyük veri) | Çok iyi (her ölçek) |
| **Hesaplama karmaşıklığı** | $O(N)$ | $O(N^2)$ | $O(N)$ |
| **Backbone olarak kullanım** | Evet | Zor | Evet |

> **📌 Not:** Pratik öneri: <10k görüntü varsa ResNet/EfficientNet ile başla. Büyük veri setinde ViT veya Swin dene. Nesne tespiti ve segmentasyon için Swin backbone mükemmel seçim.

## Özet & İleri Okuma

- **Self-attention**, görüntüdeki her yama ile diğer yamalar arasındaki uzak mesafeli ilişkileri doğrudan modeller — CNN'in katman katman büyüyen alıcı alanına ihtiyaç duymaz.
- **ViT**, görüntüyü 16×16 yamalara bölerek NLP Transformer'ını doğrudan görüntüye uygular; büyük veri setlerinde CNN'leri geçer.
- **[CLS] tokeni** tüm görüntünün global temsilini taşır; sınıflandırma kararı buradan alınır.
- **Pozisyonel encoding** yamanın görüntüdeki konumunu ağa bildirir — olmadan Transformer yamaların nerede olduğunu bilemez.
- **Swin Transformer**, yerel pencere attention ile $O(N^2)$ karmaşıklığını $O(N)$'e düşürür ve hiyerarşik yapısıyla CNN backbone'un yerini alabilir.
- **DETR**, nesne tespitini sequence-to-sequence problemine dönüştürerek anchor box ve NMS'i ortadan kaldırır.
- CNN ve ViT karşılıklı rakip değil — küçük veride CNN, büyük veride ViT/Swin daha iyi; çoğu modern sistem ikisini birleştirir.

### Referanslar

- Dosovitskiy et al., "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale" (ICLR 2021): [https://arxiv.org/abs/2010.11929](https://arxiv.org/abs/2010.11929)
- Liu et al., "Swin Transformer: Hierarchical Vision Transformer using Shifted Windows" (ICCV 2021): [https://arxiv.org/abs/2103.14030](https://arxiv.org/abs/2103.14030)
- Carion et al., "End-to-End Object Detection with Transformers" (ECCV 2020): [https://arxiv.org/abs/2005.12872](https://arxiv.org/abs/2005.12872)
