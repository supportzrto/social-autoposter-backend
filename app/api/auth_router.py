from fastapi import APIRouter, Query, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import requests
import os

from app.services.meta_service import get_meta_login_url
from app.database.database import get_db
from app.models.brand_model import Brand

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
def meta_callback(
    code: str = Query(...),
    db: Session = Depends(get_db)
):

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
            "error": token_data
        }

    # Step 2: Get Facebook Pages
    pages_response = requests.get(
        "https://graph.facebook.com/v23.0/me/accounts",
        params={"access_token": access_token}
    )
    pages_data = pages_response.json()

    if not pages_data.get("data"):
        return {
            "success": False,
            "error": "No Facebook pages found"
        }

    page = pages_data["data"][0]
    page_id = page["id"]
    page_name = page["name"]
    page_access_token = page.get("access_token", access_token)

    # Step 3: Get Instagram Business Account
    ig_response = requests.get(
        f"https://graph.facebook.com/v23.0/{page_id}",
        params={
            "fields": "instagram_business_account",
            "access_token": page_access_token
        }
    )
    ig_data = ig_response.json()
    ig_id = ig_data.get("instagram_business_account", {}).get("id")

    # Step 4: Save or update Brand in DB
    brand = db.query(Brand).filter(
        Brand.facebook_page_id == page_id
    ).first()

    if brand:
        # Update existing brand
        brand.access_token = page_access_token
        brand.instagram_business_id = ig_id
    else:
        # Create new brand
        brand = Brand(
            name=page_name,
            facebook_page_id=page_id,
            instagram_business_id=ig_id,
            access_token=page_access_token,
        )
        db.add(brand)

    db.commit()
    db.refresh(brand)

    return {
        "success": True,
        "brand_id": brand.id,
        "brand_name": brand.name,
        "facebook_page_id": brand.facebook_page_id,
        "instagram_business_id": brand.instagram_business_id,
    }