from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.post_model import Post
from app.workers.tasks import publish_post
from app.workers.scheduler import check_scheduled_posts
from app.schemas.post_schema import (
    PostCreate,
    PostResponse
)

router = APIRouter()



@router.post("/posts", response_model=PostResponse)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db)
):
    new_post = Post(
        brand_id=post.brand_id,
        
        title=post.title,
        caption=post.caption,
        media_urls=post.media_urls,
        media_type=post.media_type,
        platforms=post.platforms,
        schedule_time=post.schedule_time,
        status=post.status
    )

    # Save first
    db.add(new_post)

    db.commit()

    db.refresh(new_post)

    

    return new_post





@router.get("/posts")
def get_posts(
    db: Session = Depends(get_db)
):
    posts = db.query(Post).all()

    formatted_posts = []

    for post in posts:

        formatted_posts.append({
            "id": post.id,
            "title": post.title,
            "caption": post.caption,
            "media_urls": post.media_urls,
            "media_type": post.media_type,
            "platforms": post.platforms,
            "schedule_time": post.schedule_time,
            "status": post.status,
        })

    return formatted_posts






