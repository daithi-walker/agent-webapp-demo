import threading
from collections import deque
from datetime import datetime, timezone

from flask import Flask, request, jsonify, Response

app = Flask(__name__)

_history: deque[dict] = deque(maxlen=50)
_history_lock = threading.Lock()


def validate_value(value: object) -> tuple[bool, str]:
    """Returns a (valid, reason) tuple for whether value is a positive integer."""
    if not isinstance(value, int) or isinstance(value, bool):
        return False, "value must be an integer"
    if value <= 0:
        return False, "value must be greater than zero"
    return True, "value is a positive integer"


@app.get("/health")
def health() -> Response:
    """Returns service health status."""
    return jsonify({"status": "ok"})


@app.post("/validate")
def validate() -> tuple[Response, int]:
    """Returns validation result for the posted value."""
    body = request.get_json(silent=True)
    if body is None or "value" not in body:
        return jsonify({"valid": False, "reason": "missing field: value"}), 400
    value = body["value"]
    valid, reason = validate_value(value)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "value": value,
        "valid": valid,
        "reason": reason,
    }
    with _history_lock:
        _history.append(record)
    return jsonify({"valid": valid, "reason": reason}), 200


@app.get("/history")
def history() -> Response:
    """Returns the last 50 validation records, most recent last."""
    with _history_lock:
        records = list(_history)
    return jsonify({"history": records})
