"""SQLAlchemy session factory."""

import os
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Read from environment. Falls back to a local SQLite file for dev convenience.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./compass.db")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine, future=True)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
