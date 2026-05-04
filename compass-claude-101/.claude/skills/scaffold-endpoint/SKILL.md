---
name: scaffold-endpoint
description: Scaffold a new FastAPI endpoint with route handler, Pydantic schemas, and a test stub. Use when adding a new API route under src/api/.
argument-hint: "<METHOD> <PATH> — e.g., POST /api/events/search"
model: sonnet
---

# Scaffold Endpoint

Generates a complete vertical slice for a new API endpoint. Saves the boilerplate.

## What you provide

`$ARGUMENTS` — HTTP method and path. Examples:

- `POST /api/events/search`
- `DELETE /api/events/{event_id}`
- `GET /api/users/{user_id}/events`

## What you get

For `POST /api/events/search` you'll see:

1. **Route handler** added to the appropriate router file (`src/api/<resource>/routes.py`).
2. **Pydantic models** in `src/api/models/<resource>.py` — request and response shapes.
3. **Test stub** in `tests/test_<resource>.py` covering: 200 success, 422 validation error, 401 if auth-required.
4. **Router registration** in `src/api/main.py` if it's a new resource.

## Steps

0. Read `reference/route-template.py` (next to this file). It's the canonical shape — your output should mirror it, with names substituted from `$ARGUMENTS`.
1. Parse `$ARGUMENTS` for METHOD, PATH, and resource (path segment after `/api/`).
2. Locate the existing router for that resource. If none exists, create `src/api/<resource>/routes.py` and register it in `src/api/main.py`.
3. Add the route handler. Follow `.claude/rules/backend/api.md` — `response_model`, `Depends(get_current_user)`, `ProblemDetails` for errors.
4. Add Pydantic request/response models in `src/api/models/<resource>.py` using v2 `Annotated` syntax.
5. Add a test in `tests/test_<resource>.py` using fixtures from `conftest.py`. Include success + at least one 4xx case.
6. Run `pytest tests/test_<resource>.py -x` to confirm the stub compiles and the test infra is wired.
7. Print a summary: files added/modified, command to run the new endpoint locally.

## Don't

- Don't implement business logic — leave a `# TODO:` in the handler body. Scaffolding only.
- Don't create migrations. Separate concern.
- Don't run linters or formatters; the `PostToolUse` hook handles that automatically.
