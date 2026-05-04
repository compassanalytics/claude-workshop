"""Event SQLAlchemy model."""

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String

from src.api.models.user import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    name = Column(String, nullable=False)
    properties = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
