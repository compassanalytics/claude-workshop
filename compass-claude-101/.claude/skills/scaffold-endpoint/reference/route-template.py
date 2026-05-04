"""Canonical route template — copy this shape when scaffolding new endpoints.

A working example of `POST /api/example/items` showing the conventions:

- Pydantic v2 `Annotated[T, Field(...)]` for request and response models
- `Depends(get_current_user)` for auth, `Depends(get_db)` for the DB session
- `response_model=` and `status_code=` declared in the decorator
- `problem()` helper for any `HTTPException` `detail` payloads (RFC 7807)
- `# TODO:` left in the handler body (the skill never implements business logic)

When the skill runs, it should follow this shape — substituting the resource,
method, path, and field names from `$ARGUMENTS`.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.api.auth.tokens import get_current_user
from src.api.db.session import get_db
from src.api.errors import problem

router = APIRouter()


class CreateItemRequest(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=128)]
    properties: Annotated[dict, Field(default_factory=dict)]


class ItemResponse(BaseModel):
    id: int
    name: str


@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(
    payload: CreateItemRequest,
    user_id: Annotated[str, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ItemResponse:
    # TODO: persist the item for user_id.
    raise HTTPException(
        status_code=501,
        detail=problem("not_implemented", "Stub — implement business logic.", 501).model_dump(),
    )
