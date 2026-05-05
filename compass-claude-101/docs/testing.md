# Testing

Pytest with shared fixtures from `tests/conftest.py`. Run with `pytest -q`.

## Available fixtures

- **`client`** — `TestClient` for the FastAPI app, with `get_db` overridden to the in-memory test session.
- **`db`** — In-memory SQLite session. Schema is created from `Base.metadata` at fixture setup so all model tables exist. Uses `StaticPool` + `check_same_thread=False` so the TestClient's request thread shares the database with the fixture thread.
- **`auth_headers`** — Pre-baked `{"Authorization": "Bearer <token>"}` for a demo user.

## Writing tests

```python
def test_create_event_succeeds_with_auth(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    res = client.post("/api/events/", json={"name": "signup"}, headers=auth_headers)
    assert res.status_code == 201
```

Test names describe the behaviour: `test_login_rejects_unknown_email`, never `test_login_2`.

## Coverage expectations

Every API route has at least one happy-path test and one failure-case (4xx) test. New code requires tests; bug fixes require a regression test that fails before the fix.
