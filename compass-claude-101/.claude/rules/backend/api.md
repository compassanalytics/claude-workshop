---
paths:
  - "src/api/**/*.py"
---

# Backend API Rules

Apply when reading or editing files under `src/api/`.

## Pydantic v2 — strict syntax
- Always `from typing import Annotated`. Use `Annotated[T, Field(...)]`.
- Pydantic v1 `Field` defaults (`name: str = Field(...)`) are forbidden.
- Email fields use `EmailStr` from `pydantic`. Don't roll your own regex.

## Routers
- Each resource gets its own router file: `src/api/<resource>/routes.py` exporting `router = APIRouter()`.
- Routers register in `src/api/main.py` via `app.include_router(router, prefix="/api/<resource>", tags=["<resource>"])`.
- Always declare `response_model=` in the decorator. Always declare `status_code=` for non-200 success responses (e.g., `201` on create).

## Auth
- The auth dependency is `get_current_user` from `src.api.auth.tokens`.
  Use exactly: `user_id: Annotated[str, Depends(get_current_user)]`.
- Don't roll your own header parsing. Don't introduce parallel auth helpers.

## Database
- Get sessions via `Depends(get_db)` from `src.api.db.session`. Never instantiate engines in route handlers.
- Always parameterize. Use SQLAlchemy ORM or `text()` with bind params — never f-string interpolation.

## Errors
- All HTTP errors raise `HTTPException(status_code=..., detail=problem(...).model_dump())`.
- The `problem()` helper from `src.api.errors` is the ONLY way to construct error bodies.
  Signature: `problem(title: str, detail: str, status: int = 400)`.
- Never return raw dicts or strings as error responses. Never construct `ProblemDetails` directly.

## Pagination
- List routes accept `limit` and `offset`:
  ```python
  limit: Annotated[int, Query(ge=1, le=100)] = 50,
  offset: Annotated[int, Query(ge=0)] = 0,
  ```
- Don't invent alternative pagination shapes (cursors, page numbers) in this codebase.

## Logging
- `from loguru import logger` — never the stdlib `logging` module.
- Log levels: INFO for route entry, WARNING for handled errors, ERROR for unexpected.
