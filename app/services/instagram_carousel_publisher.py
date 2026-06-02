import requests
import time


def publish_instagram_carousel(
    instagram_business_id: str,
    access_token: str,
    image_urls: list[str],
    caption: str
):

    children = []

    # Create child containers

    for image_url in image_urls:

        response = requests.post(
            f"https://graph.facebook.com/v23.0/{instagram_business_id}/media",
            data={
                "image_url": image_url,
                "is_carousel_item": True,
                "access_token": access_token,
            }
        )

        data = response.json()

        print(
            "Carousel Child:",
            data
        )

        if "id" not in data:
            raise Exception(data)

        children.append(data["id"])

    # Create parent carousel

    carousel_response = requests.post(
        f"https://graph.facebook.com/v23.0/{instagram_business_id}/media",
        data={
            "media_type": "CAROUSEL",
            "children": ",".join(children),
            "caption": caption,
            "access_token": access_token,
        }
    )

    carousel_data = (
        carousel_response.json()
    )

    print(
        "Carousel Container:",
        carousel_data
    )

    if "id" not in carousel_data:
        raise Exception(carousel_data)

    creation_id = carousel_data["id"]

    time.sleep(10)

    publish_response = requests.post(
        f"https://graph.facebook.com/v23.0/{instagram_business_id}/media_publish",
        data={
            "creation_id": creation_id,
            "access_token": access_token,
        }
    )

    publish_data = (
        publish_response.json()
    )

    print(
        "Carousel Publish:",
        publish_data
    )

    if "id" not in publish_data:
        raise Exception(publish_data)

    return publish_data