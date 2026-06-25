# Development

Set up a dev environment, run the tests, build the docs, and publish a release.

## Setup

Clone the repository and install it in editable mode with the dev extra.

```bash
git clone https://github.com/cmx/cmx-python.git
cd cmx-python
pip install -e '.[dev]'
```

The `dev` extra pulls Black, Pylint, pytest, pandas, and tabulate. The core package itself has no runtime dependencies — those tools are for development only.

To work on the documentation as well, add the `docs` extra:

```bash
pip install -e '.[docs]'
```

:::{note}
`tabulate` ships in the `dev` extra as a test oracle, not a runtime dependency. The golden parity tests compare CMX's pure-Python table renderer (`cmx.backends.md_table`) against `tabulate` output. CMX never imports `tabulate` at runtime for the default `github` table format.
:::

## Workflow

The `Makefile` wraps the common tasks:

| Command | What it does |
|---|---|
| `make test` | Run the full pytest suite |
| `make preview` | Serve the docs with live reload on `http://localhost:8888` |
| `make docs` | Build the HTML docs and serve them once |
| `make wheel` | Build a wheel into `dist/` |
| `make dev` | Build a wheel and install it with `--ignore-installed` |
| `make publish` | Convert the README, run tests, build, and upload to PyPI |
| `make release` | Tag the release and push tags to GitHub |

## Project structure

```
cmx-python/
├── src/
│   └── cmx/                  # Package source (dependency-free core)
│       ├── __init__.py       # Exports `doc`, `md`, `data`
│       ├── data.py           # Data utilities
│       ├── utils.py          # Path resolution and helpers
│       ├── with_hack.py      # Frame-tracing for `with doc.hide:` / `doc.skip`
│       ├── backends/
│       │   ├── markdown.py    # Markdown renderer
│       │   ├── components.py  # Block types (Table, Figure, Row, ...)
│       │   ├── md_table.py    # Pure-Python github-format table renderer
│       │   ├── html.py        # HTML backend (stub)
│       │   └── latex.py       # LaTeX backend (stub)
│       └── server/           # Optional Sanic server (out-of-scope stub)
├── docs/                     # Sphinx + MyST + furo documentation
│   ├── conf.py
│   ├── index.md
│   ├── development.md        # This file
│   └── api/                  # Autodoc reference
├── examples/                 # Example scripts
├── tests/                    # pytest suite (includes the golden harness)
├── pyproject.toml            # Project + tool configuration
├── Makefile                  # Build automation
└── VERSION                   # Version number
```

`backends/html.py` and `backends/latex.py` are present but empty stubs — Markdown is the only complete backend. The `server/` package is an optional Sanic stub behind the `server` extra and is not test-verified.

## Making changes

1. Branch off `main`:
   ```bash
   git checkout -b feature/my-change
   ```
2. Make your changes under `src/cmx/`.
3. Add or update tests in `tests/`.
4. Update the docs in `docs/` if behavior changed.
5. Format and test before committing:
   ```bash
   black src/cmx tests examples
   make test
   ```

Black is configured with a 120-character line length in `pyproject.toml`. Pylint config lives there too; run it with `pylint src/cmx`.

## Testing

Run the suite with pytest (90 tests):

```bash
pytest
```

`make test` runs the same suite with `--capture=no` so prints stream live.

### The golden harness

`tests/test_golden.py` renders example documents and compares the output byte-for-byte against committed master `.md` files. When you intentionally change rendered output, refresh the masters by setting `UPDATE_GOLDEN=1`:

```bash
UPDATE_GOLDEN=1 pytest tests/test_golden.py
```

Review the resulting diff before committing — the regenerated masters become the new source of truth.

:::{tip}
`tests/test_md_table.py` checks the `md_table` renderer against `tabulate` for parity. If you touch the table renderer, run it directly: `pytest tests/test_md_table.py`.
:::

## Building docs

The site is Sphinx with MyST Markdown and the furo theme. Preview locally with live reload:

```bash
make preview
```

This serves `http://localhost:8888` and rebuilds on every save. To produce a static build:

```bash
make docs
```

The HTML lands in `docs/_build/html/`.

## Publishing

1. Bump the version:
   ```bash
   echo "0.0.48" > VERSION
   ```
2. Update `docs/CHANGE_LOG.md`.
3. Build, test, and upload to PyPI:
   ```bash
   make publish
   ```
   This converts the README to reStructuredText, runs the tests, builds the wheel, and uploads with twine. You need PyPI credentials configured.
4. Tag and push the release:
   ```bash
   make release msg="Release version 0.0.48"
   ```

:::{warning}
`make publish` uploads to the live PyPI index. Run `make test` and verify the wheel locally with `make dev` before publishing.
:::

## Contributing

1. Fork the repository and create a feature branch.
2. Make your change with tests and docs.
3. Run `black` and `make test`.
4. Open a pull request with a clear, descriptive title.

Keep commit messages specific — "Add video embedding to the markdown backend" rather than "Fixed stuff". Add docstrings and type hints to public functions.

## Troubleshooting

**Import errors after editable install.** Reinstall cleanly:

```bash
pip uninstall cmx
pip install -e '.[dev]'
```

**Docs fail to build.** Make sure the `docs` extra is installed and clear the build cache:

```bash
pip install -e '.[docs]'
rm -rf docs/_build
make docs
```

**Tests fail on import.** Confirm the dev extra is installed (`pip install -e '.[dev]'`), then rerun with verbose output: `pytest -v`.

## Next steps

- [API reference](api/index.md) — the autodoc reference for every module, including `cmx.backends.md_table`.
