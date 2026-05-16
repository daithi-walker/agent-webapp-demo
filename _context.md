## Goal
Add a web frontend HTML page for the validator (form + result display), add in-memory validation history (last 50 entries), add GET /history endpoint returning recent validations, add CHANGELOG.md and VERSION file

## This task
Update templates/index.html to add a validation history section below the existing result area. Add a 'Load History' button that calls GET /history via fetch and renders a table (columns: timestamp, value, valid, reason) inside a <section id='history'>. Keep existing form and result display intact. No external CSS/JS dependencies — inline styles only.

## Prior task results

### task-1
Files: CLAUDE.md, _context.md, app.py
Changes made to `app.py`:

- Added `import threading` and `from collections import deque` and `from datetime import datetime, timezone` at the top.
- Added module-level `_history` deque (maxlen=50) and `_history_lock` threading.Lock.
- Updated `POST /validate` to build a record with ISO-8601 UTC timestamp, value, valid, and reason, then append it to the deque inside a `with _history_lock` block.
-