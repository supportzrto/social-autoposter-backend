from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    facebook_page_id = Column(String, nullable=True)

    instagram_business_id = Column(String, nullable=True)

    access_token = Column(String, nullable=True)

    # refresh_token = Column(String, nullable=True)

    # token_expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)