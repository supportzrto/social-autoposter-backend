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

    return {
        "success": True,
        "token_data": token_data
    }