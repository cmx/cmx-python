---
name: cmx-components
description: Guide to CMX rich components — tables and figure_row media grids, images, figures, savefig, videos/GIFs, rows, and troubleshooting. Use when building CMX reports with tables, plots, or media.
---

# CMX Components Skill

This skill provides detailed guidance on CMX's rich components for building documentation. CMX renders to **Markdown** (the backend), with partial HTML rendering for some components (rows, videos).

## Component Overview

- **Text**: prose via `@` / `|` / call forms
- **Print**: `print`-style output, coalesced into code blocks
- **Pre / YAML**: raw and YAML code blocks
- **Table**: tabular data from DataFrames, CSV, or files — or a figure grid via `table.figure_row()`
- **Image**: array or file images, auto-saved through `on_save`
- **Figure / Savefig**: images and matplotlib figures with titles/captions
- **Video**: video and GIF embedding
- **Row**: horizontal layout container

Each rich block requires an extra (see the basics skill): tables need `cmx[tables]` (pandas), images need `cmx[images]` (pillow+numpy), `savefig` needs `cmx[figures]` (matplotlib), yaml needs `cmx[yaml]`. The core is dependency-free.

## Text Components

### Markdown Text — three equivalent forms

```python
from cmx import doc

doc.config(__file__)

doc("# Heading 1", end="\n")   # call form (end="\n" is the default)
doc @ "## Heading 2"           # prefix @ operator
"**Bold** and *italic*" | doc  # postfix | operator
```

All three append a text block and return `doc`. `doc.md` is an alias for the call form. Only the call form accepts keywords such as `end=`; use `end=""` to keep the next block on the same line. A tuple spreads into one block per item: `doc @ ("First.", "Second.")`. The left-side pipe `doc | other` raises `NotImplementedError`. Text is dedented by default (`dedent=True`).

### Print Component

Works like Python's `print()`, and also echoes to stdout:

```python
with doc:
    doc.print("Single line")
    doc.print("Multiple", "arguments", sep="-")
    doc.print("No newline", end="")
    doc.print(" continues here")
```

**Coalescing:** consecutive `doc.print` calls merge into a single code block. Any non-print block in between starts a fresh code block.

## Pre and YAML

`doc.pre(text, lang=None)` emits a raw fenced code block. `doc.yaml` renders a Python object as a YAML code block, or reads a `.yaml` file from disk verbatim (comments and all):

```python
config = {"model": {"name": "ResNet50", "layers": 50}}

doc("# Configuration")
doc.yaml(config)               # dump a Python object
doc.yaml(file="conf.yaml")     # show a YAML file verbatim
```

```yaml
model:
  name: ResNet50
  layers: 50
```

## Table Component

Render DataFrames or CSV data as Markdown tables (needs `cmx[tables]`). CMX inserts a blank line before each table automatically.

```python
import pandas as pd
from cmx import doc

doc.config(__file__)

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Score": [95, 87, 92],
})

doc("# Results Table")
doc.table(df, show_index=False)   # show_index defaults to False
```

The default `format="github"` is rendered by CMX's built-in pure-Python renderer (`cmx.backends.md_table`) and needs only pandas. Other formats fall back to pandas' `to_markdown` and require `tabulate`:

```python
doc.table(df, format="grid")   # needs `pip install tabulate`
doc.table(df, format="pipe")   # needs `pip install tabulate`
```

### CSV strings and files

`doc.csv` renders a CSV string directly; `doc.table` accepts the same string. To load from disk, pass `file=` — the extension is inferred (csv / tsv / json / parquet / excel / yaml):

```python
doc.csv("Model,Accuracy\nResNet50,0.95\nVGG16,0.87")

doc.table(file="data.csv")       # also .tsv / .json / .parquet / .xlsx / .yaml
doc.table(file="metrics.parquet")
```

### Figure grids — media tables with `figure_row`

`doc.table()` with no data starts an empty table filled via
`table.figure_row()`. Each figure row is one band of cells, rendered as up to
three Markdown rows — **titles**, **cells**, **captions** — with unused bands
dropped. Cell methods (one column each):

```python
with doc.table() as table:
    for ep in ("0000", "0001", "0002"):
        with table.figure_row() as row:
            row.column(title="episode", text=f"`{ep}`")     # plain-text cell
            row.figure(src=f"episodes/{ep}/frame.png",       # image cell
                       title="first frame", caption="step 0")
            row.video(src=f"episodes/{ep}/rollout.gif",      # media cell
                      title="rollout")
            # row.savefig("plot.png", ...) captures the current mpl figure
```

Rules that matter in practice:

- **GIFs in cells, MP4s below the table.** A `.gif` src renders as a
  single-line image link (table-safe). Any other extension renders as a
  multi-line HTML5 `<video>` block that **breaks a Markdown table cell** —
  embed it standalone with `doc.video(src="x.mp4")` after the table.
- **Placeholder cells.** With only `src=` (no array/frames), the default
  `on_save` does no I/O: the link renders without writing a file, so cells
  can point at artifacts a pipeline has not produced yet — the report fills
  in as files appear. Links resolve relative to the `.md` file.
- **figdir rule applies**: bare names land under `figdir`; slashed paths are
  used as-is.
- src-only links need no extras; writing arrays through cells needs
  `cmx[images]`.

## Image Component

Save numpy arrays or reference existing files (needs `cmx[images]`). Saving creates directories automatically.

```python
import numpy as np
from cmx import doc

doc.config(__file__)

# RGB array: (height, width, 3), uint8 0–255
image = (np.random.rand(100, 100, 3) * 255).astype(np.uint8)

with doc:
    doc.image(image, src="random.png")              # bare name -> figdir/random.png
    doc.image(image, src="random.png", normalize=True)
    doc.image(src="existing.png")                   # reference a file, no array
```

### Image arguments (verified against `components.py`)

- `image` — numpy array (omit it to reference an existing file via `src`).
- `src` — asset path. A **bare name** lands under `figdir`; a name **with a slash** is used as-is. With no `src`, an array is inlined as a base64 `data:` URI.
- `normalize` — forwarded to the saver to normalize pixel values.

Note: `width` / `height` / `style` / `class_name` are **not** parameters of `doc.image` — do not pass them. (`doc.savefig` and `doc.figure` do accept `width` / `height` / `zoom`; see below.)

## Figure Component

`doc.figure` attaches a `title` and/or `caption` to an image. Same array-or-`src` rules as `doc.image`:

```python
with doc:
    doc.figure(
        gradient,                 # array, or omit and pass src=
        src="gradient.png",
        title="Gradient",
        caption="A horizontal color ramp.",
    )
```

### Savefig — save the current matplotlib figure

`doc.savefig(key)` saves the **current** matplotlib figure and links it (needs `cmx[figures]`). The `key` resolves through `figdir` just like image `src`.

```python
import matplotlib.pyplot as plt
from cmx import doc

doc.config(__file__)

plt.plot([1, 2, 3], [1, 4, 9])

with doc:
    doc.savefig("plot.png", caption="A simple line plot")
```

`doc.savefig` accepts `caption`, `width`, `height`, `zoom`; any other keyword (`dpi`, `bbox_inches`, `transparent`, `facecolor`, `format`, ...) is forwarded straight to matplotlib's `savefig` and is **not** leaked into the `<img>` tag.

## Video Component

Embed videos and GIFs (frame arrays need `cmx[images]`):

```python
import numpy as np
from cmx import doc

frames = np.random.randint(0, 255, (30, 100, 100, 3), dtype=np.uint8)

with doc:
    doc.video(frames, src="animation.gif")   # .gif renders as an Image
    doc.video(src="demo.mp4")                # .mp4 renders as HTML5 <video>
```

`.gif` sources render as an `Image` (works everywhere); other extensions render as an HTML5 `<video>` (shown only where HTML is rendered). The `src` resolves through `figdir` like other assets.

## Layout — `doc.row()`

`doc.row()` is a **method call** (`with doc.row():`, not `with doc.row:`). It arranges its children in a horizontal flex container (an HTML `<div>`, so layout shows where HTML is rendered; the images themselves still render in plain Markdown).

```python
import numpy as np
from cmx import doc

doc.config(__file__)

with doc:
    doc("# Side-by-side Images")
    with doc.row():
        for i in range(3):
            img = (np.random.rand(50, 50, 3) * 255).astype(np.uint8)
            doc.image(img, src=f"mini_{i}.png")
```

## Advanced Usage

### Combining Components

```python
from cmx import doc
import pandas as pd
import matplotlib.pyplot as plt

doc.config(__file__)

data = pd.DataFrame({"x": range(10), "y": [i**2 for i in range(10)]})

plt.figure(figsize=(10, 6))
plt.plot(data["x"], data["y"])

with doc:
    doc("# Analysis Results")

    doc("## Data Table")
    doc.table(data)

    doc("## Visualization")
    doc.savefig("analysis.png", caption="Quadratic growth")

    doc("## Summary Statistics")
    doc.yaml(data.describe().to_dict())

doc.flush()
```

## Best Practices

1. **Pass bare asset names** (`"loss.png"`) and let `figdir` organize them; use a slashed path only when an asset must live somewhere specific.
2. **Add captions** to figures to help readers.
3. **Normalize images** with `normalize=True` for consistent display.
4. **Keep tables readable** — limit rows/columns; use `show_index=True` only when the index matters.
5. **Stay on the default `github` table format** unless you need a specific layout — it keeps `tabulate` out of your install.

## Troubleshooting

### Images not displaying

- Check that the `src` is what you expect: a bare name lands under `figdir`, a slashed name is used as-is, and links are written relative to the `.md`.
- You do **not** need to pre-create directories — CMX's default `on_save` creates them automatically when it writes the asset.

### Tables not formatting correctly

- Tables need `cmx[tables]` (pandas). The default `github` format needs only pandas; alternate `format=` values need `tabulate`.
- Ensure data is a DataFrame, a CSV string, or loadable via `file=`.
- Use `show_index=False` (the default) to hide the index.

### Videos not playing

- GIFs render as images and work everywhere; `.mp4`/`.webm` render as HTML5 `<video>` and show only where HTML is rendered.
- Never put an `.mp4` in a `figure_row` cell — the multi-line `<video>` block breaks the Markdown table. Use a GIF preview in the cell and the MP4 in a standalone `doc.video` block.
- Check file size and codec compatibility for MP4.

### Routing assets elsewhere (S3, a dashboard, ...)

- There is no logger. Override the `on_save` lifecycle hook (bind on the instance, or subclass `CommonMark`) to write bytes wherever you want and return the link CMX renders. See the basics skill's "Storage & integration hooks" and the Hooks guide.

## Learn More

- Full documentation: https://cmx.readthedocs.io
- API Reference: https://cmx.readthedocs.io/en/latest/api/
- Component source: `src/cmx/backends/components.py`
