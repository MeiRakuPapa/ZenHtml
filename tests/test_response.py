# Copyright (c) 2025 Yusuke KITAGAWA (tonosama_kaeru@icloud.com)
# mypy: disable-error-code=arg-type
# mypy: disable-error-code=no-untyped-def
# mypy: disable-error-code=unused-ignore

import pytest

from starlette.testclient import TestClient

from zen_html.h import H
from examples.sample import HResponse, HtmlDocument


pytest.importorskip("starlette.responses")


def collect_body(response: HResponse) -> bytes:
    async def app(scope, receive, send):
        assert scope["type"] == "http"
        await response(scope, receive, send)

    client = TestClient(app)
    res = client.get("/")
    return res.content  # type: ignore[no-any-return]


def test_hresponse_from_tree() -> None:
    response = HResponse(H.p("hello"))
    body = collect_body(response)

    assert body == b"<p>hello</p>"


def test_hresponse_from_token_stream_with_doctype() -> None:
    response = HResponse(["<div>", "</div>"], include_doctype=True)
    body = collect_body(response)

    assert body == b"<!DOCTYPE html><div></div>"


def test_hdocumentresponse_includes_doctype_and_structure() -> None:
    response = HResponse(
        HtmlDocument(
            title="Example",
            body=[H.p("body")],
            head=[H.meta(name="robots", content="noindex")],
        ),
        include_doctype=True,
    )
    body = collect_body(response)

    assert body.startswith(b"<!DOCTYPE html><html")
    assert b"<title>Example</title>" in body
    assert b"<p>body</p>" in body
