from app.workers.celery_worker import celery
from app.database.database import SessionLocal
from app.models.post_model import Post


@celery.task
def publish_post(post_id: int):

    db = SessionLocal()

    try:
        post = db.query(Post).filter(Post.id == post_id).first()

        if not post:
            print("❌ Post not found")
            return

        # Update status
        post.status = "PROCESSING"
        db.commit()

        print(f"🚀 Publishing Post: {post.title}")

        # Simulate publishing
        # Later:
        # Instagram API
        # Facebook API
        # LinkedIn API

        post.status = "PUBLISHED"

        db.commit()

        print("✅ Post published successfully")

    except Exception as e:

        print("❌ Error:", str(e))

        post.status = "FAILED"
        post.error_message = str(e)

        db.commit()

    finally:
        db.close()

