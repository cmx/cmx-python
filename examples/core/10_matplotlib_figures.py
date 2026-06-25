"""
Matplotlib Figures Example

Save matplotlib plots straight into your CMX documentation with ``doc.savefig``
-- including control over ``dpi``, bounding box, and transparency -- and arrange
several plots side-by-side as a figure table.

Run with::

    pip install "cmx[figures]"   # pulls in matplotlib
    python examples/core/10_matplotlib_figures.py
"""

from cmx import doc
import os

# Setup code: kept out of the rendered document with ``doc.hide``.
with doc.hide:
    import matplotlib

    matplotlib.use("Agg")  # headless-friendly backend; drop this for interactive use
    import matplotlib.pyplot as plt
    import numpy as np

    os.makedirs("examples/core/figures", exist_ok=True)

doc.config(filename="examples/core/10_matplotlib_figures.md")

doc @ """
# Working with Matplotlib Figures

`doc.savefig` saves the *current* matplotlib figure to disk and embeds it in
your document in a single call -- the moral equivalent of `plt.savefig` that also
writes the markdown for you.

Any keyword `doc.savefig` doesn't use for layout (`dpi`, `bbox_inches`,
`transparent`, `facecolor`, `format`, ...) is forwarded untouched to matplotlib's
own `savefig`, so it never leaks into the generated `<img>` tag.
"""

with doc:
    doc @ "## A Single Figure"

    xs = np.linspace(0, 5, 200)

    plt.figure(figsize=(5, 3))
    plt.plot(xs, np.sin(2 * np.pi * xs))
    plt.title("sine wave")

    # dpi and bbox_inches go to matplotlib; only the path is referenced in markdown.
    doc.savefig("examples/core/figures/sine.png", dpi=150, bbox_inches="tight")
    plt.close()

with doc:
    doc @ """
    ## Controlling Resolution with `dpi`

    `dpi` (dots per inch) controls how many pixels matplotlib renders. Higher
    values give crisper figures at the cost of file size -- use ~100 for quick
    drafts and 200+ for publication-quality output.
    """

    plt.figure(figsize=(4, 3))
    plt.plot(xs, np.exp(-xs) * np.cos(4 * np.pi * xs))
    plt.title("damped oscillation")

    # Save the same figure twice at different resolutions.
    doc.savefig("examples/core/figures/damped_72dpi.png", dpi=72, bbox_inches="tight")
    doc.savefig("examples/core/figures/damped_200dpi.png", dpi=200, bbox_inches="tight")
    plt.close()

with doc:
    doc @ """
    ## A Figure Table

    Group related plots into a grid with `table.figure_row()`. Each
    `row.savefig(...)` captures the current figure and adds a column with an
    optional `title` and `caption`. The forwarded `dpi` keeps the thumbnails
    consistent.
    """

    functions = {"sine": np.sin, "cosine": np.cos, "tanh": np.tanh}

    with doc.table() as table, table.figure_row() as row:
        for name, fn in functions.items():
            plt.figure(figsize=(4, 3))
            plt.plot(xs, fn(xs))
            plt.title(name)
            row.savefig(
                f"examples/core/figures/fn_{name}.png",
                title=name.capitalize(),
                caption=f"y = {name}(x)",
                dpi=100,
            )
            plt.close()

with doc:
    doc @ """
    ## Transparent Background

    Pass `transparent=True` (a matplotlib `savefig` flag) for figures that need
    to sit on a colored page -- the surrounding area is saved with an alpha
    channel instead of white.
    """

    plt.figure(figsize=(5, 3))
    plt.bar(["a", "b", "c"], [3, 7, 5])
    plt.title("counts")

    doc.savefig("examples/core/figures/bars.png", dpi=120, bbox_inches="tight", transparent=True)
    plt.close()

doc.flush()

print("\n✓ Matplotlib figures example complete! Check examples/core/10_matplotlib_figures.md")
