"""Shared pytest fixtures for the API tests."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.auth.tokens import issue_token
from src.api.db.session import get_db
from src.api.main import app
from src.api.models import Base  # importing the package also registers Event with Base.metadata


@pytest.fixture
def db() -> Iterator[Session]:
    """In-memory SQLite session for isolated tests.

    Uses StaticPool + check_same_thread=False so the FastAPI TestClient
    (which runs requests in a separate thread) can share the same in-memory
    database as the fixture thread.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(bind=engine)
    Maker = sessionmaker(bind=engine, future=True)
    session = Maker()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db: Session) -> Iterator[TestClient]:
    """FastAPI TestClient with `get_db` overridden to the in-memory session."""

    def _override_get_db() -> Iterator[Session]:
        yield db

    app.dependency_overrides[get_db] = _override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers() -> dict[str, str]:
    """Valid bearer token for a demo user."""
    token = issue_token("demo-user-1")
    return {"Authorization": f"Bearer {token}"}
