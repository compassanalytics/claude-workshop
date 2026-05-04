# Testing Rules

These rules always apply, regardless of which file is being read or written. (No `paths:` frontmatter — unscoped.)

## pytest
- Use fixtures from `tests/conftest.py`. Don't write raw setup/teardown methods.
- Available fixtures:
  - `client` — FastAPI `TestClient` with overridden DB.
  - `db` — in-memory SQLite session.
  - `auth_headers` — pre-baked JWT for a demo user (`Authorization: Bearer ...`).
- Test names describe behavior: `test_login_rejects_unknown_email`, never `test_login_2`.
- Every API route needs at least one failure-case (4xx) test in addition to the happy path.

## Frontend tests
- Vitest + React Testing Library. Files end in `.test.tsx` co-located with the component.
- Query by accessible role/text, not test IDs: `screen.getByRole("button", { name: "Sign in" })`.

## Coverage
- New code requires tests. Bug fixes require a regression test that fails before the fix.
- Don't chase 100%. Cover the meaningful paths.
