# Tables

Render DataFrames and CSV data as Markdown tables.

`doc.table` turns a pandas DataFrame, a CSV string, or anything `pd.DataFrame(...)` accepts into a Markdown table. Tables need pandas:

```bash
pip install 'cmx[tables]'
```

The default `github` format is rendered by CMX's own pure-Python renderer, so you do **not** need `tabulate` for it. CMX inserts a blank line before each table automatically; you never add one by hand.

## Basic DataFrame

Pass a DataFrame to `doc.table`.

```python
from cmx import doc
import pandas as pd

doc.config(__file__)

data = pd.DataFrame({
    "Model": ["ResNet50", "VGG16", "MobileNet"],
    "Accuracy": [0.95, 0.87, 0.92],
    "Parameters": ["25.6M", "138M", "4.2M"],
})

doc.table(data)
doc.flush()
```

This writes:

```markdown
| Model     |   Accuracy | Parameters   |
|-----------|------------|--------------|
| ResNet50  |       0.95 | 25.6M        |
| VGG16     |       0.87 | 138M         |
| MobileNet |       0.92 | 4.2M         |
```

## CSV data

`doc.csv` renders a CSV string directly.

```python
doc.csv("""\
Experiment,Success Rate,Trials
baseline,45.2%,100
optimized,67.8%,100
final,89.1%,100
""")
```

`doc.table` accepts the same CSV string, so these are equivalent:

```python
csv = "Model,Accuracy\nResNet50,0.95\nVGG16,0.87"

doc.csv(csv)
doc.table(csv)
```

To load a CSV file from disk, read it with pandas first:

```python
doc.table(pd.read_csv("results.csv"))
```

## Hiding the index

`doc.table` and `doc.csv` hide the DataFrame index by default (`show_index=False`). Pass `show_index=True` to keep it.

```python
results = pd.DataFrame({
    "Experiment": ["baseline", "optimized", "final"],
    "Success Rate": ["45.2%", "67.8%", "89.1%"],
})

doc.table(results, show_index=True)
```

```markdown
|    | Experiment   | Success Rate   |
|----|--------------|----------------|
|  0 | baseline     | 45.2%          |
|  1 | optimized    | 67.8%          |
|  2 | final        | 89.1%          |
```

## Table formats

`format="github"` (the default) is rendered by CMX's built-in renderer and needs only pandas. Any other format falls back to pandas' `to_markdown`, which requires `tabulate`:

```bash
pip install tabulate
```

```python
doc.table(data, format="grid")   # needs tabulate
doc.table(data, format="pipe")   # needs tabulate
```

| `format` | Renderer | Extra dependency |
|----------|----------|------------------|
| `github` (default) | CMX `md_table` | none |
| `pipe`, `grid`, `simple`, ... | pandas `to_markdown` | `tabulate` |

:::{tip}
Stay on the default `github` format unless you need a specific layout. It keeps your install free of `tabulate` and renders identically to `to_markdown(tablefmt="github")`.
:::

## Manual Markdown tables

When your data is already laid out, write the table as text with `doc @` instead of building a DataFrame.

```python
doc @ """
| Checkpoint | Success | Num Trials |
| ---------- | ------- | ---------- |
| v1         | 45.2%   | 100        |
| v2         | 67.8%   | 100        |
| v3         | 89.1%   | 100        |
"""
```

The text passes through unchanged, so this needs no extras.

## Figure grids and media cells

`doc.table()` with no data starts an empty table that you fill with
`table.figure_row()`. Each figure row is one horizontal band of cells; the
table renders every band as up to three Markdown rows — **titles**, **cells**,
**captions** — and drops the rows a band never used.

```python
with doc.table() as table:
    for ep in ("0000", "0001", "0002"):
        with table.figure_row() as row:
            row.column(title="episode", text=f"`{ep}`")
            row.figure(src=f"episodes/{ep}/frame.png", title="first frame")
            row.video(src=f"episodes/{ep}/rollout.gif", title="rollout")
```

The cell methods, one column each:

- `row.column(title=None, text=None, footer=None)` — a plain-text cell; use it
  to label media columns with ids, paths, or metrics.
- `row.figure(image=None, src=None, title=None, caption=None)` — an image
  cell. With an array the bytes are written through the document's `on_save`
  hook; with only `src=` the link is rendered as-is.
- `row.video(frames=None, src=None, title=None, caption=None)` — a video
  cell; see the GIF/MP4 rule below.
- `row.savefig(key, title=None, caption=None, ...)` — capture the current
  matplotlib figure into a cell (see [Figures](figures.md)).

Media cells need no extras when you only pass `src=` links; writing arrays
needs `cmx[images]`.

### GIFs go in cells, MP4s go below the table

A `.gif` `src` renders as an image link (`![...](...)`), which works inside a
table cell anywhere Markdown renders. Any other extension renders as a
multi-line HTML5 `<video>` block — and Markdown table cells are single-line,
so an `.mp4` cell breaks the table. Put GIF previews in the cells and embed
the full video in a standalone block after the table:

```python
row.video(src="rollout.gif", title="preview")   # in the cell
doc.video(src="rollout.mp4")                    # below the table
```

### Placeholder cells — link artifacts that do not exist yet

When a cell gets only `src=` (no array, no frames), the default `on_save`
hook does **no I/O**: the link is rendered without writing a file. Cells can
therefore point at artifacts your pipeline has not produced yet, and the
report becomes a live dashboard — the images and previews appear the moment
the files are written, with no change to the document.

```python
t = doc.table()
for ep in ("0000", "0001"):
    row = t.figure_row()
    row.column(title="episode", text=f"`{ep}`")
    row.column(title="goal", text=f"`outputs/{ep}/goal.json`")
    row.figure(src=f"../data/outputs/{ep}/images/rgb/00000.png", title="first ego frame")
    row.video(src=f"../data/outputs/{ep}/images/rgb/ego.gif", title="rollout")
```

Links are written into the markdown verbatim and resolve relative to the
`.md` file, so compute them accordingly (`../data/...` from a `docs/` folder).

### Path resolution in figure rows

Figure-row assets follow the same rule as `doc.image`: a **bare name**
(`"loss.png"`) lands under the document's `figdir`; a name **with a slash**
(`"episodes/0000/frame.png"`) is used as-is — explicit wins.

## Next steps

- [Installation](installation.md) — install the `cmx[tables]` extra and other optional features.
- [Images](images.md) — arrange figures in grids and rows.
- [Figures](figures.md) — matplotlib figure grids with `row.savefig`.
- [Printing](printing.md) — add computed output with `doc.print()`.
