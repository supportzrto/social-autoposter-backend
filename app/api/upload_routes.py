from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

import pandas as pd

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.post_model import Post
from app.models.brand_model import Brand
from app.models.user_model import User

from app.dependencies.auth_dependency import (
    get_current_user
)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/excel")
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    df = pd.read_excel(
        file.file
    )

    required_columns = [
        "brand_id",
        "title",
        "caption",
        "media_url",
        "media_type",
        "platforms",
        "schedule_time"
    ]

    for column in required_columns:

        if column not in df.columns:

            raise HTTPException(
                status_code=400,
                detail=f"Missing column: {column}"
            )

    created_posts = 0

    for _, row in df.iterrows():

        brand = db.query(Brand).filter(
            Brand.id == int(row["brand_id"]),
            Brand.user_id == current_user.id
        ).first()

        if not brand:
            continue

        post = Post(

            user_id=current_user.id,

            brand_id=int(
                row["brand_id"]
            ),

            title=str(
                row["title"]
            ),

            caption=str(
                row["caption"]
            ),

            media_urls=[
                str(
                    row["media_url"]
                )
            ],

            media_type=str(
                row["media_type"]
            ),

            platforms=[
                str(
                    row["platforms"]
                )
            ],

            schedule_time=pd.to_datetime(
                row["schedule_time"]
            ),

            status="PENDING"
        )

        db.add(post)

        created_posts += 1

    db.commit()

    return {
        "success": True,
        "rows_found": len(df),
        "posts_created": created_posts
    }