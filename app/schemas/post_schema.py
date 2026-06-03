from typing import List 
from datetime import datetime

from pydantic import BaseModel



class PostCreate(BaseModel):

    brand_id: int

    title: str

    caption: str

    media_urls: List[str]

    media_type: str

    platforms: List[str]

    schedule_time: datetime

    status: str = "PENDING"


class PostResponse(PostCreate):
    id: int
    created_at: datetime | None = None
    published_at: datetime | None = None
    error_message: str | None = None

    class Config:
        from_attributes = True