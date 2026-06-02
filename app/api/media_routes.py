from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

import cloudinary.uploader

from app.config.cloudinary_config import *

router = APIRouter(
    prefix="/media",
    tags=["Media"]
)


@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...)
):

    try:

        file_type = file.content_type

        if file_type.startswith("image"):

            result = cloudinary.uploader.upload(
                file.file,
                folder="social-poster/images",
                resource_type="image"
            )

        elif file_type.startswith("video"):

            result = cloudinary.uploader.upload(
                file.file,
                folder="social-poster/videos",
                resource_type="video"
            )

        else:

            raise HTTPException(
                status_code=400,
                detail="Unsupported file type"
            )

        return {
            "success": True,
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "resource_type": result["resource_type"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )