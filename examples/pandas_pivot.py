"""Example: render a pandas pivot table as HTML using H."""

from __future__ import annotations

from typing import Iterable, Sequence

import pandas as pd  # type: ignore[import-not-found]

from zen_html.h import H


def pivot_table_html(
    df: pd.DataFrame,
    *,
    index: Sequence[str],
    columns: Sequence[str],
    values: str,
    aggfunc: str | callable = "sum",
    format_cell: str | callable = "{:,.0f}",
) -> H:
    """Convert a pandas pivot table into an HTML table node."""
    # Build a pivot table (fill missing cells with zero for readability)
    pivot = df.pivot_table(
        index=index,
        columns=columns,
        values=values,
        aggfunc=aggfunc,
        fill_value=0,
    )

    column_labels: Iterable[str] = (
        (" / ".join(map(str, col)) if isinstance(col, tuple) else str(col))
        for col in pivot.columns
    )

    header = H.thead(
        H.tr(
            H.th(" / ".join(index)),
            *(H.th(label) for label in column_labels),
        )
    )

    def render_cell(value: object) -> str:
        if callable(format_cell):
            return format_cell(value)  # type: ignore[misc]
        return format_cell.format(value)

    body_rows = []
    for idx, row in pivot.iterrows():
        row_label = " / ".join(map(str, idx)) if isinstance(idx, tuple) else str(idx)
        body_rows.append(
            H.tr(
                H.th(row_label),
                *(H.td(render_cell(value)) for value in row),
            )
        )

    return H.table(
        header,
        H.tbody(*body_rows),
        class_="pivot-table",
    )


if __name__ == "__main__":
    # Demo dataset – in real apps you'll fetch this from your data source
    data = pd.DataFrame(
        [
            {"region": "APAC", "channel": "Web", "quarter": "Q1", "sales": 1200},
            {"region": "APAC", "channel": "Retail", "quarter": "Q1", "sales": 800},
            {"region": "EMEA", "channel": "Web", "quarter": "Q1", "sales": 1500},
            {"region": "EMEA", "channel": "Retail", "quarter": "Q1", "sales": 900},
            {"region": "APAC", "channel": "Web", "quarter": "Q2", "sales": 1400},
            {"region": "APAC", "channel": "Retail", "quarter": "Q2", "sales": 700},
            {"region": "EMEA", "channel": "Web", "quarter": "Q2", "sales": 1600},
            {"region": "EMEA", "channel": "Retail", "quarter": "Q2", "sales": 950},
        ]
    )

    node = pivot_table_html(
        data,
        index=["region"],
        columns=["quarter"],
        values="sales",
        format_cell="{:,}",
    )
    print(node.pretty_html())
