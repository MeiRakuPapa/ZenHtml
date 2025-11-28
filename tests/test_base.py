# Copyright (c) 2025 Yusuke KITAGAWA (tonosama_kaeru@icloud.com)
# mypy: disable-error-code=arg-type
# mypy: disable-error-code=index
# mypy: disable-error-code=list-item
# mypy: disable-error-code=no-untyped-def


import pytest

from zen_html._base import _HBase


def test_html_generation_with_nested_children() -> None:
    child = _HBase("span", "inner")
    parent = _HBase("div", "hello", child)

    assert parent.html_ == "<div>hello<span>inner</span></div>"
    result = parent.dict_
    assert result["tag"] == "div"
    assert result["children"][0] == "hello"
    assert result["children"][1]["tag"] == "span"


def test_dataset_style_and_boolean_props() -> None:
    node = _HBase(
        "button",
        "ok",
        dataset={"fooBar": "baz"},
        style={"fontSize": "12px", "display": None},
        hidden=True,
        disabled=False,
        title=None,
    )

    html = node.html_
    assert "data-foo-bar='baz'" in html
    assert "style='font-size: 12px'" in html
    assert "hidden" in html
    assert "disabled" not in html
    assert "title" not in html


def test_flatten_iterable_children() -> None:
    nested = _HBase("div", ["a", ("b", [_HBase("span", "c")])])

    assert nested.html_ == "<div>ab<span>c</span></div>"


def test_invalid_child_type_raises_type_error() -> None:
    with pytest.raises(TypeError):
        _HBase("div", object())


def test_invalid_dataset_type_raises_value_error() -> None:
    with pytest.raises(ValueError):
        _HBase("div", dataset=["not", "dict"])


def test_invalid_style_type_raises_value_error() -> None:
    with pytest.raises(ValueError):
        _HBase("div", style=123)
