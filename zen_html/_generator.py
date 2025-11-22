# Copyright (c) 2025 Yusuke KITAGAWA (tonosama_kaeru@icloud.com)

from textwrap import indent
from typing import cast

from ._base import R_PROP_NAME_MAP, VOID_TAGS
from ._tag_spec import TAG_SPEC

COMMON_PARAMS = [
    ("class_", "str | None", "None"),
    ("id", "str | None", "None"),
    ("name", "str | None", "None"),
]


def literal_type(values: list[str]) -> str:
    xs = ", ".join(f'"{v}"' for v in values)
    return f"Literal[{xs}] | None"


def generate_signature(tag: dict[str, object]) -> str:
    name = tag["tag"]
    restricted_literal = cast(dict[str, list[str]], tag.get("restricted_literal", None))
    restricted_bool = cast(list[str], tag.get("restricted_bool", None))
    is_void = name in VOID_TAGS

    params = []

    if not is_void:
        params.append("*children: Children")
    else:
        params.append("*")

    # Common parameters
    for pn, typ, default in COMMON_PARAMS:
        params.append(f"{pn}: {typ} = {default}")

    # Literal restricted parameters
    if restricted_literal:
        for pn, values in restricted_literal.items():
            if pn in R_PROP_NAME_MAP:
                pn = R_PROP_NAME_MAP[pn]
            ptype = literal_type(values)
            params.append(f"{pn}: {ptype} = None")

    # bool parameters
    if restricted_bool:
        for pn in restricted_bool:
            if pn in R_PROP_NAME_MAP:
                pn = R_PROP_NAME_MAP[pn]
            params.append(f"{pn}: bool | None = None")

    params.append("**props: PropVal")

    sig = ",\n        ".join(params)
    fname = name if name != "del" else "del_"
    return f'def {fname}(\n        {sig},\n    ) -> "H": ...'


def generate_class(
    *, spec: list[dict[str, object]] = TAG_SPEC, output: str | None = None
) -> None:

    out = []
    out.append("# mypy: disable-error-code=empty-body")
    out.append("# mypy: disable-error-code=misc")

    out.append("from typing import Literal")
    out.append("from ._base import Children, PropVal, _HBase, html_tag")
    out.append("")
    out.append("class H(_HBase):")

    for entry in spec:
        tagname = entry["tag"]

        if tagname in [
            "html",
            "article",
            "p",
            "em",
            "ins",
            "picture",
            "table",
            "form",
            "details",
            "script",
            "link",
        ]:
            out.append("")

        sig = generate_signature(entry)
        block = f"@html_tag\n{sig}"
        out.append(indent(block, "    "))
        out.append("")

    code = "\n".join(out)

    if output is None:
        print(code)
    else:
        with open(output, "w", encoding="utf-8") as f:
            f.write(code)
