import requests

def publish_facebook_image(
    page_id: str,
    access_token: str,
    image_url: str,
    caption: str
):

    response = requests.post(
        f"https://graph.facebook.com/v23.0/{page_id}/photos",
        data={
            "url": image_url,
            "caption": caption,
            "access_token": access_token
        }
    )

    return response.json()