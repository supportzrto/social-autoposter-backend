from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
import requests
import os

from app.services.meta_service import get_meta_login_url

router = APIRouter(
    prefix="/auth/meta",
    tags=["Meta Auth"]
)


@router.get("/login")
def meta_login():
    return RedirectResponse(
        get_meta_login_url()
    )


@router.get("/callback")
def meta_callback(code: str = Query(...)):

    # Step 1: Exchange code for access token
    token_response = requests.get(
        "https://graph.facebook.com/v23.0/oauth/access_token",
        params={
            "client_id": os.getenv("META_APP_ID"),
            "client_secret": os.getenv("META_APP_SECRET"),
            "redirect_uri": os.getenv("META_REDIRECT_URI"),
            "code": code,
        },
    )

    token_data = token_response.json()

    access_token = token_data.get("access_token")

    if not access_token:
        return {
            "success": False,
            "token_data": token_data
        }

    # Step 2: Get Facebook Pages
    pages_response = requests.get(
        "https://graph.facebook.com/v23.0/me/accounts",
        params={
            "access_token": access_token
        }
    )

    pages_data = pages_response.json()

    return {
        "success": True,
        "access_token": access_token,
        "pages": pages_data
    }