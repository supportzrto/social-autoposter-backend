from app.database.database import SessionLocal

from app.models.post_model import Post
from app.models.brand_model import Brand
from datetime import datetime

from app.services.instagram_publisher import (
    publish_instagram_image
)


def publish_post(post_id: int):

    db = SessionLocal()

    try:

        post = (
            db.query(Post)
            .filter(Post.id == post_id)
            .first()
        )

        if not post:

            print("❌ Post not found")
            return

        post.status = "PROCESSING"

        db.commit()

        print(
            f"🚀 Publishing Post: {post.title}"
        )

        brand = (
            db.query(Brand)
            .filter(
                Brand.id == post.brand_id
            )
            .first()
        )

        if not brand:

            raise Exception(
                "Brand not found"
            )

        if not brand.instagram_business_id:

            raise Exception(
                "Instagram Business ID missing"
            )

        if not brand.access_token:

            raise Exception(
                "Access token missing"
            )

        if not post.media_urls:

            raise Exception(
                "Media URL missing"
            )

        image_url = post.media_urls[0]

        result = publish_instagram_image(
            instagram_business_id=
                brand.instagram_business_id,

            access_token=
                brand.access_token,

            image_url=image_url,

            caption=post.caption or ""
        )

        print(
            "Instagram Response:",
            result
        )

        post.status = "PUBLISHED"
        post.published_at = datetime.utcnow()

        db.commit()

        print(
            "✅ Post published successfully"
        )

    except Exception as e:

        print(
            "❌ Publish Error:",
            str(e)
        )

        if post:

            post.status = "FAILED"

            post.error_message = str(e)

            db.commit()

    finally:

        db.close()