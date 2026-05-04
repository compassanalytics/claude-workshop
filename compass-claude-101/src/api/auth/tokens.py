"""JWT helpers and the get_current_user dependency."""

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.errors import problem

# Demo only — in production, load from env / secrets manager.
JWT_SECRET = "demo-secret-do-not-use-in-prod"
JWT_ALG = "HS256"
ACCESS_TTL = timedelta(minutes=30)

_bearer = HTTPBearer()


def issue_token(user_id: str) -> str:
    expires = datetime.now(tz=timezone.utc) + ACCESS_TTL
    payload = {"sub": user_id, "exp": int(expires.timestamp())}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def get_current_user(
    creds: Annotated[HTTPAuthorizationCredentials, Depends(_bearer)],
) -> str:
    try:
        decoded = jwt.decode(creds.credentials, JWT_SECRET, algorithms=[JWT_ALG])
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=401,
            detail=problem("invalid_token", str(exc), 401).model_dump(),
        ) from exc
    return decoded["sub"]
