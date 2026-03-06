from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "app/storage/uploads"

EXTENSION_MAP = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp"
}

MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if file.content_type not in EXTENSION_MAP:
        raise HTTPException(
            status_code=400,
            detail="Only jpg, jpeg, png, webp allowed"
        )

    file_id = str(uuid.uuid4())
    extension = EXTENSION_MAP[file.content_type]

    filename = f"{file_id}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    size = 0

    try:
        with open(file_path, "wb") as buffer:

            while chunk := await file.read(1024 * 1024):
                size += len(chunk)

                if size > MAX_FILE_SIZE:
                    buffer.close()
                    os.remove(file_path)

                    raise HTTPException(
                        status_code=400,
                        detail="File too large"
                    )

                buffer.write(chunk)

    finally:
        await file.close()

    return {
        "filename": filename,
        "status": "uploaded"
    }