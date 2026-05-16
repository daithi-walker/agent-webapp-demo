## What changed

- **`app.py`**: Added in-memory validation history using a `deque(maxlen=50)` guarded by a `threading.Lock`; each `POST /validate` call now appends a record with ISO-8601 UTC timestamp, value, valid, and reason. Added `GET /history` endpoint returning `{"history": [...]}`.
- **`templates/index.html`**: Added a "Load History" button and a `<section id="history">` that fetches `GET /history` and renders results as a table.
- **`CHANGELOG.md`**: Created in Keep a Changelog format documenting the 1.1.0 release.
- **`VERSION`**: Created, set to `1.1.0`.

## Why

The validator had no persistence or visibility into past results. This adds a lightweight history layer (capped at 50 entries, in-memory only) and exposes it through both a REST endpoint and the existing HTML frontend.

## Review notes

The security review agent raised **two critical findings and one major finding** that are not yet fixed in the submitted code. **This PR should not be merged as-is.**

**Critical — XSS via unescaped `innerHTML` (`templates/index.html:61–66`):**
History records are interpolated directly into a template literal assigned to `section.innerHTML` with no HTML escaping. An attacker can `POST {"value": "<img src=x onerror=alert(1)>"}` — the endpoint rejects it as non-integer but still appends the raw string to `_history` — and the payload executes the next time any browser loads history. Fix: build the table using DOM methods (`document.createElement` + `el.textContent = ...`) instead of string interpolation into `innerHTML`.

**Critical — API shape mismatch makes history permanently non-functional (`templates/index.html:57`):**
`GET /history` returns `{"history": [...]}` (an object), but the handler checks `Array.isArray(data)` where `data` is that object. `Array.isArray` always returns `false` for a plain object, so the handler always renders "No history found." and returns before building the table. Fix: check `Array.isArray(data.history)` and iterate over `data.history`.

**Major — No tests (`app.py`):**
Task-4 (QA agent) failed due to a Docker infrastructure error and produced no test files. Coding and testing standards require every public function to have tests covering happy path, at least one edge case, and at least one invalid input. `validate_value`, `validate`, `history`, and `health` are all untested. A `test_app.py` must be added before this work is shippable.

## Test coverage

None. The QA agent (task-4) failed with a Docker infrastructure error and produced no test files. No automated tests exist for any of the new code.

## Files changed

- `app.py`
- `templates/index.html`
- `CHANGELOG.md`
- `VERSION`
