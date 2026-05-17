# Generatif Modeller: GAN, VAE ve Diffusion

Generatif modeller, mevcut veri dağılımından yeni örnekler üretmeyi öğrenen derin öğrenme mimarileridir. Bu bölümde GAN, VAE ve Diffusion modellerini matematiksel temelleriyle inceleyecek, Stable Diffusion uygulamasını göreceğiz.

## Teorik Temel

**GAN Minimax Oyunu:**
$$\min_G \max_D \; \mathbb{E}_{x \sim p_{data}}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]$$
$G$: gürültüden görüntü üreten generator, $D$: gerçek/sahte ayırt eden discriminator. Nash dengesinde $D(x)=0.5$.

**VAE — ELBO (Evidence Lower Bound):**
$$\mathcal{L}_{ELBO} = \mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] - D_{KL}(q_\phi(z|x) \| p(z))$$
Reparameterization trick: $z = \mu + \sigma \odot \epsilon$, $\epsilon \sim \mathcal{N}(0,I)$ — gradyan akışını sağlar.

**DDPM — Forward Diffusion:**
$$q(x_t|x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t}\,x_{t-1},\, \beta_t I)$$
$T$ adımda görüntüye gürültü eklenir ($\beta_t$: gürültü takviyesi). Model $\epsilon_\theta(x_t, t)$ ile eklenen gürültüyü tahmin eder:
$$\mathcal{L}_{simple} = \mathbb{E}_{t,x_0,\epsilon}\left[\|\epsilon - \epsilon_\theta(\sqrt{\bar\alpha_t}x_0 + \sqrt{1-\bar\alpha_t}\epsilon,\, t)\|^2\right]$$

**Referanslar:**
- Ho et al., "Denoising Diffusion Probabilistic Models", NeurIPS 2020 (https://arxiv.org/abs/2006.11239)
- Rombach et al., "High-Resolution Image Synthesis with Latent Diffusion Models", CVPR 2022 (https://arxiv.org/abs/2112.10752)
- Goodfellow et al., "Generative Adversarial Networks", NeurIPS 2014 (https://arxiv.org/abs/1406.2661)

## Pratik Uygulama

```python
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch

# Stable Diffusion ile metin → görüntü üretimi
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
if pipe is None:
    raise RuntimeError("Stable Diffusion pipeline yüklenemedi")

pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)

prompt = "a photorealistic mountain landscape at sunset, high quality"
negative_prompt = "blurry, low quality, cartoon, distorted"

result = pipe(
    prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=20,   # DPMSolver ile 20 adım yeterli
    guidance_scale=7.5,       # CFG: prompt'a bağlılık (yüksek = daha az çeşitlilik)
    height=512,
    width=512,
    generator=torch.manual_seed(42)
)
image = result.images[0]
image.save("uretilen_goruntu.png")
print("Görüntü kaydedildi: uretilen_goruntu.png")

# Basit GAN eğitim döngüsü (konsept)
import torch.nn as nn

class Generator(nn.Module):
    def __init__(self, latent_dim=100, img_size=28):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, img_size * img_size),
            nn.Tanh()
        )

    def forward(self, z):
        return self.model(z)

class Discriminator(nn.Module):
    def __init__(self, img_size=28):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(img_size * img_size, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, img):
        return self.model(img)

latent_dim = 100
G = Generator(latent_dim)
D = Discriminator()
print(f"Generator parametreleri: {sum(p.numel() for p in G.parameters()):,}")
print(f"Discriminator parametreleri: {sum(p.numel() for p in D.parameters()):,}")
```

## Özet & İleri Okuma

- GAN generator/discriminator minimax oyunuyla eğitilir; mode collapse temel sorunudur
- VAE ELBO maksimize ederek latent uzayda pürüzsüz dağılım öğrenir
- Diffusion modeller gürültü ekleme→kaldırma sürecini tersine çevirerek üretim yapar
- Stable Diffusion latent uzayda çalışarak bellek ve hesaplama verimliliği sağlar
- CFG (Classifier-Free Guidance) scale ile kalite ve çeşitlilik dengesi ayarlanır
- Referans: DDPM (https://arxiv.org/abs/2006.11239), LDM (https://arxiv.org/abs/2112.10752)
