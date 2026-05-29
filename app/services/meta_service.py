import os

META_APP_ID = os.getenv("META_APP_ID")

META_REDIRECT_URI = os.getenv("META_REDIRECT_URI")


def get_meta_login_url():
    return (
        "https://www.facebook.com/v23.0/dialog/oauth"
        f"?client_id={META_APP_ID}"
        f"&redirect_uri={META_REDIRECT_URI}"
        "&scope="
        "pages_show_list,"
        "pages_manage_posts,"
        "instagram_basic,"
        "instagram_content_publish,"
        "business_management"
    )