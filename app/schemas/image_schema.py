from pydantic import BaseModel

class ImageCreate(BaseModel):
    image_url:str