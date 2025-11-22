# Copyright (c) 2025 Yusuke KITAGAWA (tonosama_kaeru@icloud.com)

# mypy: disable-error-code=empty-body
# mypy: disable-error-code=misc
from typing import Literal
from ._base import Children, PropVal, _HBase, html_tag

class H(_HBase):

    @html_tag
    def html(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def head(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def title(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def base(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def meta(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def style(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def body(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...


    @html_tag
    def article(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def section(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def nav(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def aside(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def h1(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def h2(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def h3(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def h4(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def h5(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def h6(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def header(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def footer(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def address(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...


    @html_tag
    def p(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def hr(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def pre(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def blockquote(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def ol(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            reversed: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def ul(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def menu(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def li(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def dl(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def dt(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def dd(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def figure(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def figcaption(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def main(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def div(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...


    @html_tag
    def em(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def strong(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def small(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def s(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def cite(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def q(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def dfn(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def abbr(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def ruby(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def rt(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def rp(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def data(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def time(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def code(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def var(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def samp(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def kbd(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def sub(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def sup(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def i(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def b(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def u(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def mark(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def bdi(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def bdo(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def span(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def br(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def wbr(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...


    @html_tag
    def ins(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def del_(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...


    @html_tag
    def picture(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def source(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def img(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            loading: Literal["lazy", "eager"] | None = None,
            decoding: Literal["sync", "async", "auto"] | None = None,
            fetchpriority: Literal["high", "low", "auto"] | None = None,
            ismap: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def iframe(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def embed(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def object(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def param(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def video(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            autoplay: bool | None = None,
            controls: bool | None = None,
            loop: bool | None = None,
            muted: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def audio(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            autoplay: bool | None = None,
            controls: bool | None = None,
            loop: bool | None = None,
            muted: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def track(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            default: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def map(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def area(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...


    @html_tag
    def table(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def caption(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def colgroup(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def col(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def thead(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def tbody(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def tfoot(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def tr(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def th(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def td(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...


    @html_tag
    def form(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            method: Literal["get", "post"] | None = None,
            enctype: Literal["application/x-www-form-urlencoded", "multipart/form-data", "text/plain"] | None = None,
            novalidate: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def label(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def select(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            autofocus: bool | None = None,
            disabled: bool | None = None,
            multiple: bool | None = None,
            required: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def datalist(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def optgroup(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            disabled: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def option(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            disabled: bool | None = None,
            selected: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def textarea(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            autofocus: bool | None = None,
            disabled: bool | None = None,
            readonly: bool | None = None,
            required: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def output(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def progress(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def meter(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def fieldset(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            disabled: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def legend(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def input(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            type: Literal["text", "password", "number", "email", "checkbox", "radio", "date", "datetime-local", "file", "hidden", "image", "month", "range", "reset", "search", "submit", "tel", "time", "url", "week", "color"] | None = None,
            disabled: bool | None = None,
            required: bool | None = None,
            checked: bool | None = None,
            multiple: bool | None = None,
            readonly: bool | None = None,
            autofocus: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def button(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            type: Literal["button", "submit", "reset"] | None = None,
            disabled: bool | None = None,
            formnovalidate: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def a(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            target: Literal["_self", "_blank", "_parent", "_top"] | None = None,
            **props: PropVal,
        ) -> "H": ...


    @html_tag
    def details(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            open: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def summary(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def dialog(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            open: bool | None = None,
            **props: PropVal,
        ) -> "H": ...


    @html_tag
    def script(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            type: Literal["module", "text/javascript"] | None = None,
            async_: bool | None = None,
            defer: bool | None = None,
            nomodule: bool | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def noscript(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def template(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def slot(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...

    @html_tag
    def canvas(
            *children: Children,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            **props: PropVal,
        ) -> "H": ...


    @html_tag
    def link(
            *,
            class_: str | None = None,
            id: str | None = None,
            name: str | None = None,
            rel: Literal["stylesheet", "icon", "preload", "prefetch", "modulepreload", "manifest"] | None = None,
            disabled: bool | None = None,
            **props: PropVal,
        ) -> "H": ...
