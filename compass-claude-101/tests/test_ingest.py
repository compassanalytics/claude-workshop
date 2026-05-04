"""Ingest route tests."""

from fastapi.testclient import TestClient


def test_create_event_requires_auth(client: TestClient) -> None:
    res = client.post("/api/events/", json={"name": "signup"})
    assert res.status_code in {401, 403}


def test_create_event_succeeds_with_auth(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    res = client.post("/api/events/", json={"name": "signup"}, headers=auth_headers)
    assert res.status_code == 201
    body = res.json()
    assert body["name"] == "signup"


def test_list_events_rejects_oversized_limit(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    res = client.get("/api/events/?limit=200", headers=auth_headers)
    assert res.status_code == 422
