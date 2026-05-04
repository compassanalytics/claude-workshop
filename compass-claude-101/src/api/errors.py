"""ProblemDetails (RFC 7807) error model and FastAPI handlers."""

from typing import Annotated

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class ProblemDetails(BaseModel):
    type: Annotated[str, Field(description="URI reference identifying the problem type.")] = "about:blank"
    title: Annotated[str, Field(description="Short, human-readable summary.")]
    status: Annotated[int, Field(description="HTTP status code.")]
    detail: Annotated[str | None, Field(description="Human-readable explanation specific to this occurrence.")] = None
    instance: Annotated[str | None, Field(description="URI reference identifying the specific occurrence.")] = None


def problem(
    title: str,
    detail: str,
    status: int = 400,
    type_: str = "about:blank",
) -> ProblemDetails:
    return ProblemDetails(type=type_, title=title, status=status, detail=detail)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        body = problem(
            title="validation_error",
            detail=str(exc.errors()),
            status=422,
            type_="https://compass.example/problems/validation",
        )
        return JSONResponse(status_code=422, content=body.model_dump())
