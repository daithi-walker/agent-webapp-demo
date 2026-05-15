from flask import Flask, request, jsonify, Response

app = Flask(__name__)


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
    valid, reason = validate_value(body["value"])
    return jsonify({"valid": valid, "reason": reason}), 200
