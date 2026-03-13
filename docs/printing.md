# Printing Output

**Questions**
- How do I add dynamic output to documents?
- What's the difference between `doc.print()` and `doc @`?
- Can I use format strings?

**Objectives**
- Use `doc.print()` for dynamic content
- Format output with standard print parameters
- Understand when to use printing vs markdown

## Basic Printing

`doc.print()` works like Python's built-in `print()`:

```python
with doc:
    doc.print("Hello, World!")
    doc.print("The answer is", 42)
```

Output:
```
Hello, World!
The answer is 42
```

## Format Strings

Perfect for dynamic content:

```python
with doc:
    total = sum([1, 2, 3, 4, 5])
    doc.print(f"Sum: {total}")
    doc.print(f"Mean: {total / 5:.2f}")
```

Output:
```
Sum: 15
Mean: 3.00
```

## Print Parameters

All standard parameters work:

```python
with doc:
    # Custom separator
    doc.print("a", "b", "c", sep=" | ")  # Output: a | b | c

    # Custom ending
    for i in range(5):
        doc.print(i, end=' ')  # Output: 0 1 2 3 4
```

## When to Use

**Use `doc.print()` for:**
- Loop output
- Calculated values
- Dynamic content

**Use `doc @` for:**
- Markdown text
- Headings
- Static content

```python
with doc:
    doc @ "## Results"  # Static heading

    for i in range(3):
        doc.print(f"Trial {i+1}: {results[i]}")  # Dynamic output
```

## Key Points

- `doc.print()` adds dynamic output to documentation
- Supports all standard `print()` parameters (sep, end, etc.)
- Use for loops, calculations, and variable content
- Combine with `doc @` for structured documents

## Next Steps

- [Markdown](markdown.md) - Add headings and text
- [Tables](tables.md) - Display structured data
- [Context](context.md) - Control code visibility
