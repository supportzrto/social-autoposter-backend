from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.services.meta_service import get_meta_login_url

router = APIRouter(
    prefix="/auth/meta",
    tags=["Meta Auth"]
)
@router.get("/login")
def meta_login():

    return {
        "url": get_meta_login_url()
    }