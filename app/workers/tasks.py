from datetime import datetime

from app.database.database import SessionLocal
from app.models.post_model import Post
from app.models.brand_model import Brand

from app.services.instagram_publisher import (
    publish_instagram_image
)

from app.services.instagram_reel_publisher import (
    publish_instagram_reel
)

from app.services.instagram_carousel_publisher import (
    publish_instagram_carousel
)

from app.services.facebook_publisher import (
    publish_facebook_image
)

from app.services.facebook_video_publisher import (
    publish_facebook_video
)

from app.services.facebook_carousel_publisher import (
    publish_facebook_carousel
)


def publish_post(post_id: int):

    db = SessionLocal()

    post = None

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

        if (
            "INSTAGRAM" in post.platforms
            and not brand.instagram_business_id
        ):
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

        media_url = post.media_urls[0]

        # VIDEO → Reel
        if post.media_type.upper() == "VIDEO":

            result = publish_instagram_reel(
                instagram_business_id=
                    brand.instagram_business_id,

                access_token=
                    brand.access_token,

                video_url=media_url,

                caption=post.caption or ""
            )

        # CAROUSEL → Multiple Images
        elif post.media_type.upper() == "CAROUSEL":

            result = publish_instagram_carousel(
                instagram_business_id=
                    brand.instagram_business_id,

                access_token=
                    brand.access_token,

                image_urls=
                    post.media_urls,

                caption=
                    post.caption or ""
            )

        # IMAGE → Single Image
        else:

            result = publish_instagram_image(
                instagram_business_id=
                    brand.instagram_business_id,

                access_token=
                    brand.access_token,

                image_url=media_url,

                caption=post.caption or ""
            )

        print(
            "Instagram Response:",
            result
        )

        if (
           "FACEBOOK" in post.platforms
           and brand.facebook_page_id
        ):
            if (
                post.media_type.upper()
                == "VIDEO"
            ):
                fb_result = (
                   publish_facebook_video(
                        page_id=
                            brand.facebook_page_id,

                        access_token=
                            brand.access_token,
                
                        video_url=
                            media_url,

                        caption=
                            post.caption or ""
                        
                   )
                )
            elif (
                post.media_type.upper()
                == "CAROUSEL"
            ):
                fb_result = (
                    publish_facebook_carousel(
                        page_id=
                            brand.facebook_page_id,
                        access_token=
                            brand.access_token,
                        image_urls=
                            post.media_urls,
                        caption=
                            post.caption or ""
                    )
                )
            else:
                fb_result = (
                    publish_facebook_image(
                        page_id=
                            brand.facebook_page_id,
                        access_token=
                            brand.access_token,
                        image_url=
                            media_url,
                        caption=
                            post.caption or ""
                    )
                )
            print(
                "Facebook Response:",
                fb_result
            )

        post.status = "PUBLISHED"

        post.published_at = datetime.utcnow()

        post.error_message = None

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