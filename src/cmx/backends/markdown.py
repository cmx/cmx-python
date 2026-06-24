"""The CommonMark document -- the object exported as ``cmx.doc``.

A ``CommonMark`` is an :class:`~cmx.backends.components.Article` (so it inherits
the component factories: ``table``, ``image``, ``figure``, ``row``, ``video``,
``savefig``) plus the live-document machinery: the ``@`` / ``|`` / call operators
for adding markdown, ``with doc:`` source capture, and ``flush`` to write out.
"""

import os
from copy import deepcopy
from contextlib import ExitStack

from . import components
from ..utils import get_block, dedent, SimpleLogger
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
        return ExitStack()

    @property
    def skip(self):
        """``with doc.skip:`` skips execution of its body entirely.

        Implemented via frame tracing (see :class:`SkipContextManager`); this can
        interfere with debuggers such as PyCharm's pydev.
        """
        return SkipContextManager(True)

    def __init__(self, filename=None, overwrite=True, root=None, prefix=None, logger=None):
        """
        :param filename: output markdown filename (auto-derived from the calling
            script when omitted).
        :param overwrite: clear the file on configure instead of appending.
        :param logger: a pre-built logger (e.g. to a remote server); defaults to
            a local :class:`SimpleLogger` rooted at ``root``/``prefix``.
        """
        super().__init__()
        self.logger = logger or SimpleLogger(root=root, prefix=prefix)
        self.config(filename=filename, overwrite=overwrite)

    def config(self, filename=None, overwrite=True, src_prefix=None, logger=None):
        self.overwrite = overwrite
        self.logger = logger or self.logger
        if filename:
            self.__filename = filename
            if self.overwrite:
                self.logger.log_text("", filename=self.filename, overwrite=True)

            if self.logger.root.startswith("http"):
                print(_green("File output at " + self.logger.get_dash_url() + " " + self.__filename))
            else:
                from urllib import parse

                print(_green("File output at file://" + parse.quote(os.path.realpath(self.__filename))))
        return self

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
        self.logger.log_text(text, filename=self.filename, overwrite=overwrite)

    def clear(self):
        self.write("", overwrite=True)

    def __call__(self, *snippets, dedent=True, **kwargs):
        """Add markdown text: ``doc("# Title")``."""
        self.children.append(components.Text(*snippets, dedent=dedent, **kwargs))
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
        return p

    def yaml(self, data, **kwargs):
        import yaml

        return self.pre(yaml.dump(data).rstrip(), lang="yaml")

    def csv(self, csv, show_index=False, **kwargs):
        t = components.Table(csv, show_index=show_index, logger=self.logger, **kwargs)
        self.children.append(t)
        return t

    def print(self, *args, sep=" ", end="\n"):
        # Coalesce consecutive prints into a single code block, and echo to stdout.
        if self.children and isinstance(self.children[-1], components.Print):
            self.children[-1].text += sep.join([str(a) for a in args]) + end
        else:
            self.children.append(components.Print(*args, sep=sep, end=end))
        print(*args, sep=sep, end=end)

    def flush(self, *args):
        self.write(self._md)
        self.children.clear()

    def __enter__(self):
        import inspect

        assert self.filename, "make sure that file is already set."

        prior_frame = inspect.currentframe().f_back
        filename, line_number, function_name, lines, index = inspect.getframeinfo(prior_frame)
        try:
            lines_in_block = get_block(filename, line_number + 1)
            text = "".join(lines_in_block)
            self.children.append(components.Pre(dedent(text).rstrip(), lang="python"))
        except FileNotFoundError:
            print("in iPython session")
        return self

    __exit__ = flush


class Github(CommonMark):
    """Uses tables for the layout."""

    pass


class Gist(CommonMark):
    """Saves everything inside a folder."""

    pass
