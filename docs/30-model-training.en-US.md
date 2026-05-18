[Türkçe](./30-model-egitimi-ve-degerlendirme.md) | English

# Chapter 30: Model Training and Evaluation

You want to automatically identify 5 different product types from a factory camera. These products don't exist in ImageNet. No ready Kaggle dataset. You must collect your data, label it, train the model, and evaluate using the right metrics. This chapter covers each step.

## Dataset Preparation

Machine learning has a rule: garbage in, garbage out. No matter how powerful your model, bad data yields bad results. Investing in data quality always beats investing in model complexity.

**Folder structure (PyTorch ImageFolder standard):**

```
dataset/
  train/
    product_a/  img001.jpg  img002.jpg  ...
    product_b/  img001.jpg  ...
    product_c/  ...
  val/
    product_a/  ...
    product_b/  ...
  test/
    product_a/  ...
    product_b/  ...
```

Folder names automatically become class labels — no separate label file needed.

**Labeling tools:**
- **LabelImg:** Desktop app, bounding box labeling (YOLO/VOC format)
- **Roboflow:** Web-based, team collaboration, format conversion, augmentation
- **CVAT:** Open source, video + image, segmentation support

> **💡 Tip:** Collect minimum 100-200 examples per class. If class imbalance exists (Class A 500 images, Class B 50), balance with oversampling or class weights. Validation set 15-20%, test set 10-15%.

## Data Augmentation

You collected 500 photos but the model overfits — memorization instead of learning. Solution: generate new training examples from existing images via transformations. Model sees same object from different angles, lighting, sizes.

```python
# Requirements: pip install torch torchvision
import torch
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms

# Aggressive augmentation for training
train_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomCrop(224),               # Random 224×224 crop
    transforms.RandomHorizontalFlip(p=0.5),   # 50% horizontal flip
    transforms.RandomVerticalFlip(p=0.1),     # 10% vertical flip (adjust per object)
    transforms.RandomRotation(degrees=15),    # ±15 degrees rotation
    transforms.ColorJitter(
        brightness=0.3,
        contrast=0.3,
        saturation=0.2,
        hue=0.1
    ),
    transforms.RandomGrayscale(p=0.05),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  # ImageNet means
        std=[0.229, 0.224, 0.225]
    )
])

# Minimal transforms for validation/test — NO augmentation!
val_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Load datasets
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

print(f"Training examples: {len(train_dataset)}")
print(f"Classes: {train_dataset.classes}")
print(f"Class → index: {train_dataset.class_to_idx}")
```

**Mixup:** Mix two images with $\lambda$ weight, mix labels similarly. Model learns uncertain boundaries better.

$$\tilde{x} = \lambda x_i + (1-\lambda) x_j, \quad \tilde{y} = \lambda y_i + (1-\lambda) y_j$$

```python
def mixup_batch(images, labels, alpha=0.4):
    """Apply Mixup augmentation to a batch."""
    lam = torch.distributions.Beta(alpha, alpha).sample().item()
    batch_size = images.size(0)
    idx = torch.randperm(batch_size)
    mixed_images = lam * images + (1 - lam) * images[idx]
    return mixed_images, labels, labels[idx], lam
```

> **⚠️ Warning:** Apply augmentation only to training data. Using augmentation on validation/test corrupts measurements.

## Transfer Learning

ResNet trained on 1000 ImageNet classes already knows edges, textures, shapes, gradients. Adapting these learned features to your dataset requires 10-100x less data and time than training from scratch. Like learning math — don't reinvent numbers, build on them.

**Two basic strategies:**

1. **Feature extraction:** Freeze backbone entirely, train only new final layer. Minimal data, fast training.

2. **Fine-tuning:** Train entire network at low learning rate — backbone changes slowly, final layers adapt quickly. Medium/large data.

```python
# Requirements: pip install torch torchvision
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import torchvision

# --- Data ---
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

# Demo with CIFAR-10 (use dataset/train for your data)
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

# Replace final layer — output size = num_classes
in_features = model.fc.in_features
model.fc = nn.Sequential(
    nn.Dropout(p=0.3),
    nn.Linear(in_features, num_classes)
)
model = model.to(device)

# Different learning rates: backbone slow, new layer fast
backbone_params = [p for n, p in model.named_parameters() if "fc" not in n]
head_params     = list(model.fc.parameters())

optimizer = optim.AdamW([
    {"params": backbone_params, "lr": 1e-4},  # Backbone slow
    {"params": head_params,     "lr": 1e-3},  # Head fast
], weight_decay=1e-4)

scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=20)
criterion = nn.CrossEntropyLoss()

# --- Training function ---
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

# --- Evaluation function ---
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

# --- Training loop ---
best_val_acc = 0.0
patience, patience_counter = 5, 0

for epoch in range(1, 21):
    train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion, device)
    val_loss,   val_acc   = eval_epoch(model, val_loader, criterion, device)
    scheduler.step()

    print(f"Epoch {epoch:2d}/20 | "
          f"Train: loss={train_loss:.4f} acc={train_acc:.4f} | "
          f"Val: loss={val_loss:.4f} acc={val_acc:.4f}")

    # Save best model
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), "best_model.pth")
        patience_counter = 0
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print(f"Early stopping — val accuracy didn't improve for {patience} epochs.")
            break

print(f"Best val accuracy: {best_val_acc:.4f}")
```

## Training Strategies

**Learning rate selection:**
- Too large → loss oscillates, weights destabilize
- Too small → slow learning, local minimum entrapment
- **LR finder:** Start tiny, double every iteration, stop when loss increases — 10x smaller is good starting LR

**Cosine Annealing LR:** LR slowly drops to minimum, then restarts. Restart helps escape local minima:

$$\text{LR}(t) = \text{LR}_{min} + \frac{1}{2}(\text{LR}_{max} - \text{LR}_{min})\left(1 + \cos\frac{t\pi}{T_{max}}\right)$$

**Early stopping:** Watch validation loss. Stop if no improvement for N epochs — prevents overfitting and saves computation.

> **📌 Note:** Save "best val accuracy model," not "latest epoch model." Preserve checkpoint before overfitting starts.

## Evaluation Metrics

Accuracy (correctness) isn't always sufficient. With class imbalance it's misleading: dataset of 950 negatives + 50 positives, "always predict negative" gives 95% accuracy but worthless model.

**Precision and Recall:**

$$\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}$$

- **Precision:** "Of what I said was positive, how much actually was?" — matters when false positives are costly
- **Recall:** "How many actual positives did I find?" — matters when false negatives are costly

**F1 score:** Harmonic mean of Precision and Recall — use when both matter equally:

$$F1 = 2 \cdot \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

```python
# Requirements: pip install scikit-learn torch torchvision matplotlib seaborn
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

# Model evaluation
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

# Detailed per-class report
class_names = val_set.classes
print("Classification Report:")
print(classification_report(all_labels, all_preds,
                             target_names=class_names, digits=4))

# Confusion matrix visualization
cm = confusion_matrix(all_labels, all_preds)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_names, yticklabels=class_names)
plt.title("Confusion Matrix")
plt.xlabel("Predicted Class")
plt.ylabel("True Class")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150)
plt.show()
print("Saved to confusion_matrix.png.")
```

Confusion matrix diagonal shows correct predictions. Off-diagonal reveals which classes confuse the model — informs data collection and augmentation strategy.

> **💡 Tip:** In `classification_report`, `macro avg` weights each class equally despite imbalance. For imbalanced datasets, `macro F1` is more reliable.

## Summary & Further Reading

- **Data quality** precedes model complexity. Balanced, diverse examples per class are essential.
- **ImageFolder** auto-labels from folder names, simplifying data loading.
- **Data augmentation** reduces overfitting by artificially diversifying training data; never apply to validation/test.
- **Transfer learning** achieves good results with much less data and time than from-scratch training.
- Feature extraction (freeze backbone) suits small data; fine-tuning (train all) suits medium/large data.
- **Cosine Annealing** and **early stopping** improve training stability and prevent unnecessary computation.
- **Accuracy** is misleading with class imbalance; use Precision, Recall, F1, and confusion matrix instead.
- Confusion matrix visualizes which classes confuse the model, guiding data and augmentation improvements.

### References

- He et al., "Deep Residual Learning for Image Recognition" (CVPR 2016): [https://arxiv.org/abs/1512.03385](https://arxiv.org/abs/1512.03385)
- Zhang et al., "mixup: Beyond Empirical Risk Minimization" (ICLR 2018): [https://arxiv.org/abs/1710.09412](https://arxiv.org/abs/1710.09412)
- Loshchilov & Hutter, "SGDR: Stochastic Gradient Descent with Warm Restarts" (ICLR 2017): [https://arxiv.org/abs/1608.03983](https://arxiv.org/abs/1608.03983)
