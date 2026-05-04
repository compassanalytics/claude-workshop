"""Compass ingestion service — FastAPI entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.api.auth.login import router as auth_router
from src.api.errors import register_error_handlers
from src.api.ingest.routes import router as ingest_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("api.startup")
    yield
    logger.info("api.shutdown")


app = FastAPI(title="Compass Ingest", version="0.1.0", lifespan=lifespan)

register_error_handlers(app)
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(ingest_router, prefix="/api/events", tags=["events"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
