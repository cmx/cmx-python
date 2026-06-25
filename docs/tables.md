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

## Next steps

- [Installation](installation.md) — install the `cmx[tables]` extra and other optional features.
- [Images](images.md) — arrange figures in grids and rows.
- [Printing](printing.md) — add computed output with `doc.print()`.
