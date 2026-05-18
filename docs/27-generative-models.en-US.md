[Türkçe](./27-generatif-modeller.md) | English

# Chapter 27: Generative Models

Data scarcity is one of the biggest challenges in medical imaging — collecting X-ray images of rare diseases is both expensive and ethically complex. What if we could generate synthetic yet realistic images? What if a user could type "red sports car, mountain background" and get exactly that image? This chapter covers three fundamental approaches to image generation: GAN, VAE, and Diffusion models.

## GAN (Generative Adversarial Network)

Imagine a counterfeiter and a detective in an arms race. The counterfeiter produces increasingly convincing fake money to fool the detective; the detective learns better detection. Eventually, the fake money becomes nearly indistinguishable from real currency. GAN models this game mathematically.

- **Generator:** Produces fake images from random noise
- **Discriminator:** Predicts whether an image is real or fake
- They improve together — Generator learns to deceive, Discriminator learns to catch deception

**Mathematical formula (minimax game):**

$$\min_G \max_D \; \mathbb{E}_{x \sim p_{data}}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]$$

The Discriminator $D$ tries to maximize this (saying real is 1, fake is 0); the Generator $G$ tries to minimize it (deceiving the Discriminator).

```python
# Requirements: pip install torch torchvision matplotlib
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# --- Hyperparameters ---
latent_dim = 100
img_size = 28 * 28
batch_size = 128
lr = 0.0002
epochs = 30
device = "cuda" if torch.cuda.is_available() else "cpu"

# --- Generator ---
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
            nn.Tanh()  # Pixel values in [-1, 1]
        )

    def forward(self, z):
        return self.net(z).view(-1, 1, 28, 28)

# --- Discriminator ---
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
            nn.Sigmoid()  # Real probability [0, 1]
        )

    def forward(self, img):
        return self.net(img)

# --- Dataset ---
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])  # Normalize to [-1, 1]
])
dataset = torchvision.datasets.MNIST(root="./data", train=True,
                                     download=True, transform=transform)
loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# --- Models, loss, and optimizer ---
G = Generator().to(device)
D = Discriminator().to(device)
criterion = nn.BCELoss()
opt_G = torch.optim.Adam(G.parameters(), lr=lr, betas=(0.5, 0.999))
opt_D = torch.optim.Adam(D.parameters(), lr=lr, betas=(0.5, 0.999))

# --- Training loop ---
for epoch in range(epochs):
    for real_imgs, _ in loader:
        real_imgs = real_imgs.to(device)
        b = real_imgs.size(0)

        # Train Discriminator
        z = torch.randn(b, latent_dim, device=device)
        fake_imgs = G(z).detach()
        real_labels = torch.ones(b, 1, device=device)
        fake_labels = torch.zeros(b, 1, device=device)

        loss_D = criterion(D(real_imgs), real_labels) + \
                 criterion(D(fake_imgs), fake_labels)
        opt_D.zero_grad(); loss_D.backward(); opt_D.step()

        # Train Generator
        z = torch.randn(b, latent_dim, device=device)
        fake_imgs = G(z)
        loss_G = criterion(D(fake_imgs), real_labels)  # Fool Discriminator
        opt_G.zero_grad(); loss_G.backward(); opt_G.step()

    print(f"Epoch {epoch+1}/{epochs} | D loss: {loss_D.item():.4f} | G loss: {loss_G.item():.4f}")

# --- Display generated images ---
G.eval()
with torch.no_grad():
    z = torch.randn(16, latent_dim, device=device)
    fake = G(z).cpu()
grid = torchvision.utils.make_grid(fake, nrow=4, normalize=True)
plt.imshow(grid.permute(1, 2, 0).numpy(), cmap="gray")
plt.title("GAN-generated digits")
plt.axis("off")
plt.savefig("gan_output.png", dpi=150)
plt.show()
print("Images saved to gan_output.png.")
```

> **⚠️ Warning:** GAN training can be unstable — **mode collapse** (Generator always produces the same image) and **training instability** are common. Solutions: WGAN, spectral normalization, or switch to Diffusion models.

## VAE (Variational Autoencoder)

A standard autoencoder compresses an image into a small vector and decompresses it. But this latent space is disorganized — you can't generate new images from points between two different latent vectors.

VAE's trick: instead of compressing to a single point, compress to a probability distribution (mean $\mu$ and standard deviation $\sigma$). By sampling from that distribution, you generate new images. This makes the **latent space** organized and meaningful.

**What's in latent space?** In a well-trained face VAE, one dimension might encode smiling, another hair color, another face angle. Interpolating between two face latent vectors produces smooth transitions.

**ELBO loss** has two terms:

$$\mathcal{L} = \underbrace{\mathbb{E}[\log p(x|z)]}_{\text{Reconstruction loss}} - \underbrace{D_{KL}(q(z|x) \| p(z))}_{\text{KL divergence}}$$

- **Reconstruction loss:** How well are we reconstructing the original image?
- **KL divergence:** How close is the latent distribution to standard normal? (Regularizer)

> **📌 Note:** VAE tends to produce blurry images — pixel-wise MSE loss doesn't penalize soft edges. VAE-GAN hybrids combining both methods address this.

## Diffusion Models (DDPM)

Take a clean photo and gradually add noise in T steps — eventually it becomes pure noise. Now reverse it: start from noise and gradually denoise step by step. If a deep network learns these denoising steps, it can generate realistic images from pure noise. Like developing a photograph in a darkroom — initially nothing, then gradually the image emerges.

**Forward process** (data → noise):

$$q(x_t \mid x_{t-1}) = \mathcal{N}\!\left(\sqrt{1-\beta_t}\, x_{t-1},\; \beta_t I\right)$$

Each step adds some noise; $\beta_t$ controls the noise schedule.

**Reverse process** (noise → data): The network predicts the added noise $\epsilon_\theta(x_t, t)$ at each step and gradually denoise the image.

**Why Diffusion beats GAN?**
- More stable training — no mode collapse
- More diverse samples — covers broad distribution
- Higher image quality (FID score)
- Disadvantage: slow sampling (50-1000 steps needed)

## Stable Diffusion Application

Stable Diffusion runs diffusion not in raw pixel space but in **latent space** (Latent Diffusion Model). This dramatically reduces computational cost. Additionally, it uses CLIP text encoder for conditional generation — "Bosphorus bridge at sunset, oil painting" becomes an image.

```python
# Requirements: pip install diffusers transformers accelerate
# GPU recommended; very slow on CPU (~minutes)
import torch
from diffusers import StableDiffusionPipeline

model_id = "runwayml/stable-diffusion-v1-5"

# Float16 with GPU, float32 without
dtype = torch.float16 if torch.cuda.is_available() else torch.float32
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=dtype)
pipe = pipe.to(device)

# Text → image
prompt = "a golden retriever playing fetch on a sunny beach, photorealistic"
negative_prompt = "blurry, low quality, distorted"

image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=30,   # Fewer steps = faster, lower quality
    guidance_scale=7.5,       # Text adherence: high = more text influence
    generator=torch.Generator(device=device).manual_seed(42)
).images[0]

image.save("stable_diffusion_output.png")
print("Image saved to stable_diffusion_output.png.")
```

> **💡 Tip:** Without GPU, use `torch_dtype=torch.float32` but it's slow (5-15 minutes on CPU). Google Colab's free T4 GPU is sufficient.

**img2img:** Transform an existing image to another style using `StableDiffusionImg2ImgPipeline` with reference image + text prompt.

**ControlNet:** Add extra conditions beyond text:
- Edge map (Canny edges) → Preserve your lines while changing style
- Depth map → Preserve depth structure
- Pose skeleton → Preserve character pose

## Generative Models for Data Augmentation

With limited labeled medical data, you can establish this loop:
1. Train GAN or Diffusion on your small real image set
2. Generate synthetic images (positive + negative classes)
3. Train your actual classifier on synthetic + real data
4. Result: 15-30% accuracy improvement (literature findings)

> **⚠️ Warning:** Synthetic data doesn't fully replace real data. In medical applications, models trained on synthetic data must be validated only on real data.

## Method Comparison

| Method | Advantage | Disadvantage | When to Use |
|--------|-----------|------------|------------|
| **GAN** | Sharp, high-quality images | Unstable training, mode collapse | When quality is critical |
| **VAE** | Stable training, meaningful latent space | Blurry output | Interpolation, latent analysis |
| **DDPM** | Very high quality, stable | Slow sampling | Quality is top priority |
| **Stable Diffusion** | Text-guided, versatile | Large model, GPU needed | Text→image, style transfer |

## Summary & Further Reading

- **GAN** trains Generator and Discriminator against each other to produce high-quality images; training instability is the main challenge.
- **VAE** compresses images to probability distributions; meaningful latent space enables interpolation and structured sampling.
- **Diffusion models** generate images by learning to denoise; more stable than GAN but slower sampling.
- **Stable Diffusion** runs diffusion in latent space and combines CLIP text encoder — text-to-image generation has become standard practice.
- **ControlNet** enables extra guidance like pose, edges, and depth for directed generation.
- Synthetic data augmentation in limited medical imaging can improve classifier accuracy — validation on real data is mandatory.
- **FID (Fréchet Inception Distance)** score measures generation quality — lower FID means more realistic.

### References

- Goodfellow et al., "Generative Adversarial Nets" (NeurIPS 2014): [https://arxiv.org/abs/1406.2661](https://arxiv.org/abs/1406.2661)
- Kingma & Welling, "Auto-Encoding Variational Bayes" (ICLR 2014): [https://arxiv.org/abs/1312.6114](https://arxiv.org/abs/1312.6114)
- Ho et al., "Denoising Diffusion Probabilistic Models" (NeurIPS 2020): [https://arxiv.org/abs/2006.11239](https://arxiv.org/abs/2006.11239)
- Rombach et al., "High-Resolution Image Synthesis with Latent Diffusion Models" (CVPR 2022): [https://arxiv.org/abs/2112.10752](https://arxiv.org/abs/2112.10752)
