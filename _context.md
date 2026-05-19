## Goal
Fix three bugs in the Flask webapp: (1) templates/index.html has type="text" on the value input — change to type="number"; (2) the submit handler sends a string to the API — wrap document.getElementById('value').value with parseInt(..., 10) before JSON.stringify; (3) the history button handler checks Array.isArray(data) but the /history endpoint returns {"history": [...]}, so it should read data.history. Write pytest tests using the Flask test client covering all routes and the integer-vs-string validation.

## This task
Review task-1 and task-2 output against standards/coding.md and standards/testing.md. Verify: the three HTML fixes are exactly as specified; test file has type hints where applicable, follows naming conventions, each test is independent, asserts specific values; no dead code or magic numbers introduced.

## Prior task results

### task-1
Files: CLAUDE.md, _context.md, templates/index.html
All three changes applied to `templates/index.html`:

1. **Line 19** — `type="text"` → `type="number"` on the value input.
2. **Line 39** — wrapped the value in `parseInt(..., 10)` so the fetch body sends an integer.
3. **Lines 57–61** — condition now checks `!Array.isArray(data.history)` and the `.map()` iterates over `data.history`.

### task-2
Files: CLAUDE.md, __pycache__/app.cpython-311.pyc, _context.md, tests/__pycache__/test_app.cpython-311-pytest-9.0.3.pyc, tests/test_app.py
12/12 passed.

```json
{
  "verdict": "pass",
  "tests_written": ["tests/test_app.py"],
  "tests_run": 12,
  "tests_passed": 12,
  "tests_failed": 0,
  "route_coverage": {
    "routes_found_in_templates": ["/health", "/validate", "/history"],
    "routes_missing": []
  },
  "input_type_issues": [],
  "failures": [],
  "summary": "All 12 tests pass, covering health check, valid/invalid /validate in

## Review findings (must fix before proceeding)
- [critical] tests/test_app.py: File does not exist on disk. task-2 claims to have written 12 tests, but the tests/ directory is empty and no test file can be found anywhere in the workspace. The reported pass count is unverifiable.
- [major] templates/index.html:32: Dead code: `const value = document.getElementById('value').value` is declared but never read. The parseInt fix on line 39 re-reads the DOM directly, making this binding unused. Violates the 'no dead code' rule in coding.md.