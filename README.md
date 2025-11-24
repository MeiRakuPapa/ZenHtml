![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Dependencies](https://img.shields.io/badge/Dependencies-0-lightgrey.svg)
![LOC](https://img.shields.io/badge/LOC-<400-lightgreen.svg)
![Tests](https://img.shields.io/badge/Tests-Passed-brightgreen.svg)
![Philosophy](https://img.shields.io/badge/Philosophy-Simple%20Design-82c91e.svg)

# ZenHtml
# H

[日本語 README](README.ja.md)

Typed HTML builder for Python. Call tag helpers in `zen_html.h` to build HTML directly in Python with strong typing. It runs solely on the standard library—no external dependencies. `_base.py` contains the rendering logic, and `_generator.py` autogenerates the tag API (`zen_html.h`) from `_tag_spec.py`.

```
pip install zenhtml
```

## Features
- **Fully typed API**: Each tag exposes common props (`class_`, `id`, `name`, …) plus Literal/boolean-restricted attributes.
- **Simple DOM composition**: Nested iterables are accepted as children, so `H.div(list_of_nodes)` just works.
- **Convenient helpers**: `dataset` dict → `data-*`, `style` dict → CSS strings, and `pretty_html`/`pretty_dict` for debugging.
- **Reusable tokens**: `to_token()`, `html_`, and `dict_` can be used for streaming or structured rendering.
- **HTML5 coverage**: 110+ tags (metadata, forms, tables, interactive elements…) are generated from `_tag_spec.py`. SVG/MathML are intentionally out of scope.
- **Escaped by default**: Text children/attribute values are HTML-escaped automatically. Wrap trusted fragments with `H.raw()` when you really need unescaped output, and keep `H.strict_validation` enabled to fail fast on invalid props/void-tag children.

## Usage
```python
from typing import Literal
from zen_html.h import H

page: H = H.html(
    H.head(
        H.meta(charset="utf-8"),
        H.title("Hello, H"),
    ),
    H.body(
        H.h1("Hello"),
        H.p("Generated in Python.", class_="lead"),
        H.button("Click", type="button", disabled=None),
    ),
    lang="ja",
)

print(page.html_)          # plain string
print(page.pretty_html())  # indented output

def button(kind: Literal["button", "submit"]) -> H:
    return H.button("Click", type=kind)

button("button")    # OK
button("invalid")   # mypy error thanks to Literal
```

`examples/sample.py` includes Starlette/FastAPI helpers (`HResponse`, `HDocumentResponse`, `select`) showing real-world usage. `examples/pandas_pivot.py` demonstrates how to turn a pandas pivot table into an HTML table (pandas is an optional dependency for that example). Run it with `python -m examples.pandas_pivot` to keep imports working from the repo root.

### Key properties & methods
- `html_`: Concatenated HTML string for the node (eager render). Suitable for templates that just need a string.
- `pretty_html(indent=0)`: Prints a human-readable representation, handy for debugging or inspection.
- `to_token()`: Generator yielding individual HTML tokens. Use it for streaming responses (`StreamingResponse`, ASGI, etc.).
- `dict_`: JSON-serializable tree containing `tag`, escaped `props`, and `children`. Useful for client-side rendering or feeding into other serializers.

### Escaping & validation
- All text nodes and attribute values are escaped automatically. If you need to inject a pre-escaped fragment, wrap it with `H.raw("<span>safe</span>")`.
- Runtime validation is enabled by default (`H.strict_validation = True`) and raises when you pass children to void tags or supply unsupported Literal/bool values. Set it to `False` when you prefer warnings and best-effort rendering. Validation occurs during node construction, so token streaming (`to_token()` / `HResponse`) never yields partial or invalid HTML—errors surface up front.

### Rendering via `dict_` in JavaScript
`dict_` returns a JSON-serializable structure. You can ship it to the browser and render it there:

```python
import json
from zen_html.h import H

payload = json.dumps(H.div("Hi", class_="greeting").dict_)
```

```html
<script type="module">
  import { HRender } from "/examples/h_render.js";
  const tree = JSON.parse({{ payload | tojson }});
  document.body.appendChild(HRender(tree));
</script>
```

## Regenerating tag API
`H/h.py` is generated from `_tag_spec.py`. After editing the spec, run:

```bash
python3 - <<'PY'
from zen_html._generator import generate_class
generate_class(output="H/h.py")
PY
```

## Development notes
- Tooling (Black/Isort/djlint) is configured in `pyproject.toml`.
- Boolean props render only when `True`; `False`/`None` are ignored.
- `dataset={"fooBar": "baz"}` → `data-foo-bar="baz"`; `style={"fontSize": "12px"}` → `font-size: 12px`.
- Requires Python 3.10+ so ParamSpec-based decorators keep IDE (VS Code) completions accurate.

## License
See `LICENSE`.
