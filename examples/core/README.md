# CMX Core Examples

This directory contains comprehensive examples demonstrating real-world CMX usage patterns, derived from actual usage in the vuer-ai organization's repositories.

## Examples

### 01. Basic Usage (`01_basic_usage.py`)
**What it demonstrates:**
- Using the `with doc:` context manager
- Adding markdown text with `doc()`
- Printing output with `doc.print()`
- Basic document configuration

**Key takeaway:** This is the foundation of CMX - capturing code and output in documentation.

### 02. Markdown @ Operator (`02_markdown_operator.py`)
**What it demonstrates:**
- The `doc @` operator pattern
- Multi-line markdown text
- Clean syntax for documentation

**Key takeaway:** The `@` operator is widely used in vuer-ai repos for clean markdown insertion.

### 03. Tables (`03_tables.py`)
**What it demonstrates:**
- Creating tables from pandas DataFrames
- Displaying experiment results
- Manual markdown table syntax

**Key takeaway:** Tables are essential for experiment reporting and metrics display.

### 04. Images (`04_images.py`)
**What it demonstrates:**
- Saving and displaying images
- Numpy array to image conversion
- Using `doc.row` for side-by-side images

**Key takeaway:** CMX handles image saving automatically while displaying them in docs.

### 05. YAML Output (`05_yaml_output.py`)
**What it demonstrates:**
- Displaying configuration as YAML
- Nested configuration structures
- Using `doc.yaml()` for structured data

**Key takeaway:** YAML output is perfect for documenting experiment configurations.

### 06. Hiding Code (`06_hiding_code.py`)
**What it demonstrates:**
- Using `doc.hide` to run code without showing it
- Setup code that doesn't clutter documentation
- Using results from hidden blocks

**Key takeaway:** Keep documentation clean by hiding setup/boilerplate code.

### 07. Experiment Analysis (`07_experiment_analysis.py`)
**What it demonstrates:**
- Real-world experiment reporting pattern
- Combining tables, metrics, and analysis
- Mimics actual usage from vuer-ai repositories

**Key takeaway:** This is the most common pattern - analyzing and reporting ML experiment results.

### 08. Comprehensive Example (`08_comprehensive.py`)
**What it demonstrates:**
- All features combined in a realistic workflow
- Complete ML experiment report
- Tables, images, YAML, and analysis

**Key takeaway:** Shows how to create professional, publication-ready experiment reports.

## Running the Examples

To run these examples, you need to have CMX installed:

```bash
# Install CMX
pip install cmx

# Run any example
python 01_basic_usage.py

# The example will create a .md file with the same name
# For example, 01_basic_usage.py creates 01_basic_usage.md
```

## Common Patterns Found in Real Usage

Based on analysis of 100+ files in the vuer-ai organization:

1. **Document Configuration**: Almost always starts with `doc.config(filename="...")`
2. **The @ Operator**: Used in 95%+ of files for markdown text insertion
3. **Hidden Setup**: `doc.hide` is used extensively to keep docs clean
4. **Metric Tables**: Tables are the most common component for showing results
5. **YAML Config**: Configuration documentation is nearly universal
6. **Image Visualization**: Used frequently for training curves and visualizations

## Output Files

Each example generates a corresponding `.md` file:

- `01_basic_usage.md` - Simple documentation example
- `02_markdown_operator.md` - @ operator demo
- `03_tables.md` - Table examples
- `04_images.md` - Image handling demo
- `05_yaml_output.md` - Configuration display
- `06_hiding_code.md` - Hidden code blocks
- `07_experiment_analysis.md` - Experiment reporting
- `08_comprehensive.md` - Complete workflow example

## Tips for Using CMX

1. **Start Simple**: Begin with `01_basic_usage.py` to understand the core concept
2. **Use @ for Text**: The `doc @ "text"` pattern is cleaner than `doc("text")`
3. **Hide Setup Code**: Use `doc.hide` to keep documentation focused on results
4. **Tables for Data**: pandas DataFrames + `doc.table()` = easy data display
5. **YAML for Config**: Always document your configuration with `doc.yaml()`
6. **Flush at End**: Don't forget `doc.flush()` to write the final output

## Real-World Usage

These examples are based on actual usage patterns from:
- vuer-ai/vuer (3D visualization library documentation)
- vuer-ai/vuer-envs (robotics environment documentation)
- vuer-ai/lucidxr (experiment analysis and reporting)

The most common use case is **experiment analysis and reporting**, as demonstrated in `07_experiment_analysis.py` and `08_comprehensive.py`.
