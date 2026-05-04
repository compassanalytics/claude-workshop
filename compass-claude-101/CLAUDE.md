# Compass Claude 101 — Demo Project

A small ingestion service used to demo Claude Code config layers. FastAPI backend + tiny React dashboard.

## Stack

- Python 3.11+ / FastAPI / Pydantic v2 / SQLAlchemy / SQLite (`src/api/`)
- TypeScript / React 18 / Vite (`web/`)
- pytest with shared fixtures from `tests/conftest.py`

## Project shape

- API source: `src/api/` — split by resource (`auth/`, `ingest/`, `models/`, `db/`).
- Web source: `web/src/` — components in `web/src/components/`, hooks in `web/src/hooks/`.
- Tests: `tests/` — one file per resource, fixtures live in `conftest.py`.

## Broad principles

- snake_case for Python, camelCase for TS, PascalCase for components/types.
- Ask before adding new dependencies.
- Never push directly to `main`.
- Don't modify `.claude/` config files unless the user asks.

## Build & test

- Backend tests: `pytest`
- Backend run: `uvicorn src.api.main:app --reload`
- Frontend dev: `cd web && npm run dev`
- Lint: `ruff check src/ tests/` and `cd web && npm run lint`

## Where the details live

Project-wide CLAUDE.md is intentionally short. Detailed conventions are scoped:

- `.claude/rules/backend/api.md` — applies when reading files in `src/api/`.
- `.claude/rules/frontend/ui.md` — applies when reading files in `web/src/`.
- `.claude/rules/testing.md` — always loaded (unscoped).
