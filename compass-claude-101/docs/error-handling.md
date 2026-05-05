# Error handling

All HTTP errors in this codebase return a **ProblemDetails** payload (RFC 7807) instead of bare strings or unstructured dicts.

## The contract

- Status code in the HTTP response (4xx, 5xx).
- `detail` field on every `HTTPException` is a `ProblemDetails` model dumped to dict.
- Standard fields: `type` (URI), `title` (short summary), `status` (HTTP code), `detail` (human-readable explanation), optional `instance`.

## The helper

Use `problem()` from `src/api/errors.py`:

```python
from fastapi import HTTPException
from src.api.errors import problem

raise HTTPException(
    status_code=422,
    detail=problem("invalid_event_type", "Unknown event type", 422).model_dump(),
)
```

Signature: `problem(title: str, detail: str, status: int = 400, type_: str = "about:blank")`.

## Don't

- Don't return bare strings as error responses.
- Don't construct `ProblemDetails` directly — use `problem()` so future schema changes stay centralized.
