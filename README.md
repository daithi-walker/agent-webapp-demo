# agent-webapp-demo

Seed repository for the temporal-agent-poc end-to-end webapp test.

## Goal

Build a Python Flask web application with:

- `GET /health` — returns `{"status": "ok"}`
- `POST /validate` — accepts JSON `{"value": <any>}`, returns `{"valid": true/false, "reason": "..."}`
  - valid means `value` is a positive integer (> 0)
  - invalid inputs: strings, floats, zero, negatives, missing field, null
- `GET /` — minimal HTML page with a form that calls `/validate` via `fetch` and shows the result
- `requirements.txt` listing `flask`
- `test_app.py` with pytest tests using Flask test client, covering all routes and edge cases

## Running with Docker

```bash
docker compose up
```

The app will be available at http://localhost:5000.

To stop the app, run:

```bash
docker compose down
```
