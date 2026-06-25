# Lifecycle hooks

Send a document's text and assets anywhere — local disk, S3/GCS, dash.ml — without a storage framework.

Each lifecycle moment is a **hook**: a method on the document with a sensible default that writes to the local filesystem. You change behavior two ways — **bind** a function on the instance for a one-off, or **subclass** `CommonMark` and override for something reusable. No logger, no backend registry.

## The key effects

Five hooks carry the document's life. A storage integration usually touches two or three.

| Hook | Fires | Returns |
|---|---|---|
| `on_mount` | once, when `doc.config()` resolves output — the destination/name **handshake** | `dest` (base key / URL / id) |
| `on_save` | per binary asset (image / video / figure) | the **link** written into `![]( )` |
| `on_flush` | per `doc.flush()` — a rendered chunk | — |
| `on_close` | once, on `doc.close()` / `atexit` | — |
| `on_error` | per failed `with doc:` block | — |

`on_mount` and `on_save` are the heart of storage — *where bytes go* and *what name comes back*. `on_flush`/`on_close` are the text: stream chunks, or write the whole thing once at the end. All hooks take **keyword-only** arguments and accept `**kw`, so adding a field later never breaks an existing hook. Only `on_mount` and `on_save` use their **return value**.

(two-patterns)=
## Two ways to set hooks

### Pattern 1 — One-off binding

Bind a function (or lambda) on the document instance. Best for a single script or a quick remote target.

```python
from cmx import doc

doc.config(__file__)

doc.on_mount = lambda *, filename, **kw: dash.create_readme(filename)   # handshake
doc.on_save  = lambda *, data, path, **kw: dash.put_file(path, encode(data))  # -> URL
doc.on_close = lambda *, full_text, dest, **kw: dash.put_readme(dest, full_text)
```

A bound function has **no `self`** — it shadows the default method on that one instance. To keep the default behavior and add to it, capture and wrap it:

```python
_save = doc.on_save                                  # built-in local writer
doc.on_save = lambda **kw: upload(**kw) or _save(**kw)   # upload AND keep local
```

### Pattern 2 — Class inheritance

Subclass `CommonMark` and override the hook methods. Best for a reusable integration you import across projects, test in isolation, or ship as a package.

```python
from cmx.backends.markdown import CommonMark


class S3Doc(CommonMark):
    bucket = "runs"

    def on_mount(self, *, filename, wd, figdir, doc, **kw):
        return f"s3://{self.bucket}/{filename}"

    def on_save(self, *, data, path, kind, dest, doc, **kw):
        s3_put(f"{self.bucket}/{path}", encode(data))
        return f"https://{self.bucket}.s3.amazonaws.com/{path}"

    def on_close(self, *, full_text, path, dest, doc, **kw):
        super().on_close(full_text=full_text, path=path, dest=dest, doc=doc, **kw)
        s3_put(dest, full_text.encode())


doc = S3Doc()
doc.config(__file__)
```

Overridden methods have `self`; call `super().on_<event>(...)` to keep the default behavior alongside yours.

### Which to use

| | One-off binding | Class inheritance |
|---|---|---|
| Shape | `doc.on_save = fn` | `class X(CommonMark): def on_save(self, …)` |
| Best for | one script, quick remote target | reusable, packaged, testable integrations |
| Keep the default | capture-and-wrap | `super().on_<event>(…)` |
| State | closure variables | `self` |

Both drive the same hooks; pick by how reusable the integration needs to be.

(optional-hooks)=
## Optional hooks

The same model covers content and capture — set them only if you need them.

**Content** — observe or export blocks as they're added:

| Hook | Fires | Note |
|---|---|---|
| `on_block` | every block, with `kind ∈ {text, code, table, image, figure, video}` | one hook for all blocks; dispatch on `kind` (e.g. export a CSV when `kind == "table"`). New component types never add a hook. |

```python
doc.on_block = lambda *, kind, node, **kw: export_csv(node) if kind == "table" else None
```

**Capture** — observe `with doc:` control:

| Hook | Fires | Note |
|---|---|---|
| `on_hide` | a `with doc.hide:` block runs (not shown) | side-effect only |
| `on_skip` | a `with doc.skip:` block is skipped | side-effect only |

`on_hide` and `on_skip` fire when the `doc.hide` / `doc.skip` property is read — at the top of the `with` block. An inline-span hook (`on_inline`) is not yet available.

(hook-context)=
## Hook context — a concrete trace

For this script at `/proj/report.py`:

```python
from cmx import doc

doc.config(__file__)

with doc:
    doc @ "# Run 042"
    doc.table(df)                 # df = pd.DataFrame({"a": [1], "b": [2]})
    doc.image(arr, "loss.png")    # arr = uint8 ndarray, shape (480, 640, 3)

doc.flush()
```

CMX resolves `.py → report.md`, `wd=/proj`, `figdir="report"` (the `{fname}` default), then calls each hook with exactly these keyword payloads:

```text
on_mount(filename="report.md", wd="/proj", figdir="report", doc=<doc>)
        -> return a dest (e.g. "s3://runs/report.md") or None for local

on_block(kind="table", node=<Table>, doc=<doc>)        # if set

on_save(kind="image",
        path="report/loss.png",          # bare "loss.png" placed under figdir
        data=<ndarray (480,640,3) uint8>,
        dest=<whatever on_mount returned>,
        doc=<doc>)
        -> return the link, e.g. "report/loss.png" (local) or an https URL

on_flush(text=<rendered chunk below>, path="report.md", dest=<...>, doc=<doc>)

on_close(full_text=<complete report.md>, path="report.md", dest=<...>, doc=<doc>)
```

The `text` passed to `on_flush` (and the `full_text` at `on_close`). The leading code block is the source captured by `with doc:`:

````markdown
```python
doc @ "# Run 042"
doc.table(df)
doc.image(arr, "loss.png")
```

# Run 042

|   a |   b |
|-----|-----|
|   1 |   2 |

![report/loss.png](report/loss.png)
````

`on_save`'s returned link is what lands in `![ ](report/loss.png)` — the round-trip a remote store uses to swap relative paths for hosted URLs. `on_close` gets `full_text`, so a PUT-only target (S3, a "set README" endpoint) can write the whole document once instead of appending per flush.

(how-it-works)=
## How it works

Hooks are methods on `CommonMark`, each with a local-disk default body. CMX dispatches each lifecycle moment with `self.on_<event>(**ctx)`:

- `on_mount` fires inside `config()`, after the filename, working directory, and figdir resolve. Its return becomes `doc.dest` (a remote base key / URL, or `None` for local).
- `on_save` fires from the `image` / `video` / `figure` / `savefig` factories. CMX renders its returned link into the `![]( )`; the default writes the bytes under `doc.wd` and returns the relative path.
- `on_flush` fires from `flush()` (and the end of `with doc:`); the default appends the rendered chunk to the `.md`.
- `on_close` fires from `doc.close()` and a registered `atexit` guard — exactly once across both. `full_text` is the file's full content (local), falling back to the accumulated document buffer.
- `on_error` fires in the `with doc:` exception path; it does not suppress the exception, which still propagates.

Override a hook by subclassing (the method has `self`) or by binding a plain function on the instance (it shadows the default — no `self`). Both work in plain Python; there is no registry. Subclass methods survive `doc.new()` automatically.

## Next steps

- [Configuration](configuration.md) — how `dest`, `wd`, and filenames are resolved before `on_mount` fires.
- [Images](images.md) — what `on_save` receives and the link it returns.
