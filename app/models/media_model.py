# app/models/media_model.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from datetime import datetime

from app.database.database import Base


class Media(Base):

    __tablename__ = "media"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    public_id = Column(
        String,
        nullable=False
    )

    url = Column(
        String,
        nullable=False
    )

    resource_type = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )