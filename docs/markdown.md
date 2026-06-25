# Adding text

Add Markdown text to a document with the `@`, `|`, and call forms.

Every line of prose in a CMX document is a text block. You append one by handing a string to `doc`. Start with the example, then pick the form that reads best.

```python
from cmx import doc

doc.config(__file__)

doc @ "# Experiment Report"
doc @ "Training finished. Results follow."

doc.flush()
```

```md
# Experiment Report
Training finished. Results follow.
```

## The three equivalent forms

There are three ways to append a text block. They do the same thing — append a `Text` block and return `doc` — so you can chain further calls off any of them.

```python
doc("# Title")        # call form
doc @ "# Title"       # prefix @ operator
"# Title" | doc       # postfix | operator
```

A tuple spreads into one block per item:

```python
doc @ ("First paragraph.", "Second paragraph.")
```

:::{warning}
The pipe only works with the string on the left: `"text" | doc`. The left-side form `doc | other` raises `NotImplementedError`.
:::

## Multi-line text and dedent

Use a triple-quoted string for multi-line content. Text is dedented by default (`dedent=True`), so the common leading indentation is stripped and indented source stays clean in the output.

```python
with doc:
    doc @ """
    ## Results

    The model converged after 12 epochs.

    - Accuracy: 0.97
    - Loss: 0.08
    """
```

```md
## Results

The model converged after 12 epochs.

- Accuracy: 0.97
- Loss: 0.08
```

The leading spaces from the source indentation are gone, but the blank lines and list structure are preserved.

## Controlling line endings with `end=`

Each text block ends with a single newline by default (`end="\n"`). Pass `end=` on the call form to change it. Only the trailing run of newlines is replaced — newlines inside the block are left alone.

Use `end=""` to keep the next block on the same line:

```python
doc("Status: ")
doc("OK")
```

```md
Status:
OK
```

With `end=""` on the first block, the two join:

```python
doc("Status: ", end="")
doc("OK")
```

```md
Status: OK
```

Because only the trailing newlines change, a multi-line block keeps its internal structure while you control just the final separator.

:::{note}
`end=` is a keyword argument, so it is available on the call form `doc("...", end="...")`. The `@` and `|` operators take a single value and use the default ending.
:::

## When to use each form

All three forms are functionally identical; choose for readability.

| Form | Reads best for |
|---|---|
| `doc("...")` | Passing arguments such as `end=`; explicit, lints cleanly. |
| `doc @ "..."` | Quick prose where the document leads the line. |
| `"..." | doc` | A line that reads left-to-right like a Unix pipe. |

Be consistent within a file. Reach for the call form whenever you need a keyword argument, since `@` and `|` accept only the text.

## Inside `with doc:`

All three forms work inside a [capture block](context.md). The captured source and any text you append appear in document order, interleaved with [`doc.print()`](printing.md) output.

```python
with doc:
    doc @ "## Summary"
    "Run completed without errors." | doc
    doc.print(f"Elapsed: {elapsed:.1f}s")
```

## Next steps

- [Printing](printing.md) — Add computed output with `doc.print()`.
- [Context managers](context.md) — Control what appears using `with doc:`, `doc.hide`, and `doc.skip`.
