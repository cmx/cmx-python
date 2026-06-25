# Configuration

Control where your Markdown and assets are written.

Every document needs to know two things: where to write the `.md` file, and where to put the images, figures, and other assets it references. You set both with a single `doc.config(...)` call. The recommended call is `doc.config(__file__)` — it anchors output to the script you run, so files land next to your code, not wherever you happened to launch Python.

## Anchor output to your script

Pass `__file__` to `doc.config`. CMX writes the Markdown next to the script and roots all assets there too.

```python
from cmx import doc

doc.config(__file__)

doc @ "# Report"
doc.flush()
```

Run `report.py` and you get `report.md` in the same directory. The script's base name carries over to the Markdown file (`report.py` → `report.md`), and the **working directory** defaults to the script's folder — not the current working directory. This is what makes a script produce the same output no matter where you run it from.

On configure, CMX prints a green confirmation line so you can click straight through to the result:

```
File output at file:///Users/you/project/report.md
```

## Set an explicit output path

To name the output file yourself, pass a path ending in `.md` (or use the `filename=` keyword). The working directory defaults to that file's directory.

```python
doc.config("report.md")              # first positional, ends in .md
doc.config(filename="report.md")     # equivalent keyword form
```

CMX decides what `file` means by its extension: a `.py` path is treated as the **script**, anything else is treated as the **output Markdown path**.

## Override the working directory

The working directory roots both the Markdown file and its assets. Override it with `wd=` to relocate everything — useful for writing into a build folder while keeping your script in place.

```python
doc.config(__file__, wd="/tmp/out")
```

The Markdown name still comes from the script (`report.md`), but the file and its asset folder now live under `/tmp/out`.

## The figdir template

Assets go into a **figure directory** (`figdir`). `figdir` is a template, and `{fname}` expands to the Markdown file's name **without its extension** (`report.md` → `report`) — distinct from `doc.filename`, which is the full name *with* extension. The default is `"{fname}"`, so each document gets its own folder named after it.

```python
doc.config(__file__)                  # 04_images.py -> assets in 04_images/
doc.config(__file__, figdir="assets") # all assets in assets/
doc.config(__file__, figdir="")       # assets beside the .md, no subfolder
```

A per-file folder keeps assets from different scripts from colliding. Point several documents at a shared `figdir="assets"` only when you want them to share one folder.

Read the resolved directory back from the `doc.figdir` property:

```python
doc.config(__file__)   # in 04_images.py
doc.figdir             # "04_images"
```

## Asset resolution rules

When you call `doc.image`, `doc.figure`, `doc.video`, or `doc.savefig`, CMX decides where the `src` lives by one rule: **does the name contain a slash?**

| You pass | CMX stores | Why |
|---|---|---|
| `"gradient.png"` (bare name) | `figdir/gradient.png` | bare names go under `figdir` |
| `"sub/x.png"` (has a slash) | `sub/x.png` | explicit path wins, used as-is |

Bare names get the managed treatment — they land in `figdir` automatically. A name with a directory component is taken literally, so you stay in control when you need a specific location.

Stored paths always use forward slashes, and every link is written **relative to the Markdown file**. The `.md` and its assets move together as a unit.

This example, configured with `doc.config(__file__)` in `04_images.py`, saves a bare name:

```python
doc.image(random_image, src="random.png")
```

The generated Markdown links into the per-file folder:

```markdown
![04_images/random.png](04_images/random.png)
```

:::{tip}
Pass bare names and let `figdir` organize your assets. Reach for a slashed path only when an asset must live somewhere specific.
:::

## Reading config back

Two read-only properties report the resolved configuration:

- `doc.filename` — the Markdown basename, **with** extension (e.g. `report.md`). If you never call `doc.config`, it's derived lazily from the calling script (`foo.py` → `foo.md`, `__init__.py` → `README.md`).
- `doc.figdir` — the figure directory after `{fname}` expansion (the name **without** extension, e.g. `report`).

```python
doc.config(__file__)   # in report.py
doc.filename           # "report.md"
doc.figdir             # "report"
```

`doc.config(...)` returns `self`, so calls are chainable.

## Next steps

- [Images](images.md) — save arrays and files into your `figdir`.
- [Overview](overview.md) — the config → capture → flush workflow.
- [Installation](installation.md) — extras for tables, images, and figures.
