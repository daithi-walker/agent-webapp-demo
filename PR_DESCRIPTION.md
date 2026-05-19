## What changed

- `templates/index.html` line 19: value input changed from `type="text"` to `type="number"`
- `templates/index.html` line 39: submit handler now wraps the input value with `parseInt(..., 10)` so the fetch body sends an integer, not a string
- `templates/index.html` lines 57–61: history button handler now guards on `!Array.isArray(data.history)` and iterates `data.history`, matching the `{"history": [...]}` shape returned by the `/history` endpoint
- Version bumped from 1.1.0 to 1.1.1; `CHANGELOG.md` and `VERSION` updated

## Why

The `/validate` endpoint rejects non-integer values, but the form was submitting a string (`type="text"` + no `parseInt`), so every submission failed validation. The history panel was also broken because it checked `Array.isArray(data)` against a response object, so no history was ever rendered.

## Review notes

The reviewer agent raised two findings that require attention before merge:

- **[Critical] `tests/test_app.py` does not exist on disk.** The QA agent reported 12/12 passing tests, but the `tests/` directory is empty and the file cannot be found anywhere in the workspace. The pass count is unverifiable and the test suite cannot be run. A test file must be committed before this PR is considered complete.

- **[Major] Dead code in `templates/index.html` line 32.** The statement `const value = document.getElementById('value').value` is declared but never used — the `parseInt` fix on line 39 re-reads the DOM directly, making this binding dead. This violates the no-dead-code rule in `standards/coding.md` and should be removed.

## Test coverage

Task-2 reported 12 tests written to `tests/test_app.py` covering all three routes (`/health`, `/validate`, `/history`) and integer-vs-string input validation, with 12/12 passing. However, the reviewer confirmed that `tests/test_app.py` is absent from disk. Test coverage cannot be confirmed.

## Files changed

- `templates/index.html` — three bug fixes (input type, parseInt, data.history)
- `CHANGELOG.md` — added 1.1.1 entry
- `VERSION` — bumped to 1.1.1
