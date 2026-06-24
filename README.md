# CMX - REPL with Python Scripts via Live Documents

[![PyPI version](https://badge.fury.io/py/cmx.svg)](https://badge.fury.io/py/cmx)
[![Documentation Status](https://readthedocs.org/projects/cmx-python/badge/?version=latest)](https://cmx-python.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Create live, interactive documentation directly from your Python scripts.

**CMX** is a Python library that enables REPL-style documentation generation. It works like Jupyter notebooks but integrates directly into your Python scripts using context managers. Only code you include in a `with doc:` block appears in the output.

## Features

- **Live Documentation**: Generate markdown/HTML/LaTeX from Python code execution
- **Multiple Backends**: Markdown (GitHub-compatible), HTML, and LaTeX output
- **Rich Components**: Tables, images, videos, figures, YAML output
- **Context Management**: Use `with doc:` blocks to control what appears
- **File Logging**: Built-in support for saving images, videos, and data
- **Layout Control**: Arrange content horizontally with row layouts

## Quick Start

Install from PyPI:

```bash
pip install cmx
```

Create your first live document:

```python
from cmx import doc

# Configure output (optional - auto-detects from script name)
doc.config(filename="output.md")

# Everything in 'with doc:' blocks appears in output
with doc:
    doc("# Hello, CMX!")

    for i in range(10):
        doc.print(i, end=' ')
```

Output in `output.md`:
```python
for i in range(10):
    doc.print(i, end=' ')
```
```
0 1 2 3 4 5 6 7 8 9
```

## Documentation

Full documentation is available at: **https://cmx-python.readthedocs.io**

- [Quick Start Guide](https://cmx-python.readthedocs.io/en/latest/overview.html)
- [Development Guide](https://cmx-python.readthedocs.io/en/latest/development.html)
- [API Reference](https://cmx-python.readthedocs.io/en/latest/api/)

## Usage Examples

### Basic Usage

```python
from cmx import doc

doc.config(filename="output.md")

with doc:
    doc("# Hello, CMX!")

    for i in range(10):
        doc.print(i, end=' ')

doc.flush()
```

### The @ Operator

The `@` operator provides clean syntax for adding markdown (used extensively in vuer-ai repositories):

```python
doc @ """
# Experiment Report

This is a clean way to add markdown content.
"""

with doc:
    doc @ "## Results"
    results = [1, 2, 3, 4, 5]
    doc.print(f"Total: {sum(results)}")
```

### Tables

Display experiment results and metrics:

```python
import pandas as pd

data = pd.DataFrame({
    'Model': ['ResNet50', 'VGG16', 'MobileNet'],
    'Accuracy': [0.95, 0.87, 0.92],
    'Parameters': ['25.6M', '138M', '4.2M']
})

with doc:
    doc.table(data)
```

### Images

```python
import numpy as np

image = np.random.rand(100, 100, 3)

with doc:
    doc.image(image, src="figures/random.png")
```

### YAML Configuration

```python
config = {
    'model': 'ResNet50',
    'batch_size': 32,
    'learning_rate': 0.001,
    'optimizer': 'Adam'
}

with doc:
    doc.yaml(config)
```

### Hiding Setup Code

Keep documentation clean by hiding boilerplate:

```python
with doc.hide:
    # This code runs but doesn't appear in output
    import numpy as np
    data = load_experiment_data()

with doc:
    doc @ "## Analysis Results"
    doc.print(f"Mean: {data.mean():.4f}")
```

### Complete Workflow Example

```python
from cmx import doc
import pandas as pd

doc.config(filename="experiment_report.md")

doc @ """
# Experiment Report
**Date**: 2024-01-15
"""

# Hidden setup
with doc.hide:
    results = load_results()

# Configuration
with doc:
    doc @ "## Configuration"
    doc.yaml({'model': 'ResNet50', 'epochs': 100})

# Results table
with doc:
    doc @ "## Results"
    df = pd.DataFrame(results)
    doc.table(df)

# Analysis
with doc:
    doc @ "## Analysis"
    best = df['accuracy'].max()
    doc.print(f"Best accuracy: {best:.2%}")

doc.flush()
```

More examples in the [`examples/core/`](examples/core/) directory, including:
- Basic usage patterns
- Tables and data display
- Image handling
- YAML configuration output
- Experiment analysis workflows
- Complete reporting examples

See [`examples/core/README.md`](examples/core/README.md) for detailed explanations.

## Development

Set up a development environment:

```bash
# Clone the repository
git clone https://github.com/cmx/cmx-python.git
cd cmx-python

# Install in development mode
make dev

# Run tests
make test

# Preview documentation
make preview
```

## Claude Code Skills

CMX includes Claude Code skills for enhanced assistance when working with the library. The skills are located in `.claude-plugin/` and provide guidance on:

- Basic usage patterns
- Component usage (tables, images, videos, etc.)
- Advanced features and best practices

## Publishing

Build and publish to PyPI:

```bash
# Update VERSION file
echo "0.0.47" > VERSION

# Build and publish
make publish
```

## Project Structure

```
cmx-python/
├── src/cmx/              # Main package source
├── docs/                 # Sphinx documentation
├── examples/             # Example scripts
│   ├── three/           # 3D visualization examples
│   └── old_demos/       # Legacy examples
├── tests/               # Test suite
├── .claude-plugin/      # Claude Code skills
├── pyproject.toml       # Project configuration
├── Makefile            # Build automation
└── README.md           # This file
```

## Contributing

Contributions are welcome! Please see the [Development Guide](https://cmx-python.readthedocs.io/en/latest/development.html) for details.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

Ge Yang (ge.ike.yang@gmail.com)

## Links

- **Documentation**: https://cmx-python.readthedocs.io
- **GitHub**: https://github.com/cmx/cmx-python
- **PyPI**: https://pypi.org/project/cmx/
- **Issues**: https://github.com/cmx/cmx-python/issues
