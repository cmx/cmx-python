# Matplotlib Figures

**Questions**
- How do I save a matplotlib plot into my documentation?
- How do I control resolution (`dpi`) and other `savefig` options?
- How do I lay several plots out as a figure table?

**Objectives**
- Save the current figure with `doc.savefig`
- Forward matplotlib options like `dpi`, `bbox_inches`, and `transparent`
- Build a grid of plots with `table.figure_row()`

> Matplotlib is an optional dependency. Install it with `pip install "cmx[figures]"`.

## Saving the Current Figure

`doc.savefig(path)` is the moral equivalent of `plt.savefig` that *also* writes
the markdown for you: it saves whatever figure is currently active and embeds a
reference to it in the document.

```python
from cmx import doc
import matplotlib.pyplot as plt
import numpy as np

doc.config(filename="output.md")

with doc:
    doc @ "## Sine Wave"

    xs = np.linspace(0, 5, 200)
    plt.figure(figsize=(5, 3))
    plt.plot(xs, np.sin(2 * np.pi * xs))

    doc.savefig("figures/sine.png")
    plt.close()

doc.flush()
```

The figure is written to `figures/sine.png` (directories are created for you) and
displayed inline.

## Controlling Resolution and Layout

Any keyword `doc.savefig` does not use for layout is forwarded **untouched** to
matplotlib's own `savefig`. The most common ones:

- `dpi` — dots per inch; higher means crisper figures and larger files. Use ~100
  for drafts and 200+ for publication-quality output.
- `bbox_inches="tight"` — trim surrounding whitespace.
- `transparent=True` — save with an alpha channel instead of a white background.
- `facecolor`, `pad_inches`, `format`, … — anything `plt.savefig` accepts.

```python
with doc:
    doc.savefig("figures/plot.png", dpi=200, bbox_inches="tight", transparent=True)
```

These options affect the saved file only — they never leak into the generated
`<img>` tag.

## Layout Options

`doc.savefig` accepts a few keywords for *displaying* the figure (as opposed to
saving it): `title`, `caption`, `width`, `height`, and `zoom`.

```python
with doc:
    doc.savefig(
        "figures/loss.png",
        dpi=150,              # -> matplotlib
        caption="Training loss",  # -> document
        zoom=0.5,                 # -> document
    )
```

## Figure Tables

Group related plots into a grid with `table.figure_row()`. Each
`row.savefig(...)` captures the current figure and adds a column with an optional
`title` and `caption`:

```python
with doc:
    doc @ "## Activation Functions"

    functions = {"sine": np.sin, "cosine": np.cos, "tanh": np.tanh}

    with doc.table() as table, table.figure_row() as row:
        for name, fn in functions.items():
            plt.figure(figsize=(4, 3))
            plt.plot(xs, fn(xs))
            row.savefig(
                f"figures/{name}.png",
                title=name.capitalize(),
                caption=f"y = {name}(x)",
                dpi=100,
            )
            plt.close()
```

This renders as a Markdown table with one column per figure: a row of titles, a
row of images, and a row of captions. Call `table.figure_row()` again for a
second band of figures.

## Key Points

- Use `doc.savefig("path.png")` to save the current matplotlib figure and embed it
- `dpi`, `bbox_inches`, `transparent`, and friends are forwarded to matplotlib
- `title`, `caption`, `width`, `height`, `zoom` control how the figure is displayed
- Use `table.figure_row()` + `row.savefig(...)` to lay out a grid of plots
- Call `plt.close()` after saving to free the figure

## Next Steps

- [Images](images.md) - Display numpy arrays as images
- [Tables](tables.md) - Display data tables
