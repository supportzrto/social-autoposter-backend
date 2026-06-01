from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.post_model import Post
from app.models.user_model import User

from app.dependencies.auth_dependency import (
    get_current_user
)

from app.schemas.post_schema import (
    PostCreate,
    PostResponse
)

from app.workers.tasks import publish_post
from app.workers.scheduler import check_scheduled_posts

router = APIRouter()


@router.post(
    "/posts",
    response_model=PostResponse
)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    new_post = Post(
        user_id=current_user.id,

        brand_id=post.brand_id,

        title=post.title,

        caption=post.caption,

        media_urls=post.media_urls,

        media_type=post.media_type,

        platforms=post.platforms,

        schedule_time=post.schedule_time,

        status=post.status
    )

    db.add(new_post)

    db.commit()

    db.refresh(new_post)

    return new_post


@router.get("/posts")
def get_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    posts = db.query(Post).filter(
        Post.user_id == current_user.id
    ).all()

    formatted_posts = []

    for post in posts:

        formatted_posts.append({
            "id": post.id,
            "brand_id": post.brand_id,
            "title": post.title,
            "caption": post.caption,
            "media_urls": post.media_urls,
            "media_type": post.media_type,
            "platforms": post.platforms,
            "schedule_time": post.schedule_time,
            "status": post.status,
            "created_at": post.created_at,
            "published_at": post.published_at,
            "error_message": post.error_message
        })

    return formatted_posts