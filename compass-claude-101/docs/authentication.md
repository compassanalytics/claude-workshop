# Authentication

JWT bearer-token auth via the `get_current_user` FastAPI dependency.

## The pattern

Routes that require an authenticated user inject the user id like this:

```python
from typing import Annotated
from fastapi import APIRouter, Depends
from src.api.auth.tokens import get_current_user

router = APIRouter()

@router.post("/", response_model=EventOut)
def create_event(
    user_id: Annotated[str, Depends(get_current_user)],
    ...
):
    ...
```

The dependency:

1. Reads `Authorization: Bearer <token>` via FastAPI's `HTTPBearer`.
2. Decodes the JWT with `JWT_SECRET` (read from environment at import time).
3. Returns the `sub` claim as the user id.
4. Raises `401` with a `ProblemDetails` body if the token is missing, malformed, or expired.

## Issuing tokens

Use `issue_token(user_id)` from `src/api/auth/tokens.py`. Returns a signed JWT with a 30-minute TTL.

## Don't

- Don't roll your own header parsing or token validation. Reuse `get_current_user`.
- Don't store the secret in source. `JWT_SECRET` is read from the environment; deployments MUST set it.
