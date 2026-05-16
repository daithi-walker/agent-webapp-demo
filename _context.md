## Goal
Add a web frontend HTML page for the validator (form + result display), add in-memory validation history (last 50 entries), add GET /history endpoint returning recent validations, add CHANGELOG.md and VERSION file

## This task
Review all changes from tasks 1-4 against standards/coding.md, standards/security.md, and standards/testing.md. Check: history deque is properly bounded, /history does not expose unexpected data, thread-safety is correct, type hints and docstrings are present on new functions, HTML does not introduce XSS via unescaped history values rendered into the DOM, CHANGELOG format is valid, VERSION is consistent with CHANGELOG.

## Prior task results

### task-1
Files: CLAUDE.md, _context.md, app.py
Changes made to `app.py`:

- Added `import threading` and `from collections import deque` and `from datetime import datetime, timezone` at the top.
- Added module-level `_history` deque (maxlen=50) and `_history_lock` threading.Lock.
- Updated `POST /validate` to build a record with ISO-8601 UTC timestamp, value, valid, and reason, then append it to the deque inside a `with _history_lock` block.
-

### task-2
Files: _context.md, templates/index.html
Changes made to `templates/index.html`:
- Added a "Load History" button and an empty `<section id="history">` below the result div.
- Added a click handler that fetches `GET /history`, then renders a bordered table with columns `timestamp`, `value`, `valid`, and `reason` using inline styles only. Handles empty results and fetch errors gracefully. The existing form and result display are untouched.

### task-3
Files: CHANGELOG.md, VERSION, _context.md
Created both files:

- **`VERSION`** — contains `1.1.0`
- **`CHANGELOG.md`** — Keep a Changelog format with an `[Unreleased]` section and a `[1.1.0] - 2026-05-16` section documenting the three added features, plus comparison links at the bottom

### task-4
Files: none
FAILED: Command '['docker', 'run', '--rm', '--network', 'bridge', '-v', '/Users/david.walker/.config/gcloud/application_default_credentials.json:/run/secrets/vertex-credentials.json:ro', '-e', 'GOOGLE_APPLICATION_CREDENTIALS=/run/secrets/vertex-credentials.json', '-e', 'CLAUDE_CODE_USE_VERTEX=1', '-e', 'ANTHROPIC_VERTEX_PROJECT_ID=simopt-dev', '-e', 'CLOUD_ML_REGION=global', '-v', '/var/folders/x9

## Review findings (must fix before proceeding)
- [critical] templates/index.html:63: XSS via unescaped innerHTML: r.timestamp, r.value, r.valid, and r.reason are interpolated directly into a template literal that is assigned to section.innerHTML without any HTML escaping. An attacker can POST {"value": "<img src=x onerror=alert(1)>"} to /validate — the endpoint rejects it as non-integer but still appends the record to _history — and the payload executes the next time a browser loads history. Fix: build the table using DOM methods (document.createElement + el.textContent = ...) rather than string interpolation into innerHTML.
- [critical] templates/index.html:57: API shape mismatch makes history permanently non-functional: GET /history returns {"history": [...]} (an object), but the handler checks Array.isArray(data) where data is that object. Array.isArray always returns false for a plain object, so !Array.isArray(data) is always true and the handler always renders 'No history found.' and returns before building the table. Fix: check Array.isArray(data.history) and iterate over data.history, not data.
- [major] app.py:1: No test file exists for any new public function. Task-4 failed entirely (Docker infrastructure error) and produced no files. Testing standards require every public function to have at least one test covering happy path, at least one edge case, and at least one invalid input. Functions validate_value, validate, history, and health are all untested. A test_app.py must be added before this work is shippable.