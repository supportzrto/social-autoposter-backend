from sqlalchemy import Column, Integer, String
from app.database.database import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime




class Post(Base):
    __tablename__ = "posts"

    

    id = Column(Integer, primary_key=True, index=True)

    brand_id = Column(
    Integer,
    ForeignKey("brands.id"),
    nullable=False
)

    title = Column(String, nullable=False)

    caption = Column(String, nullable=True)

    media_urls = Column(JSONB, nullable=False)

    media_type = Column(String, nullable=False)

    # platforms = Column(String, nullable=False)
    platforms = Column(JSONB, nullable=False)

    # schedule_time = Column(String, nullable=False)
    schedule_time = Column(DateTime, nullable=False)

    status = Column(String, default="PENDING")
    

    created_at = Column(DateTime, default=datetime.utcnow) 

    published_at = Column(DateTime, nullable=True) 
    
    error_message = Column(String, nullable=True)