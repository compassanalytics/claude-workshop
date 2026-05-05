# Backend API source

Loaded when Claude works inside `src/api/`. Stacks on top of the project root `CLAUDE.md`.

When you're working in this directory, the canonical references are:

- `../../docs/authentication.md` — how `Depends(get_current_user)` works and where to use it
- `../../docs/error-handling.md` — the `problem()` helper and ProblemDetails contract
- `.claude/rules/backend/api.md` — detailed coding conventions, auto-loads when Claude reads any `*.py` file in this tree

## Layout

- `auth/` — JWT helpers + the login endpoint (intentionally insecure; the `FIXME[security]` markers exist for the security-scanner subagent demo)
- `ingest/` — event ingestion routes
- `db/` — SQLAlchemy session factory
- `models/` — declarative models (User, Event)
- `errors.py` — `problem()` helper and `ProblemDetails` exception handlers
- `main.py` — FastAPI app entry, router registration, lifespan
