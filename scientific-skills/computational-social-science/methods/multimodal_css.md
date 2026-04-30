# Multimodal CSS: Images as Data

**Goal**: Analyze valid social signals from Images and Video, moving beyond text-only analysis.
**Scenario**: "Do candidates portray themselves differently on Instagram vs. TikTok? Does visual imagery of protests predict violence?"

---

## 1. The Methodological Shift
*   **Old Way**: Manual Content Analysis. (Human coders rate 500 images).
*   **SOTA Way**: **Visual Embeddings (CLIP)**.
    *   Use OpenAI's **CLIP** (Contrastive Language-Image Pre-training) to project images and text into the *same* vector space.
    *   Calculate $Cos(Image, "Democracy")$ vs $Cos(Image, "Chaos")$.

---

## 2. Python Pattern: CLIP Zero-Shot Analysis

Using HuggingFace `transformers`.

### A. Setup
```bash
pip install transformers torch pillow
```

### B. Analytical Pipeline

```python
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import pandas as pd

# 1. Load Pre-trained CLIP (ViT-B/32)
# 'openai/clip-vit-base-patch32' is the standard baseline
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# 2. Define "Visual Hypotheses" (Text Anchors)
# We want to know if the image is more about "Community" or "Conflict"
labels = ["a photo of community cooperation", "a photo of violent conflict", 
          "a photo of political leadership", "a photo of grassroots activism"]

# 3. Load Image
image = Image.open("data/raw/instagram_post_001.jpg")

# 4. Zero-Shot Classification
inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)

with torch.no_grad():
    outputs = model(**inputs)
    
# Get Probabilities (Softmax)
probs = outputs.logits_per_image.softmax(dim=1) 
print("Probabilities:", probs)

# 5. Visual Embedding Extraction (for Regression)
# If you want to use the image as a variable in a regression:
image_features = outputs.image_embeds # This is your 512-dim vector Z.
```

## 3. Advanced: Visual "Semantic Decoupling"

Just like with text, you can measure the "Visual Framings".

*   **Step 1**: Embed all images ($Z_i$).
*   **Step 2**: Define a visual axis. e.g., $Axis = Embed("Formal Suit") - Embed("Casual Hoodie")$.
*   **Step 3**: Project all candidate photos onto this "Formality Axis".
*   **Result**: Quantitative measure of "Visual Formality" for every politician.

## 4. Video Analysis (Frame Sampling)

For TikTok/Reels:
1.  **Sampling**: Extract 1 frame per second (1 fps).
2.  **Embedding**: Run CLIP on each frame.
3.  **Aggregation**: Average the embeddings to get a "Video Vector".
    *   *Warning*: Averaging loses temporal sequence. For sequence, use `TimeSformer` or simpler Sequence Mining on the frame clusters.

## 5. Reporting Checklist
*   [ ] **Model Choice**: Did you use `Laion/CLIP-ViT-L-14` (Better) or base CLIP?
*   [ ] **Validation**: You MUST manually validate the top 50 and bottom 50 images of your metric. Does "High Conflict Score" actually look like conflict?
