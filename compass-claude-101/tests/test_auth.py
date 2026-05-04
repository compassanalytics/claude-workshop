"""Auth route tests."""

from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_login_rejects_invalid_payload_shape(client: TestClient) -> None:
    res = client.post("/api/auth/login", json={"email": "not-an-email"})
    assert res.status_code == 422


def test_login_rejects_unknown_email(client: TestClient) -> None:
    res = client.post(
        "/api/auth/login",
        json={"email": "ghost@example.com", "password": "x"},
    )
    assert res.status_code == 401
