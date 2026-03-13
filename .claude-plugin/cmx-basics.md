# CMX Basics Skill

This skill helps you understand and use CMX for creating live, interactive documentation from Python scripts.

## What is CMX?

CMX is a Python library that enables REPL-style documentation generation. It works like a Jupyter notebook but integrates directly into your Python scripts using context managers.

## Basic Usage Pattern

```python
from cmx import doc

# Configure output (optional - auto-detects based on script name)
doc.config(filename="output.md")

# Use 'with doc:' to capture code and output
with doc:
    doc.print("Hello, World!")

    for i in range(5):
        doc.print(i, end=' ')
```

## Key Concepts

### 1. The Global `doc` Object

Import and use the global document object:
```python
from cmx import doc
```

### 2. Context Management

Code inside `with doc:` blocks is captured and shown in output:
```python
with doc:
    # This code appears in the markdown output
    result = 42
    doc.print(f"The answer is {result}")
```

### 3. Output Methods

- `doc.print(*args, sep=" ", end="\n")` - Print values (like built-in print)
- `doc("text")` or `doc.md("text")` - Add markdown text
- `doc.table(dataframe)` - Display tables
- `doc.image(array, src="path.png")` - Save and display images
- `doc.yaml(data)` - Display structured data as YAML

### 4. File Configuration

Control where output is written:
```python
# Explicit filename
doc.config(filename="results.md")

# Auto-detect from script name (example.py → example.md)
# (This happens automatically if you don't call config)

# Create multiple documents
doc2 = doc.new(filename="second_doc.md")
```

## Common Patterns

### Pattern 1: Simple Output

```python
from cmx import doc

with doc:
    doc("# My Results")
    for i in range(10):
        doc.print(i, end=' ')
```

### Pattern 2: Data Tables

```python
import pandas as pd
from cmx import doc

data = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'score': [95, 87]
})

with doc:
    doc("# Test Scores")
    doc.table(data)
```

### Pattern 3: Visualization

```python
import numpy as np
import matplotlib.pyplot as plt
from cmx import doc

# Create a plot
plt.plot([1, 2, 3, 4])
plt.ylabel('values')

with doc:
    doc("# My Plot")
    doc.savefig("figures/plot.png")
```

### Pattern 4: Development with Skip

```python
from cmx import doc

# Skip expensive computations during development
with doc.skip:
    # This runs but doesn't appear in output
    expensive_training()

with doc:
    # This appears in output
    doc.print("Training complete!")
```

## Tips

1. **Auto-detection**: If you don't call `doc.config()`, CMX automatically creates `script_name.md` next to your script
2. **Remote logging**: Integrate with ML-Logger for remote document storage
3. **Multiple backends**: CMX supports Markdown (default), HTML, and LaTeX output
4. **Layout**: Use `doc.row` context for horizontal layouts (HTML only)

## When to Use CMX

- Creating documentation that stays in sync with code
- Logging experiment results with code provenance
- Building interactive tutorials
- Generating reports from data analysis scripts
- Replacing Jupyter notebooks with plain Python scripts

## Installation

```bash
pip install cmx
```

## Learn More

- Full documentation: https://cmx-python.readthedocs.io
- Examples: Check the `examples/` directory in the repository
- API Reference: https://cmx-python.readthedocs.io/en/latest/api/
