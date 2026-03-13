# Adding Markdown Text

**Questions**
- How do I add markdown text to documents?
- What's the difference between @ and | operators?
- When should I use each operator?

**Objectives**
- Learn the @ operator for adding markdown
- Learn the | operator for adding markdown
- Understand when to use each

## The @ Operator

The `@` operator adds markdown text with prefix syntax:

```python
from cmx import doc

doc.config(filename="output.md")

doc @ "# My Document"
doc @ "This is a paragraph."

doc.flush()
```

Use `@` for multi-line markdown:

```python
doc @ """
# Experiment Report

This is a longer section with multiple paragraphs.

Results are shown below.
"""
```

## The | Operator

The `|` operator adds markdown text with postfix syntax:

```python
"# My Document" | doc
"This is a paragraph." | doc
```

This reads left-to-right like a pipeline.

## When to Use Each

**Use `@` when:**
- Adding multi-line content
- Markdown comes before code
- You prefer doc-first syntax

**Use `|` when:**
- Adding single-line content
- Content reads like a pipeline
- You prefer data-first syntax

## Inside Context Blocks

Both operators work inside `with doc:` blocks:

```python
with doc:
    doc @ "## Results"
    "The experiment completed successfully." | doc
    doc.print(f"Accuracy: {accuracy:.2%}")
```

## Key Points

- Use `doc @ "text"` for prefix syntax
- Use `"text" | doc` for postfix syntax
- Both operators work the same way
- Choose based on readability

## Next Steps

- [Context Managers](context.md) - Control what appears in output
- [Tables](tables.md) - Display structured data
