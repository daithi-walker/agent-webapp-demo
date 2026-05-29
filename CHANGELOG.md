# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2026-05-29
### Added
- Stats panel on the homepage displaying Total, Valid, and Invalid validation counts fetched from `GET /stats`
- Panel updates automatically after each `/validate` call without a full page reload
- Panel shows "No validations yet" when all counts are zero
- Panel is positioned between the result message and the history table

## [1.2.0] - 2026-05-29
### Added
- GET /stats endpoint returning total, valid, and invalid validation counts as a JSON summary of all /validate calls since server start
- Three new pytest tests covering /stats in empty state, after valid submissions, and after mixed valid/invalid submissions

## [1.1.1] - 2026-05-19
### Fixed
- Value input in templates/index.html changed from `type="text"` to `type="number"`
- Submit handler now sends an integer to the API by wrapping the input value with `parseInt(..., 10)` before serialization
- History button handler now reads `data.history` from the `/history` response object instead of checking `Array.isArray(data)` directly

### Added
- pytest test suite (`tests/test_app.py`) covering all routes (`/health`, `/validate`, `/history`) and integer-vs-string input validation (12 tests)

## [1.1.0] - 2026-05-16

### Added

- In-memory validation history storing the last 50 entries
- GET /history endpoint to retrieve validation history
- History display section in the HTML frontend

[Unreleased]: https://github.com/example/project/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/example/project/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/example/project/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/example/project/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/example/project/compare/v1.0.0...v1.1.0
