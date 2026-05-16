## Goal
Add a web frontend HTML page for the validator (form + result display), add in-memory validation history (last 50 entries), add GET /history endpoint returning recent validations, add CHANGELOG.md and VERSION file

## This task
Modify app.py to add in-memory validation history: import collections.deque (maxlen=50) as a module-level variable; update the POST /validate handler to append a record {timestamp (ISO-8601 UTC), value, valid, reason} to the deque after each validation; add a new GET /history route that returns {"history": [...]} with the deque contents as a list (most recent last). Use thread-safe access — wrap deque appends with a threading.Lock. Follow existing type-hint and docstring conventions from standards/coding.md.