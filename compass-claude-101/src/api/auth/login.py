"""Login route.

NOTE: this file contains intentional, well-marked security issues used for
the workshop's `security-scanner` subagent demo. Do NOT copy these patterns.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.api.auth.tokens import issue_token
from src.api.db.session import get_db
from src.api.errors import problem

router = APIRouter()


class LoginRequest(BaseModel):
    email: Annotated[EmailStr, Field(description="User email")]
    password: Annotated[str, Field(min_length=1, description="Plaintext password")]


class LoginResponse(BaseModel):
    access_token: str
    token_type: Annotated[str, Field(description="Always 'bearer'")] = "bearer"


@router.post("/login", response_model=LoginResponse)
def login(
    payload: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
) -> LoginResponse:
    # FIXME[security]: no rate limit on this endpoint — credential stuffing possible.
    # FIXME[security]: SQL injection — email is interpolated directly into the query.
    row = db.execute(
        text(f"SELECT id, password FROM users WHERE email = '{payload.email}'")
    ).first()

    # FIXME[security]: plaintext password comparison. Should use bcrypt/argon2 + constant-time compare.
    if not row or row.password != payload.password:
        raise HTTPException(
            status_code=401,
            detail=problem("invalid_credentials", "Bad email or password", 401).model_dump(),
        )

    return LoginResponse(access_token=issue_token(str(row.id)))
