from datetime import datetime
from zoneinfo import ZoneInfo

from app.database.database import SessionLocal
from app.models.post_model import Post
from app.workers.tasks import publish_post


def check_scheduled_posts():

    db = SessionLocal()

    try:
        now = datetime.now(ZoneInfo("Asia/Kolkata"))

        print(f"Current IST Time: {now}")

        due_posts = (
            db.query(Post)
            .filter(
                Post.status == "PENDING",
                Post.schedule_time <= now
            )
            .all()
        )

        print(f"Found {len(due_posts)} due posts")

        for post in due_posts:

            publish_post.delay(post.id)

            post.status = "QUEUED"

        db.commit()

    finally:
        db.close()

