# Copyright (c) 2025 Yusuke KITAGAWA (tonosama_kaeru@icloud.com)

from typing import Iterable, Sequence

from starlette.datastructures import URL
from starlette.responses import StreamingResponse

from zen_html.h import H


def select(name: str, label: str, item_map: dict[str, str], values: list[str]) -> H:
    return H.div(
        H.label(label, class_="form-label m-0"),
        H.select(
            *(
                H.option(v, value=k, selected=True if k in values else None)
                for k, v in item_map.items()
            ),
            name=name,
            class_="dl",
            multiple=True,
            size=8
        ),
        dataName=name,
        class_="mb-1"
    )


HtmlContent = H | Iterable[str]


class HResponse(StreamingResponse):
    """StreamResponse that renders `H` nodes or raw HTML token iterables."""

    def __init__(
        self,
        content: HtmlContent,
        *,
        include_doctype: bool = False,
        media_type: str = "text/html; charset=utf-8",
        **kwargs,
    ) -> None:
        stream = self._render(content, include_doctype)
        super().__init__(stream, media_type=media_type, **kwargs)

    @staticmethod
    def _render(content: HtmlContent, include_doctype: bool) -> Iterable[str]:
        def iterator() -> Iterable[str]:
            if include_doctype:
                yield "<!DOCTYPE html>"
            if isinstance(content, H):
                yield from content.to_token()
            else:
                yield from content

        return iterator()


def HtmlDocument(
        *,
        title: str,
        description: str = "", 
        keywords: str = "",
        head: Sequence[H] | None = None,
        body: Sequence[H] | None = None,
        css: Sequence[str | URL] | None = None,
        script: Sequence[str | URL] | None = None,
        lang: str = "ja",
    ) -> H:
        head_nodes = list(head or ())
        body_nodes = list(body or ())
        css_nodes = [str(i) for i in css or ()]
        script_nodes = [str(i) for i in script or ()]
        return H.html(
            H.head(
                H.meta(charset="utf-8"),
                H.meta(name="viewport", content="width=device-width, initial-scale=1"),
                H.meta(name="description", content=description),
                H.meta(name="keywords", content=keywords),
                H.meta(httpEquiv="Pragma", content="no-cache"),
                H.meta(httpEquiv="Cache-Control", content="no-store"),
                H.title(title),
                *(H.link(href=href, rel="stylesheet") for href in css_nodes),
                *(H.script(src=src) for src in script_nodes),
                *head_nodes,
            ),
            H.body(*body_nodes),
            lang=lang,
        )
