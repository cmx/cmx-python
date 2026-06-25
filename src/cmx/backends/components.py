"""Render components for the CMX markdown backend.

Each component knows how to render itself as Markdown (``_md``) and HTML
(``_html``). Components form a tree: an :class:`Article` holds children, some of
which (``Table``, ``FigureRow``, ``Row``) hold children of their own.

This module is dependency-inverted the simple way: there is no class registry or
``__getattribute__`` proxy. Parents create their children by calling the
component classes directly. Components are pure *render* objects -- they no
longer write files; the document's lifecycle hooks (``on_save`` and friends, see
:class:`cmx.backends.markdown.CommonMark`) own all I/O and hand each component
the final ``src`` link to render. Anything that needs heavy third-party
libraries (numpy, PIL, pyyaml) imports them lazily so ``import cmx`` stays cheap.
"""

import os
import posixpath
import re
from io import StringIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

from .. import utils
from ..utils import is_subclass, to_snake  # re-exported for backwards compatibility


def read_table(file, sep=None, **kwargs):
    """Load a tabular file into a pandas ``DataFrame``, inferred by extension.

    Supports ``.csv`` / ``.tsv`` (text), ``.json``, ``.parquet``, and Excel
    (``.xls`` / ``.xlsx``); ``.yaml`` / ``.yml`` are parsed and fed to the
    ``DataFrame`` constructor. Extra ``kwargs`` are forwarded to the matching
    pandas reader. ``sep`` overrides the delimiter for text files (defaulting to
    a tab for ``.tsv`` and a comma otherwise). Unknown extensions are read as CSV.
    """
    import pandas as pd

    ext = os.path.splitext(file)[1].lower()
    if ext == ".json":
        return pd.read_json(file, **kwargs)
    if ext == ".parquet":
        return pd.read_parquet(file, **kwargs)
    if ext in (".xls", ".xlsx"):
        return pd.read_excel(file, **kwargs)
    if ext in (".yaml", ".yml"):
        import yaml

        with open(file) as f:
            return pd.DataFrame(yaml.safe_load(f))
    if sep is None:
        sep = "\t" if ext == ".tsv" else ","
    return pd.read_csv(file, sep=sep, **kwargs)


def attrs(class_name=None, **kwargs):
    attrs_str = f'class="{class_name}"' if class_name else ""
    # Drop ``None`` values so optional attrs (e.g. an unset width/height) don't
    # render as the literal string ``width="None"``.
    attrs_str += " ".join([k.replace("_", "-") + f'="{str(v)}"' for k, v in kwargs.items() if v is not None])
    return attrs_str


def styles(**kwargs):
    return " ".join([k.replace("_", "-") + f":{str(v)};" for k, v in kwargs.items()])


class Component:
    """Base node in the document tree.

    A component renders to Markdown via ``_md`` and to HTML via ``_html``. The
    default implementation emits a generic ``<tag>...children...</tag>``; most
    subclasses override one or both properties.
    """

    tag = None
    data = None
    class_name = None

    def __init__(self, tag=None, children=None, **kwargs):
        self.tag = tag or self.tag
        self.kwargs = kwargs
        self.style = {}
        self.children = [] if children is None else children

    def now(self, fmt=None):
        from datetime import datetime

        now = datetime.now().astimezone()
        return now.strftime(fmt) if fmt else now

    @property
    def _attrs(self):
        return attrs(class_name=self.class_name, **self.kwargs)

    @property
    def _md(self):
        return self._html + "\n"

    @property
    def _html(self):
        inner = "".join([c._html for c in self.children if c is not None])
        return f"<{self.tag} {self._attrs}>{inner}</{self.tag}>"

    # Components double as context managers so ``with doc.table() as t:`` works.
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Container(Component):
    """A holder that is rendered by its parent, never on its own."""

    @property
    def _md(self):
        raise RuntimeError(f"Container {type(self).__name__} does not support markdown generation directly")

    @property
    def _html(self):
        raise RuntimeError(f"Container {type(self).__name__} does not support html generation directly")


class Div(Component):
    tag = "div"


class Span(Component):
    tag = "span"

    def __init__(self, *args, sep=" ", dedent=None, end="\n", **kwargs):
        super().__init__(**kwargs)
        self.text = sep.join([str(a) for a in args])
        if dedent:
            self.text = utils.dedent(self.text)
        self.end = end

    @property
    def _md(self):
        # Block-level text terminates with a configurable ``end`` (default
        # "\n") so siblings don't run together. Only the trailing run of
        # newlines is replaced -- internal newlines are preserved -- so a
        # triple-quoted multi-line block doesn't double up its terminator.
        if not self.text:
            return ""
        return self.text.rstrip("\n") + self.end

    @property
    def _html(self):
        return f"<{self.tag}>{self.text}</{self.tag}>"


Text = Span


class Bold(Span):
    tag = "b"

    @property
    def _md(self):
        # Wrap the stripped text so the ``**`` markers hug the content. (The old
        # implementation wrapped ``Span._md``, which left the trailing newline
        # *inside* the markers, e.g. ``**title\n**`` -- broken inside tables.)
        return f"**{self.text.strip()}**\n"


class Pre(Component):
    tag = "pre"

    def __init__(self, text, lang=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.lang = lang

    @property
    def _md(self):
        text = self.text + ("" if self.text.endswith("\n") else "\n")
        if not text.startswith("\n"):
            text = "\n" + text
        # CommonMark: the outer fence must be longer than the longest run of
        # backticks inside the code so nested fences don't break out.
        longest = max((len(m) for m in re.findall(r"`+", self.text)), default=0)
        fence = "`" * max(3, longest + 1)
        return f"{fence}{self.lang or ''}{text}{fence}\n"

    @property
    def _html(self):
        if self.lang:
            segs = ["<pre>", f'<code class="{self.lang}">', f"{self.text}", "</code>", "</pre>"]
        else:
            segs = ["<pre>", f"{self.text}", "</pre>"]
        return "\n".join(segs) + "\n"


class Link(Component):
    tag = "span"

    def __init__(self, href="", text="", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.href = href

    @property
    def _md(self):
        return f"[{self.text}]({self.href})"

    @property
    def _html(self):
        return f'<a href="{self.href}">{self.text}</a>'


class Img(Component):
    tag = "img"
    zoom = None

    def __init__(self, src=None, zoom=None, alt=None, **kwargs):
        super().__init__(**kwargs)
        self.src = src
        self.alt = alt
        if zoom is not None:
            self.style = {"zoom": zoom}
        self.zoom = zoom

    @property
    def _md(self):
        if self.zoom is None:
            return f"![{self.src}]({self.alt or self.src})"
        return self._html

    @property
    def _html(self):
        # align_self prevents stretching inside a flex Row.
        return f'<img style="{styles(align_self="center", **self.style)}" src="{self.src}" {self._attrs}/>'


class Image(Img):
    """An image that either references a ``src`` link or inlines base64 data.

    Components no longer perform any file I/O -- the document's ``on_save`` hook
    writes the bytes and returns the link, which is passed here as ``src``.

    - ``src`` given      -> reference that link (already resolved by ``on_save``).
    - ``image`` only     -> inline the array as a base64 ``data:`` URI.
    """

    data = None

    def __init__(self, image=None, src=None, normalize=False, **kwargs):
        if src is not None:
            super().__init__(src=src, **kwargs)
        elif image is not None:
            import numpy as np

            # todo: support 16/32-bit images (e.g. depth maps).
            self.data = np.array(image).astype(np.uint8)
            super().__init__(src=self.base64, **kwargs)
        else:
            super().__init__(src=None, **kwargs)

    @property
    def base64(self):
        assert self.data is not None
        from io import BytesIO
        from PIL import Image as pImage
        import base64

        with BytesIO() as buf:
            pImage.fromarray(self.data).save(buf, "png")
            return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")


class Video(Component):
    def __init__(self, src=None, width=320, height=240, controls=True, **kwargs):
        super().__init__(**kwargs)
        self.src = src
        self.width = width
        self.height = height
        self.controls = controls

    @property
    def _html(self):
        return utils.dedent(
            f"""
        <video width="{self.width}" height="{self.height}" controls="{str(self.controls).lower()}">
          <source src="{self.src}" type="video/mp4">
          Your browser does not support the video tag.
        </video>
        """
        )


def video(frames=None, *, src, **kwargs):
    """Return the component matching ``src``.

    ``.gif`` sources render as an ``Image``; everything else as a ``Video``.
    Frame data is saved by the document's ``on_save`` hook, not here.
    """
    file_path, *_ = src.split("?")
    if file_path.endswith("gif"):
        return Image(src=src, **kwargs)
    return Video(src=src, **kwargs)


class Figure(Component):
    tag = "div"

    def __init__(self, image=None, src=None, title=None, caption=None, **kwargs):
        super().__init__()
        self.src = src
        if isinstance(image, Component):
            self.img = image
        else:
            self.img = Image(image=image, src=src, **kwargs)
        self.title = title
        self.caption = caption
        self.children = [self.title, self.img, self.caption]

    @property
    def _html(self):
        if self.title and self.caption:
            return (
                f'<table><tr><td rowspan="2">{self.img._html}</td>'
                f"<td>{self.title}</td></tr><tr><td>{self.caption}</td></tr></table>"
            )
        elif self.caption:
            return f'<table><tr><td rowspan="2">{self.img._html}</td><td>{self.caption}</td></tr></table>'
        elif self.title:
            return f"<table><tr><th>{self.title}</th></tr><tr><td>{self.img._html}</td></tr></table>"
        return self.img._html


class Savefig(Figure):
    """Save the current matplotlib figure to ``key`` and reference it inline.

    ``key`` is the destination path (an optional ``?...`` query suffix is
    stripped before writing, so it can double as a cache-buster in the ``src``).
    ``title``/``caption``/``width``/``height``/``zoom`` control how the figure is
    displayed; every other keyword (``dpi``, ``bbox_inches``, ``transparent``,
    ``facecolor``, ``format`` ...) is forwarded untouched to matplotlib's
    ``savefig`` (through the document's ``on_save`` hook) and is *not* leaked
    into the ``<img>`` tag.
    """

    def __init__(self, key, caption=None, width=None, height=None, zoom=None, **kwargs):
        super().__init__(src=key, width=width, height=height, caption=caption, zoom=zoom, **kwargs)


class Row(Component):
    styles = dict(
        display="flex",
        flex_direction="row",
        item_align="center",
    )

    def __init__(self, wrap=False, styles=None, **kwargs):
        super().__init__(**kwargs)
        if wrap is not None:
            wrap = "wrap" if wrap else "nowrap"
        self.styles = dict(flex_wrap=wrap, **Row.styles)
        self.styles.update(styles or {})

    @property
    def _html(self):
        inner = "".join([c._html for c in self.children])
        return f'<div style="{styles(**self.styles)}">{inner}</div>'


class FigureRow(Container):
    """A horizontal band of figures rendered by its parent ``Table`` as up to
    three Markdown rows: titles, images, and captions (empty bands are dropped).
    """

    def __init__(self, header=None, n_cols=None, doc=None, **kwargs):
        super().__init__(**kwargs)
        # ``doc`` is the owning document, threaded so that nested assets are
        # written through the document's ``on_save`` lifecycle hook.
        self._doc = doc
        self.n_cols = n_cols
        self.titles = []
        self.images = []
        self.footers = []

    def _save(self, *, data, path, kind, **extra):
        """Route a nested asset through the owning document's ``on_save`` hook.

        Falls back to the bare ``path`` (no I/O) when there is no document.
        """
        on_save = getattr(self._doc, "on_save", None)
        if on_save is None:
            return path
        # Note: nested figure-row assets use the path as-is (no ``_resolve_asset``
        # figdir placement) -- matching the historical behavior.
        return on_save(data=data, path=path, kind=kind, dest=getattr(self._doc, "dest", None), doc=self._doc, **extra)

    def figure(self, image=None, src=None, title=None, caption=None, **kwargs):
        self.titles.append(None if title is None else Bold(title))
        self.footers.append(None if caption is None else Span(caption))
        if src is not None:
            src = self._save(data=image, path=src, kind="image", **kwargs)
            self.children.append(Image(src=src))
        else:
            self.children.append(Image(image=image, **kwargs))

    def video(self, frames=None, src=None, title=None, caption=None, **kwargs):
        self.titles.append(None if title is None else Bold(title))
        self.footers.append(None if caption is None else Span(caption))
        src = self._save(data=frames, path=src, kind="video", **kwargs)
        self.children.append(video(src=src, **kwargs))

    def column(self, title=None, text=None, footer=None):
        self.titles.append(None if title is None else Bold(title))
        self.footers.append(None if footer is None else Span(footer))
        self.children.append(Text(text))

    def savefig(self, key, title=None, caption=None, **kwargs):
        self.titles.append(None if title is None else Bold(title))
        self.footers.append(None if caption is None else Span(caption))
        src = self._save(data=None, path=key, kind="figure", **kwargs)
        self.children.append(Savefig(src, caption=caption))

    @property
    def rows(self):
        non_empty_rows = []
        for r in [self.titles, self.children, self.footers]:
            for item in r:
                if item is not None:
                    non_empty_rows.append(r)
                    break
        return non_empty_rows


class Table(Component):
    """A Markdown/HTML table.

    Pass tabular ``data`` (a DataFrame, CSV string, or anything pandas accepts)
    for a data table, or build a figure grid with :meth:`figure_row`.
    """

    data: "pd.DataFrame | None" = None

    def __init__(self, table=None, file=None, show_index=None, format="github", sep=",*", doc=None, **kwargs):
        super().__init__()
        # ``doc`` is threaded so figure rows can save nested assets via the
        # document's ``on_save`` hook.
        self._doc = doc
        self.show_index = show_index
        self.kwargs = kwargs  # forwarded to pandas' to_markdown / to_html
        self.format = format
        if file is not None:
            # Load tabular data straight from disk (csv/tsv/json/parquet/excel/yaml).
            # ``,*`` is the constructor's regex default for inline strings; let
            # read_table infer the delimiter unless the caller set a real one.
            self.data = read_table(file, sep=None if sep == ",*" else sep)
        elif table is None:
            pass
        else:
            try:
                import pandas as pd
            except ImportError as e:
                raise ImportError(
                    "CMX tables require pandas. Install with: pip install 'cmx[tables]'"
                ) from e

            if isinstance(table, str):
                self.data = pd.read_csv(StringIO(table), sep=sep)
            elif isinstance(table, pd.DataFrame):
                self.data = table
            else:
                self.data = pd.DataFrame(table)

    def figure_row(self, **kwargs):
        row = FigureRow(doc=self._doc, **kwargs)
        self.children.append(row)
        return row

    @property
    def _md(self):
        if not self.children:
            # The default "github" format is rendered by our own pure-Python
            # renderer -- no tabulate at runtime. Other formats still need
            # tabulate (via pandas' to_markdown).
            if self.format == "github" and not self.kwargs:
                from .md_table import render

                return render(self.data, index=bool(self.show_index)) + "\n"
            try:
                import tabulate  # noqa: F401  -- required by DataFrame.to_markdown
            except ImportError as e:
                raise ImportError(
                    f"CMX tables in the '{self.format}' format require tabulate. "
                    "Install with: pip install tabulate "
                    "(the default 'github' format needs only pandas)."
                ) from e
            return self.data.to_markdown(index=self.show_index, tablefmt=self.format, **self.kwargs) + "\n"
        # Flatten children into rows of cells. FigureRows expand to their
        # (titles / images / captions) bands; any other child yields its cells.
        rows = []
        for child in self.children:
            if isinstance(child, FigureRow):
                rows.extend(child.rows)
            else:
                rows.append(child.children)
        _md_str = ""
        for i, r in enumerate(rows):
            _md_str += "| " + " | ".join([" " if c is None else c._md.strip() for c in r]) + " |\n"
            if i == 0:
                _md_str += "|:" + ":|:".join(["-" if c is None else "-" * len(c._md.strip()) for c in r]) + ":|\n"
        return _md_str

    @property
    def _html(self):
        return self.data.to_html(index=self.show_index, **self.kwargs)


class _Factory:
    """Mixin of component-creating helpers shared by document containers.

    Each helper resolves the asset path, routes the bytes through the document's
    ``on_save`` lifecycle hook (which returns the *link* to render), instantiates
    the matching pure-render component, appends it, fires ``on_block``, and
    returns it -- so the result can be used directly or as a ``with`` block.
    """

    def _resolve_asset(self, name):
        """Place a bare asset name under the resolved ``figdir``.

        A name WITHOUT a directory component (e.g. ``"gradient.png"``) is placed
        under the document's ``figdir``. A name WITH a directory (e.g.
        ``"sub/x.png"``) is used AS-IS (explicit wins). Forward slashes are used
        for the stored src so markdown links stay portable.
        """
        if not name:
            return name
        base, _tail = posixpath.split(name) if "/" in name else os.path.split(name)
        if base:  # explicit directory -> as-is
            return name
        figdir = getattr(self, "figdir", "") or ""
        return posixpath.join(figdir, name) if figdir else name

    def _emit_save(self, *, data, path, kind, **extra):
        """Hand an asset to ``on_save`` (if present) and return the link.

        Falls back to the resolved ``path`` when no hook exists (a bare
        :class:`Article` with no lifecycle machinery).
        """
        on_save = getattr(self, "on_save", None)
        if on_save is None:
            return path
        return on_save(data=data, path=path, kind=kind, dest=getattr(self, "dest", None), doc=self, **extra)

    def _emit_block(self, *, kind, node):
        on_block = getattr(self, "on_block", None)
        if on_block is not None:
            on_block(kind=kind, node=node, doc=self)

    def table(self, table=None, **kwargs):
        t = Table(table, doc=self, **kwargs)
        self.children.append(t)
        self._emit_block(kind="table", node=t)
        return t

    def image(self, image=None, src=None, **kwargs):
        src = self._resolve_asset(src)
        if src is not None:
            link = self._emit_save(data=image, path=src, kind="image", **kwargs)
            img = Image(src=link)
        else:
            # Inline base64 path: no src, no on_save -- render the data directly.
            img = Image(image=image, **kwargs)
        self.children.append(img)
        self._emit_block(kind="image", node=img)
        return img

    def figure(self, image=None, src=None, title=None, caption=None, **kwargs):
        src = self._resolve_asset(src)
        if src is not None:
            link = self._emit_save(data=image, path=src, kind="image", **kwargs)
            fig = Figure(src=link, title=title, caption=caption)
        else:
            fig = Figure(image=image, title=title, caption=caption, **kwargs)
        self.children.append(fig)
        self._emit_block(kind="figure", node=fig)
        return fig

    def video(self, frames=None, src=None, **kwargs):
        src = self._resolve_asset(src)
        link = self._emit_save(data=frames, path=src, kind="video", **kwargs)
        v = video(src=link, **kwargs)
        self.children.append(v)
        self._emit_block(kind="video", node=v)
        return v

    def savefig(self, key, caption=None, width=None, height=None, zoom=None, **kwargs):
        key = self._resolve_asset(key)
        link = self._emit_save(data=None, path=key, kind="figure", **kwargs)
        fig = Savefig(link, caption=caption, width=width, height=height, zoom=zoom)
        self.children.append(fig)
        self._emit_block(kind="figure", node=fig)
        return fig

    def row(self, *args, **kwargs):
        r = Row(*args, **kwargs)
        self.children.append(r)
        return r


class Html(_Factory, Component):
    tag = "body"


# Block-level elements need a blank line before them in Markdown (tables,
# images, code fences, figures, rows, videos). Subclasses (Print/Image/Savefig)
# are covered via isinstance. Plain text blocks stay tight (single newline).
_BLOCK_TYPES = (Pre, Table, Img, Figure, Row, Video)


class Article(Html):
    tag = "article"
    class_name = "commonmark"

    @property
    def _md(self):
        out = ""
        for c in self.children:
            if c is None:
                continue
            md = c._md
            if not md:
                continue
            if isinstance(c, _BLOCK_TYPES):
                # Block elements: drop their own leading newlines and ensure
                # exactly one blank line separates them from prior output.
                md = md.lstrip("\n")
                if out:
                    out = out.rstrip("\n") + "\n\n"
            else:
                # Text/inline: keep tight, just a single newline separator.
                if out and not out.endswith("\n"):
                    out += "\n"
            out += md
            if not out.endswith("\n"):
                out += "\n"
        return out


class Print(Pre):
    def __init__(self, *args, sep=" ", end="\n", **kwargs):
        super().__init__(sep.join([str(a) for a in args]) + end, **kwargs)
