# API Reference

This section contains the complete API reference for CMX.

## Core Module

The main module provides the global `doc` object and data utilities.

```{eval-rst}
.. automodule:: cmx
   :members:
   :undoc-members:
   :show-inheritance:
```

## Backends

CMX supports multiple output backends for different use cases.

### Markdown Backend

The primary backend for generating markdown documents.

```{eval-rst}
.. automodule:: cmx.backends.markdown
   :members:
   :undoc-members:
   :show-inheritance:
```

### Components

Base components used across all backends.

```{eval-rst}
.. automodule:: cmx.backends.components
   :members:
   :undoc-members:
   :show-inheritance:
```

### HTML Backend

HTML output support.

```{eval-rst}
.. automodule:: cmx.backends.html
   :members:
   :undoc-members:
   :show-inheritance:
```

### LaTeX Backend

LaTeX output support for academic papers and publications.

```{eval-rst}
.. automodule:: cmx.backends.latex
   :members:
   :undoc-members:
   :show-inheritance:
```

## Utilities

### Utils Module

Helper functions and utilities.

```{eval-rst}
.. automodule:: cmx.utils
   :members:
   :undoc-members:
   :show-inheritance:
```

### Data Module

Data processing utilities.

```{eval-rst}
.. automodule:: cmx.data
   :members:
   :undoc-members:
   :show-inheritance:
```

### Context Managers

Advanced context management utilities.

```{eval-rst}
.. automodule:: cmx.with_hack
   :members:
   :undoc-members:
   :show-inheritance:
```

## Server

Optional server components for live document serving.

```{eval-rst}
.. automodule:: cmx.server
   :members:
   :undoc-members:
   :show-inheritance:
```
