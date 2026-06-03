from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base
from sqlalchemy import ForeignKey


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
    Integer,
    ForeignKey("users.id"),
    nullable=False
)

    name = Column(String, nullable=False)

    facebook_page_id = Column(String, nullable=True)

    instagram_business_id = Column(String, nullable=True)

    access_token = Column(String, nullable=True)

    user_access_token = Column(String,nullable=True)

    # refresh_token = Column(String, nullable=True)

    # token_expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)