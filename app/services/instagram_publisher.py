import requests
import time


def publish_instagram_image(
    instagram_business_id: str,
    access_token: str,
    image_url: str,
    caption: str
):

    create_response = requests.post(
        f"https://graph.facebook.com/v23.0/{instagram_business_id}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token,
        }
    )

    create_data = create_response.json()

    print("Create Container:", create_data)

    if "id" not in create_data:

        raise Exception(
            f"Container Error: {create_data}"
        )

    creation_id = create_data["id"]

    # Wait for Instagram to process media
    for _ in range(12):

        status_response = requests.get(
            f"https://graph.facebook.com/v23.0/{creation_id}",
            params={
                "fields": "status_code",
                "access_token": access_token
            }
        )

        status_data = (
            status_response.json()
        )

        print(
            "Image Status:",
            status_data
        )

        if (
            status_data.get(
                "status_code"
            )
            == "FINISHED"
        ):
            break

        time.sleep(5)

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

    print("Publish:", publish_data)

    if "id" not in publish_data:

        raise Exception(
            f"Publish Error: {publish_data}"
        )

    return publish_data