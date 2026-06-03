from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.brand_model import Brand
from app.models.user_model import User
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.schemas.brand_schema import (
    BrandCreate,
    BrandResponse
)

router = APIRouter(prefix="/brands")


@router.post("")
def create_brand(
    brand: BrandCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    new_brand = Brand(
        name=brand.name,
        user_id=current_user.id
    )

    db.add(new_brand)

    db.commit()

    db.refresh(new_brand)

    return new_brand


@router.get("")
def get_brands(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return (
        db.query(Brand)
        .filter(
            Brand.user_id ==
            current_user.id
        )
        .all()
    )

@router.get("/me")
def get_my_brands(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    brands = db.query(Brand).filter(
        Brand.user_id == current_user.id
    ).all()

    return brands

@router.delete("/{brand_id}")
def delete_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    brand = (
        db.query(Brand)
        .filter(
            Brand.id == brand_id,
            Brand.user_id ==
            current_user.id
        )
        .first()
    )

    if not brand:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )

    try:

        db.delete(brand)

        db.commit()

        return {
            "success": True
        }

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=
            "Cannot delete brand because posts exist for this brand"
        )

@router.put("/{brand_id}")
def update_brand(
    brand_id: int,
    brand_data: BrandCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    brand = (
        db.query(Brand)
        .filter(
            Brand.id == brand_id,
            Brand.user_id ==
            current_user.id
        )
        .first()
    )

    if not brand:
        return {
            "error":
            "Brand not found"
        }

    brand.name = brand_data.name

    db.commit()

    db.refresh(brand)

    return brand

@router.put("/{brand_id}")
def update_brand(
    brand_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    brand = db.query(Brand).filter(
        Brand.id == brand_id,
        Brand.user_id == current_user.id
    ).first()

    if not brand:

        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )

    brand.facebook_page_id = data.get(
        "facebook_page_id"
    )

    brand.instagram_business_id = data.get(
        "instagram_business_id"
    )

    db.commit()

    return {
        "success": True
    }

@router.post("/{brand_id}/disconnect")
def disconnect_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    brand = db.query(Brand).filter(
        Brand.id == brand_id,
        Brand.user_id == current_user.id
    ).first()

    if not brand:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )

    brand.facebook_page_id = None
    brand.instagram_business_id = None
    brand.access_token = None

    # if you added this column
    brand.user_access_token = None

    db.commit()

    return {
        "success": True
    }