"""Event ingestion routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.api.auth.tokens import get_current_user
from src.api.db.session import get_db

router = APIRouter()


class EventIn(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=128)]
    properties: Annotated[dict, Field(default_factory=dict)]


class EventOut(BaseModel):
    id: int
    name: str


@router.post("/", response_model=EventOut, status_code=201)
def create_event(
    payload: EventIn,
    user_id: Annotated[str, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> EventOut:
    # TODO: persist event for user_id.
    return EventOut(id=1, name=payload.name)


@router.get("/", response_model=list[EventOut])
def list_events(
    user_id: Annotated[str, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[EventOut]:
    # TODO: paginate from DB.
    return []
