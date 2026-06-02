from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException
)

from sqlalchemy.orm import Session

import cloudinary.uploader

from app.database.database import get_db

from app.models.media_model import Media
from app.models.user_model import User

from app.dependencies.auth_dependency import (
    get_current_user
)

from app.config.cloudinary_config import *

router = APIRouter(
    prefix="/media",
    tags=["Media"]
)


@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
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

        media = Media(
            user_id=current_user.id,
            public_id=result["public_id"],
            url=result["secure_url"],
            resource_type=result["resource_type"]
        )

        db.add(media)

        db.commit()

        db.refresh(media)

        return {
            "success": True,
            "media_id": media.id,
            "url": media.url,
            "public_id": media.public_id,
            "resource_type": media.resource_type
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("")
def get_media(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    media = (
        db.query(Media)
        .filter(
            Media.user_id == current_user.id
        )
        .order_by(
            Media.created_at.desc()
        )
        .all()
    )

    return media


@router.get("/{media_id}")
def get_single_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    media = db.query(Media).filter(
        Media.id == media_id,
        Media.user_id == current_user.id
    ).first()

    if not media:

        raise HTTPException(
            status_code=404,
            detail="Media not found"
        )

    return media


@router.delete("/{media_id}")
def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    media = db.query(Media).filter(
        Media.id == media_id,
        Media.user_id == current_user.id
    ).first()

    if not media:

        raise HTTPException(
            status_code=404,
            detail="Media not found"
        )

    try:

        cloudinary.uploader.destroy(
            media.public_id,
            resource_type=media.resource_type
        )

    except Exception:
        pass

    db.delete(media)

    db.commit()

    return {
        "success": True,
        "message": "Media deleted successfully"
    }