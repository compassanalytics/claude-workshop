"""User SQLAlchemy model.

NOTE: stores password as plaintext String. This is intentional for the
workshop's `security-scanner` demo. Do NOT copy this pattern.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from src.api.db.session import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    # FIXME[security]: should be a hash, not plaintext.
    password = Column(String, nullable=False)


def init_users_table() -> None:
    Base.metadata.create_all(bind=engine, tables=[User.__table__])
