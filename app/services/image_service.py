import cloudinary.uploader

#Upload image on cloudinary

async def upload_image_cloudinary(file):
    result = cloudinary.uploader.upload(file.file)
    return result['secure_url']