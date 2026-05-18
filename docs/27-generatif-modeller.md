# Bölüm 27: Generatif Modeller

Tıbbi görüntü analizinde veri kıtlığı en büyük engellerden biridir — nadir hastalıkların X-ray görüntüsünü toplamak hem pahalı hem etik açıdan karmaşıktır. Ya sentetik ama gerçekçi görüntüler üretebilseydik? Ya da kullanıcı "kırmızı spor araba, arka plan dağ manzarası" diye yazınca tam aradığı görüntü oluşsa? Bu bölümde görüntü üretmenin üç temel yöntemini inceleyeceğiz: GAN, VAE ve Diffusion modelleri.

## GAN (Üretici Çekişmeli Ağ)

Düşün ki bir sahte para basan var ve onu yakalamaya çalışan bir dedektif. Sahte para basan her seferinde dedektifi kandırmak için daha iyi sahte para üretiyor; dedektif ise her seferinde daha iyi gerçek-sahte ayırt etmeyi öğreniyor. Uzun süre sonra sahte para gerçeğinden neredeyse ayırt edilemez hale geliyor. GAN tam olarak bu oyunu matematiksel olarak modeller.

- **Üretici (Generator):** Rastgele gürültüden sahte görüntü üretir
- **Ayrıştırıcı (Discriminator):** Görüntünün gerçek mi sahte mi olduğunu tahmin eder
- İkisi birbirini eğiterek gelişir — Üretici kandırmayı, Ayrıştırıcı yakalamayı öğrenir

**Matematiksel formül (minimax oyunu):**

$$\min_G \max_D \; \mathbb{E}_{x \sim p_{data}}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]$$

Ayrıştırıcı $D$ bu değeri maksimize etmeye (gerçeği 1, sahteyı 0 demek), Üretici $G$ minimize etmeye (Ayrıştırıcı'yı kandırmak) çalışır.

```python
# Gereksinimler: pip install torch torchvision matplotlib
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# --- Hiperparametreler ---
latent_dim = 100
img_size = 28 * 28
batch_size = 128
lr = 0.0002
epochs = 30
device = "cuda" if torch.cuda.is_available() else "cpu"

# --- Üretici ---
class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(256),
            nn.Linear(256, 512),
            nn.LeakyReLU(0.2),
            nn.BatchNorm1d(512),
            nn.Linear(512, img_size),
            nn.Tanh()  # Piksel değerleri [-1, 1] aralığında
        )

    def forward(self, z):
        return self.net(z).view(-1, 1, 28, 28)

# --- Ayrıştırıcı ---
class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(img_size, 512),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(256, 1),
            nn.Sigmoid()  # Gerçek olasılığı [0, 1]
        )

    def forward(self, img):
        return self.net(img)

# --- Veri seti ---
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])  # [-1, 1] normalize
])
dataset = torchvision.datasets.MNIST(root="./data", train=True,
                                     download=True, transform=transform)
loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# --- Modeller, kayıp ve optimizer ---
G = Generator().to(device)
D = Discriminator().to(device)
criterion = nn.BCELoss()
opt_G = torch.optim.Adam(G.parameters(), lr=lr, betas=(0.5, 0.999))
opt_D = torch.optim.Adam(D.parameters(), lr=lr, betas=(0.5, 0.999))

# --- Eğitim döngüsü ---
for epoch in range(epochs):
    for real_imgs, _ in loader:
        real_imgs = real_imgs.to(device)
        b = real_imgs.size(0)

        # Ayrıştırıcı eğitimi
        z = torch.randn(b, latent_dim, device=device)
        fake_imgs = G(z).detach()
        real_labels = torch.ones(b, 1, device=device)
        fake_labels = torch.zeros(b, 1, device=device)

        loss_D = criterion(D(real_imgs), real_labels) + \
                 criterion(D(fake_imgs), fake_labels)
        opt_D.zero_grad(); loss_D.backward(); opt_D.step()

        # Üretici eğitimi
        z = torch.randn(b, latent_dim, device=device)
        fake_imgs = G(z)
        loss_G = criterion(D(fake_imgs), real_labels)  # Ayrıştırıcıyı kandır
        opt_G.zero_grad(); loss_G.backward(); opt_G.step()

    print(f"Epoch {epoch+1}/{epochs} | D loss: {loss_D.item():.4f} | G loss: {loss_G.item():.4f}")

# --- Üretilen görüntüleri göster ---
G.eval()
with torch.no_grad():
    z = torch.randn(16, latent_dim, device=device)
    fake = G(z).cpu()
grid = torchvision.utils.make_grid(fake, nrow=4, normalize=True)
plt.imshow(grid.permute(1, 2, 0).numpy(), cmap="gray")
plt.title("GAN ile üretilen rakamlar")
plt.axis("off")
plt.savefig("gan_output.png", dpi=150)
plt.show()
print("Görüntüler gan_output.png'ye kaydedildi.")
```

> **⚠️ Dikkat:** GAN eğitimi dengesiz olabilir — **mode collapse** (Üretici hep aynı görüntüyü üretir) ve **training instability** yaygın sorunlardır. Çözüm: WGAN, spectral normalization, ya da Diffusion modeline geçiş.

## VAE (Değişimsel Öz-Kodlayıcı)

Normal bir oto-kodlayıcı görüntüyü alır, küçük bir vektöre sıkıştırır, geri açar. Ama bu vektör uzayı düzensizdir — iki farklı noktanın ortasından yeni görüntü üretemezsiniz.

VAE'nin farkı şu: görüntüyü tek bir noktaya değil, bir olasılık dağılımına (ortalama $\mu$ ve standart sapma $\sigma$) sıkıştırır. O dağılımdan örnekleyerek yeni görüntüler üretilir. Bu sayede **latent uzay** düzenli ve anlamlı hale gelir.

**Latent space'de ne var?** İyi eğitilmiş bir yüz VAE'sinde bir boyut gülümsemeyi, diğeri saç rengini, başkası yüz açısını kodlayabilir. İki farklı yüzün latent vektörleri arasında interpolasyon yaparak kademeli geçiş elde edersiniz.

**ELBO kaybı** iki terimden oluşur:

$$\mathcal{L} = \underbrace{\mathbb{E}[\log p(x|z)]}_{\text{Yeniden oluşturma kaybı}} - \underbrace{D_{KL}(q(z|x) \| p(z))}_{\text{KL diverjansı}}$$

- **Yeniden oluşturma kaybı:** Orijinal görüntüyü ne kadar iyi geri üretiyoruz?
- **KL diverjansı:** Latent dağılım standart normal dağılıma ne kadar yakın? (Düzenlileştirici)

> **📌 Not:** VAE görüntüleri biraz bulanık üretme eğilimindedir — piksel başına MSE kaybı keskin kenarları cezalandırmaz. GAN ile birleştirilen VAE-GAN mimarileri bu sorunu giderir.

## Diffusion Modelleri (DDPM)

Temiz bir fotoğrafı al, üzerine T adımda kademeli olarak gürültü ekle — en sonunda tamamen gürültüye dönüşüyor. Şimdi bu süreci tersine çevir: gürültüden başlayarak adım adım temizle. Bir derin ağ bu temizleme adımlarını öğrenirse, saf gürültüden başlayarak gerçekçi görüntüler üretebilir. Sanki karanlık odada fotoğraf geliştirmek gibi — başlangıçta hiçbir şey yok, adım adım netleşiyor.

**İleri süreç** (veri → gürültü):

$$q(x_t \mid x_{t-1}) = \mathcal{N}\!\left(\sqrt{1-\beta_t}\, x_{t-1},\; \beta_t I\right)$$

Her adımda biraz gürültü ekleniyor; $\beta_t$ gürültü zamanlamasını kontrol ediyor.

**Geri süreç** (gürültü → veri): Ağ her adımda $\epsilon_\theta(x_t, t)$ ile eklenen gürültüyü tahmin eder ve görüntüyü adım adım temizler.

**Neden Diffusion GAN'dan iyi?**
- Daha kararlı eğitim — mode collapse yok
- Daha çeşitli örnekler — geniş dağılımı kapsar
- Daha yüksek görüntü kalitesi (FID skoru)
- Dezavantaj: örnekleme yavaş (50-1000 adım gerekebilir)

## Stable Diffusion ile Uygulama

Stable Diffusion, diffusion işlemini ham piksel uzayında değil **latent uzayda** çalıştırır (Latent Diffusion Model). Bu sayede hesaplama maliyeti dramatik düşer. Ek olarak CLIP metin encoder'ı ile koşullu üretim sağlar — "gün batımında Boğaz köprüsü, yağlı boya" gibi metinleri görüntüye dönüştürür.

```python
# Gereksinimler: pip install diffusers transformers accelerate
# GPU önerilir; CPU'da çok yavaş olur (~dakikalar)
import torch
from diffusers import StableDiffusionPipeline

model_id = "runwayml/stable-diffusion-v1-5"

# GPU varsa float16, yoksa float32
dtype = torch.float16 if torch.cuda.is_available() else torch.float32
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=dtype)
pipe = pipe.to(device)

# Metin → görüntü
prompt = "a golden retriever playing fetch on a sunny beach, photorealistic"
negative_prompt = "blurry, low quality, distorted"

image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=30,   # Daha az adım = daha hızlı, daha düşük kalite
    guidance_scale=7.5,       # Metne bağlılık: yüksek = metin etkisi artar
    generator=torch.Generator(device=device).manual_seed(42)
).images[0]

image.save("stable_diffusion_output.png")
print("Görüntü stable_diffusion_output.png'ye kaydedildi.")
```

> **💡 İpucu:** GPU yoksa `torch_dtype=torch.float32` kullan ama yavaş olur (CPU'da 5-15 dakika). Google Colab'ın ücretsiz T4 GPU'su yeterli.

**img2img:** Mevcut bir görüntüyü başka bir stile dönüştür. `StableDiffusionImg2ImgPipeline` ile referans görüntü + metin prompt vererek çalışır.

**ControlNet:** Sadece metin değil, ek koşullar da verebilirsiniz:
- Edge map (Canny kenarları) → Belirlediğin çizgiyi koruyarak stil değiştir
- Depth map → Derinlik yapısını koru
- Pose skeleton → Karakterin pozunu koru

## Veri Artırma için Generatif Modeller

Az etiketli tıbbi görüntüde şu döngü kurulabilir:
1. Elimizdeki az sayıda gerçek görüntüyle GAN veya Diffusion modeli eğit
2. Sentetik görüntüler üret (pozitif + negatif sınıf)
3. Sentetik + gerçek veriyle asıl sınıflandırıcıyı eğit
4. Sonuç: %15-30 doğruluk artışı (literatür bulguları)

> **⚠️ Dikkat:** Sentetik veri gerçek verinin yerini tam tutmaz. Tıbbi uygulamalarda sentetik veriyle eğitilen model, yalnızca gerçek veriyle doğrulanmalıdır.

## Yöntem Karşılaştırması

| Yöntem | Avantaj | Dezavantaj | Ne Zaman |
|--------|---------|------------|----------|
| **GAN** | Keskin, yüksek kaliteli görüntü | Eğitim kararsız, mode collapse | Yüksek kalite gerekince |
| **VAE** | Kararlı eğitim, anlamlı latent uzay | Bulanık çıktı | Interpolasyon, latent analiz |
| **DDPM** | Çok yüksek kalite, kararlı | Örnekleme yavaş | Kalite birincil öncelikse |
| **Stable Diffusion** | Metin güdümlü, çok yönlü | Büyük model, GPU gerekli | Metin → görüntü, stil transferi |

## Özet & İleri Okuma

- **GAN** Üretici ve Ayrıştırıcı'yı birbirine karşı eğiterek yüksek kaliteli görüntü üretir; eğitim dengesizliği temel sorundur.
- **VAE** görüntüyü olasılık dağılımına kodlar; anlamlı latent uzayda interpolasyon ve düzenli örnekleme mümkün olur.
- **Diffusion modelleri**, görüntüye kademeli gürültü ekleyip tersine çevirerek üretim yapar; GAN'dan daha kararlı ama örnekleme daha yavaştır.
- **Stable Diffusion**, diffusion'ı latent uzayda çalıştırarak CLIP metin encoder'ıyla birleştirir — metin-görüntü üretiminin pratik standardı haline gelmiştir.
- **ControlNet** poz, kenar ve derinlik gibi ek koşullarla üretimi yönlendirmeyi sağlar.
- Tıbbi görüntü gibi az veri durumlarında sentetik veri artırma, sınıflandırıcı doğruluğunu artırabilir — ama gerçek veriyle doğrulama zorunludur.
- Üretim kalitesini ölçmek için **FID (Fréchet Inception Distance)** skoru kullanılır — düşük FID daha gerçekçi demektir.

### Referanslar

- Goodfellow et al., "Generative Adversarial Nets" (NeurIPS 2014): [https://arxiv.org/abs/1406.2661](https://arxiv.org/abs/1406.2661)
- Kingma & Welling, "Auto-Encoding Variational Bayes" (ICLR 2014): [https://arxiv.org/abs/1312.6114](https://arxiv.org/abs/1312.6114)
- Ho et al., "Denoising Diffusion Probabilistic Models" (NeurIPS 2020): [https://arxiv.org/abs/2006.11239](https://arxiv.org/abs/2006.11239)
- Rombach et al., "High-Resolution Image Synthesis with Latent Diffusion Models" (CVPR 2022): [https://arxiv.org/abs/2112.10752](https://arxiv.org/abs/2112.10752)
