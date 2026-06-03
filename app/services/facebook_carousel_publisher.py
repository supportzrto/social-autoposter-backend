import requests


def publish_facebook_carousel(
    page_id: str,
    access_token: str,
    image_urls: list,
    caption: str
):

    results = []

    for index, image_url in enumerate(
        image_urls
    ):

        response = requests.post(
            f"https://graph.facebook.com/v23.0/{page_id}/photos",
            data={
                "url": image_url,
                "caption":
                    caption
                    if index == 0
                    else "",
                "access_token":
                    access_token
            }
        )

        result = response.json()

        print(
            "Facebook Photo:",
            result
        )

        results.append(result)

    return results