from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import cloudinary.uploader
from app.utils.cloudinary_config import cloudinary
from app.database.postgres import get_db
from app.schemas.image_schema import ImageCreate
from app.models.image_model import Image
from app.ml_models.clip_model import generate_image_embedding
from app.database.vector_db import store_embedding


router = APIRouter()

EXTENSION_MAP = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp"
}

MAX_FILE_SIZE = 5 * 1024 * 1024


# @router.post("/upload-image")
# async def upload_image(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):

#     if file.content_type not in EXTENSION_MAP:
#         raise HTTPException(
#             status_code=400,
#             detail="Only jpg, png, webp allowed"
#         )

#     size = 0
#     chunks = []

#     while chunk := await file.read(1024 * 1024):  # 1MB chunks
#         size += len(chunk)

#         if size > MAX_FILE_SIZE:
#             raise HTTPException(
#                 status_code=400,
#                 detail="File too large"
#             )

#         chunks.append(chunk)

#     contents = b"".join(chunks)

#     result = cloudinary.uploader.upload(
#         contents,
#         folder="ai_images_folder"
#     )

#     image_url = result["secure_url"]

#     new_image = Image(image_url = image_url)
#     db.add(new_image)
#     db.commit()
#     db.refresh(new_image)

#     return {
#         "image_url": image_url,
#         "status": "uploaded"
#     }


@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if file.content_type not in EXTENSION_MAP:
        raise HTTPException(
            status_code=400,
            detail="Only jpg, png, webp allowed"
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large"
        )

    result = cloudinary.uploader.upload(
        contents,
        folder="ai_images_folder"
    )

    image_url = result["secure_url"]
    embendding = generate_image_embedding(image_url)
    print("embendding vector :",embendding)
    store_embedding(embedding=embendding , image_path=image_url)

    # new_image = Image(image_url=image_url)
    # db.add(new_image)
    # db.commit()
    # db.refresh(new_image)

    return {
        "image_url": image_url,
        "status": "uploaded"
    }