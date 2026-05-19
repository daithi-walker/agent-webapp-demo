import json
import pytest
from app import app


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
