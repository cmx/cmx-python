"""The CommonMark document -- the object exported as ``cmx.doc``.

A ``CommonMark`` is an :class:`~cmx.backends.components.Article` (so it inherits
the component factories: ``table``, ``image``, ``figure``, ``row``, ``video``,
``savefig``) plus the live-document machinery: the ``@`` / ``|`` / call operators
for adding markdown, ``with doc:`` source capture, and ``flush`` to write out.
"""

import atexit
import os
from copy import deepcopy
from contextlib import ExitStack

from . import components
from .. import utils
from ..utils import get_block, dedent
from ..with_hack import SkipContextManager

# Re-exported so existing ``from cmx.backends.markdown import ...`` imports keep
# working after the components were unified into one module.
from .components import Image, Figure, Savefig, video  # noqa: F401

USER = os.environ.get("USER", None)
PWD = os.environ.get("PWD", None)


def _green(message):
    """Return ``message`` wrapped in ANSI green (replaces the termcolor dep)."""
    return f"\033[32m{message}\033[0m"


class CommonMark(components.Article):
    __filename = None
    counter = 0

    @property
    def hide(self):
        """``with doc.hide:`` runs its body but does *not* capture the source as
        a code block -- handy for boilerplate you want to execute but not show.
        """
        self.on_hide(doc=self)
        return ExitStack()

    @property
    def skip(self):
        """``with doc.skip:`` skips execution of its body entirely.

        Implemented via frame tracing (see :class:`SkipContextManager`); this can
        interfere with debuggers such as PyCharm's pydev.
        """
        self.on_skip(doc=self)
        return SkipContextManager(True)

    _figdir_template = "{fname}"

    def __init__(self, filename=None, overwrite=True, root=None, prefix=None):
        """
        :param filename: output markdown filename (auto-derived from the calling
            script when omitted).
        :param overwrite: clear the file on configure instead of appending.
        :param root: initial working directory for the document (where assets
            and the markdown file are written by the default local hooks).
        :param prefix: legacy path prefix joined under ``root`` (kept only for
            the package-level singleton's ``CommonMark(root=cwd, prefix=".")``).
        """
        super().__init__()
        # ``wd`` is the resolved (abspath) working directory; ``dest`` is whatever
        # ``on_mount`` returns (None for local, a base key / URL for remote).
        self.dest = None
        if root or prefix:
            base = root or os.getcwd()
            self.wd = os.path.abspath(os.path.join(base, prefix) if prefix else base)
        else:
            self.wd = os.getcwd()
        self._closed = False
        # Idempotent close-on-exit: ``close()`` guards against a double-fire so
        # an explicit ``doc.close()`` and this atexit hook together fire once.
        atexit.register(self.close)
        self.config(filename=filename, overwrite=overwrite)

    # ------------------------------------------------------------------ #
    # Lifecycle hooks. Each has a sensible local-disk default; override by
    # subclassing (``def on_save(self, ...)``) or by binding a plain function
    # on the instance (``doc.on_save = lambda *, data, path, **kw: ...``). All
    # hooks are keyword-only and accept ``**kw`` so new fields never break an
    # existing override. Only ``on_mount`` and ``on_save`` use their return.
    # ------------------------------------------------------------------ #

    def on_mount(self, *, filename, wd, figdir, doc, **kw):
        """Fires once in ``config()`` after paths resolve. Return a ``dest``
        (base key / URL / id) or ``None`` for the local filesystem."""
        return None

    def on_save(self, *, data, path, kind, dest, doc, **kw):
        """Fires per binary asset. Write the bytes locally and return the link.

        ``kind`` is one of ``"image"`` / ``"video"`` / ``"figure"``. The bytes
        land under ``self.wd`` at ``path`` (with any ``?query`` stripped); the
        returned *link* (the full ``path``, query intact) is what gets rendered
        into ``![]( )``.
        """
        if path is None:
            return path
        file_path, *_ = path.split("?")
        if kind == "image":
            if data is not None:
                utils.write_image(data, file_path, wd=self.wd, normalize=kw.get("normalize", False))
        elif kind == "video":
            if data is not None:
                utils.write_video(data, file_path, wd=self.wd)
        elif kind == "figure":
            savefig_kwargs = {k: v for k, v in kw.items() if k != "normalize"}
            utils.write_savefig(file_path, wd=self.wd, **savefig_kwargs)
        return path

    def on_flush(self, *, text, path, dest, doc, **kw):
        """Fires per ``flush()``. Append the rendered ``text`` to the md file."""
        utils.append_text(text, path, wd=self.wd, overwrite=False)

    def on_close(self, *, full_text, path, dest, doc, **kw):
        """Fires once via ``doc.close()`` / ``atexit``. Default: no-op."""
        return None

    def on_error(self, *, exc, block, doc, **kw):
        """Fires in the ``with doc:`` exception path. Default: no-op (returns a
        falsy value so the exception still propagates)."""
        return None

    def on_block(self, *, kind, node, doc, **kw):
        """Fires when a block is appended. ``kind`` is one of
        ``text`` / ``code`` / ``table`` / ``image`` / ``figure`` / ``video``."""
        return None

    def on_hide(self, *, doc, **kw):
        """Fires from ``with doc.hide:``. Default: no-op."""
        return None

    def on_skip(self, *, doc, **kw):
        """Fires from ``with doc.skip:``. Default: no-op."""
        return None

    # (``on_inline`` is intentionally deferred -- not implemented yet.)

    def config(self, file=None, *, wd=None, figdir="{fname}", overwrite=True, filename=None, src_prefix=None):
        """Configure where script output lands.

        :param file: EITHER a script path (``doc.config(__file__)``, ends with
            ``.py``) OR an explicit output path (ends with ``.md``). Outputs
            resolve relative to the script/output, not the cwd.
        :param wd: working directory; overrides the default derived from
            ``file``/``filename`` (or the cwd when neither is given).
        :param figdir: a template string for the figure directory. ``{fname}``
            expands to the markdown stem. Default ``"{fname}"``.
        :param overwrite: clear the file on configure instead of appending.
        :param filename: explicit output path (back-compat keyword).
        """
        self.overwrite = overwrite
        self._figdir_template = figdir

        # Resolve the source of truth for the output basename and working dir.
        md_basename = None
        default_wd = None
        if file is not None and str(file).endswith(".py"):
            # ``file`` is the SCRIPT.
            stem = os.path.splitext(os.path.basename(file))[0]
            default_wd = os.path.dirname(os.path.abspath(file))
            md_basename = f"{stem}.md"
        else:
            # Treat ``file`` (a non-.py path) or ``filename`` as the output md.
            path = file if file is not None else filename
            if path:
                dirname = os.path.dirname(path)
                default_wd = os.path.dirname(os.path.abspath(path)) if dirname else os.getcwd()
                md_basename = os.path.basename(path)

        if md_basename is not None:
            resolved_wd = os.path.abspath(wd) if wd else default_wd
            self.wd = resolved_wd
            self.__filename = md_basename

            # Hand off to the mount hook -- returns a remote dest, or None local.
            self.dest = self.on_mount(filename=md_basename, wd=self.wd, figdir=self.figdir, doc=self)

            is_http = isinstance(self.dest, str) and self.dest.startswith("http")
            if self.overwrite and not self.dest:
                # Local case: truncate the markdown file.
                self.clear()

            abs_md = os.path.join(resolved_wd, md_basename)
            if is_http:
                print(_green("File output at " + self.dest + " " + md_basename))
            else:
                from urllib import parse

                print(_green("File output at file://" + parse.quote(abs_md)))
        elif wd is not None:
            # No output path given, but an explicit working dir was requested.
            self.wd = os.path.abspath(wd)
        return self

    @property
    def figdir(self):
        stem = os.path.splitext(os.path.basename(self.filename))[0]
        return self._figdir_template.replace("{fname}", stem)

    def new(self, filename=None, **kwargs):
        if filename:
            filename = os.path.abspath(filename)
        return deepcopy(self).config(filename=filename, **kwargs)

    @property
    def filename(self):
        if self.__filename is None:
            import inspect

            # Walk out of cmx's own frames to find the user's script.
            filename = "cmx/"
            frame = inspect.currentframe()
            while "cmx/" in filename or "importlib" in filename or "contextlib" in filename:
                frame = frame.f_back
                filename, line_number, function_name, lines, index = inspect.getframeinfo(frame)

            if filename.endswith("__init__.py"):
                self.__filename = filename[:-11] + "README.md"
            else:
                self.__filename = filename.replace(".py", ".md")

            if self.overwrite:
                self.clear()

            from urllib import parse

            print(_green("File output at file://" + parse.quote(self.__filename)))

        return self.__filename

    def write(self, text, overwrite=None):
        utils.append_text(text, self.filename, wd=self.wd, overwrite=bool(overwrite))

    def clear(self):
        self.write("", overwrite=True)

    def __call__(self, *snippets, dedent=True, **kwargs):
        """Add markdown text: ``doc("# Title")``."""
        node = components.Text(*snippets, dedent=dedent, **kwargs)
        self.children.append(node)
        self.on_block(kind="text", node=node, doc=self)
        return self

    md = __call__

    def __matmul__(self, string_or_array):
        """Prefix ``@`` syntax: ``doc @ "text"``."""
        if isinstance(string_or_array, tuple):
            string, *rest = string_or_array
            return self(string, *rest)
        return self(string_or_array)

    def __ror__(self, string_or_array):
        """Postfix pipe syntax: ``"text" | doc``."""
        if isinstance(string_or_array, tuple):
            string, *rest = string_or_array
            return self(string, *rest)
        return self(string_or_array)

    def __or__(self, other):
        raise NotImplementedError("Left-side pipe operator not yet implemented")

    def pre(self, text, lang=None, **kwargs):
        p = components.Pre(text, lang=lang, **kwargs)
        self.children.append(p)
        self.on_block(kind="code", node=p, doc=self)
        return p

    def yaml(self, data, **kwargs):
        import yaml

        return self.pre(yaml.dump(data).rstrip(), lang="yaml")

    def csv(self, csv, show_index=False, **kwargs):
        t = components.Table(csv, show_index=show_index, doc=self, **kwargs)
        self.children.append(t)
        self.on_block(kind="table", node=t, doc=self)
        return t

    def print(self, *args, sep=" ", end="\n"):
        # Coalesce consecutive prints into a single code block, and echo to stdout.
        if self.children and isinstance(self.children[-1], components.Print):
            self.children[-1].text += sep.join([str(a) for a in args]) + end
        else:
            node = components.Print(*args, sep=sep, end=end)
            self.children.append(node)
            self.on_block(kind="code", node=node, doc=self)
        print(*args, sep=sep, end=end)

    def flush(self, *args):
        text = self._md
        self.on_flush(text=text, path=self.filename, dest=self.dest, doc=self)
        self.children.clear()

    def close(self):
        """Render/send the document's full text once (idempotent).

        Fires ``on_close`` exactly once across explicit ``close()`` calls and the
        registered ``atexit`` guard. ``full_text`` is the file's full content for
        the local case, falling back to the accumulated document text.
        """
        if getattr(self, "_closed", False):
            return
        self._closed = True
        # An unconfigured document (no resolved filename) has nothing to close.
        # Resolving ``self.filename`` here would inspect frames -- unsafe and
        # pointless at interpreter shutdown (the atexit path).
        if self.__filename is None:
            return
        full_text = self._read_full_text()
        self.on_close(full_text=full_text, path=self.filename, dest=self.dest, doc=self)

    def _read_full_text(self):
        """Best-effort full document text: the local md file, else the buffer."""
        if not self.dest:
            full_path = utils._resolve_full_path(self.filename, self.wd)
            try:
                with open(full_path) as f:
                    return f.read()
            except (FileNotFoundError, OSError):
                pass
        return self._md

    def __enter__(self):
        import inspect

        assert self.filename, "make sure that file is already set."

        prior_frame = inspect.currentframe().f_back
        filename, line_number, function_name, lines, index = inspect.getframeinfo(prior_frame)
        try:
            lines_in_block = get_block(filename, line_number + 1)
            text = "".join(lines_in_block)
            node = components.Pre(dedent(text).rstrip(), lang="python")
            self.children.append(node)
            self.on_block(kind="code", node=node, doc=self)
        except FileNotFoundError:
            print("in iPython session")
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        if exc_type is not None:
            # Report the failure but do NOT suppress it -- return falsy so the
            # exception still propagates out of the ``with doc:`` block.
            self.on_error(exc=exc_val, block=self, doc=self)
        self.flush()
        return False


class Github(CommonMark):
    """Uses tables for the layout."""

    pass


class Gist(CommonMark):
    """Saves everything inside a folder."""

    pass
