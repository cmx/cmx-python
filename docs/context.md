# Context Managers

**Questions**
- How do I control what appears in the documentation?
- How do I hide setup code?
- How do I skip sections during development?

**Objectives**
- Learn to use `with doc:` for documentation
- Use `doc.hide` to hide setup code
- Use `doc.skip` to skip sections

## The `with doc:` Pattern

Only code inside `with doc:` blocks appears in the output:

```python
from cmx import doc

doc.config(filename="report.md")

# This code runs but doesn't appear
data = [10, 20, 30, 40, 50]
mean = sum(data) / len(data)

# This code appears in the output
with doc:
    doc @ "# Analysis"
    doc.print(f"Mean: {mean}")

doc.flush()
```

## Hiding Setup Code

Use `doc.hide` to run code without showing it:

```python
with doc.hide:
    # Load data, imports, expensive computations
    import numpy as np
    data = np.random.randn(1000)
    mean = data.mean()
    std = data.std()

with doc:
    doc @ "## Results"
    doc.print(f"Mean: {mean:.4f}")
    doc.print(f"Std:  {std:.4f}")
```

The output shows only the results, not the setup.

## Skipping Sections

Use `doc.skip` to skip sections during development:

```python
with doc.skip:
    # This code doesn't run at all
    expensive_computation()
    doc @ "This won't appear"
```

This is useful when iterating on specific parts of a document.

## Key Points

- Use `with doc:` to include code in output
- Use `doc.hide` to run code without showing it
- Use `doc.skip` to skip execution entirely
- Code outside all blocks runs but doesn't appear

## Next Steps

- [Markdown](markdown.md) - Add text with @ and | operators
- [Tables](tables.md) - Display data
- [Images](images.md) - Add visualizations
