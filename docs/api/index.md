# API Reference

Complete reference for every CMX module, generated from the source with autodoc.

The API splits into four groups. **Core** is what you import and call day to day. **Backends** turn the document tree into output. **Utilities** support both. **Server** is optional, for serving live documents.

## Core

You interact with CMX through the `cmx` module: the global `doc` object, its `md` alias, and the re-exported `cmx.data` helpers.

```{eval-rst}
.. automodule:: cmx
   :members:
   :undoc-members:
   :show-inheritance:
```

## Backends

A backend renders the accumulated document blocks into a concrete format. Markdown is the primary, fully supported backend; the others cover narrower cases.

### Markdown

Renders the document tree to Markdown. This is the default backend.

```{eval-rst}
.. automodule:: cmx.backends.markdown
   :members:
   :undoc-members:
   :show-inheritance:
```

### Components

The block types (`Text`, `Pre`, `Table`, `Image`, `Figure`, `Row`, `Video`) shared across backends.

```{eval-rst}
.. automodule:: cmx.backends.components
   :members:
   :undoc-members:
   :show-inheritance:
```

### Table renderer

Pure-Python renderer for the default `github` table format. It needs no `tabulate` and matches `to_markdown(tablefmt="github")` byte for byte.

```{eval-rst}
.. automodule:: cmx.backends.md_table
   :members:
   :undoc-members:
   :show-inheritance:
```

### HTML

HTML output support.

```{eval-rst}
.. automodule:: cmx.backends.html
   :members:
   :undoc-members:
   :show-inheritance:
```

### LaTeX

LaTeX output support for academic papers and publications.

```{eval-rst}
.. automodule:: cmx.backends.latex
   :members:
   :undoc-members:
   :show-inheritance:
```

## Utilities

### Utils

Helper functions used across the package.

```{eval-rst}
.. automodule:: cmx.utils
   :members:
   :undoc-members:
   :show-inheritance:
```

### Data

Data-processing helpers, re-exported as `cmx.data`.

```{eval-rst}
.. automodule:: cmx.data
   :members:
   :undoc-members:
   :show-inheritance:
```

### Context managers

The frame-tracing machinery behind `with doc:`, `doc.hide`, and `doc.skip`.

```{eval-rst}
.. automodule:: cmx.with_hack
   :members:
   :undoc-members:
   :show-inheritance:
```

## Server

Optional components for serving live documents.

```{eval-rst}
.. automodule:: cmx.server
   :members:
   :undoc-members:
   :show-inheritance:
```

## Next steps

- [Development](../development.md) — set up a dev environment, run tests, and build these docs.
