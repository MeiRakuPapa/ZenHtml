![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Dependencies](https://img.shields.io/badge/Dependencies-0-lightgrey.svg)
![Typing](https://img.shields.io/badge/Typing-mypy-blue.svg)
![Tests](https://img.shields.io/badge/Tests-Passed-brightgreen.svg)
![Philosophy](https://img.shields.io/badge/Philosophy-Simple%20Design-82c91e.svg)
# H

[English README](README.md)

型安全で書きやすい HTML ビルダです。`zen_html.h` に用意されたタグメソッドを呼び出すだけで、Python コードからそのまま HTML を生成できます。標準ライブラリのみで動作し、追加依存はゼロです。`_base.py` がレンダリング処理を担い、`_generator.py` がタグ API (`zen_html.h`) を自動生成する構成になっています。

```
pip install zenhtml
```

## 特徴
- **フルタイピング**: 各タグは `class_`, `id`, `name` など共通属性に加え、タグ固有の Literal/boolean 属性を型で制限しています。`class_` 自体は `str`・`Iterable[str]`・`None` を受け取れるため、クラスリストを組み立ててから渡すようなコードでも追加処理が要りません。
- **DOM ツリー合成が簡単**: 子要素はネストした Iterable も渡せるので、`H.div(list_of_nodes)` のように配列をそのまま差し込めます。プロパティを先に書きたい場合は `children=[...]` をキーワード引数で指定すれば同じ結果になります。
- **便利な補助機能**: `dataset` dict → `data-*` 属性、`style` dict → CSS 文字列、`pretty_html`/`pretty_dict` による整形表示などをサポートしています。
- **生成済みトークンの再利用**: `to_token()` / `html_` / `dict_` プロパティから用途に応じたフォーマットを取得できます。
- **HTML5 の主要タグをカバー**: `_tag_spec.py` に定義された 110+ タグ（メタデータ、フォーム、テーブル、インタラクティブ要素など）を網羅し、SVG/MathML などを除く一般的な HTML ドキュメントをほぼすべて記述できます。対象を絞っているためコードベースもコンパクトに保たれています。
- **デフォルトでエスケープ済み**: 文字列の子要素や属性値は自動的に HTML エスケープされます。どうしてもプレーン HTML を差し込みたい場合は `H.RAW_STR()` で opt-out し、`H.strict_validation` を `True` のままにしておけば void タグへの子要素や不正な Literal が即座に検出されます。

## 使い方
```python
from zen_html.h import H
from typing import Literal

page: H = H.html(
    H.head(
        H.meta(charset="utf-8"),
        H.title("Hello, H"),
    ),
    H.body(
        children=[
            H.h1("Hello"),
            H.p("This markup was generated in Python.", class_=["lead", "muted"]),
            H.button("Click", type="button", disabled=None),
        ],
        class_="page",
    ),
    lang="ja",
)

print(page.html_)          # 1 行の HTML
print(page.pretty_html())  # インデント込みで出力

# mypy での検証例
def button(kind: Literal["button", "submit"]) -> H:
    return H.button("Click", type=kind)

button("button")    # OK
button("invalid")   # mypy でエラー: Literal["button","submit"] に含まれない値
```

`examples/sample.py` には HTML フラグメント/完全な文書を返す `HResponse` / `HDocumentResponse` と `select` ヘルパが含まれており、FastAPI/Starlette 等での実際のレンダリング手順の参考になります。また `examples/pandas_pivot.py` では pandas のピボットテーブルを HTML テーブルに変換するサンプルを紹介しています（pandas は任意依存です）。プロジェクトルートで `python -m examples.pandas_pivot` を実行すると import を崩さずに動作確認できます。

### 主なプロパティ/メソッド
- `html_`: ノード全体を文字列で取得します（テンプレート向け）。
- `pretty_html(indent=0)`: 人が読みやすい形で出力します（デバッグ用途）。
- `to_token()`: HTML トークンを順次生成するジェネレータ。ストリーミングレスポンスに便利です。
- `dict_`: `tag`/`props`/`children` を含む JSON 化しやすい辞書を返します。クライアントに渡したり、Pydantic モデルへ流し込むケースに使えます。

### エスケープとバリデーション
- 文字列ノードと属性値はすべて自動で `html.escape` されます。プレエスケープ済みの断片を挿入したい場合は `H.RAW_STR("<span>safe</span>")` のように明示してください。
- 実行時バリデーション（`H.strict_validation = True` が既定）により、void タグへ子要素を渡したり、Literal/boolean 制約に違反すると `ValueError`/`TypeError` が発生します。警告ログだけで続行したい場合は `False` に切り替えられます。検証はノード生成時に行われるので、`to_token()` や `HResponse` でストリーミングしても途中で壊れた HTML が流れることはありません。

### `dict_` を通じて JavaScript で描画する例
`dict_` は JSON 化できる構造なので、クライアントに渡して JS でレンダリングできます。

```python
import json
from zen_html.h import H

payload = json.dumps(H.div("Hi", class_=["greeting", "highlight"]).dict_)
```

```html
<script type="module">
  import { HRender } from "/examples/h_render.js";
  const tree = JSON.parse({{ payload | tojson }});
  document.body.appendChild(HRender(tree));
</script>
```

## タグ API の再生成
`H/h.py` は `_generator.py` が `_tag_spec.py` を基に自動生成しています。タグ仕様を変更したら以下を実行して再生成してください。

```bash
python3 - <<'PY'
from zen_html._generator import generate_class
generate_class(output="H/h.py")
PY
```

## 開発メモ
- Lint 設定は `pyproject.toml` で管理しています（Black/Isort/djlint）。
- boolean 属性は `True` なら属性名のみを出力し、`False`/`None` は無視します。
- `dataset` 引数に dict を渡すと自動的に `data-foo-bar` のような属性へ展開されます。`style` 引数に dict を渡すと `font-size: 12px` のような文字列へ変換されます。
- Python 3.10 以上を想定しており、`ParamSpec` ベースのデコレータで VS Code 等の補完も正しく機能します。

## ライセンス
ライセンス情報は `LICENSE` を参照してください。
