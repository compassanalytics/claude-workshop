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

## Workflow

- Ask before adding new dependencies.
- Treat `.claude/` config as user-managed — ask before changing it.

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

## Canonical patterns to follow

Plain path references below — read them on demand, not loaded eagerly. (If we
used `@path` instead, all three files would load into context at session start.)

- `src/api/errors.py` — the `problem()` helper for ProblemDetails error bodies.
- `src/api/auth/tokens.py` — the `get_current_user` auth dependency.
- `tests/conftest.py` — shared pytest fixtures (`client`, `db`, `auth_headers`).
