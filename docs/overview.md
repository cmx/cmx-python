# Overview

**Questions**
- What is CMX?
- How do I create a document?
- What are the key patterns?

**Objectives**
- Understand the basic CMX workflow
- Learn the three essential methods: `config()`, `with doc:`, `flush()`
- Create your first document

## What is CMX?

CMX generates live documentation from Python scripts. Think of it as a Jupyter notebook where you control exactly what appears in the output.

```python
from cmx import doc

doc.config(filename="report.md")

with doc:
    doc.print("Hello, World!")

doc.flush()
```

This creates `report.md` containing both the code and its output.

## The Three-Step Pattern

Every CMX script follows this pattern:

### 1. Configure

Tell CMX where to write:

```python
doc.config(filename="output.md")
```

### 2. Capture

Use `with doc:` to mark code for documentation:

```python
with doc:
    # This code appears in the output
    result = 42
    doc.print(f"The answer is {result}")
```

Code outside `with doc:` blocks runs but doesn't appear in the document.

### 3. Flush

Write everything to disk:

```python
doc.flush()
```

## Complete Example

```python
from cmx import doc

doc.config(filename="analysis.md")

# Setup (hidden from output)
data = [10, 20, 30, 40, 50]
mean = sum(data) / len(data)

# Documentation (shown in output)
with doc:
    doc @ "# Analysis Results"
    doc.print(f"Dataset mean: {mean}")

doc.flush()
```

**Output (`analysis.md`):**
````markdown
# Analysis Results

```python
doc.print(f"Dataset mean: {mean}")
```

```
Dataset mean: 30.0
```
````

## Key Points

- Use `doc.config()` to set the output file
- Use `with doc:` to control what appears in documentation
- Use `doc.flush()` to write the file
- Code outside `with doc:` blocks is hidden

## Claude Code Integration

CMX includes a Claude Code plugin that provides AI assistance when working with CMX. The plugin helps you understand CMX syntax, patterns, and components through natural language interaction.

To use the CMX skills in Claude Code, the plugin is automatically detected from the `.claude-plugin/` directory when you work in this repository. The plugin provides two skills:

- **cmx-basics**: Quick start guide and basic usage patterns
- **cmx-components**: Detailed guide for tables, images, videos, YAML, and layouts

Simply mention CMX-related tasks in Claude Code, and the AI will have access to comprehensive CMX knowledge to help you write scripts, debug issues, and learn best practices.

## Next Steps

- [Installation](installation.md) - Set up CMX
- [Markdown](markdown.md) - Add text and headings
- [Printing](printing.md) - Add dynamic output
