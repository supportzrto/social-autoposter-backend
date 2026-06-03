from fastapi import APIRouter, Query, Depends, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import requests
import os

from app.services.meta_service import get_meta_login_url
from app.database.database import get_db
from app.models.brand_model import Brand
from app.dependencies.auth_dependency import get_current_user
from app.models.user_model import User
from fastapi import Depends
from fastapi import HTTPException

router = APIRouter(
    prefix="/auth/meta",
    tags=["Meta Auth"]
)


@router.get("/login")
def meta_login():
    return RedirectResponse(
        get_meta_login_url()
    )

@router.post("/logout")
def logout(response: Response):

    response.set_cookie(
        key="access_token",
        value="",
        max_age=0,
        expires=0,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
    )

    return {
        "success": True
    }

@router.get("/callback")
def meta_callback(
    code: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print("CALLBACK HIT")

    
@router.get("/callback")
def meta_callback(
    code: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    print(token_response.json())

    token_data = token_response.json()
    access_token = token_data.get("access_token")
    user_access_token = access_token
    

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
    print("ALL PAGES:")
    print(pages_data)

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
    Brand.facebook_page_id == page_id,
    Brand.user_id == current_user.id
).first()

    if brand:
        # Update existing brand
        brand.access_token = page_access_token
        brand.user_access_token = (user_access_token)
        brand.instagram_business_id = ig_id
    else:
        # Create new brand
        brand = Brand(
            name=page_name,

            user_id=current_user.id,

            facebook_page_id=page_id,

            instagram_business_id=ig_id,

            access_token=page_access_token,

            user_access_token=user_access_token
        )
        db.add(brand)
        print("ACCESS TOKEN:", access_token)
        print("USER ACCESS TOKEN:", user_access_token)
        print("BEFORE SAVE:", brand.user_access_token)

    db.commit()
    db.refresh(brand)

    print(
        "AFTER SAVE:",
        brand.user_access_token
    )

    return {
        "success": True,
        "brand_id": brand.id,
        "brand_name": brand.name,
        "facebook_page_id": brand.facebook_page_id,
        "instagram_business_id": brand.instagram_business_id,
    }

@router.get("/pages")
def get_pages(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    brand = (
        db.query(Brand)
        .filter(
            Brand.user_id ==
            current_user.id
        )
        .first()
    )

    if not brand:

        raise HTTPException(
            status_code=404,
            detail="No connected brand found"
        )
    
    print(
        "TOKEN:",
        brand.access_token
    )

    response = requests.get(
        "https://graph.facebook.com/v23.0/me",
        params={
            "access_token":
                brand.access_token
        }
    )
    print(
        "META RESPONSE:",
        response.json()
    )

    return response.json()

@router.get("/all-pages")
def get_all_pages(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    brand = (
        db.query(Brand)
        .filter(
            Brand.user_id ==
            current_user.id
        )
        .first()
    )

    if not brand:
        return {
            "error": "No brand found"
        }

    print(
        "USER TOKEN:",
        brand.user_access_token
    )

    response = requests.get(
        "https://graph.facebook.com/v23.0/me/accounts",
        params={
            "access_token":
                brand.user_access_token
        }
    )

    return response.json()

# @router.get("/test-kriday")
# def test_kriday(
#     db: Session = Depends(get_db)
# ):

#     brand = db.query(Brand).first()

#     response = requests.get(
#         "https://graph.facebook.com/v23.0/844102702122155",
#         params={
#             "fields": "id,name,instagram_business_account",
#             "access_token": brand.access_token
#         }
#     )

#     return response.json()

# @router.get("/test-page")
# def test_page(
#     db: Session = Depends(get_db)
# ):

#     brand = db.query(Brand).first()

#     response = requests.get(
#         "https://graph.facebook.com/v23.0/61583357375569",
#         params={
#             "fields": "id,name",
#             "access_token": brand.access_token
#         }
#     )

#     return response.json()