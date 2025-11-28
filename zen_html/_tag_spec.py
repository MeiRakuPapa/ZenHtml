# Copyright (c) 2025 Yusuke KITAGAWA (tonosama_kaeru@icloud.com)

from __future__ import annotations

from typing import Literal, TypedDict, cast


PropDeclaration = str | dict[str, "PropOptions"]


class PropOptions(TypedDict, total=False):
    kind: Literal["str", "bool", "choices"]
    values: list[str]
    required: bool


class TagConfig(TypedDict, total=False):
    props: list[PropDeclaration]


COMMON_PROPS: tuple[PropDeclaration, ...] = ("class", "id", "name")


def _normalize_prop(prop: PropDeclaration) -> tuple[str, PropOptions]:
    if isinstance(prop, str):
        return prop, {}
    if not isinstance(prop, dict) or len(prop) != 1:
        raise ValueError(f"Invalid prop declaration: {prop!r}")
    ((name, options),) = prop.items()
    normalized = cast(PropOptions, dict(options or {}))
    return name, normalized


def _normalize_props(config: TagConfig | None) -> list[tuple[str, PropOptions]]:
    raw = (config or {}).get("props")
    if raw is None:
        props: list[PropDeclaration] = list(COMMON_PROPS)
    else:
        props = list(raw)
    return [_normalize_prop(prop) for prop in props]


def normalized_tag_spec(
    spec: dict[str, TagConfig] | None = None,
) -> dict[str, list[tuple[str, PropOptions]]]:
    base = spec or TAG_SPEC
    return {tag: _normalize_props(config) for tag, config in base.items()}


TAG_SPEC: dict[str, TagConfig] = {
    # ===================== Metadata =====================
    "html": {
        "props": [
            *COMMON_PROPS,
            "lang",
        ],
    },
    "head": {},
    "title": {},
    "base": {
        "props": [
            "href",
            "target",
        ],
    },
    "meta": {
        "props": [
            "charset",
            "http-equiv",
            "name",
            "content",
        ],
    },
    "style": {
        "props": [
            *COMMON_PROPS,
            "media",
        ],
    },
    "body": {},
    # ===================== Sectioning =====================
    "article": {},
    "section": {},
    "nav": {},
    "aside": {},
    "h1": {},
    "h2": {},
    "h3": {},
    "h4": {},
    "h5": {},
    "h6": {},
    "header": {},
    "footer": {},
    "address": {},
    # ===================== Grouping =====================
    "p": {},
    "hr": {},
    "pre": {},
    "blockquote": {
        "props": [
            *COMMON_PROPS,
            "cite",
        ],
    },
    "ol": {
        "props": [
            *COMMON_PROPS,
            {"reversed": {"kind": "bool"}},
        ],
    },
    "ul": {},
    "menu": {},
    "li": {},
    "dl": {},
    "dt": {},
    "dd": {},
    "figure": {},
    "figcaption": {},
    "main": {},
    "div": {},
    # ===================== Text-level =====================
    "em": {},
    "strong": {},
    "small": {},
    "s": {},
    "cite": {
        "props": [
            *COMMON_PROPS,
            "cite",
        ],
    },
    "q": {
        "props": [
            *COMMON_PROPS,
            "cite",
        ],
    },
    "dfn": {},
    "abbr": {},
    "ruby": {},
    "rt": {},
    "rp": {},
    "data": {
        "props": [
            *COMMON_PROPS,
            "value",
        ],
    },
    "time": {
        "props": [
            *COMMON_PROPS,
            "datetime",
        ],
    },
    "code": {},
    "var": {},
    "samp": {},
    "kbd": {},
    "sub": {},
    "sup": {},
    "i": {},
    "b": {},
    "u": {},
    "mark": {},
    "bdi": {},
    "bdo": {},
    "span": {},
    "br": {
        "props": [],
    },
    "wbr": {
        "props": [],
    },
    # ===================== Edits =====================
    "ins": {
        "props": [
            *COMMON_PROPS,
            "cite",
            "datetime",
        ],
    },
    "del": {
        "props": [
            *COMMON_PROPS,
            "cite",
            "datetime",
        ],
    },
    # ===================== Embedded content =====================
    "picture": {},
    "source": {
        "props": [
            *COMMON_PROPS,
            "src",
            "type",
            "media",
            "sizes",
            "srcset",
        ],
    },
    "img": {
        "props": [
            *COMMON_PROPS,
            {"src": {"required": True}},
            "alt",
            {"loading": {"kind": "choices", "values": ["lazy", "eager"]}},
            {"decoding": {"kind": "choices", "values": ["sync", "async", "auto"]}},
            {"fetchpriority": {"kind": "choices", "values": ["high", "low", "auto"]}},
            {"ismap": {"kind": "bool"}},
        ],
    },
    "iframe": {
        "props": [
            *COMMON_PROPS,
            "src",
            "title",
        ],
    },
    "embed": {
        "props": [
            *COMMON_PROPS,
            "src",
            "type",
        ],
    },
    "object": {
        "props": [
            *COMMON_PROPS,
            "data",
            "type",
        ],
    },
    "param": {
        "props": [
            "name",
            "value",
        ],
    },
    "video": {
        "props": [
            *COMMON_PROPS,
            {"src": {"required": True}},
            "poster",
            {"autoplay": {"kind": "bool"}},
            {"controls": {"kind": "bool"}},
            {"loop": {"kind": "bool"}},
            {"muted": {"kind": "bool"}},
        ],
    },
    "audio": {
        "props": [
            *COMMON_PROPS,
            {"src": {"required": True}},
            {"autoplay": {"kind": "bool"}},
            {"controls": {"kind": "bool"}},
            {"loop": {"kind": "bool"}},
            {"muted": {"kind": "bool"}},
        ],
    },
    "track": {
        "props": [
            "src",
            {
                "kind": {
                    "kind": "choices",
                    "values": ["subtitles", "captions", "descriptions", "chapters", "metadata"],
                    "required": True,
                }
            },
            "srclang",
            "label",
            {"default": {"kind": "bool"}},
        ],
    },
    "map": {},
    "area": {
        "props": [
            "alt",
            "coords",
            "shape",
            "href",
        ],
    },
    # ===================== Tables =====================
    "table": {},
    "caption": {},
    "colgroup": {},
    "col": {},
    "thead": {},
    "tbody": {},
    "tfoot": {},
    "tr": {},
    "th": {},
    "td": {},
    # ===================== Forms =====================
    "form": {
        "props": [
            *COMMON_PROPS,
            "action",
            {"method": {"kind": "choices", "values": ["get", "post"]}},
            {
                "enctype": {
                    "kind": "choices",
                    "values": [
                        "application/x-www-form-urlencoded",
                        "multipart/form-data",
                        "text/plain",
                    ],
                }
            },
            "target",
            {"novalidate": {"kind": "bool"}},
        ],
    },
    "label": {
        "props": [
            *COMMON_PROPS,
            "for",
        ],
    },
    "select": {
        "props": [
            *COMMON_PROPS,
            "form",
            {"autofocus": {"kind": "bool"}},
            {"disabled": {"kind": "bool"}},
            {"multiple": {"kind": "bool"}},
            {"required": {"kind": "bool"}},
        ],
    },
    "datalist": {},
    "optgroup": {
        "props": [
            *COMMON_PROPS,
            "label",
            {"disabled": {"kind": "bool"}},
        ],
    },
    "option": {
        "props": [
            *COMMON_PROPS,
            "label",
            "value",
            {"disabled": {"kind": "bool"}},
            {"selected": {"kind": "bool"}},
        ],
    },
    "textarea": {
        "props": [
            *COMMON_PROPS,
            "rows",
            "cols",
            {"autofocus": {"kind": "bool"}},
            {"disabled": {"kind": "bool"}},
            {"readonly": {"kind": "bool"}},
            {"required": {"kind": "bool"}},
        ],
    },
    "output": {
        "props": [
            *COMMON_PROPS,
            "for",
        ],
    },
    "progress": {
        "props": [
            *COMMON_PROPS,
            "value",
            "max",
        ],
    },
    "meter": {
        "props": [
            *COMMON_PROPS,
            "value",
            "min",
            "max",
        ],
    },
    "fieldset": {
        "props": [
            *COMMON_PROPS,
            {"disabled": {"kind": "bool"}},
        ],
    },
    "legend": {},
    "input": {
        "props": [
            *COMMON_PROPS,
            {
                "type": {
                    "kind": "choices",
                    "values": [
                        "text",
                        "password",
                        "number",
                        "email",
                        "checkbox",
                        "radio",
                        "date",
                        "datetime-local",
                        "file",
                        "hidden",
                        "image",
                        "month",
                        "range",
                        "reset",
                        "search",
                        "submit",
                        "tel",
                        "time",
                        "url",
                        "week",
                        "color",
                    ],
                }
            },
            "value",
            "placeholder",
            "min",
            "max",
            "step",
            "pattern",
            "accept",
            "autocomplete",
            {"disabled": {"kind": "bool"}},
            {"required": {"kind": "bool"}},
            {"checked": {"kind": "bool"}},
            {"multiple": {"kind": "bool"}},
            {"readonly": {"kind": "bool"}},
            {"autofocus": {"kind": "bool"}},
        ],
    },
    "button": {
        "props": [
            *COMMON_PROPS,
            "value",
            {"type": {"kind": "choices", "values": ["button", "submit", "reset"]}},
            {"disabled": {"kind": "bool"}},
            {"formnovalidate": {"kind": "bool"}},
        ],
    },
    "a": {
        "props": [
            *COMMON_PROPS,
            "href",
            {"target": {"kind": "choices", "values": ["_self", "_blank", "_parent", "_top"]}},
            "rel",
            "download",
        ],
    },
    # ===================== Interactive =====================
    "details": {
        "props": [
            *COMMON_PROPS,
            {"open": {"kind": "bool"}},
        ],
    },
    "summary": {},
    "dialog": {
        "props": [
            *COMMON_PROPS,
            {"open": {"kind": "bool"}},
        ],
    },
    # ===================== Scripting =====================
    "script": {
        "props": [
            *COMMON_PROPS,
            "src",
            {"type": {"kind": "choices", "values": ["module", "text/javascript"]}},
            {"async": {"kind": "bool"}},
            {"defer": {"kind": "bool"}},
            {"nomodule": {"kind": "bool"}},
        ],
    },
    "noscript": {},
    "template": {},
    "slot": {},
    "canvas": {
        "props": [
            *COMMON_PROPS,
            "width",
            "height",
        ],
    },
    # ===================== Links =====================
    "link": {
        "props": [
            {"href": {"required": True}},
            {
                "rel": {
                    "kind": "choices",
                    "values": [
                        "stylesheet",
                        "icon",
                        "preload",
                        "prefetch",
                        "modulepreload",
                        "manifest",
                    ],
                }
            },
            "as",
            "type",
            {"disabled": {"kind": "bool"}},
            "media",
            "sizes",
        ],
    },
}
