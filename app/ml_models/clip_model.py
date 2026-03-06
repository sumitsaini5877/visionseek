import torch
import clip
from PIL import Image


#Load device 
device = "cuda" if torch.cuda.is_available() else "cpu"


# Load CLIP model 
model , preprocess = clip.load("ViT-B/32" ,device=device)

def generate_image_embendding(image_path:str):
    """
    Genrate embendding vector for an image using CLIP
    """
    #Load image
    image = Image.open(image_path)
    
    #Preprocess image
    image_input = preprocess(image).unsqueeze(0).to(device)
    
    
    #Genrate embendding
    with torch.no_grad():
        image_features = model.encode_image(image_input)
    
    #Normalize vector
    image_features /=image_features.norm(dim=1 , keepdim=True)
    
    #Convert tensor -> list
    embedding = image_features.cpu().numpy().tolist()[0]
    
    
    return embedding