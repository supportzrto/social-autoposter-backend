from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.brand_model import Brand
from app.models.user_model import User
from app.schemas.brand_schema import (
    BrandCreate,
    BrandResponse
)

router = APIRouter(prefix="/brands")


@router.post("")
def create_brand(
    brand: BrandCreate,
    db: Session = Depends(get_db)
):
    new_brand = Brand(
        name=brand.name
    )

    db.add(new_brand)

    db.commit()

    db.refresh(new_brand)

    return new_brand


@router.get("")
def get_brands(
    db: Session = Depends(get_db)
):
    return db.query(Brand).all()

@router.get("/me")
def get_my_brands(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    brands = db.query(Brand).filter(
        Brand.user_id == current_user.id
    ).all()

    return brands