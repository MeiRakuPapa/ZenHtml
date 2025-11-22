# Copyright (c) 2025 Yusuke KITAGAWA (tonosama_kaeru@icloud.com)

from __future__ import annotations
import html
import logging
import re
from datetime import date, datetime, time
from typing import Callable, ClassVar, Iterable, ParamSpec, TypeVar

from ._tag_spec import TAG_SPEC

VOID_TAGS: set[str] = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

PROP_NAME_MAP: dict[str, str] = {
    "for_": "for",
    "class_": "class",
    "async_": "async",
}
R_PROP_NAME_MAP = {v: k for k, v in PROP_NAME_MAP.items()}


class _RawHTML(str):
    """Marker type representing intentionally unescaped HTML fragments."""


def raw(value: str) -> _RawHTML:
    """Wrap pre-escaped HTML so it bypasses auto-escaping."""
    if not isinstance(value, str):
        raise TypeError("raw() expects str input")
    return _RawHTML(value)


PropVal = str | int | bool | float | date | datetime | time | dict[str, object] | None

TO_KEBAB1 = re.compile(r"([A-Z]+)([A-Z][a-z])")
TO_KEBAB2 = re.compile(r"([a-z0-9])([A-Z])")
TO_COL = re.compile(r"(?<=\w)__|__(?=\w)")

_TAG_RULES: dict[str, dict[str, object]] = {entry["tag"]: entry for entry in TAG_SPEC}


class _HBase:
    strict_validation: ClassVar[bool] = True
    logger: ClassVar[logging.Logger] = logging.getLogger("H")

    def __init__(self, tag: str, *children: Children, **props: PropVal):
        self._tag = tag
        self._children = tuple(self._flatten_children(children))
        dataset = props.pop("dataset", None)
        match dataset:
            case None:
                pass
            case dict():
                for dk, dv in dataset.items():
                    key = f"data-{_to_html_prop_name(dk)}"
                    props[key] = _to_dataset_value(dv)
            case _:
                raise ValueError(f"dataset must be dict: {type(dataset)}")

        style = props.pop("style", None)
        match style:
            case None:
                pass
            case dict():
                props["style"] = "; ".join(
                    f"{_to_html_prop_name(k)}: {v}"
                    for k, v in style.items()
                    if v is not None
                )
            case str():
                props["style"] = style
            case _:
                raise ValueError("style must be dict or str:", {type(style)})

        props = self._validate_constraints(props)

        processed_props: dict[str, str | bool] = {}
        for k, v in props.items():
            if v is None:
                continue
            value = _to_html_value(v)
            if value is False:
                continue
            processed_props[_to_html_prop_name(k)] = value
        self._props = processed_props

    def _validate_constraints(self, props: dict[str, PropVal]) -> dict[str, PropVal]:
        spec = _TAG_RULES.get(self._tag)
        if spec is None:
            return props

        checked = dict(props)
        if self._tag in VOID_TAGS and self._children:
            exc = ValueError(f"Void element <{self._tag}> cannot have children")
            if self._handle_violation(exc):
                self._children = ()

        restricted_literal = spec.get("restricted_literal")
        if isinstance(restricted_literal, dict):
            for pk, pv in list(checked.items()):
                if pv is None:
                    continue
                html_name = _to_html_prop_name(pk)
                allowed = restricted_literal.get(html_name)
                if allowed is None:
                    continue
                if not isinstance(pv, str):
                    exc = TypeError(
                        f"Attribute '{html_name}' on <{self._tag}> must be str"
                    )
                    if self._handle_violation(exc):
                        checked.pop(pk, None)
                    continue
                if pv not in allowed:
                    exc = ValueError(
                        f"Attribute '{html_name}' on <{self._tag}> must be one of {allowed}: {pv!r}"
                    )
                    if self._handle_violation(exc):
                        checked.pop(pk, None)

        restricted_bool = spec.get("restricted_bool")
        if isinstance(restricted_bool, list):
            bool_names = set(restricted_bool)
            for pk, pv in list(checked.items()):
                if pv is None:
                    continue
                html_name = _to_html_prop_name(pk)
                if html_name in bool_names and not isinstance(pv, bool):
                    exc = TypeError(
                        f"Attribute '{html_name}' on <{self._tag}> must be bool"
                    )
                    if self._handle_violation(exc):
                        checked.pop(pk, None)

        return checked

    @classmethod
    def _handle_violation(cls, exc: Exception) -> bool:
        if cls.strict_validation:
            raise exc
        cls.logger.warning("%s", exc)
        return True

    @classmethod
    def _flatten_children(
        cls, children: Iterable[Children]
    ) -> Iterable[Child]:
        for c in children:
            match c:
                case _RawHTML():
                    yield c
                case str():
                    yield c
                case _HBase():
                    yield c
                case _ if isinstance(c, Iterable):
                    yield from cls._flatten_children(c)
                case _:
                    raise TypeError(f"Invalid child type: {c}:{type(c)!r}")

    def to_token(self) -> Iterable[str]:
        yield f"<{self._tag}"
        for k, v in self._props.items():
            if v is True:
                yield f" {k}"
            else:
                escaped = v if isinstance(v, _RawHTML) else _escape_attr(str(v))
                yield f" {k}='{escaped}'"
        if self._tag in VOID_TAGS:
            yield "/>"
            return
        yield ">"
        for child in self._children:
            if isinstance(child, _RawHTML):
                yield str(child)
            elif isinstance(child, str):
                yield _escape_text(child)
            else:
                yield from child.to_token()
        yield f"</{self._tag}>"

    @property
    def html_(self) -> str:
        return "".join(self.to_token())

    @property
    def dict_(self) -> dict[str, object]:
        return {
            "tag": self._tag,
            "children": [
                _serialize_child(child) for child in self._children
            ],
            "props": {
                k: _serialize_prop_value(v) for k, v in self._props.items()
            },
        }

    def __str__(self) -> str:
        return self.html_

    def __repr__(self) -> str:
        return f"H({self._tag!r}, props={self._props!r}, children={self._children!r})"

    def pretty_html(self, indent: int = 0) -> None:
        print(self._pretty_html(indent))

    def _pretty_html(self, indent: int = 0) -> str:
        pad = "  " * indent
        parts = []
        for k, v in self._props.items():
            if v is True:
                parts.append(f" {k}")
            else:
                escaped = v if isinstance(v, _RawHTML) else _escape_attr(str(v))
                parts.append(f" {k}='{escaped}'")
        attrs = "".join(parts)
        if self._tag in VOID_TAGS:
            return f"{pad}<{self._tag}{attrs} />"

        inner_parts = []
        for c in self._children:
            if isinstance(c, _RawHTML):
                inner_parts.append("  " * (indent + 1) + str(c))
            elif isinstance(c, str):
                inner_parts.append("  " * (indent + 1) + _escape_text(c))
            else:
                inner_parts.append(c._pretty_html(indent + 1))

        inner = "\n".join(inner_parts)

        return f"{pad}<{self._tag}{attrs}>\n{inner}\n{pad}</{self._tag}>"

    def pretty_dict(self, indent: int = 0) -> None:
        print(self._pretty_dict(indent))

    def _pretty_dict(self, indent: int = 0) -> str:
        pad = "  " * indent
        lines = []
        lines.append(f"{pad}{{")
        pad2 = "  " * (indent + 1)
        pad3 = "  " * (indent + 2)

        lines.append(f"{pad2}'tag': {self._tag!r},")

        if self._props:
            lines.append(f"{pad2}'props': {{")
            for k, v in self._props.items():
                lines.append(f"{pad2}  {k!r}: {_repr_prop_value(v)},")
            lines.append(f"{pad2}}},")
        else:
            lines.append(f"{pad2}'props': {{}},")

        lines.append(f"{pad2}'children': [")
        for c in self._children:
            if isinstance(c, (_RawHTML, str)):
                lines.append(f"{pad3}  {_escape_text(str(c))!r},")
            else:
                lines.append(c._pretty_dict(indent + 2))
        lines.append(f"{pad2}],")

        lines.append(f"{pad}}}")
        return "\n".join(lines)

Child = _HBase | str | _RawHTML
Children = Child | Iterable[Child]


_P = ParamSpec("_P")
_S = TypeVar("_S", bound=_HBase)


def html_tag(fn: Callable[_P, _S]) -> Callable[_P, _S]:
    name = fn.__name__

    def wrapper(
        cls: type[_S],
        *children: Children,
        **props: PropVal,
    ) -> _S:
        return cls(name, *children, **props)

    wrapper.__name__ = fn.__name__
    wrapper.__qualname__ = fn.__qualname__
    wrapper.__doc__ = fn.__doc__
    return classmethod(wrapper)  # type: ignore[arg-type, return-value]


def _to_html_prop_name(name: str) -> str:
    if name in PROP_NAME_MAP:
        return PROP_NAME_MAP[name]
    s = TO_KEBAB1.sub(r"\1-\2", name)
    s = TO_KEBAB2.sub(r"\1-\2", s)
    s = TO_COL.sub(":", s)

    return s.lower()


def _to_html_value(v: PropVal | object) -> str | bool:
    if isinstance(v, datetime):
        return v.isoformat(timespec="seconds")
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, time):
        return v.isoformat(timespec="seconds")
    if isinstance(v, bool):
        return v
    return str(v)


def _to_dataset_value(v: object) -> str:
    value = _to_html_value(v)
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def _escape_text(value: str) -> str:
    return html.escape(value, quote=False)


def _escape_attr(value: str) -> str:
    return html.escape(value, quote=True)


def _repr_prop_value(value: str | bool) -> str:
    if isinstance(value, (_RawHTML, str)):
        return repr(_escape_attr(str(value)))
    return repr(value)


def _serialize_child(child: Child) -> object:
    if isinstance(child, _HBase):
        return child.dict_
    if isinstance(child, _RawHTML):
        return str(child)
    return _escape_text(child)


def _serialize_prop_value(value: str | bool) -> object:
    if isinstance(value, (_RawHTML, str)):
        return _escape_attr(str(value))
    return value
