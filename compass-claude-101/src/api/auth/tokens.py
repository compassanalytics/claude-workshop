"""JWT helpers and the get_current_user dependency."""

import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.errors import problem

# Read from environment. Production deployments MUST set JWT_SECRET.
# Falls back to a clearly-marked dev value if unset (tests, local runs without .env).
# Length ≥32 bytes to satisfy JWT's SHA-256 HMAC minimum.
JWT_SECRET = os.environ.get(
    "JWT_SECRET",
    "DEV-ONLY-set-JWT_SECRET-env-var-in-prod-this-fallback-is-not-a-secret",
)
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
