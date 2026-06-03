import requests


def publish_facebook_video(
    page_id: str,
    access_token: str,
    video_url: str,
    caption: str
):

    response = requests.post(
        f"https://graph.facebook.com/v23.0/{page_id}/videos",
        data={
            "file_url": video_url,
            "description": caption,
            "access_token": access_token,
        }
    )

    result = response.json()

    print(
        "Facebook Video:",
        result
    )

    if "id" not in result:

        raise Exception(
            f"Facebook Video Error: {result}"
        )

    return result