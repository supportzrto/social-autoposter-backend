from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from fastapi import HTTPException
from app.models.brand_model import Brand

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

    brand = db.query(Brand).filter(
        Brand.user_id == current_user.id
    ).first()

    if not brand:

        raise HTTPException(
            status_code=400,
            detail="No Instagram account connected"
        )

    new_post = Post(
        user_id=current_user.id,

        brand_id=brand.id,

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

@router.get("/posts/stats")
def get_post_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    posts = db.query(Post).filter(
        Post.user_id == current_user.id
    )

    total_posts = posts.count()

    scheduled = posts.filter(
        Post.status == "PENDING"
    ).count()

    published = posts.filter(
        Post.status == "PUBLISHED"
    ).count()

    failed = posts.filter(
        Post.status == "FAILED"
    ).count()

    return {
        "total_posts": total_posts,
        "scheduled": scheduled,
        "published": published,
        "failed": failed
    }

@router.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()

    if not post:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    db.delete(post)

    db.commit()

    return {
        "success": True,
        "message": "Post deleted successfully"
    }