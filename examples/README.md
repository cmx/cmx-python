# CMX Examples

This directory contains comprehensive examples demonstrating CMX usage patterns based on real-world applications from the vuer-ai organization.

## Directory Structure

```
examples/
├── core/              # Core features and common patterns (NEW! START HERE)
│   ├── 01_basic_usage.py
│   ├── 02_markdown_operator.py
│   ├── 03_tables.py
│   ├── 04_images.py
│   ├── 05_yaml_output.py
│   ├── 06_hiding_code.py
│   ├── 07_experiment_analysis.py
│   ├── 08_comprehensive.py
│   └── README.md
├── three/             # 3D visualization examples
└── old_demos/         # Legacy examples
```

## Quick Start

### Running Examples

```bash
# Install CMX
pip install cmx

# Run any example
cd examples/core
python 01_basic_usage.py

# The output will be in the corresponding .md file
cat 01_basic_usage.md
```

## Core Examples (Recommended Starting Point)

The `core/` directory contains 8 comprehensive examples demonstrating real-world usage patterns:

### Beginner Examples

1. **[01_basic_usage.py](core/01_basic_usage.py)** - Start here!
   - Using `with doc:` context manager
   - Adding markdown text
   - Printing output
   - Basic configuration

2. **[02_markdown_operator.py](core/02_markdown_operator.py)** - The `@` operator
   - Clean syntax for markdown
   - Multi-line text handling
   - Most commonly used pattern in real projects

### Feature-Specific Examples

3. **[03_tables.py](core/03_tables.py)** - Displaying data
   - pandas DataFrame tables
   - Experiment results
   - Manual markdown tables

4. **[04_images.py](core/04_images.py)** - Image handling
   - Saving and displaying images
   - Multiple images in rows
   - Automatic file management

   See also **[10_matplotlib_figures.py](core/10_matplotlib_figures.py)** - Matplotlib figures
   - Saving plots with `doc.savefig` (dpi, bbox_inches, transparent)
   - Building figure tables with `table.figure_row()`

5. **[05_yaml_output.py](core/05_yaml_output.py)** - Configuration documentation
   - YAML output
   - Nested configurations
   - Experiment parameters

6. **[06_hiding_code.py](core/06_hiding_code.py)** - Clean documentation
   - Using `doc.hide`
   - Hiding setup code
   - Focusing on results

### Real-World Workflows

7. **[07_experiment_analysis.py](core/07_experiment_analysis.py)** - Typical ML workflow
   - Experiment reporting pattern
   - Metrics and analysis
   - Based on actual vuer-ai usage

8. **[08_comprehensive.py](core/08_comprehensive.py)** - Complete example
   - All features combined
   - Publication-ready reports
   - Professional experiment documentation

## Usage Patterns from Real Projects

Based on analysis of 100+ files from vuer-ai repositories:

### Most Common Pattern: Experiment Analysis

```python
from cmx import doc
import pandas as pd

doc.config(filename="report.md")

doc @ "# Experiment Report"

with doc.hide:
    # Load data without cluttering docs
    results = load_experiment_data()

with doc:
    doc @ "## Configuration"
    doc.yaml(config)

with doc:
    doc @ "## Results"
    doc.table(pd.DataFrame(results))

doc.flush()
```

### The @ Operator (95%+ adoption)

The `@` operator is the preferred way to add markdown in real projects:

```python
doc @ """
# Title

Multi-line markdown content goes here.
"""

doc @ "## Single line"
```

### Hidden Setup Code

Almost all real-world examples use `doc.hide` to keep documentation clean:

```python
with doc.hide:
    import numpy as np
    import matplotlib.pyplot as plt
    # Setup code here
    data = expensive_computation()

with doc:
    # Show only the results
    doc @ "## Results"
    doc.print(f"Mean: {data.mean():.4f}")
```

## Common Use Cases

### 1. ML Experiment Reporting
**Files**: `07_experiment_analysis.py`, `08_comprehensive.py`

Document machine learning experiments with metrics, configurations, and analysis.

### 2. Robotics Documentation
**Common in**: vuer-ai/vuer-envs, vuer-ai/lucidxr

Document robot control experiments, success rates, and trajectories.

### 3. 3D Visualization Documentation
**Files**: `three/` directory

Document 3D scenes, camera positions, and rendering setups.

### 4. Configuration Documentation
**Files**: `05_yaml_output.py`

Document system configurations, hyperparameters, and experiment settings.

### 5. Data Analysis Reports
**Files**: `03_tables.py`, `07_experiment_analysis.py`

Create analysis reports with tables, statistics, and visualizations.

## Tips for Success

1. **Start Simple**: Begin with `core/01_basic_usage.py`
2. **Use the @ Operator**: It's cleaner and more readable
3. **Hide Setup Code**: Keep docs focused on results
4. **Always Flush**: Don't forget `doc.flush()` at the end
5. **Structure Your Reports**: Use sections with `doc @ "## Section"`
6. **Tables for Data**: Use pandas + `doc.table()` for structured data
7. **YAML for Config**: Always document your configuration

## Real-World Projects Using CMX

These examples are based on actual usage from:

- **vuer-ai/vuer** - 3D visualization library (40+ documentation files)
- **vuer-ai/vuer-envs** - Robotics environments (30+ experiment reports)
- **vuer-ai/lucidxr** - Robot learning experiments (20+ analysis files)
- **vuer-ai/vuer_mjcf** - MuJoCo integration (10+ tutorial files)

## Legacy Examples

### 3D Visualization (three/)

Examples showing 3D scene setup and visualization with Tassa:
- Camera frustums
- Robot animations
- Video streaming
- Point clouds

### Old Demos (old_demos/)

Older examples that may use deprecated APIs but still demonstrate core concepts.

## Getting Help

- **Documentation**: https://cmx.readthedocs.io
- **Quick Start**: https://cmx.readthedocs.io/en/latest/overview.html
- **API Reference**: https://cmx.readthedocs.io/en/latest/api/
- **Issues**: https://github.com/cmx/cmx-python/issues

## Contributing Examples

When adding new examples:
1. Include clear docstrings explaining what the example demonstrates
2. Add example description to this README
3. Test the example works with latest cmx version
4. Consider adding to the `core/` directory if it demonstrates a common pattern
5. Include expected output or generated .md file
