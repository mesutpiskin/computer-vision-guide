# Model Eğitimi, Augmentation ve Değerlendirme

Başarılı bir bilgisayarlı görü modeli geliştirmek için doğru eğitim stratejisi, veri artırma ve değerlendirme metodolojisi kritiktir. Bu bölümde bu süreçlerin matematiksel temellerini ve pratik uygulamalarını inceleyeceğiz.

## Teorik Temel

**Transfer Learning:**
ImageNet pre-trained ağırlıklar $\theta^*$ ile başlatma:
- Feature extraction: backbone dondurulur ($\nabla_\theta \mathcal{L} = 0$ backbone için), yalnızca classifier eğitilir
- Fine-tuning: tüm ağ veya son katmanlar düşük learning rate ile eğitilir

**Mixup Augmentation:**
$$\tilde{x} = \lambda x_i + (1-\lambda)x_j, \quad \tilde{y} = \lambda y_i + (1-\lambda)y_j, \quad \lambda \sim \text{Beta}(\alpha, \alpha)$$
İki örneği enterpolasyonla karıştırır; regularization etkisi gösterir.

**Cosine Annealing (Learning Rate Schedule):**
$$\eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min})\left(1 + \cos\left(\frac{\pi t}{T}\right)\right)$$
$T$: toplam epoch, $\eta_{max}$: başlangıç LR, $\eta_{min}$: minimum LR.

**F1 Score ve Precision-Recall:**
$$\text{Precision} = \frac{TP}{TP+FP}, \quad \text{Recall} = \frac{TP}{TP+FN}, \quad F_1 = \frac{2 \cdot P \cdot R}{P + R}$$

**Referanslar:**
- He et al., "Deep Residual Learning for Image Recognition", CVPR 2016 (https://arxiv.org/abs/1512.03385)
- Zhang et al., "Mixup: Beyond Empirical Risk Minimization", ICLR 2018 (https://arxiv.org/abs/1710.09412)

## Pratik Uygulama

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms, models
from torchvision.datasets import ImageFolder
from sklearn.metrics import classification_report
import numpy as np

# Veri artırma pipeline
train_transforms = transforms.Compose([
    transforms.RandomResizedCrop(224, scale=(0.7, 1.0)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Dataset ve DataLoader
train_ds = ImageFolder("data/train", transform=train_transforms)
val_ds   = ImageFolder("data/val",   transform=val_transforms)

if len(train_ds) == 0:
    raise ValueError("Eğitim veri seti boş: data/train dizinini kontrol edin")
if len(val_ds) == 0:
    raise ValueError("Doğrulama veri seti boş: data/val dizinini kontrol edin")

train_dl = DataLoader(train_ds, batch_size=32, shuffle=True,  num_workers=4, pin_memory=True)
val_dl   = DataLoader(val_ds,   batch_size=32, shuffle=False, num_workers=4, pin_memory=True)

# Transfer learning: ResNet50 fine-tuning
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
model.fc = nn.Sequential(
    nn.Dropout(0.4),
    nn.Linear(model.fc.in_features, len(train_ds.classes))
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.01)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=20)


def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss, correct = 0.0, 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * imgs.size(0)
        correct += (outputs.argmax(1) == labels).sum().item()
    return total_loss / len(loader.dataset), correct / len(loader.dataset)


def eval_epoch(model, loader, criterion, device):
    model.eval()
    total_loss, correct = 0.0, 0
    all_preds, all_labels = [], []
    with torch.no_grad():
        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)
            outputs = model(imgs)
            total_loss += criterion(outputs, labels).item() * imgs.size(0)
            preds = outputs.argmax(1)
            correct += (preds == labels).sum().item()
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    return total_loss / len(loader.dataset), correct / len(loader.dataset), all_preds, all_labels


for epoch in range(20):
    train_loss, train_acc = train_epoch(model, train_dl, optimizer, criterion, device)
    val_loss, val_acc, preds, labels_list = eval_epoch(model, val_dl, criterion, device)
    scheduler.step()
    print(f"Epoch {epoch+1:2d} | Train Loss: {train_loss:.4f} Acc: {train_acc:.3f} "
          f"| Val Loss: {val_loss:.4f} Acc: {val_acc:.3f}")

print("\nSınıflandırma Raporu:")
print(classification_report(labels_list, preds, target_names=train_ds.classes))
```

## Özet & İleri Okuma

- Transfer learning ImageNet pre-trained modelle eğitim süresini ve veri ihtiyacını azaltır
- Cosine annealing LR schedule, learning rate'i kademeli azaltarak yakınsama kalitesini artırır
- Label smoothing one-hot yerine yumuşak etiket kullanır; overconfidence'ı önler
- Mixup iki örneği enterpolasyonla karıştırır; genelleme kapasitesini güçlendirir
- classification_report: precision, recall, F1 sınıf bazında raporlar
- Referans: ResNet (https://arxiv.org/abs/1512.03385), Mixup (https://arxiv.org/abs/1710.09412)
