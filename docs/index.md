# CMX

Generate live Markdown documentation from Python scripts — you choose exactly what appears.

CMX runs your script and captures the parts you mark, turning code and its output into a Markdown file. It works like a notebook, but you control what shows up: source, printed results, tables, images, and more. The core has zero third-party dependencies; richer blocks pull in small, opt-in extras.

## Quick example

Configure an output file, capture a block of code, then write it to disk. Create a file called `report.py`:

```python
from cmx import doc

doc.config(__file__)

with doc:
    doc @ "# Daily Report"
    total = sum(range(100))
    doc.print(f"Sum of 0-99: {total}")

doc.flush()
```

Run it with `python report.py`. CMX writes `report.md` next to the script:

````markdown
# Daily Report

```python
total = sum(range(100))
doc.print(f"Sum of 0-99: {total}")
```

```
Sum of 0-99: 4950
```
````

The `with doc:` block captures its own source as a code fence and runs it; `doc.print` echoes to your terminal and appends the output. Code outside a `with doc:` block still runs — it just doesn't appear in the document.

## Features

- **Selective output.** Only code inside `with doc:` shows up. Use `doc.hide` to run setup without showing it, and `doc.skip` to keep a block in the document without running it. See [Context managers](context.md).
- **Zero-dependency core.** `import cmx` pulls in no third-party packages. Text, operators, `doc.print`, `doc.pre`, code capture, and `doc.flush` all work on a bare install.
- **Opt-in extras.** Add only what you use: `cmx[tables]` for DataFrames, `cmx[images]` for arrays and figures, `cmx[yaml]` for config blocks, or `cmx[all]`. See [Installation](installation.md).
- **Rich blocks.** Render pandas DataFrames and CSV as [tables](tables.md), numpy arrays and files as [images](images.md), and dictionaries as [YAML](yaml.md).
- **Managed output paths.** `doc.config(__file__)` writes Markdown next to your script and stores assets in a per-file folder. See [Configuration](configuration.md).

```{toctree}
:maxdepth: 1
:caption: Getting Started

overview
installation
configuration
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
:caption: Integrations

hooks
```

```{toctree}
:maxdepth: 1
:caption: Reference

api/index
development
CHANGE_LOG
```

## Next steps

- [Get started](overview.md) — learn the config → capture → flush workflow.
- [Installation](installation.md) — install the core and pick the extras you need.
- [Configuration](configuration.md) — control where Markdown and assets are written.

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
