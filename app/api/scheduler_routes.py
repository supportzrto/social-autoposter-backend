from fastapi import (
    APIRouter,
    HTTPException,
    Query
)

import os

from app.workers.scheduler import (
    check_scheduled_posts
)

router = APIRouter()


@router.get("/scheduler/run")
def run_scheduler(
    secret: str = Query(...)
):

    expected_secret = os.getenv(
        "SCHEDULER_SECRET"
    )

    if secret != expected_secret:

        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    check_scheduled_posts()

    return {
        "success": True
    }