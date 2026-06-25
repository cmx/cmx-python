# Printing

Add dynamic, computed output to a document with `doc.print()`.

## Basic printing

`doc.print()` works like Python's built-in `print()`. It echoes to your terminal *and* appends the same text to the document as a code block.

```python
with doc:
    doc.print("Hello, World!")
    doc.print("The answer is", 42)
```

Generated Markdown:

````md
```
Hello, World!
The answer is 42
```
````

You pass any number of positional arguments, and each one is converted with `str()`. Multiple arguments are joined with a space by default.

## Format strings

Use f-strings to print computed values. This is the common case: capture a result inside a `with doc:` block and report it.

```python
with doc:
    total = sum([1, 2, 3, 4, 5])
    doc.print(f"Sum: {total}")
    doc.print(f"Mean: {total / 5:.2f}")
```

Generated Markdown:

````md
```
Sum: 15
Mean: 3.00
```
````

## Controlling `sep` and `end`

`doc.print(*args, sep=" ", end="\n")` accepts the same `sep` and `end` keywords as the built-in.

`sep` sets the string placed between arguments. `end` sets the string appended after the last argument.

```python
with doc:
    doc.print("a", "b", "c", sep=" | ")
    doc.print("no newline here", end="")
    doc.print(" — same line")
```

Generated Markdown:

````md
```
a | b | c
no newline here — same line
```
````

## Coalescing consecutive prints

Consecutive `doc.print()` calls merge into a **single** code block. CMX appends each call's text to the previous `Print` block instead of opening a new fence, so a run of prints reads as one continuous output stream.

This is why a loop produces one tidy block. Set `end=" "` to build a single line:

```python
with doc:
    for i in range(5):
        doc.print(i, end=" ")
```

Generated Markdown:

````md
```
0 1 2 3 4 
```
````

The merge only spans an unbroken run of prints. Any other content between them — a `doc @` line, a table, an image — closes the current block, and the next `doc.print()` starts a fresh one.

```python
with doc:
    doc.print("first block")
    doc @ "Some markdown in between."
    doc.print("second block")
```

Generated Markdown:

````md
```
first block
```
Some markdown in between.
```
second block
```
````

:::{note}
Coalescing also applies across separate `with doc:` blocks, as long as no other element is appended between the prints.
:::

## Print vs `doc @`

`doc.print()` and the [`doc @` operator](markdown.md) append different kinds of content. Reach for `doc.print()` when the value is computed at runtime, and `doc @` when the text is Markdown you author directly.

| Use `doc.print()` for | Use `doc @` for |
|---|---|
| Computed values and variables | Headings and prose |
| Loop and iteration output | Static Markdown text |
| Anything you'd send to `print()` | Lists, links, formatting |

`doc.print()` always renders inside a fenced code block — literal, monospaced text. `doc @` renders as live Markdown. Combine them to interleave narrative with results:

```python
with doc:
    doc @ "## Results"
    for i in range(3):
        doc.print(f"Trial {i + 1}: {results[i]}")
```

The heading renders as Markdown; the three trials coalesce into one code block beneath it.

## Next steps

- [Markdown](markdown.md) — Add headings and prose with `doc @`, `|`, and the call form.
- [Context](context.md) — Control what runs and what shows with `with doc:`, `doc.hide`, and `doc.skip`.
