# Changelog

## Unreleased
### Added
- Added `py.typed` file to properly support type checking.
- Enabled Ruff for linting and formatting (replacing Black, isort, flake8).
- Moved development dependencies to `dependency-groups.dev` instead of `optional-dependencies`.

## 0.1.4 - 2025-11-28
### Added
- Support for `H.RAW_STR` to handle unescaped HTML fragments.
- Improved validation for void tags and attributes.

### Changed
- Updated documentation to reflect new API usage.
- Refactored tag generation logic for better maintainability.

### Fixed
- Minor bug fixes in `examples/pandas_pivot.py`.

## 0.1.3 - 2025-11-25
- Allow passing `class_` as `str | Iterable[str] | None` and normalize lists into space-separated class strings.
- Support `children=[...]` keyword argument on every tag; positional and keyword children can no longer be mixed accidentally.
- Document the above ergonomics in both English and Japanese README files.
- Add regression tests for iterable `class_` handling and `children` keyword usage; regenerate tag helpers accordingly.

## 0.1.2 - 2025-11-20
- Initial public release.
