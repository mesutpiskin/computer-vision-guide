[Türkçe](./31-vision-language-modeller.md) | English

# Chapter 31: Vision-Language Models

An e-commerce site where users type "red sports shoes" and the system returns matching product photos from thousands — yet no photo was manually labeled "red sports shoes." Or a blind user where every uploaded photo is automatically described in English. These tasks can't be solved by vision or language models alone. This chapter examines models combining both modalities.

## Why Multimodal?

Image model understands visuals but can't answer "what is this?" in text. Language model understands text but can't see photos. Vision-Language models embed both modalities in the same vector space, answering "how well does this image match this text?"

This unlocks surprising capability: recognizing classes it's never seen, knowing just their text description — **zero-shot** classification.

## CLIP (Contrastive Language-Image Pre-Training)

Trained on 400 million image-text pairs. Model learned to place "cat photo" text near real cat photos in the same vector space, and unrelated pairs far apart.

**Dual encoder architecture:**
- **Image encoder (ViT):** Converts image to fixed-size vector → $f_I$
- **Text encoder (Transformer):** Converts text to fixed-size vector → $f_T$
- Both encoders work independently, produce equal-dimension output

**Similarity measurement:**

$$\text{sim}(I, T) = \frac{f_I \cdot f_T}{\|f_I\| \cdot \|f_T\|}$$

This is cosine similarity — measures angle between vectors. 1 = perfect match, 0 = unrelated.

**Training:** A batch has N image-text pairs. Correct matches' similarity increases, wrong matches decrease. **Contrastive loss** enables this.

**Zero-shot classification:** No training needed — convert class names to text, find closest text to image.

```python
# Requirements: pip install transformers Pillow torch requests
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import requests

model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)
model.eval()

# Test image
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

# Class candidates — classify without any training
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

# Logits are image-text similarity scores
logits = outputs.logits_per_image  # (1, num_labels)
probs = torch.softmax(logits, dim=-1)[0]

print("Zero-shot classification results:")
for label, prob in sorted(zip(candidate_labels, probs), key=lambda x: x[1], reverse=True):
    print(f"  {label}: {prob.item()*100:.1f}%")
```

> **💡 Tip:** `"A photo of a {label}"` template works better than bare label. "Labrador" alone is weaker than "a photo of a Labrador dog" — this is prompt engineering, a subtle art.

**Semantic image search:**

```python
# Requirements: pip install transformers Pillow torch numpy
import numpy as np
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model.eval()

def encode_image(image: Image.Image) -> np.ndarray:
    """Convert image to CLIP feature vector."""
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        features = model.get_image_features(**inputs)
    features = features / features.norm(dim=-1, keepdim=True)
    return features.cpu().numpy()[0]

def encode_text(text: str) -> np.ndarray:
    """Convert text to CLIP feature vector."""
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    with torch.no_grad():
        features = model.get_text_features(**inputs)
    features = features / features.norm(dim=-1, keepdim=True)
    return features.cpu().numpy()[0]

# Usage: encode image database, compute cosine similarity with query
query = "a red sports car"
query_vec = encode_text(query)
# image_vectors = [encode_image(img) for img in image_database]
# similarities = [np.dot(query_vec, iv) for iv in image_vectors]
# Return images with highest similarity

print(f"Query vector size: {query_vec.shape}")
print("Query encoded. Can compute similarities with image database.")
```

## LLaVA (Large Language and Vision Assistant)

CLIP puts images and text in same space but only produces short text embeddings — can't generate long, multi-step responses. LLaVA asks: what if we connect CLIP's visual features to a large language model (Llama, Vicuna)?

**Architecture:**
1. CLIP image encoder → visual feature vectors
2. Linear projection layer (linear adapter) → align to language model dimension
3. Large language model (Llama/Vicuna) → process visual + text tokens together → generate text

Result: a model that talks about images, answers questions, writes descriptions.

```python
# Requirements: pip install transformers Pillow torch requests
# Note: llava-1.5-7b-hf needs ~14GB RAM. GPU recommended.
from transformers import LlavaForConditionalGeneration, AutoProcessor
from PIL import Image
import torch
import requests

model_id = "llava-hf/llava-1.5-7b-hf"

# If low memory, use 4-bit quantization
try:
    from transformers import BitsAndBytesConfig
    quantization_config = BitsAndBytesConfig(load_in_4bit=True)
    model = LlavaForConditionalGeneration.from_pretrained(
        model_id, quantization_config=quantization_config
    )
except Exception:
    # Fall back to float16
    model = LlavaForConditionalGeneration.from_pretrained(
        model_id, torch_dtype=torch.float16
    )

processor = AutoProcessor.from_pretrained(model_id)

# Image and question
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

# LLaVA chat format
conversation = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "What do you see in this image? Describe the dog's breed and mood."}
        ]
    }
]

prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
inputs = processor(images=image, text=prompt, return_tensors="pt")

with torch.no_grad():
    output = model.generate(**inputs, max_new_tokens=200, do_sample=False)

response = processor.decode(output[0], skip_special_tokens=True)
# Extract only assistant response
answer = response.split("ASSISTANT:")[-1].strip()
print(f"LLaVA response:\n{answer}")
```

> **⚠️ Warning:** LLaVA-7B needs roughly 14GB GPU memory. For smaller GPU, use `llava-hf/llava-1.5-7b-hf` with 4-bit quantization or cloud services (HuggingFace Inference API).

## BLIP-2

While LLaVA uses simple projection, BLIP-2 builds a more sophisticated bridge: **Q-Former (Querying Transformer)**.

Q-Former uses learnable query tokens to distill important information from image features into language model. This "information distillation" layer lets BLIP-2 easily combine with different language models (OPT, FlanT5).

```python
# Requirements: pip install transformers Pillow torch requests
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

# Generate image caption
inputs = processor(images=image, return_tensors="pt").to(
    device, torch.float16 if device == "cuda" else torch.float32
)

with torch.no_grad():
    generated_ids = model.generate(**inputs, max_new_tokens=50)

caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
print(f"BLIP-2 caption: {caption}")

# Visual question answering
question = "What breed is the dog?"
inputs_vqa = processor(images=image, text=question, return_tensors="pt").to(
    device, torch.float16 if device == "cuda" else torch.float32
)

with torch.no_grad():
    generated_ids = model.generate(**inputs_vqa, max_new_tokens=30)

answer = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
print(f"Question: {question}")
print(f"BLIP-2 answer: {answer}")
```

> **📌 Note:** BLIP-2 excels at image captioning and short-answer VQA. For long dialog and multi-step reasoning, LLaVA is more suitable.

## Use Cases

**Search by image:** Encode thousands of product photos with CLIP, encode user query as text, fetch closest images. No manual tags needed.

**Accessibility:** For blind users, BLIP-2 or LLaVA generates automatic descriptions for every uploaded photo.

**Medical image reporting:** System that reads radiology images and drafts initial findings reports (final decision always with specialist).

**Content moderation:** CLIP zero-shot classification — "violent content," "inappropriate" categories without training.

**E-commerce:** Auto-generate product titles, categories, feature lists from photos.

## Method Comparison

| Model | Primary Task | GPU Memory | Speed | Strength |
|-------|-------------|-----------|-------|----------|
| **CLIP ViT-B/32** | Zero-shot classification, search | ~1 GB | Very fast | Large-scale search, classification |
| **CLIP ViT-L/14** | Zero-shot (higher accuracy) | ~3 GB | Fast | Better accuracy |
| **BLIP-2 (2.7B)** | Caption, VQA | ~6 GB | Medium | Short answers, descriptions |
| **LLaVA-1.5-7B** | Multi-turn chat, VQA | ~14 GB | Slow | Long explanations, dialog |

## Summary & Further Reading

- **CLIP** trained on 400 million image-text pairs via contrastive learning; embeds images and text in same space.
- **Zero-shot classification** takes class names as text, classifies without training — prompt template "A photo of a {label}" yields strong results.
- **Cosine similarity** measures image-text match score; foundation of semantic image search.
- **LLaVA** connects CLIP visual features to language model, enabling long text responses and multi-turn dialog.
- **BLIP-2** Q-Former bridge lets it work with various language models; strong on captioning and short VQA.
- Vision-language models create real value in accessibility, e-commerce, medical reporting, content moderation.
- Field evolves rapidly: GPT-4o, Gemini, Claude integrate image understanding directly into base models.

### References

- Radford et al., "Learning Transferable Visual Models From Natural Language Supervision" (ICML 2021): [https://arxiv.org/abs/2103.00020](https://arxiv.org/abs/2103.00020)
- Liu et al., "Visual Instruction Tuning" / LLaVA (NeurIPS 2023): [https://arxiv.org/abs/2304.08485](https://arxiv.org/abs/2304.08485)
- Li et al., "BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models" (ICML 2023): [https://arxiv.org/abs/2301.12597](https://arxiv.org/abs/2301.12597)
