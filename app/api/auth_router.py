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

router = APIRouter(prefix="/auth/meta", tags=["Meta Auth"])


@router.get("/login")
def meta_login(current_user: User = Depends(get_current_user)):

    print("LOGIN USER:", current_user.id)

    url = get_meta_login_url(current_user.id)

    print("META URL:", url)

    return RedirectResponse(url)


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

    return {"success": True}


@router.get("/callback")
def meta_callback(
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db)
):

    print("CALLBACK HIT")

    user_id = int(state)

    print("STATE USER:", user_id)

    # Exchange code for access token
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

    print("TOKEN DATA:", token_data)

    access_token = token_data.get("access_token")

    if not access_token:
        return {
            "success": False,
            "error": token_data
        }

    # Check pages exist
    pages_response = requests.get(
        "https://graph.facebook.com/v23.0/me/accounts",
        params={
            "access_token": access_token
        }
    )

    pages_data = pages_response.json()

    print("ALL PAGES:", pages_data)

    if not pages_data.get("data"):
        return {
            "success": False,
            "error": "No Facebook pages found"
        }

    # Find any existing brand for this user
    brand = (
        db.query(Brand)
        .filter(
            Brand.user_id == user_id
        )
        .first()
    )

    if brand:

        brand.user_access_token = access_token

    else:

        brand = Brand(
            name="Meta Connected",
            user_id=user_id,
            user_access_token=access_token
        )

        db.add(brand)

    db.commit()
    db.refresh(brand)

    return {
        "success": True,
        "message": "Meta connected successfully"
    }


@router.get("/pages")
def get_pages(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):

    brand = db.query(Brand).filter(Brand.user_id == current_user.id).first()

    if not brand:

        raise HTTPException(status_code=404, detail="No connected brand found")

    response = requests.get(
        "https://graph.facebook.com/v23.0/me",
        params={"access_token": brand.access_token},
    )

    return response.json()


@router.get("/all-pages")
def get_all_pages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    brand = (
        db.query(Brand)
        .filter(
            Brand.user_id == current_user.id,
            Brand.user_access_token.isnot(None)
        )
        .first()
    )

    if not brand:
        return {
            "error": "No Meta account connected"
        }

    response = requests.get(
        "https://graph.facebook.com/v23.0/me/accounts",
        params={
            "access_token":
            brand.user_access_token
        }
    )

    pages_data = response.json()

    result = []

    for page in pages_data.get("data", []):

        page_id = page["id"]

        page_token = page.get(
            "access_token"
        )

        ig_response = requests.get(
            f"https://graph.facebook.com/v23.0/{page_id}",
            params={
                "fields":
                "instagram_business_account",
                "access_token":
                page_token
            }
        )

        ig_data = ig_response.json()

        result.append({
            "id": page_id,
            "name": page["name"],
            "access_token": page_token,
            "instagram_business_id":
            ig_data.get(
                "instagram_business_account",
                {}
            ).get("id")
        })

    return {
        "data": result
    }