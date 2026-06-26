# CMX Basics Skill

This skill helps you understand and use CMX for creating live, interactive documentation from Python scripts.

## What is CMX?

CMX is a Python library that generates Markdown documentation directly from your Python scripts. It works like a Jupyter notebook, but lives inside plain `.py` files: you wrap code in `with doc:` to capture its source and output, add prose and rich blocks with the document API, and CMX writes it all to a `.md` file next to your script.

The default (and primary) backend is **Markdown**, with partial HTML rendering for some components (rows, videos). HTML and LaTeX backends are stubs — Markdown is the backend you use.

## Installation

```bash
pip install cmx
```

The core is dependency-free: `import cmx` pulls in zero third-party packages. Requires **Python 3.11+**. Richer blocks load their dependencies lazily — install only the extras you use:

| Install | Pulls | Enables |
|---|---|---|
| `pip install cmx` | nothing | core: text, `@`/`|`/call operators, `doc.print`, `doc.pre`, capture, flush |
| `pip install 'cmx[tables]'` | pandas | `doc.table`, `doc.csv` (default `github` format) |
| `pip install 'cmx[images]'` | pillow, numpy | array images: `doc.image` / `doc.figure` / `doc.video` |
| `pip install 'cmx[figures]'` | matplotlib | `doc.savefig` |
| `pip install 'cmx[yaml]'` | pyyaml | `doc.yaml` |
| `pip install 'cmx[all]'` | all of the above | everything |

Note: `tabulate` is **not** a runtime dependency. The default `github` table format renders through CMX's built-in pure-Python renderer (`cmx.backends.md_table`) and needs only pandas. `tabulate` is required only for alternate `format=` values (`pipe`, `grid`, ...).

## Basic Usage Pattern

```python
from cmx import doc

# Anchor output to this script: writes <script>.md next to the script.
doc.config(__file__)

# Use 'with doc:' to capture the block's source AND run it.
with doc:
    doc.print("Hello, World!")

    for i in range(5):
        doc.print(i, end=" ")

doc.flush()
```

## Key Concepts

### 1. The Global `doc` Object

Import and use the global document object:

```python
from cmx import doc
```

### 2. Configuration — `doc.config(__file__)`

The recommended call is `doc.config(__file__)`. It anchors output to the script you run:

- The `.md` lands **next to the script** (`report.py` → `report.md`).
- The **working directory** (`wd`) defaults to the script's folder, so the script produces the same output no matter where you launch Python from.

CMX decides what the argument means by its extension: a `.py` path is the **script**; anything else (or the `filename=` keyword) is treated as the explicit **output Markdown path**.

```python
doc.config(__file__)                  # script-relative: report.py -> report.md
doc.config("report.md")               # explicit output path (wd = its directory)
doc.config(filename="report.md")      # equivalent keyword form
doc.config(__file__, wd="/tmp/out")   # relocate everything under /tmp/out
```

On configure, CMX prints a green `File output at file://...` line you can click through to.

`doc.config(...)` returns `self`, so calls chain.

### 3. The `figdir` template — where assets land

Assets (images, figures, videos) go into a **figure directory** (`figdir`). It is a template string; `{fname}` expands to the Markdown file's name **without** its extension. When you omit `figdir`, the default is the per-document `"{fname}"` folder when the document's name is known (`doc.config(__file__)` / `doc.config(filename=...)`), and a shared `"figures"` directory otherwise (a bare `doc` / REPL with no resolved name).

```python
doc.config(__file__)                   # 04_images.py -> assets in 04_images/
doc.config(__file__, figdir="figures") # collect plots into a shared figures/
doc.config(__file__, figdir="assets")  # all assets in assets/
doc.config(__file__, figdir="")        # assets beside the .md, no subfolder
doc                                    # bare doc, no config -> assets in figures/
```

Read the resolved values back from `doc.filename` (the basename **with** extension, e.g. `report.md`) and `doc.figdir` (the name **without** extension, e.g. `report`).

### 4. Asset path resolution

When you call `doc.image` / `doc.figure` / `doc.video` / `doc.savefig`, CMX decides where `src` lives by one rule — **does the name contain a slash?**

| You pass | CMX stores | Why |
|---|---|---|
| `"random.png"` (bare name) | `figdir/random.png` | bare names go under `figdir` |
| `"sub/x.png"` (has a slash) | `sub/x.png` | explicit path wins, used as-is |

Links are written **relative to the `.md`**, and stored paths use forward slashes, so the document and its assets move together. Saving **creates directories automatically** (the default `on_save` hook), so you never pre-create asset folders.

### 5. Context Management

CMX gives you three context managers for deciding what lands in the document:

- `with doc:` — captures the block's source as a Python code fence **and runs it**. Source plus any `doc.print` output appear in document order.
- `with doc.hide:` — **runs** the body but does **not** show its source. Variables defined inside persist afterward. Use it for imports, data loading, helpers, expensive setup.
- `with doc.skip:` — does **not** run the body at all (nothing executes, nothing appears). Implemented via a frame-tracing trick, so it can interfere with debuggers such as PyCharm's pydev — avoid it while stepping through code under a debugger.

```python
with doc.hide:
    import numpy as np
    data = np.random.randn(1000)   # runs, hidden; `data` stays in scope

with doc:
    doc @ "### Summary"
    doc.print(f"Mean: {data.mean():.4f}")   # shown: source + output

with doc.skip:
    expensive_training()           # never runs while skipped
```

### 6. Output Methods

- `doc("text")`, `doc @ "text"`, `"text" | doc` — three equivalent forms to add a markdown text block (see Patterns below). `doc.md` is an alias for the call form.
- `doc.print(*args, sep=" ", end="\n")` — print values like the built-in `print` (also echoes to stdout).
- `doc.pre(text, lang=None)` — a raw code/preformatted block.
- `doc.table(df)` / `doc.csv(csv_string)` — tables.
- `doc.yaml(data)` — render a Python object as a YAML code block.
- `doc.image(arr, src=...)`, `doc.figure(...)`, `doc.savefig(key)`, `doc.video(frames, src=...)` — rich blocks (see the components skill).
- `doc.flush()` — render the accumulated blocks and append them to the `.md`.

### 7. Adding text — three forms and `end=`

```python
doc("# Title", end="\n")   # call form (end="\n" is the default)
doc @ "# Title"            # prefix @ operator
"# Title" | doc            # postfix | operator
```

All three append a text block and return `doc`, so they chain. Only the call form takes keywords like `end=`. Use `end=""` to keep the next block on the same line:

```python
doc("Status: ", end="")
doc("OK")                  # -> "Status: OK"
```

Text is dedented by default (`dedent=True`), so triple-quoted multi-line strings stay clean. The left-side pipe `doc | other` is not implemented and raises `NotImplementedError`; only `"text" | doc` works.

### 8. `doc.print` coalescing

Consecutive `doc.print` calls **merge into a single code block** — they don't each produce their own fence. A non-print block in between starts a fresh code block.

```python
with doc:
    doc.print("line 1")
    doc.print("line 2")     # joins the same code block as line 1
    doc("## A heading")     # breaks the run
    doc.print("line 3")     # starts a new code block
```

### 9. Multiple documents

```python
doc2 = doc.new(filename="second_doc.md")
```

## Common Patterns

### Pattern 1: Simple Output

```python
from cmx import doc

doc.config(__file__)

with doc:
    doc("# My Results")
    for i in range(10):
        doc.print(i, end=" ")

doc.flush()
```

### Pattern 2: Data Tables

```python
import pandas as pd
from cmx import doc

doc.config(__file__)

data = pd.DataFrame({"name": ["Alice", "Bob"], "score": [95, 87]})

doc("# Test Scores")
doc.table(data)
doc.flush()
```

### Pattern 3: Visualization

```python
import matplotlib.pyplot as plt
from cmx import doc

doc.config(__file__)

plt.plot([1, 2, 3, 4])
plt.ylabel("values")

doc("# My Plot")
doc.savefig("plot.png")   # bare name -> lands under figdir, dir auto-created
doc.flush()
```

### Pattern 4: Run-but-hide vs. skip during development

```python
from cmx import doc

doc.config(__file__)

# RUNS but its source is not shown; variables persist.
with doc.hide:
    result = expensive_setup()

# Does NOT run at all — parked until you're ready.
with doc.skip:
    even_more_expensive_training()

with doc:
    doc.print("Setup complete!", result)

doc.flush()
```

## Storage & integration hooks

CMX has **no logger and no storage framework**. Storage and remote integration happen through **lifecycle hooks** — methods on the document, each with a sensible local-disk default. Override them to send text and assets anywhere (S3/GCS, a dashboard, an API).

| Hook | Fires | Returns |
|---|---|---|
| `on_mount` | once, when `doc.config()` resolves output — the destination handshake | a `dest` (base key / URL / id), or `None` for local |
| `on_save` | per binary asset (image / video / figure) | the **link** written into `![]( )` |
| `on_flush` | per `doc.flush()` — a rendered text chunk | — |
| `on_close` | once, on `doc.close()` / `atexit` | — |
| `on_error` | per failed `with doc:` block (does not suppress the exception) | — |
| `on_block` | every block, with `kind ∈ {text, code, table, image, figure, video}` | — |
| `on_hide` / `on_skip` | when a `doc.hide` / `doc.skip` block is entered | — |

All hooks are **keyword-only** and accept `**kw`, so new fields never break an existing override. Set them two ways:

```python
# 1) Bind a function on the instance (no `self`) — quick, one-off:
doc.on_save = lambda *, data, path, **kw: my_upload(path, data)   # returns the link

# 2) Subclass CommonMark and override (methods have `self`) — reusable:
from cmx.backends.markdown import CommonMark

class S3Doc(CommonMark):
    def on_save(self, *, data, path, kind, dest, doc, **kw):
        s3_put(path, encode(data))
        return f"https://bucket.s3.amazonaws.com/{path}"
```

To keep the default behavior, capture-and-wrap it (`_save = doc.on_save; doc.on_save = lambda **kw: upload(**kw) or _save(**kw)`) or call `super().on_save(...)`. See the Hooks guide for the full lifecycle trace.

## Tips

1. **Use `doc.config(__file__)`** so output is script-relative and reproducible. If you skip `config` entirely, CMX lazily derives `script_name.md` from the calling frame.
2. **Pass bare asset names** and let `figdir` organize them; reach for a slashed path only when an asset must live somewhere specific.
3. **Call `doc.flush()`** to write the accumulated blocks. `with doc:` flushes automatically on exit; `doc.close()` (and `atexit`) finalize once.

## When to Use CMX

- Creating documentation that stays in sync with code
- Logging experiment results with code provenance
- Building interactive tutorials
- Generating reports from data-analysis scripts
- Replacing Jupyter notebooks with plain Python scripts

## Learn More

- Full documentation: https://cmx-python.readthedocs.io
- API Reference: https://cmx-python.readthedocs.io/en/latest/api/
