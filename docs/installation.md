# Installation

Install CMX and verify it works.

## Requirements

CMX requires Python 3.11 or later.

## Install the core

```bash
pip install cmx
```

The core is dependency-free. `import cmx` pulls in zero third-party packages, so you get text, the `@`/`|`/call operators, `doc.print`, `doc.pre`, code capture, and `doc.flush` with nothing else installed.

## Optional features

Richer blocks load their dependencies lazily. Install only the extras you use, or `cmx[all]` for everything.

| Install | Pulls | Enables |
|---|---|---|
| `pip install cmx` | nothing | core: text, operators, `print`, `pre`, capture, flush |
| `pip install 'cmx[tables]'` | pandas | `doc.table`, `doc.csv` (github format) |
| `pip install 'cmx[images]'` | pillow, numpy | array images, `doc.image`/`figure`/`video` |
| `pip install 'cmx[figures]'` | matplotlib | `doc.savefig` |
| `pip install 'cmx[yaml]'` | pyyaml | `doc.yaml` |
| `pip install 'cmx[all]'` | all of the above | everything |

:::{note}
The default `github` table format is rendered by CMX's own pure-Python renderer, so `cmx[tables]` needs only pandas. `tabulate` is a development-only dependency, required at runtime only for alternate `format=` values like `pipe` or `grid`.
:::

See [Tables](tables.md), [Images](images.md), and [YAML](yaml.md) for what each extra unlocks.

## Verify

Create a file called `check.py`:

```python
from cmx import doc

doc.config(__file__)

with doc:
    doc @ "# Installation check"
    doc.print("CMX is working!")

doc.flush()
```

Run it:

```bash
python check.py
```

CMX prints a green `File output at file://...` line and writes `check.md` next to your script:

````markdown
# Installation check

```python
doc.print("CMX is working!")
```

```
CMX is working!
```
````

`doc.config(__file__)` writes the Markdown beside the script and roots assets in the script's directory. See [Configuration](configuration.md) for output and figure paths.

## Next steps

- [Overview](overview.md) — learn the config, capture, flush workflow.
- [Configuration](configuration.md) — control where Markdown and assets are written.
- [Tables](tables.md) — render DataFrames and CSV with `cmx[tables]`.
- [Images](images.md) — display arrays and files with `cmx[images]`.
