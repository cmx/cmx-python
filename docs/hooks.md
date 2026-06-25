# Hooks

Send a document's text and assets to an external service — like dash.ml's README endpoint — by giving CMX your own logger.

CMX never writes to disk directly. Every write goes through a **logger** object, and you can swap in your own. The logger is the integration seam: implement its methods and CMX will call them as it renders, so the same script that produces a local `.md` can instead stream text and images to a remote service.

## Set a logger

Pass any object that implements the [logger protocol](logger-protocol) when you configure the document:

```python
from cmx import doc
from myproject.dash import DashLogger

doc.config(__file__, logger=DashLogger(project="experiments", run="run-042"))
```

The default logger (`cmx.utils.SimpleLogger`) writes to the local filesystem, rooted at the document's working directory. A custom logger can write anywhere — an HTTP endpoint, an object store, a database. When the logger's `root` is an `http(s)` URL, CMX prints the dashboard URL from `get_dash_url()` instead of a `file://` path.

## When CMX calls each hook

These are the methods CMX calls today. A logger only needs to implement the ones used by the features you use — a text-only document never triggers `save_image`.

| Hook | Signature | CMX calls it when |
|---|---|---|
| `log_text` | `log_text(text, filename, overwrite=False)` | On `doc.config` (to clear, `overwrite=True`) and on every `doc.flush()` (to append rendered content). |
| `save_image` | `save_image(image, filename, normalize=False)` | `doc.image(array, src=...)` with array data. |
| `save_video` | `save_video(frames, filename)` | `doc.video(frames, src=...)`. |
| `savefig` | `savefig(filename, **kwargs)` | `doc.savefig(key)` — saves the current matplotlib figure. |
| `get_dash_url` | `get_dash_url() -> str` | On `doc.config`, when `root` starts with `http`, to print where output landed. |
| `now` | `now() -> str` | Available for timestamps (e.g. report headers). |
| `job_started` | `job_started()` | Reserved lifecycle marker (no-op by default). |
| `load_json` / `load_file` | `load_json(filename)` / `load_file(filename)` | Reading prior data back in. |

CMX also reads and sets `logger.root` to resolve the working directory, and joins relative paths under it.

## The four core hooks

These map directly to what you asked for when integrating with dash.ml.

### 1. Saving images and other data

`save_image`, `save_video`, and `savefig` receive the in-memory data (a numpy array, a list of frames, or the live matplotlib figure) and the resolved relative `filename`. Your logger decides where the bytes go — write a file, `POST` to an upload endpoint, or push to an object store — and the markdown link CMX emits (`![](filename)`) should resolve to wherever you put it. See [Asset links](asset-links) for rewriting those links to absolute URLs.

### 2. Flushing intermediate text

Each `doc.flush()` renders the document's accumulated blocks and calls `log_text(text, filename, overwrite=False)`, then clears those blocks. A long-running script can flush repeatedly to stream progress. Your logger decides whether each flush **appends** to the destination (the default, good for a growing log) or **replaces** it with the full content so far (good for a README that should always show the complete document).

### 3. Saving the final text

There is no separate "final" call today — the last `doc.flush()` carries the tail of the document. For services that want the complete document in one shot at the end, buffer in `log_text` and send on `close()` (see [Proposed hooks](proposed-hooks)), or call `doc.flush()` once at the end of the script.

### 4. The destination handshake

Deciding *where* output goes and *what it's named* happens at `doc.config` time:

- CMX sets `logger.root` to the resolved working directory and passes a relative `filename` (the document's basename) to every hook.
- If `logger.root` is an `http(s)` URL, CMX treats output as remote and prints `get_dash_url()`.

This is enough for a fixed destination. For services that **assign** an id or canonical path (dash.ml minting a README slug from the project and run), do the handshake in your logger's constructor or lazily on the first write, then return the resolved location from `get_dash_url()`. The [proposed `resolve(stem)` hook](proposed-hooks) makes this an explicit step.

## Example: a dash.ml logger

A logger that streams a CMX document to a dash.ml README endpoint. The handshake resolves the README's URL from the project/run; flushes are sent as replacements so the README always shows the whole document; images are uploaded as files.

```python
import os
import requests  # or the ml-dash client


class DashLogger:
    """Stream a CMX document to a dash.ml README endpoint."""

    def __init__(self, project, run, base_url="https://dash.ml/api"):
        self.project = project
        self.run = run
        # `root` being an http URL puts CMX in "remote" mode.
        self.root = f"{base_url}/{project}/{run}"
        self.prefix = ""
        self._buffer = ""          # full document, for replace-on-flush

    # --- destination handshake -------------------------------------------
    def get_dash_url(self):
        return f"https://dash.ml/{self.project}/{self.run}/README"

    # --- text (intermediate + final) -------------------------------------
    def log_text(self, text, filename, overwrite=False):
        # Replace semantics: keep the remote README in sync with the doc.
        self._buffer = text if overwrite else self._buffer + text
        requests.put(f"{self.root}/readme", json={"path": filename,
                                                   "content": self._buffer})

    # --- assets ----------------------------------------------------------
    def save_image(self, image, filename, normalize=False):
        from io import BytesIO
        from PIL import Image
        import numpy as np

        if isinstance(image, np.ndarray):
            if image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8)
            image = Image.fromarray(image)
        buf = BytesIO()
        image.save(buf, "png")
        requests.post(f"{self.root}/files/{filename}", data=buf.getvalue())

    def savefig(self, filename, **kwargs):
        import matplotlib.pyplot as plt
        from io import BytesIO

        buf = BytesIO()
        plt.savefig(buf, format="png", **kwargs)
        requests.post(f"{self.root}/files/{filename}", data=buf.getvalue())

    # --- niceties --------------------------------------------------------
    @staticmethod
    def now():
        from datetime import datetime
        return datetime.now().isoformat()

    def job_started(self):
        requests.post(f"{self.root}/status", json={"state": "running"})
```

Use it like any logger:

```python
doc.config(__file__, logger=DashLogger(project="experiments", run="run-042"))

doc @ "# Training run 042"
with doc:
    doc.image(make_loss_plot(), src="loss.png")   # uploaded to dash.ml
doc.flush()                                         # README updated on dash.ml
```

:::{note}
The endpoint paths above are illustrative. Wire `log_text`/`save_image` to the real dash.ml (ml-dash) client for your deployment.
:::

(asset-links)=
## Asset links

CMX writes image links relative to the document (`![](loss.png)`). When assets live on a remote service, the rendered README needs absolute URLs. Two options: serve assets under the README's own path so relative links resolve as-is, or rewrite links to absolute URLs before sending — the natural place is the proposed [`before_write`](proposed-hooks) hook.

(proposed-hooks)=
## Proposed hooks

CMX does not call these yet. They are the extension points worth adding for richer dash.ml integration — listed so a logger can be designed forward-compatibly.

| Hook | Signature | Purpose |
|---|---|---|
| `resolve` | `resolve(stem) -> str` | Explicit destination handshake: mint/return the canonical path, id, or URL for this document. |
| `close` | `close()` | End-of-run finalize: flush buffers, mark the run complete, send the full document once. |
| `before_write` | `before_write(text) -> text` | Transform rendered markdown before it leaves (rewrite asset links to absolute URLs, inject frontmatter). |
| `asset_url` | `asset_url(filename) -> str` | Return the public URL for a saved asset, so links point at hosted files. |
| `set_meta` | `set_meta(**fields)` | Attach title, tags, author, timestamps to the remote document. |
| `on_progress` | `on_progress(stage, fraction)` | Heartbeat/progress for long runs surfaced on the dashboard. |
| `save_data` | `save_data(obj, filename)` | Generic blob/artifact save beyond images and video (arrays, JSON, checkpoints). |
| `on_error` | `on_error(exc)` | Mark the run failed and capture the traceback in the document. |

If you want any of these wired into the core render loop, open an issue describing the dash.ml flow it unblocks.

(logger-protocol)=
## Logger protocol

The minimum a custom logger must provide for the features you use:

```python
class Logger:
    root: str                                  # base path or URL; CMX reads/sets this
    prefix: str                                # optional path prefix

    def log_text(self, text, filename, overwrite=False): ...   # required for any output
    def get_dash_url(self) -> str: ...                          # required if root is http

    def save_image(self, image, filename, normalize=False): ...  # for doc.image(array)
    def save_video(self, frames, filename): ...                  # for doc.video
    def savefig(self, filename, **kwargs): ...                   # for doc.savefig
    def load_json(self, filename): ...                           # optional read-back
    def load_file(self, filename): ...                           # optional read-back
    @staticmethod
    def now() -> str: ...                                        # optional timestamp
    def job_started(self): ...                                   # optional lifecycle
```

`cmx.utils.SimpleLogger` is the reference implementation — read it for the exact filesystem behavior.

## Next steps

- [Configuration](configuration.md) — how `root`, `wd`, and filenames are resolved before hooks run.
- [Images](images.md) — what `save_image` / `savefig` receive and how asset links are formed.
- [API reference](api/index.md) — the `SimpleLogger` reference implementation.
