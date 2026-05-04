"""Importing this package registers all SQLAlchemy models with `Base.metadata`."""

from src.api.models.event import Event
from src.api.models.user import Base, User

__all__ = ["Base", "Event", "User"]
