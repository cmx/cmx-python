# Context managers

*Control what appears in your document using `with doc:`, `doc.hide`, and `doc.skip`.*

CMX gives you three context managers for deciding what lands in the rendered Markdown. `with doc:` captures and runs a block. `doc.hide` runs a block without showing it. `doc.skip` skips a block entirely.

## Capture and run a block — `with doc:`

A `with doc:` block captures its own source as a Python code fence, then runs it. The captured source and any `doc.print` output appear in the document, in order.

```python
from cmx import doc

doc.config(__file__)

with doc:
    data = [10, 20, 30, 40, 50]
    mean = sum(data) / len(data)
    doc.print(f"Mean: {mean}")

doc.flush()
```

The output shows the block's source followed by its printed result:

````markdown
```python
data = [10, 20, 30, 40, 50]
mean = sum(data) / len(data)
doc.print(f"Mean: {mean}")
```

```
Mean: 30.0
```
````

Code outside any `with doc:` block still runs — it just doesn't appear in the document. The block is what you show; the surrounding script is what you don't.

## Run code without showing it — `doc.hide`

Use `doc.hide` for setup you want executed but not displayed: imports, data loading, expensive computations, helper definitions. The body runs, its source is not captured, and any variables you define inside remain in scope afterward.

```python
with doc.hide:
    import numpy as np

    data = np.random.randn(1000)
    mean = data.mean()
    std = data.std()

with doc:
    doc @ "### Summary Statistics"
    doc.print(f"Mean: {mean:.4f}")
    doc.print(f"Std:  {std:.4f}")
```

The document shows only the second block — the statistics and their output — while `mean` and `std`, defined in the hidden block, are still available to use:

````markdown
```python
doc @ "### Summary Statistics"
doc.print(f"Mean: {mean:.4f}")
doc.print(f"Std:  {std:.4f}")
```

### Summary Statistics

```
Mean: 0.0390
Std:  0.9869
```
````

Because hidden variables persist, you can define a helper in one `doc.hide` block and call it from a later visible block.

```python
with doc.hide:
    def helper_function():
        return "computed without clutter"

    result = helper_function()

with doc:
    doc.print(result)
```

## Skip a block entirely — `doc.skip`

Use `doc.skip` to keep a block in your script without running it. Nothing inside executes, and nothing appears in the document. This is handy while iterating: park an expensive section behind `doc.skip` until you're ready for it.

```python
with doc.skip:
    expensive_computation()
    doc @ "This won't appear"
```

```{warning}
`doc.skip` skips execution using a frame-tracing trick. This can interfere with debuggers that rely on the same mechanism, such as PyCharm's pydev. Avoid `doc.skip` when stepping through code under a debugger.
```

## Next steps

- [Overview](overview.md) — The config → capture → flush workflow these blocks fit into.
- [Printing](printing.md) — Add computed output with `doc.print()` inside your blocks.
