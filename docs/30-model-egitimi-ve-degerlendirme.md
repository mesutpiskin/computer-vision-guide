# Bölüm 30: Model Eğitimi ve Değerlendirme

Fabrikadaki üretim hattında 5 farklı ürün türünü kameradan otomatik tanımak istiyorsun. ImageNet'te bu ürünler yok. Kaggle'da hazır veri seti yok. Kendi veri setini toplamalı, etiketlemeli, modeli eğitmeli ve doğru metrikleri seçerek değerlendirmelisin. Bu bölümde bu sürecin her adımını ele alacağız.

## Veri Seti Hazırlama

Makine öğrenmesinde bir kural var: çöp girdi, çöp çıktı (*garbage in, garbage out*). Ne kadar güçlü model seçersen seç, kötü veri ile iyi sonuç alınamaz. Veri kalitesine yatırım, model karmaşıklığına yatırımdan her zaman daha verimlidir.

**Klasör yapısı (PyTorch ImageFolder standartı):**

```
dataset/
  train/
    urun_a/  img001.jpg  img002.jpg  ...
    urun_b/  img001.jpg  ...
    urun_c/  ...
  val/
    urun_a/  ...
    urun_b/  ...
  test/
    urun_a/  ...
    urun_b/  ...
```

Klasör adları otomatik olarak sınıf etiketi olur — ayrı etiket dosyası gerekmez.

**Etiketleme araçları:**
- **LabelImg:** Masaüstü uygulama, bounding box etiketleme (YOLO/VOC formatı)
- **Roboflow:** Web tabanlı, ekip çalışması, format dönüşümü, augmentation dahil
- **CVAT:** Açık kaynak, video ve görüntü, segmentasyon desteği

> **💡 İpucu:** Her sınıf için en az 100-200 örnek topla. Sınıflar arası dengesizlik varsa (sınıf A 500, sınıf B 50 görüntü) oversampling veya class weight ile dengele. Val seti %15-20 oranında, test seti %10-15 olmalı.

## Veri Artırma (Data Augmentation)

500 fotoğraf aldın ama model ezberliyor — overfitting var. Çözüm: Her görüntüden farklı dönüşümlerle yeni eğitim örnekleri üret. Model aynı nesneyi farklı açılardan, aydınlatmalardan, boyutlardan görmüş gibi öğrenir.

```python
# Gereksinimler: pip install torch torchvision
import torch
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms

# Eğitim için agresif augmentation
train_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomCrop(224),               # Rastgele 224×224 kırp
    transforms.RandomHorizontalFlip(p=0.5),   # %50 yatay çevir
    transforms.RandomVerticalFlip(p=0.1),     # %10 dikey çevir (ürüne göre ayarla)
    transforms.RandomRotation(degrees=15),    # ±15 derece döndür
    transforms.ColorJitter(
        brightness=0.3,
        contrast=0.3,
        saturation=0.2,
        hue=0.1
    ),
    transforms.RandomGrayscale(p=0.05),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  # ImageNet ortalamaları
        std=[0.229, 0.224, 0.225]
    )
])

# Val/Test için minimal dönüşüm — augmentation yok!
val_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Veri seti yükle
train_dataset = torchvision.datasets.ImageFolder(
    root="dataset/train", transform=train_transforms
)
val_dataset = torchvision.datasets.ImageFolder(
    root="dataset/val", transform=val_transforms
)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True,
                          num_workers=4, pin_memory=True)
val_loader   = DataLoader(val_dataset,   batch_size=32, shuffle=False,
                          num_workers=4, pin_memory=True)

print(f"Eğitim örnekleri: {len(train_dataset)}")
print(f"Sınıflar: {train_dataset.classes}")
print(f"Sınıf → indeks: {train_dataset.class_to_idx}")
```

**Mixup:** İki görüntüyü $\lambda$ ağırlıkla karıştır, etiketi de aynı oranda karıştır. Model belirsiz sınır bölgelerini daha iyi öğrenir.

$$\tilde{x} = \lambda x_i + (1-\lambda) x_j, \quad \tilde{y} = \lambda y_i + (1-\lambda) y_j$$

```python
def mixup_batch(images, labels, alpha=0.4):
    """Bir batch'e Mixup augmentation uygula."""
    lam = torch.distributions.Beta(alpha, alpha).sample().item()
    batch_size = images.size(0)
    idx = torch.randperm(batch_size)
    mixed_images = lam * images + (1 - lam) * images[idx]
    return mixed_images, labels, labels[idx], lam
```

> **⚠️ Dikkat:** Augmentation yalnızca eğitim verisine uygulanır. Val ve test setlerinde augmentation kullanmak ölçümü bozar.

## Transfer Learning

ImageNet'te 1000 farklı sınıf üzerinde eğitilmiş ResNet, kenar, doku, şekil, renk gradyanı gibi genel görsel özellikleri bilir. Bu öğrenilmiş özellikleri senin veri setine uyarlamak, sıfırdan eğitmekten 10-100 kat daha az veri ve süre gerektirir. Biyolojide buna benzetme yapabiliriz: İnsan matematik öğrenirken sayıları sıfırdan icat etmek zorunda kalmıyor.

**İki temel strateji:**

1. **Feature extraction (özellik çıkarma):** Backbone'u tamamen dondur, yalnızca yeni son katmanı eğit. Az veri, hızlı eğitim istiyorsan.

2. **Fine-tuning (ince ayar):** Tüm ağı düşük learning rate ile eğit — backbone yavaş değişir, son katmanlar hızlı adapte olur. Orta/fazla veri varsa.

```python
# Gereksinimler: pip install torch torchvision
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import torchvision

# --- Veri ---
train_transforms = transforms.Compose([
    transforms.Resize(256), transforms.RandomCrop(224),
    transforms.RandomHorizontalFlip(), transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
val_transforms = transforms.Compose([
    transforms.Resize(256), transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# CIFAR-10 ile demo (kendi verinle dataset/train yolunu kullan)
train_set = torchvision.datasets.CIFAR10(root="./data", train=True,
                                          download=True, transform=train_transforms)
val_set   = torchvision.datasets.CIFAR10(root="./data", train=False,
                                          download=True, transform=val_transforms)
train_loader = DataLoader(train_set, batch_size=64, shuffle=True, num_workers=2)
val_loader   = DataLoader(val_set,   batch_size=64, shuffle=False, num_workers=2)
num_classes  = 10

# --- Model: ResNet50 fine-tuning ---
device = "cuda" if torch.cuda.is_available() else "cpu"
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

# Son katmanı değiştir — çıkış boyutu num_classes'a ayarla
in_features = model.fc.in_features
model.fc = nn.Sequential(
    nn.Dropout(p=0.3),
    nn.Linear(in_features, num_classes)
)
model = model.to(device)

# Öğrenme hızı farkı: backbone için küçük, yeni katman için büyük
backbone_params = [p for n, p in model.named_parameters() if "fc" not in n]
head_params     = list(model.fc.parameters())

optimizer = optim.AdamW([
    {"params": backbone_params, "lr": 1e-4},  # Backbone yavaş
    {"params": head_params,     "lr": 1e-3},  # Head hızlı
], weight_decay=1e-4)

scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=20)
criterion = nn.CrossEntropyLoss()

# --- Eğitim fonksiyonu ---
def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss, correct, total = 0.0, 0, 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * images.size(0)
        correct += (outputs.argmax(dim=1) == labels).sum().item()
        total += labels.size(0)
    return total_loss / total, correct / total

# --- Değerlendirme fonksiyonu ---
def eval_epoch(model, loader, criterion, device):
    model.eval()
    total_loss, correct, total = 0.0, 0, 0
    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            total_loss += loss.item() * images.size(0)
            correct += (outputs.argmax(dim=1) == labels).sum().item()
            total += labels.size(0)
    return total_loss / total, correct / total

# --- Eğitim döngüsü ---
best_val_acc = 0.0
patience, patience_counter = 5, 0

for epoch in range(1, 21):
    train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion, device)
    val_loss,   val_acc   = eval_epoch(model, val_loader, criterion, device)
    scheduler.step()

    print(f"Epoch {epoch:2d}/20 | "
          f"Train: loss={train_loss:.4f} acc={train_acc:.4f} | "
          f"Val: loss={val_loss:.4f} acc={val_acc:.4f}")

    # En iyi modeli kaydet
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), "best_model.pth")
        patience_counter = 0
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print(f"Early stopping — val accuracy {patience} epoch boyunca iyileşmedi.")
            break

print(f"En iyi val accuracy: {best_val_acc:.4f}")
```

## Eğitim Stratejileri

**Learning rate seçimi:**
- Çok büyük → kayıp salınır, ağırlıklar kararsızlaşır
- Çok küçük → yavaş öğrenme, lokal minimumda takılma
- **LR finder:** Çok küçükten başla, her iterasyonda iki kat artır, kayıp artmaya başladığında dur — bu noktanın 10 katı küçüğü iyi başlangıç LR'si

**Cosine Annealing LR:** LR yavaş yavaş minimum değere düşer, sonra yeniden başlar. Yeniden başlama lokal minimumdan çıkmaya yardımcı olur:

$$\text{LR}(t) = \text{LR}_{min} + \frac{1}{2}(\text{LR}_{max} - \text{LR}_{min})\left(1 + \cos\frac{t\pi}{T_{max}}\right)$$

**Early stopping:** Val loss'u izle. Belirli epoch sayısı boyunca iyileşme yoksa eğitimi durdur — overfitting'i önler ve hesaplama tasarrufu sağlar.

> **📌 Not:** "En son epoch modeli" değil, "en iyi val accuracy/loss modeli" kaydedilmeli. Eğitim boyunca checkpoint'ler saklanır, overfitting başlamadan önceki en iyi nokta seçilir.

## Değerlendirme Metrikleri

Accuracy (doğruluk) her zaman yeterli değildir. Özellikle sınıf dengesizliği varsa yanıltıcı olabilir: 950 negatif, 50 pozitif olan veri setinde "hepsini negatif tahmin et" %95 accuracy verir ama modelin hiçbir değeri yoktur.

**Precision ve Recall:**

$$\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}$$

- **Precision:** "Pozitif dediğimin ne kadarı gerçekten pozitif?" — yanlış alarm (false positive) maliyetliyse precision kritik
- **Recall:** "Gerçek pozitiflerin ne kadarını buldum?" — kaçırma (false negative) maliyetliyse recall kritik

**F1 skoru:** Precision ve Recall'ın harmonik ortalaması — her ikisi de önemliyse:

$$F1 = 2 \cdot \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

```python
# Gereksinimler: pip install scikit-learn torch torchvision matplotlib seaborn
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

# Model değerlendirme
model.load_state_dict(torch.load("best_model.pth", map_location=device))
model.eval()

all_preds, all_labels = [], []
with torch.no_grad():
    for images, labels in val_loader:
        images = images.to(device)
        outputs = model(images)
        preds = outputs.argmax(dim=1).cpu().numpy()
        all_preds.extend(preds)
        all_labels.extend(labels.numpy())

all_preds  = np.array(all_preds)
all_labels = np.array(all_labels)

# Detaylı sınıf bazlı rapor
class_names = val_set.classes
print("Sınıflandırma Raporu:")
print(classification_report(all_labels, all_preds,
                             target_names=class_names, digits=4))

# Confusion matrix görselleştirme
cm = confusion_matrix(all_labels, all_preds)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_names, yticklabels=class_names)
plt.title("Confusion Matrix")
plt.xlabel("Tahmin Edilen Sınıf")
plt.ylabel("Gerçek Sınıf")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150)
plt.show()
print("confusion_matrix.png kaydedildi.")
```

Confusion matrix'in köşegeni doğru tahminleri gösterir. Köşegen dışındaki değerler hangi sınıfların birbiriyle karıştırıldığını ortaya koyar — bu bilgi ile veri toplama stratejisini veya augmentation'ı iyileştirebilirsin.

> **💡 İpucu:** `classification_report` çıktısında `macro avg` sınıf dengesizliğine rağmen her sınıfa eşit ağırlık verir. Dengesiz veri setlerinde `macro F1` daha güvenilir metriktir.

## Özet & İleri Okuma

- **Veri kalitesi**, model karmaşıklığından önce gelir. Her sınıf için dengeli, çeşitli örnekler toplanmalı.
- **ImageFolder** sınıfı, klasör adlarını otomatik etiket olarak kabul ederek veri yüklemeyi basitleştirir.
- **Veri artırma** eğitim setini yapay çeşitlendirerek overfitting'i azaltır; val/test setine uygulanmaz.
- **Transfer learning**, ImageNet ağırlıklarından başlayarak çok daha az veri ve süreyle iyi sonuç verir.
- Feature extraction (backbone dondur) az veri için, fine-tuning (tümünü eğit) orta/fazla veri için uygundur.
- **Cosine Annealing** ve **early stopping** eğitim kararlılığını artırır ve gereksiz hesaplamayı önler.
- **Accuracy** sınıf dengesizliğinde yanıltıcıdır; **Precision, Recall, F1** ve **confusion matrix** daha bilgilendirici.
- Confusion matrix, hangi sınıfların birbiriyle karıştırıldığını görselleştirerek veri toplama stratejisine yön gösterir.

### Referanslar

- He et al., "Deep Residual Learning for Image Recognition" (CVPR 2016): [https://arxiv.org/abs/1512.03385](https://arxiv.org/abs/1512.03385)
- Zhang et al., "mixup: Beyond Empirical Risk Minimization" (ICLR 2018): [https://arxiv.org/abs/1710.09412](https://arxiv.org/abs/1710.09412)
- Loshchilov & Hutter, "SGDR: Stochastic Gradient Descent with Warm Restarts" (ICLR 2017): [https://arxiv.org/abs/1608.03983](https://arxiv.org/abs/1608.03983)
