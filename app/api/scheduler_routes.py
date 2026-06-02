from fastapi import APIRouter

from app.workers.scheduler import (
    check_scheduled_posts
)

router = APIRouter()


@router.get("/scheduler/run")
def run_scheduler():

    check_scheduled_posts()

    return {
        "success": True
    }