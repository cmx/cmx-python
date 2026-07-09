# CMX

[![PyPI version](https://badge.fury.io/py/cmx.svg)](https://badge.fury.io/py/cmx)
[![Documentation Status](https://readthedocs.org/projects/cmx-python/badge/?version=latest)](https://cmx-python.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generate live Markdown documentation from Python scripts — you choose exactly what appears.

CMX runs your script and captures the parts you mark, turning code and its output into a Markdown file. It works like a notebook, but you control what shows up: source, printed results, tables, images, and more. The core has zero third-party dependencies; richer blocks pull in small, opt-in extras.

## Installation

Install the core from PyPI. It needs no third-party packages:

```bash
pip install cmx
```

Add extras only for the features you use:

| Install | Pulls in | Enables |
|---|---|---|
| `pip install cmx` | nothing | text, operators, `doc.print`, `doc.pre`, capture, flush |
| `pip install 'cmx[tables]'` | pandas | `doc.table`, `doc.csv` |
| `pip install 'cmx[images]'` | pillow, numpy | array images, `doc.image` / `figure` / `video` |
| `pip install 'cmx[figures]'` | matplotlib | `doc.savefig` |
| `pip install 'cmx[yaml]'` | pyyaml | `doc.yaml` |
| `pip install 'cmx[all]'` | all of the above | everything |

CMX requires Python 3.11 or later.

## Quick start

Configure an output file, capture a block of code, then write it to disk. Create `report.py`:

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

## Common patterns

**Add text three equivalent ways.** Each appends a text block and returns `doc`:

```python
doc("## Results", end="\n")   # call form (end="\n" is the default)
doc @ "## Results"         # prefix @ operator
"## Results" | doc         # postfix | operator
```

**Render a DataFrame** (needs `cmx[tables]`):

```python
import pandas as pd

with doc:
    doc.table(pd.DataFrame({"model": ["a", "b"], "acc": [0.95, 0.87]}))
```

**Save and link an image** (needs `cmx[images]`). A bare filename lands in the document's figure folder; a path with a slash is used as written:

```python
import numpy as np

with doc:
    doc.image(np.random.rand(64, 64, 3), src="sample.png")
```

**Render a config dict as YAML** (needs `cmx[yaml]`):

```python
with doc:
    doc.yaml({"model": "ResNet50", "epochs": 100})
```

**Hide setup, keep results.** `doc.hide` runs a block without showing it; variables it defines stay in scope:

```python
with doc.hide:
    data = load_results()

with doc:
    doc @ "## Analysis"
    doc.print(f"Best: {data['accuracy'].max():.2%}")
```

## Documentation

Full documentation: **https://cmx-python.readthedocs.io**

- [Get started](https://cmx-python.readthedocs.io/en/latest/overview.html) — the config → capture → flush workflow.
- [Configuration](https://cmx-python.readthedocs.io/en/latest/configuration.html) — where Markdown and assets are written.
- [Adding text](https://cmx-python.readthedocs.io/en/latest/markdown.html), [Tables](https://cmx-python.readthedocs.io/en/latest/tables.html), [Images](https://cmx-python.readthedocs.io/en/latest/images.html).
- [API reference](https://cmx-python.readthedocs.io/en/latest/api/).

Runnable examples live in [`examples/core/`](examples/core/) — see its [README](examples/core/README.md).

## Development

```bash
git clone https://github.com/cmx/cmx-python.git
cd cmx-python
pip install -e '.[dev,docs]'   # editable install with test + docs tooling

make test       # run the pytest suite
make preview    # live-reload docs at http://localhost:8000
make docs       # build the HTML docs
```

See the [Development guide](https://cmx-python.readthedocs.io/en/latest/development.html) for the full workflow.

## Claude Code plugin

CMX ships a Claude Code plugin with two skills that guide Claude through CMX's API and component usage when you work on a CMX project. To set it up, run inside Claude Code:

```
/plugin marketplace add cmx/cmx-python
/plugin install cmx@cmx
```

Claude then loads the skills automatically whenever a task touches CMX; you can also invoke them directly:

- `/cmx:cmx-basics` — configuration (`doc.config`, `figdir`), context managers, output methods, and lifecycle hooks
- `/cmx:cmx-components` — tables and `figure_row` media grids, images, figures, videos, and troubleshooting

The skill sources live in [`skills/`](skills/); plugin and marketplace metadata live in [`.claude-plugin/`](.claude-plugin/).

## Project structure

```
cmx-python/
├── src/cmx/
│   ├── backends/        # markdown, components, md_table, html, latex
│   └── server/          # optional server stub
├── docs/                # Sphinx + MyST documentation
├── examples/core/       # numbered tutorial examples
├── tests/               # pytest suite + golden-file harness
├── skills/              # Claude Code plugin skills (SKILL.md per skill)
├── .claude-plugin/      # Claude Code plugin + marketplace metadata
├── pyproject.toml       # project configuration
└── Makefile             # build automation
```

## Contributing

Contributions are welcome. See the [Development guide](https://cmx-python.readthedocs.io/en/latest/development.html) for setup, tests, and the publishing flow.

## Authors

- Ge Yang
- Tom Tao

## License

MIT — see [LICENSE](LICENSE).

## Links

- **Documentation**: https://cmx-python.readthedocs.io
- **GitHub**: https://github.com/cmx/cmx-python
- **PyPI**: https://pypi.org/project/cmx/
- **Issues**: https://github.com/cmx/cmx-python/issues
