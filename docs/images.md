# Images

Display numpy arrays and image files in your documentation, and arrange them in rows.

Image support needs the `images` extra (`pip install 'cmx[images]'`), which pulls in `pillow` and `numpy`. Saving matplotlib figures needs the `figures` extra. See [Installation](installation.md) for the full list.

## Basic image

Pass a numpy array to `doc.image` and CMX writes it to disk, then links it from the Markdown.

```python
from cmx import doc
import numpy as np

doc.config(__file__)

with doc:
    doc @ "## Random Image"

    # Create a random RGB image (height, width, 3)
    random_image = np.random.rand(100, 100, 3)
    random_image = (random_image * 255).astype(np.uint8)

    doc.image(random_image, src="random.png")

doc.flush()
```

The array is saved to `random.png` and the generated Markdown links to it:

```markdown
## Random Image

![04_images/random.png](04_images/random.png)
```

The link points at `04_images/`, not the bare name you passed. That folder is the **figdir** — explained in [Where files land](where-files-land) below.

:::{note}
RGB arrays are shaped `(height, width, 3)` with `uint8` values in `0–255`. Scale floats and cast before passing them in, as shown above.
:::

## Referencing existing files

To link an image that already exists on disk, pass only `src` and omit the array.

```python
with doc:
    doc @ "## Existing Figure"

    doc.image(src="diagram.png")
```

CMX writes the link without touching the file. The same resolution rules apply: a bare name lands under figdir, a name with a slash is used as you wrote it.

(where-files-land)=
## Where files land

The `src` you pass is resolved against the document's **figdir**, the folder where assets are written and linked from.

- A **bare name** (no slash, e.g. `"random.png"`) is placed **under figdir**. By default figdir is `{fname}` — a per-document folder named after the script, so `04_images.py` writes to `04_images/`.
- A name **with a directory** (e.g. `"shared/diagram.png"`) is used **as-is**. An explicit path always wins.
- Links are written **relative to the Markdown file**, so the document stays portable.

```python
doc.config(__file__)                 # figdir defaults to "04_images/"

doc.image(arr, src="random.png")     # -> 04_images/random.png
doc.image(arr, src="plots/a.png")    # -> plots/a.png (used verbatim)
```

To change where bare names go, set `figdir` when you configure the document:

```python
doc.config(__file__, figdir="assets")   # bare names land under assets/
```

See [Configuration](configuration.md) for the full figdir template and working-directory rules.

## Side-by-side with `doc.row()`

Wrap several `doc.image` calls in `with doc.row():` to lay them out horizontally.

```python
with doc:
    doc @ "## Multiple Images in a Row"

    with doc.row():
        for i in range(3):
            img = np.random.rand(50, 50, 3)
            img = (img * 255).astype(np.uint8)
            doc.image(img, src=f"mini_{i}.png")
```

The row renders as a flex container followed by the images:

```markdown
## Multiple Images in a Row

<div style="flex-wrap:nowrap; display:flex; flex-direction:row; item-align:center;"></div>

![04_images/mini_0.png](04_images/mini_0.png)

![04_images/mini_1.png](04_images/mini_1.png)

![04_images/mini_2.png](04_images/mini_2.png)
```

Each image still resolves through figdir, so the three files land in `04_images/`.

## Figures and captions

Use `doc.figure` to attach a title or caption to an image. It accepts the same array-or-path arguments as `doc.image`, plus `title` and `caption`.

```python
with doc:
    doc.figure(
        gradient,
        src="gradient.png",
        title="Gradient",
        caption="A horizontal-vertical color ramp.",
    )
```

## Saving matplotlib figures

`doc.savefig` saves the **current** matplotlib figure to a file and links it. This needs the `figures` extra (`pip install 'cmx[figures]'`).

```python
import matplotlib.pyplot as plt

with doc:
    doc @ "## Plot"

    plt.plot([0, 1, 2], [0, 1, 4])
    doc.savefig("plot.png")
```

The filename resolves through figdir exactly like `doc.image`, so `"plot.png"` lands under the document's figdir. For dpi control, figure tables, and transparent backgrounds, see [Matplotlib Figures](figures.md).

## Next steps

- [Matplotlib Figures](figures.md) — save plots with `doc.savefig` (dpi, figure tables)
- [Configuration](configuration.md) — control figdir and where assets are written
- [Installation](installation.md) — install the `images` and `figures` extras
- [Tables](tables.md) — build figure grids alongside tabular data
