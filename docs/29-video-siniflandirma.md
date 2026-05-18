# Bölüm 29: Video Sınıflandırma

Bir güvenlik kamerasının yalnızca "düşme" eylemini tespit etmesini istiyorsun. Akla ilk gelen çözüm her kareyi ayrı ayrı sınıflandırmak. Ama tek bir kare sana "birisi oturuyor mu yoksa yeni mi düştü?" sorusunu cevaplayamaz. Eylem, zamanın içinde açılan bir süreçtir — birden fazla kareye yayılır. Bu bölümde videoyu zaman boyutuyla birlikte işlemenin yöntemlerini inceleyeceğiz.

## Neden Video Ayrı Bir Problemdir?

Görüntü sınıflandırmasında girdi H×W×3 boyutunda tek bir karedir. Videoda ise T adet kare ardışık gelir: T×H×W×3. Bu boyut genişlemesi küçük bir teknik detay değil, temel bir zorluk.

Her kare bağımsız sınıflandırılırsa: "futbolcu" görürsün ama "pas mı atıyor, şut mu çekiyor, duruyor mu?" bilmezsin. Zaman boyutu bu soruların cevabını taşır. Dahası, insanlar günlük hayatta zamansal örüntülerle düşünür — "kapı açılıyor", "araba frenleniyor", "el dalgalıyor" tümünde zaman kritiktir.

## 3D Convolution (C3D)

2D konvolüsyon bir H×W uzaysal alana filtre uygular — "bu bölgede kenar var mı?" gibi uzaysal örüntüler öğrenir. 3D konvolüsyon bunu T×H×W'ye genişletir: hem uzay hem zaman boyutunda aynı anda filtre uygular — "bu nesne bu 8 karede nasıl hareket etti?" örüntüsünü öğrenir.

```
2D: filtre boyutu k×k     → uzaysal örüntü
3D: filtre boyutu k×k×k   → uzaysal + zamansal örüntü
```

**Kısıtlama:** 2D konvolüsyona göre parametre sayısı ~k kat artar. C3D modelinin tek bir eğitimi günler sürebilir, bellek ihtiyacı çok yüksektir.

## Two-Stream Networks

İki akış ağı, insan görsel sisteminden ilham alır: nörobilim araştırmaları beyinde iki ayrı görsel yolun olduğunu ortaya koymuştur — "ne var?" ve "nasıl hareket ediyor?". Two-stream ağları da aynı ayrımı yapar.

- **Birinci akış (Spatial/RGB):** Normal video karelerini işler — "ne var?" (nesne, renk, doku)
- **İkinci akış (Temporal/Optik akış):** Ardışık kareler arasındaki piksel hareketi (optik akış) görüntülerini işler — "nasıl hareket ediyor?"

İki akışın tahminleri son aşamada birleştirilir (late fusion). Birisi görünümü, diğeri hareketi kodladığından birlikte daha iyi performans gösterirler.

**Dezavantaj:** Optik akış hesaplama pahalıdır ve ayrı depolanması disk alanı tüketir.

## SlowFast Networks

Beyin farklı frekanslarda işlem yapar. Yavaş işlemler (nesne tanıma, sahne anlama) milisaniye ölçeğinde değişmez. Hızlı işlemler (el çırpma, top hareketi) çok daha kısa zaman dilimlerinde gerçekleşir. SlowFast bu gözlemi doğrudan mimariye yerleştirir.

**Yavaş yol (Slow pathway):**
- Az sayıda kare örnekle (örn. 32 kareden 4 kare = her 8. kare)
- Yüksek uzamsal çözünürlük
- Nesne görünümünü, bağlamı öğrenir
- Yüksek kapasite, çok kanal

**Hızlı yol (Fast pathway):**
- Çok sayıda kare (32 kareden 32 kare = her kare)
- Düşük uzamsal çözünürlük, az kanal (Slow pathway'in 1/8'i)
- Hareketi, zamansal değişimi öğrenir
- Hesaplama maliyeti düşük

İki yol **lateral bağlantılar** ile bilgi paylaşır — Fast yolun hareketi Slow yolun nesne temsilini zenginleştirir.

```python
# Gereksinimler: pip install torch torchvision
import torch

# PyTorch Hub'dan hazır SlowFast modeli
# (Gerçek video inferansı için torchvision>=0.13)
try:
    model = torch.hub.load("facebookresearch/pytorchvideo",
                            "slowfast_r50", pretrained=True)
    model.eval()
    print("SlowFast-R50 yüklendi.")
    print(f"Parametre sayısı: {sum(p.numel() for p in model.parameters()):,}")

    # SlowFast giriş formatı: [slow_clip, fast_clip]
    # slow_clip: (B, C, T_slow, H, W) — örn. (1, 3, 4, 224, 224)
    # fast_clip: (B, C, T_fast, H, W) — örn. (1, 3, 32, 224, 224)
    slow_clip = torch.randn(1, 3, 4, 224, 224)
    fast_clip = torch.randn(1, 3, 32, 224, 224)

    with torch.no_grad():
        output = model([slow_clip, fast_clip])
    print(f"Çıktı boyutu: {output.shape}")  # (1, 400) — Kinetics-400 sınıfı

except Exception as e:
    print(f"Model yükleme hatası: {e}")
    print("Manuel kurulum için: pip install pytorchvideo")
```

## VideoMAE

BERT dil modelinde kelimelerın %15'i maskelenir, model geri kalanından maskeli kelimeleri tahmin etmeyi öğrenir. VideoMAE aynı fikri videoya uygular — ama maskele oranı %90 gibi çok yüksek tutulur.

Neden bu kadar yüksek? Çünkü video kareleri zamansal olarak çok benzerdir — %15 maskelersen model sadece komşu karelerden kopyalayarak öğrenir. %90 maskelerken ağ gerçekten sahnedeki yapıyı anlamak zorunda kalır.

**Maskeleme tüp şeklinde (temporal masking):** Aynı uzaysal konum ardışık karelerde maskelenir. Bu, "zamansal interpolasyon" hilesini engeller.

Az etiketli veriyle güçlü temsil öğrenir (self-supervised pre-training), sonra az etiketle fine-tune edilebilir.

```python
# Gereksinimler: pip install transformers torch av numpy
from transformers import VideoMAEForVideoClassification, VideoMAEImageProcessor
import torch
import numpy as np

model_name = "MCG-NJU/videomae-base-finetuned-kinetics"
processor = VideoMAEImageProcessor.from_pretrained(model_name)
model = VideoMAEForVideoClassification.from_pretrained(model_name)
model.eval()

# VideoMAE 16 kare bekler
# Gerçek uygulamada video dosyasından kare örnekle
# Burada rastgele video simüle ediyoruz
num_frames = 16
height, width = 224, 224

# (num_frames, H, W, C) formatında rastgele video
video_frames = [
    np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    for _ in range(num_frames)
]

# İşle ve tahmin al
inputs = processor(video_frames, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# İlk 3 tahmini göster
probs = torch.softmax(outputs.logits, dim=-1)[0]
top3 = torch.topk(probs, k=3)

print("VideoMAE — İlk 3 eylem tahmini:")
for prob, idx in zip(top3.values, top3.indices):
    label = model.config.id2label[idx.item()]
    print(f"  {label}: {prob.item()*100:.1f}%")
```

> **💡 İpucu:** Gerçek video dosyasından kare örneklemek için `av` (PyAV) kütüphanesi kullan: `pip install av`. `av.open("video.mp4")` ile videoyu aç, eşit aralıklı 16 kare seç.

> **📌 Not:** Kinetics-400 veri seti 400 günlük eylem sınıfı içerir. Model bu sınıflar üzerinde fine-tune edilmiştir. Kendi veri setine uyarlamak için son katmanı değiştir ve fine-tune et.

## Yöntem Karşılaştırması

| Yöntem | Parametre | Kinetics Doğruluğu | Eğitim | Ne Zaman Kullan |
|--------|-----------|-------------------|---------|-----------------|
| **C3D** | ~78M | ~82% Top-1 | Pahalı | Basit eylem tanıma, küçük veri |
| **Two-Stream** | ~2×22M | ~88% Top-1 | Orta | Optik akış hesaplanabiliyorsa |
| **SlowFast-R50** | ~34M | ~77.9% Top-1 (Kinetics-400) | Orta | Hız/doğruluk dengesi önemliyse |
| **VideoMAE-B** | ~87M | ~80.9% Top-1 (Kinetics-400) | Uzun (pre-train) | Az etiketli veri, transfer learning |

> **⚠️ Dikkat:** Video modelleri görüntü modellerinden çok daha fazla bellek tüketir. Batch size 1'den başla, bellek hatasında (OOM) kare sayısını veya çözünürlüğü düşür.

## Özet & İleri Okuma

- Tek kare sınıflandırması, "düşme" gibi zamansal olayları yakalayamaz — zaman boyutu zorunludur.
- **3D Convolution**, uzay ve zamanı aynı anda filtreler; parametre maliyeti yüksektir.
- **Two-Stream ağları** RGB (görünüm) ve optik akış (hareket) akışlarını ayrı işleyerek birleştirir.
- **SlowFast Networks**, yavaş (nesne) ve hızlı (hareket) yollarla beynin ikili görsel sistemini taklit eder.
- **VideoMAE**, %90 maskeleme ile self-supervised pre-training yapar; az etiketle fine-tune edilebilir güçlü temsiller üretir.
- Video modellerini eğitmek/inference yapmak görüntü modellerinden belirgin biçimde daha fazla GPU belleği gerektirir.
- Kinetics-400/600/700 veri setleri video eylem tanıma alanının standart benchmark'larıdır.

### Referanslar

- Tran et al., "Learning Spatiotemporal Features with 3D Convolutional Networks" (ICCV 2015): [https://arxiv.org/abs/1412.0767](https://arxiv.org/abs/1412.0767)
- Simonyan & Zisserman, "Two-Stream Convolutional Networks for Action Recognition in Videos" (NeurIPS 2014): [https://arxiv.org/abs/1406.2199](https://arxiv.org/abs/1406.2199)
- Feichtenhofer et al., "SlowFast Networks for Video Recognition" (ICCV 2019): [https://arxiv.org/abs/1812.01548](https://arxiv.org/abs/1812.01548)
- Tong et al., "VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training" (NeurIPS 2022): [https://arxiv.org/abs/2203.12602](https://arxiv.org/abs/2203.12602)
