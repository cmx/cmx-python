"""Render components for the CMX markdown backend.

Each component knows how to render itself as Markdown (``_md``) and HTML
(``_html``). Components form a tree: an :class:`Article` holds children, some of
which (``Table``, ``FigureRow``, ``Row``) hold children of their own.

This module is dependency-inverted the simple way: there is no class registry or
``__getattribute__`` proxy. Parents create their children by calling the
component classes directly, and the optional file-writing ``logger`` is threaded
down explicitly. Anything that needs heavy third-party libraries (numpy, PIL,
pyyaml) imports them lazily so ``import cmx`` stays cheap.
"""

from io import StringIO

from .. import utils
from ..utils import is_subclass, to_snake  # re-exported for backwards compatibility


def attrs(class_name=None, **kwargs):
    attrs_str = f'class="{class_name}"' if class_name else ""
    attrs_str += " ".join([k.replace("_", "-") + f'="{str(v)}"' for k, v in kwargs.items()])
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

    def __init__(self, tag=None, children=None, logger=None, **kwargs):
        self.tag = tag or self.tag
        self.kwargs = kwargs
        self.style = {}
        self.children = [] if children is None else children
        self.logger = logger

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

    def __init__(self, *args, sep=" ", dedent=None, **kwargs):
        super().__init__(**kwargs)
        self.text = sep.join([str(a) for a in args])
        if dedent:
            self.text = utils.dedent(self.text)

    @property
    def _md(self):
        # Block-level text ends with a newline so siblings don't run together.
        text = self.text
        if text and not text.endswith("\n"):
            text = text + "\n"
        return text

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
        return f"```{self.lang if self.lang else ''}{text}```\n"

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
    """An image that can reference a file, save data to a file, or inline base64.

    - ``src`` only            -> reference the file path.
    - ``src`` + ``image`` + a ``logger`` -> write the file, then reference it.
    - ``image`` only          -> inline the data as a base64 ``data:`` URI.
    """

    data = None

    def __init__(self, image=None, src=None, logger=None, normalize=False, **kwargs):
        if src is not None:
            file_path, *_ = src.split("?")
            if image is not None and logger is not None:
                logger.save_image(image, file_path, normalize=normalize)
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


def video(frames=None, *, src, logger=None, **kwargs):
    """Save video frames (if given) and return the matching component.

    ``.gif`` sources render as an ``Image``; everything else as a ``Video``.
    """
    file_path, *_ = src.split("?")
    if frames is not None and logger is not None:
        logger.save_video(frames, file_path)
    if file_path.endswith("gif"):
        return Image(src=src, **kwargs)
    return Video(src=src, **kwargs)


class Figure(Component):
    tag = "div"

    def __init__(self, image=None, src=None, title=None, caption=None, logger=None, **kwargs):
        super().__init__(logger=logger)
        self.src = src
        if isinstance(image, Component):
            self.img = image
        else:
            self.img = Image(image=image, src=src, logger=logger, **kwargs)
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
    def __init__(self, key, caption=None, width=None, height=None, zoom=None, logger=None, **kwargs):
        file_path, *_ = key.split("?")
        super().__init__(src=key, width=width, height=height, caption=caption, zoom=zoom, logger=logger, **kwargs)
        if logger is not None:
            logger.savefig(file_path, **kwargs)


class Row(Component):
    styles = dict(
        display="flex",
        flex_direction="row",
        item_align="center",
    )

    def __init__(self, wrap=False, styles=None, logger=None, **kwargs):
        super().__init__(logger=logger, **kwargs)
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

    def __init__(self, header=None, n_cols=None, logger=None, **kwargs):
        super().__init__(logger=logger, **kwargs)
        self.n_cols = n_cols
        self.titles = []
        self.images = []
        self.footers = []

    def figure(self, image=None, src=None, title=None, caption=None, **kwargs):
        self.titles.append(None if title is None else Bold(title))
        self.footers.append(None if caption is None else Span(caption))
        self.children.append(Image(image=image, src=src, logger=self.logger, **kwargs))

    def video(self, frames=None, src=None, title=None, caption=None, **kwargs):
        self.titles.append(None if title is None else Bold(title))
        self.footers.append(None if caption is None else Span(caption))
        self.children.append(video(frames=frames, src=src, logger=self.logger, **kwargs))

    def column(self, title=None, text=None, footer=None):
        self.titles.append(None if title is None else Bold(title))
        self.footers.append(None if footer is None else Span(footer))
        self.children.append(Text(text))

    def savefig(self, key, title=None, caption=None, **kwargs):
        self.titles.append(None if title is None else Bold(title))
        self.footers.append(None if caption is None else Span(caption))
        self.children.append(Savefig(key, logger=self.logger, **kwargs))

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

    data = None

    def __init__(self, table=None, show_index=None, format="github", sep=",*", logger=None, **kwargs):
        super().__init__(logger=logger)
        self.show_index = show_index
        self.kwargs = kwargs  # forwarded to pandas' to_markdown / to_html
        self.format = format
        if table is None:
            pass
        else:
            import pandas as pd

            if isinstance(table, str):
                self.data = pd.read_csv(StringIO(table), sep=sep)
            elif isinstance(table, pd.DataFrame):
                self.data = table
            else:
                self.data = pd.DataFrame(table)

    def figure_row(self, **kwargs):
        row = FigureRow(logger=self.logger, **kwargs)
        self.children.append(row)
        return row

    @property
    def _md(self):
        if not self.children:
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

    Each helper instantiates a component (threading this container's ``logger``),
    appends it as a child, and returns it -- so the result can be used directly
    or as a ``with`` block.
    """

    def table(self, table=None, **kwargs):
        t = Table(table, logger=self.logger, **kwargs)
        self.children.append(t)
        return t

    def image(self, image=None, src=None, **kwargs):
        img = Image(image=image, src=src, logger=self.logger, **kwargs)
        self.children.append(img)
        return img

    def figure(self, image=None, src=None, title=None, caption=None, **kwargs):
        fig = Figure(image=image, src=src, title=title, caption=caption, logger=self.logger, **kwargs)
        self.children.append(fig)
        return fig

    def video(self, frames=None, src=None, **kwargs):
        v = video(frames=frames, src=src, logger=self.logger, **kwargs)
        self.children.append(v)
        return v

    def savefig(self, key, **kwargs):
        fig = Savefig(key, logger=self.logger, **kwargs)
        self.children.append(fig)
        return fig

    def row(self, *args, **kwargs):
        r = Row(*args, logger=self.logger, **kwargs)
        self.children.append(r)
        return r


class Html(_Factory, Component):
    tag = "body"


class Article(Html):
    tag = "article"
    class_name = "commonmark"

    @property
    def _md(self):
        # Each child's _md already ends in a newline, so plain concatenation
        # keeps blocks separated.
        return "".join([c._md for c in self.children])


class Print(Pre):
    def __init__(self, *args, sep=" ", end="\n", **kwargs):
        super().__init__(sep.join([str(a) for a in args]) + end, **kwargs)
