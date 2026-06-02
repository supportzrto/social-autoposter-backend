from datetime import datetime

from app.database.database import (
    SessionLocal
)

from app.models.post_model import Post

from app.workers.tasks import (
    publish_post
)


def check_scheduled_posts():

    db = SessionLocal()

    try:

        posts = (
            db.query(Post)
            .filter(
                Post.status == "PENDING",
                Post.schedule_time
                <= datetime.utcnow()
            )
            .all()
        )

        print(
            f"Found {len(posts)} posts"
        )

        for post in posts:

            print(
                f"Publishing {post.id}"
            )

            publish_post(post.id)

    finally:

        db.close()