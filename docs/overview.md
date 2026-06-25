# Quickstart

Learn the configure → capture → flush workflow and write your first document.

CMX generates live Markdown from a Python script. You wrap the code you want to document in a `with doc:` block, and CMX writes both that source and its output to a `.md` file. Think of it as a notebook where you decide exactly what appears.

## Your first document

Create a file called `report.py`:

```python
from cmx import doc

doc.config(__file__)

with doc:
    doc @ "# Hello, CMX"
    doc.print("It works.")

doc.flush()
```

Run it. CMX writes `report.md` next to the script:

````markdown
# Hello, CMX

```python
doc.print("It works.")
```

```
It works.
```
````

The captured source and its output appear in order. The rest of this page covers the three steps you just used.

## The three steps

### 1. Configure

Call `doc.config(__file__)` once at the top. Passing `__file__` anchors the output to the script: CMX writes `<script>.md` in the **same directory as the script**, and roots any assets there too.

```python
doc.config(__file__)
```

You can also pass an explicit path or relocate the output. See [Configuration](configuration.md) for `wd=`, `figdir`, and asset paths.

### 2. Capture

Wrap the code you want shown in `with doc:`. CMX captures the block's source as a Python code fence, then runs it. Anything you add with `doc.print` or the text operators appears alongside the source.

```python
with doc:
    result = 42
    doc.print(f"The answer is {result}")
```

Use `doc.print(...)` for computed output, and `doc @ "text"` to add Markdown such as headings and prose. The `@`, `|`, and call forms are equivalent:

```python
doc @ "# Title"      # prefix
"# Title" | doc      # postfix
doc("# Title", end="\n")       # call (end="\n" is the default)
```

All three append text and return `doc`. See [Markdown](markdown.md) for the full treatment, including multi-line dedent and `end=` control.

### 3. Flush

Call `doc.flush()` to render everything to the `.md` file. Leaving a `with doc:` block also flushes, so an explicit call at the end is enough for most scripts.

```python
doc.flush()
```

## Code outside `with doc:` runs but isn't shown

Only code inside a `with doc:` block is captured. Code at module level still executes — it just doesn't appear in the document. This is how you keep setup, imports, and bookkeeping out of the output.

```python
data = [10, 20, 30, 40, 50]      # runs, not shown
mean = sum(data) / len(data)     # runs, not shown

with doc:
    doc.print(f"Mean: {mean}")   # shown
```

For finer control — running boilerplate without showing it, or skipping a block entirely — see [Context managers](context.md).

## Complete example

This script combines configuration, hidden setup, captured blocks, and several block types.

```python
from cmx import doc
import pandas as pd
import numpy as np

doc.config(__file__)

doc @ """
# Machine Learning Experiment Report

This report documents a baseline image-classification experiment.
"""

# Setup runs but stays out of the document.
with doc.hide:
    np.random.seed(42)
    models = ["ResNet50", "VGG16", "MobileNetV2", "EfficientNet-B0"]
    accuracies = [0.945, 0.872, 0.918, 0.956]

with doc:
    doc @ "## Results"
    results = pd.DataFrame(
        {
            "Model": models,
            "Accuracy": [f"{a:.1%}" for a in accuracies],
        }
    )
    doc.table(results, show_index=False)

with doc:
    doc @ "## Analysis"
    best_model = models[np.argmax(accuracies)]
    doc.print(f"Best model: {best_model} ({max(accuracies):.1%})")

doc.flush()
```

The tables and figures used here pull optional dependencies. See [Installation](installation.md) for the extras (`tables`, `images`, `figures`, `yaml`).

## Claude Code integration

CMX ships a Claude Code plugin in the `.claude-plugin/` directory. When you work in this repository, Claude Code picks it up automatically and gains skills for CMX syntax, patterns, and components — so you can ask it to write scripts or explain behavior in natural language.

## Next steps

- [Markdown](markdown.md) — Add text with the `@`, `|`, and call forms.
- [Context managers](context.md) — Hide setup or skip blocks with `doc.hide` and `doc.skip`.
- [Configuration](configuration.md) — Control where Markdown and assets are written.
