import requests
import time


def publish_instagram_reel(
    instagram_business_id: str,
    access_token: str,
    video_url: str,
    caption: str
):

    create_response = requests.post(
        f"https://graph.facebook.com/v23.0/{instagram_business_id}/media",
        data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": access_token,
        }
    )

    create_data = create_response.json()

    print("Create Reel:", create_data)

    if "id" not in create_data:
        raise Exception(create_data)

    creation_id = create_data["id"]

    time.sleep(10)

    publish_response = requests.post(
        f"https://graph.facebook.com/v23.0/{instagram_business_id}/media_publish",
        data={
            "creation_id": creation_id,
            "access_token": access_token,
        }
    )

    publish_data = publish_response.json()

    print("Publish Reel:", publish_data)

    if "id" not in publish_data:
        raise Exception(publish_data)

    return publish_data