# CMX Documentation

> Generate live documentation from Python scripts

**CMX** turns your Python scripts into interactive documentation. It works like a Jupyter notebook but gives you complete control over what appears in the output.

## Quick Example

```python
from cmx import doc

doc.config(filename="output.md")

with doc:
    doc @ "# My Analysis"
    doc.print("Results:", 42)

doc.flush()
```

## Features

- **Selective Output**: Only code in `with doc:` blocks appears in documentation
- **Multiple Formats**: Markdown, HTML, and LaTeX backends
- **Rich Components**: Tables, images, YAML, and more
- **File Logging**: Built-in support for saving images and videos

```{toctree}
:maxdepth: 1
:caption: Getting Started

overview
installation
```

```{toctree}
:maxdepth: 1
:caption: Core Concepts

markdown
printing
context
```

```{toctree}
:maxdepth: 1
:caption: Components

tables
images
figures
yaml
```

```{toctree}
:maxdepth: 1
:caption: Reference

api/index
development
CHANGE_LOG
```

## Real-World Example

CMX is used extensively in the vuer-ai organization for documenting robotics and ML experiments:

```python
from cmx import doc
import pandas as pd

doc.config(filename="experiment.md")

doc @ "# Experiment Report"

# Hidden setup
with doc.hide:
    results = load_experiment_results()

# Show configuration
with doc:
    doc @ "## Configuration"
    doc.yaml({'batch_size': 64, 'learning_rate': 0.001})

# Show results
with doc:
    doc @ "## Results"
    doc.table(pd.DataFrame(results))

doc.flush()
```

## Indices and Tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
