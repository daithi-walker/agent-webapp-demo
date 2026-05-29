import json
import pytest
import app as app_module
from app import app


@pytest.fixture(autouse=True)
def clear_history():
    app_module._history.clear()
    yield
    app_module._history.clear()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ── / ─────────────────────────────────────────────────────────────────────────


def test_index_returns_200(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_index_returns_html(client):
    resp = client.get("/")
    assert b"<!DOCTYPE html>" in resp.data or b"<html" in resp.data


# ── /health ───────────────────────────────────────────────────────────────────


def test_health_returns_200(client):
    resp = client.get("/health")
    assert resp.status_code == 200


def test_health_returns_ok_status(client):
    resp = client.get("/health")
    assert resp.get_json()["status"] == "ok"


# ── /validate ─────────────────────────────────────────────────────────────────


def test_validate_positive_integer(client):
    resp = client.post("/validate", json={"value": 5})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["valid"] is True


def test_validate_zero_is_invalid(client):
    resp = client.post("/validate", json={"value": 0})
    assert resp.get_json()["valid"] is False


def test_validate_negative_is_invalid(client):
    resp = client.post("/validate", json={"value": -3})
    assert resp.get_json()["valid"] is False


def test_validate_string_is_invalid(client):
    resp = client.post("/validate", json={"value": "hello"})
    assert resp.get_json()["valid"] is False


def test_validate_bool_is_invalid(client):
    resp = client.post("/validate", json={"value": True})
    assert resp.get_json()["valid"] is False


def test_validate_missing_field_returns_400(client):
    resp = client.post("/validate", json={"other": 1})
    assert resp.status_code == 400


def test_validate_no_body_returns_400(client):
    resp = client.post("/validate", content_type="application/json", data="")
    assert resp.status_code == 400


def test_validate_reason_present(client):
    resp = client.post("/validate", json={"value": 1})
    assert "reason" in resp.get_json()


# ── /history ──────────────────────────────────────────────────────────────────


def test_history_returns_list(client):
    resp = client.get("/history")
    assert resp.status_code == 200
    assert "history" in resp.get_json()
    assert isinstance(resp.get_json()["history"], list)


def test_history_records_validation(client):
    client.post("/validate", json={"value": 42})
    records = client.get("/history").get_json()["history"]
    assert any(r["value"] == 42 for r in records)


def test_history_record_has_expected_fields(client):
    client.post("/validate", json={"value": 7})
    record = client.get("/history").get_json()["history"][-1]
    for field in ("timestamp", "value", "valid", "reason"):
        assert field in record


# ── /stats ────────────────────────────────────────────────────────────────────


def test_stats_empty_state(client):
    resp = client.get("/stats")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] == 0
    assert data["valid"] == 0
    assert data["invalid"] == 0


def test_stats_after_valid_submissions(client):
    client.post("/validate", json={"value": 1})
    client.post("/validate", json={"value": 2})
    data = client.get("/stats").get_json()
    assert data["total"] == 2
    assert data["valid"] == 2
    assert data["invalid"] == 0


def test_stats_after_mixed_submissions(client):
    client.post("/validate", json={"value": 5})
    client.post("/validate", json={"value": -1})
    data = client.get("/stats").get_json()
    assert data["total"] == 2
    assert data["valid"] == 1
    assert data["invalid"] == 1
    assert data["total"] == data["valid"] + data["invalid"]
