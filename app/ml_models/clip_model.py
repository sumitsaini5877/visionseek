import torch
import clip
from PIL import Image
import requests
from io import BytesIO

# Select device (GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"


# Load CLIP model
model, preprocess = clip.load("ViT-B/32", device=device)


def generate_image_embedding(image_url: str):
    """
    Generate embedding vector for an image using CLIP
    """

    # Load image
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content)).convert("RGB")

    # Preprocess image
    image_input = preprocess(image).unsqueeze(0).to(device)

    # Generate embedding
    with torch.no_grad():
        image_features = model.encode_image(image_input)

    # Normalize vector
    image_features /= image_features.norm(dim=-1, keepdim=True)

    # Convert tensor -> Python list
    embedding = image_features.cpu().numpy().tolist()[0]

    return embedding