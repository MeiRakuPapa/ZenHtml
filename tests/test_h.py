# Copyright (c) 2025 Yusuke KITAGAWA (tonosama_kaeru@icloud.com)

from datetime import datetime, time

import pytest

from zen_html import raw
from zen_html.h import H


def test_button_renders_with_literal_and_bool_props() -> None:
    node = H.button("Click", type="submit", disabled=True, dataset={"foo": "bar"})
    html = node.html_

    assert html.startswith("<button")
    assert "type='submit'" in html
    assert "disabled" in html
    assert "data-foo='bar'" in html
    assert html.endswith("</button>")


def test_img_literal_attributes() -> None:
    node = H.img(
        src="/logo.png",
        alt="logo",
        decoding="async",
        loading="lazy",
        fetchpriority="high",
        dataset={"foo": "bar"},
    )
    html = node.html_
    assert html.startswith("<img")
    assert "alt='logo'" in html
    assert "decoding='async'" in html
    assert "loading='lazy'" in html
    assert "fetchpriority='high'" in html
    assert "data-foo='bar'" in html
    assert html.endswith("/>")


def test_void_tag_rejects_children() -> None:
    with pytest.raises(ValueError):
        H.meta("ignored", charset="utf-8")


def test_dataset_bool_is_stringified() -> None:
    node = H.div(dataset={"flag": True, "count": 1})
    html = node.html_
    assert "data-flag='true'" in html
    assert "data-count='1'" in html


def test_style_dict_is_flattened() -> None:
    node = H.div("content", style={"fontSize": "12px", "display": None})
    html = node.html_
    assert "style='font-size: 12px'" in html
    assert "display" not in html


def test_double_underscore_translates_to_colon() -> None:
    node = H.div(style={"grid__templateColumns": "1fr 1fr"})
    html = node.html_
    assert "grid:template-columns" in html


def test_camel_case_to_kebab_case() -> None:
    node = H.input(checked=True, ariaLabel="label")
    html = node.html_
    assert "aria-label" in html
    assert "checked" in html


def test_underscore_translates_to_dash() -> None:
    node = H.meta(http_equiv="refresh")
    assert "http-equiv='refresh'" in node.html_


def test_reserved_keyword_mapping() -> None:
    node = H.script("console.log(1);", async_=True, class_="foo")
    html = node.html_
    assert "async" in html
    assert "class='foo'" in html
    assert html.startswith("<script")


def test_class_attribute_accepts_iterable() -> None:
    node = H.div("text", class_=["foo", None, " bar ", "baz"])
    html = node.html_
    assert "class='foo bar baz'" in html


def test_class_attribute_rejects_non_string_items() -> None:
    with pytest.raises(TypeError):
        H.div(class_=["foo", 1])  # type: ignore[list-item]


def test_children_keyword_argument() -> None:
    node = H.div(children=[H.span("inner"), "tail"], class_="wrapper")
    html = node.html_
    assert html == "<div class='wrapper'><span>inner</span>tail</div>"


def test_children_keyword_conflict_with_positional() -> None:
    with pytest.raises(ValueError):
        H.div("text", children=["extra"])


def test_simple_div_with_nested_content() -> None:
    node = H.div(
        "text",
        H.span("inner", class_="label"),
        class_="wrapper",
        id="root",
    )
    html = node.html_
    assert html.startswith("<div class='wrapper' id='root'>")
    assert "<span class='label'>inner</span>" in html
    assert html.endswith("</div>")


def test_a_tag_literal_target_and_href() -> None:
    link = H.a("Go", href="/home", target="_blank")
    html = link.html_
    assert html == "<a href='/home' target='_blank'>Go</a>"


def test_datetime_and_time_values_keep_seconds() -> None:
    node = H.time(datetime=datetime(2024, 1, 2, 3, 4, 5))
    html = node.html_
    assert "datetime='2024-01-02T03:04:05'" in html

    time_input = H.input(type="time", value=time(12, 30, 45))
    assert "value='12:30:45'" in time_input.html_


def test_literal_restrictions_are_enforced() -> None:
    with pytest.raises(ValueError):
        H.button("x", type="invalid")


def test_bool_restrictions_require_bool() -> None:
    with pytest.raises(TypeError):
        H.button("x", disabled="yes")  # type: ignore[arg-type]


def test_text_and_attribute_values_are_escaped() -> None:
    node = H.div("<script>", title="1 < 2 & '3'")
    html = node.html_
    assert "&lt;script&gt;" in html
    assert "title='1 &lt; 2 &amp; &#x27;3&#x27;'" in html


def test_raw_helper_inserts_unescaped_html() -> None:
    node = H.div(raw("<span>safe</span>"))
    assert node.html_.startswith("<div>")
    assert "<span>safe</span>" in node.html_


def test_pretty_dict_escapes_strings() -> None:
    node = H.div("<x>", title="1 < 2")
    output = node._pretty_dict()
    assert "'&lt;x&gt;'" in output
    assert "'1 &lt; 2'" in output


def test_pretty_dict_escapes_raw_children() -> None:
    node = H.div(raw("<span>safe</span>"))
    output = node._pretty_dict()
    assert "&lt;span&gt;" in output


def test_dict_property_escapes_plain_strings() -> None:
    node = H.div("<span>aa</span>")
    data = node.dict_
    assert data["children"][0] == "&lt;span&gt;aa&lt;/span&gt;"


def test_dict_property_preserves_raw_children() -> None:
    node = H.div(raw("<span>aa</span>"))
    data = node.dict_
    assert data["children"][0] == "<span>aa</span>"


def test_void_children_are_dropped_in_non_strict_mode() -> None:
    old = H.strict_validation
    H.strict_validation = False
    try:
        node = H.meta("ignored", charset="utf-8")
        assert node.html_ == "<meta charset='utf-8'/>"
    finally:
        H.strict_validation = old


def test_invalid_literal_is_removed_in_non_strict_mode() -> None:
    old = H.strict_validation
    H.strict_validation = False
    try:
        html = H.button("x", type="invalid").html_
        assert "type=" not in html
    finally:
        H.strict_validation = old
