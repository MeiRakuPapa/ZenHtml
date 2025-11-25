# Changelog

## 0.1.3 - 2025-11-25
- Allow passing `class_` as `str | Iterable[str] | None` and normalize lists into space-separated class strings.
- Support `children=[...]` keyword argument on every tag; positional and keyword children can no longer be mixed accidentally.
- Document the above ergonomics in both English and Japanese README files.
- Add regression tests for iterable `class_` handling and `children` keyword usage; regenerate tag helpers accordingly.

## 0.1.2 - 2025-11-20
- Initial public release.
