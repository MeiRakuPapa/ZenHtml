"""
_base.py

This module provides the core functionality for rendering HTML elements in a structured and type-safe manner.
It defines the base class `_HBase` for HTML nodes, utility functions for attribute normalization, and constants
for HTML tag specifications.

Classes:
    _HBase: Represents an HTML node with children, attributes, and rendering capabilities.

Functions:
    html_tag: A decorator for defining HTML tag helper methods.
    raw: Wraps pre-escaped HTML to bypass auto-escaping.
"""

# Copyright (c) 2025 Yusuke KITAGAWA (tonosama_kaeru@icloud.com)

from __future__ import annotations

import html
import logging
import re
import warnings
from datetime import date, datetime, time
from typing import Callable, ClassVar, Iterable, ParamSpec, TypedDict, TypeVar, cast

from ._tag_spec import normalized_tag_spec

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
    "as_": "as",
}
R_PROP_NAME_MAP = {v: k for k, v in PROP_NAME_MAP.items()}


# Ensure PropVal and related constants are defined
ClassAttr = str | Iterable[str] | None
PropVal = str | int | bool | float | date | datetime | time | dict[str, object] | None

TO_KEBAB1 = re.compile(r"([A-Z]+)([A-Z][a-z])")
TO_KEBAB2 = re.compile(r"([a-z0-9])([A-Z])")
TO_COL = re.compile(r"(?<=\w)__|__(?=\w)")


class _TagRule(TypedDict):
    bools: set[str]
    choices: dict[str, list[str]]
    required: set[str]


def _build_tag_rules() -> dict[str, _TagRule]:
    rules: dict[str, _TagRule] = {}
    for tag, props in normalized_tag_spec().items():
        bools = {name for name, opt in props if opt.get("kind") == "bool"}
        choices = {name: opt.get("values", []) for name, opt in props if opt.get("kind") == "choices"}
        required = {name for name, opt in props if opt.get("required")}
        rules[tag] = {
            "bools": bools,
            "choices": choices,
            "required": required,
        }
    return rules


_TAG_RULES: dict[str, _TagRule] = _build_tag_rules()


class _HBase:
    """
    Represents an HTML node with attributes, children, and rendering capabilities.

    Attributes:
        strict_validation (ClassVar[bool]): If True, raises exceptions for invalid attributes or children.
        logger (ClassVar[logging.Logger]): Logger for validation warnings.

    Methods:
        to_token: Generates HTML tokens for the node.
        html_: Returns the HTML string representation of the node.
        dict_: Returns a dictionary representation of the node.
    """

    class RAW_STR(str):
        """Marker type representing intentionally unescaped HTML fragments.
        This class is used to wrap raw HTML strings that should bypass
        automatic escaping. Use with caution, as improper use may lead
        to security vulnerabilities (e.g., XSS attacks).
        """

        def __init__(self, value: str) -> None:
            if not isinstance(value, str):
                raise TypeError("RAW_STR value must be a string")
            super().__init__()

    strict_validation: ClassVar[bool] = True
    logger: ClassVar[logging.Logger] = logging.getLogger("H")

    def __init__(
        self,
        tag: str,
        *children: Children,
        children_kw: Children | None = None,
        **props: PropVal,
    ):
        self._tag = tag
        if children_kw is not None and children:
            raise ValueError("Provide children either positionally or via 'children' keyword, not both")
        if children_kw is not None:
            flattened = self._flatten_children((children_kw,))
        else:
            flattened = self._flatten_children(children)
        self._children = tuple(flattened)
        class_value = props.get("class_")
        if class_value is not None:
            props["class_"] = _normalize_class_attr(class_value)
        elif "class" in props and props["class"] is not None:
            props["class"] = _normalize_class_attr(props["class"])
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
                    f"{_to_html_prop_name(k)}: {v}" for k, v in style.items() if v is not None
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
        provided: set[str] = set()
        if self._tag in VOID_TAGS and self._children:
            if self._handle_violation(ValueError(f"Void element <{self._tag}> cannot have children")):
                self._children = ()

        for pk, pv in list(checked.items()):
            if pv is None:
                continue
            html_name = _to_html_prop_name(pk)
            provided.add(html_name)
            allowed = spec["choices"].get(html_name)
            if allowed:
                if not isinstance(pv, str):
                    if self._handle_violation(
                        TypeError(f"Attribute '{html_name}' on <{self._tag}> must be str")
                    ):
                        checked.pop(pk, None)
                    continue
                if pv not in allowed:
                    if self._handle_violation(
                        ValueError(
                            f"Attribute '{html_name}' on <{self._tag}> must be one of {allowed}: {pv!r}"
                        )
                    ):
                        checked.pop(pk, None)
            if html_name in spec["bools"] and not isinstance(pv, bool):
                if self._handle_violation(
                    TypeError(f"Attribute '{html_name}' on <{self._tag}> must be bool")
                ):
                    checked.pop(pk, None)

        missing = spec["required"] - provided
        if missing:
            self._handle_violation(
                ValueError(f"<{self._tag}> missing required attributes: {', '.join(sorted(missing))}")
            )

        return checked

    @classmethod
    def _handle_violation(cls, exc: Exception) -> bool:
        if cls.strict_validation:
            raise exc
        cls.logger.warning("%s", exc)
        return True

    @classmethod
    def _flatten_children(cls, children: Iterable[Children]) -> Iterable[Child]:
        for c in children:
            match c:
                case _HBase.RAW_STR():
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
                escaped = v if isinstance(v, _HBase.RAW_STR) else _escape_attr(str(v))
                yield f" {k}='{escaped}'"
        if self._tag in VOID_TAGS:
            yield "/>"
            return
        yield ">"
        for child in self._children:
            if isinstance(child, _HBase.RAW_STR):
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
            "children": [_serialize_child(child) for child in self._children],
            "props": {k: _serialize_prop_value(v) for k, v in self._props.items()},
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
                escaped = v if isinstance(v, _HBase.RAW_STR) else _escape_attr(str(v))
                parts.append(f" {k}='{escaped}'")
        attrs = "".join(parts)
        if self._tag in VOID_TAGS:
            return f"{pad}<{self._tag}{attrs} />"

        inner_parts = []
        for c in self._children:
            if isinstance(c, _HBase.RAW_STR):
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
            if isinstance(c, _HBase.RAW_STR):
                lines.append(f"{pad3}  {str(c)!r},")
            elif isinstance(c, str):
                lines.append(f"{pad3}  {_escape_text(str(c))!r},")
            else:
                lines.append(c._pretty_dict(indent + 2))
        lines.append(f"{pad2}],")

        lines.append(f"{pad}}}")
        return "\n".join(lines)


Child = _HBase | str | _HBase.RAW_STR
Children = Child | Iterable[Child]


_P = ParamSpec("_P")
_S = TypeVar("_S", bound=_HBase)


def html_tag(fn: Callable[_P, _S]) -> Callable[_P, _S]:
    """
    A decorator for defining HTML tag helper methods.

    Args:
        fn (Callable): The function to wrap as a tag helper.

    Returns:
        Callable: The wrapped function as a class method.
    """
    name = fn.__name__

    def wrapper(
        cls: type[_S],
        *children: Children,
        **props: PropVal,
    ) -> _S:
        children_kw = cast(Children | None, props.pop("children", None))
        return cls(name, *children, children_kw=children_kw, **props)

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
    s = s.replace("_", "-")

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
    if isinstance(v, _HBase.RAW_STR):
        return v
    return str(v)


def _to_dataset_value(v: object) -> str:
    value = _to_html_value(v)
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def _normalize_class_attr(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, Iterable):
        classes: list[str] = []
        for item in value:
            if item is None:
                continue
            if not isinstance(item, str):
                raise TypeError("class_ iterable entries must be str")
            token = item.strip()
            if token:
                classes.append(token)
        return " ".join(classes)
    raise TypeError("class_ must be str or iterable of str values")


def _escape_text(value: str) -> str:
    return html.escape(value, quote=False)


def _escape_attr(value: str) -> str:
    return html.escape(value, quote=True)


def _repr_prop_value(value: str | bool) -> str:
    if isinstance(value, (_HBase.RAW_STR, str)):
        return repr(_escape_attr(str(value)))
    return repr(value)


def _serialize_child(child: Child) -> object:
    if isinstance(child, _HBase):
        return child.dict_
    if isinstance(child, _HBase.RAW_STR):
        return str(child)
    return _escape_text(child)


def _serialize_prop_value(value: str | _HBase.RAW_STR | bool) -> object:
    if isinstance(value, _HBase.RAW_STR):
        return str(value)
    if isinstance(value, str):
        return _escape_attr(str(value))
    return value


def raw(value: str) -> _HBase.RAW_STR:
    """
    Wrap pre-escaped HTML so it bypasses auto-escaping.

    .. deprecated::
       This function is deprecated and will be removed in a future version.
       Use `_HBase.RAW_STR` directly instead.

    Args:
        value (str): The raw HTML string.

    Returns:
        _HBase.RAW_STR: A marker type for raw HTML.
    """
    warnings.warn(
        "raw() is deprecated and will be removed in a future version. Use _HBase.RAW_STR directly instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _HBase.RAW_STR(value)
